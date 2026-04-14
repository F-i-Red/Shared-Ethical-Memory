# influence_router.py
# Garante que a memória recuperada influencia ativamente o raciocínio do LLM

import json
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class InfluenceContext:
    """Contexto enriquecido que será injetado no prompt do LLM."""
    base_query: str
    raw_memories: List[Dict[str, Any]]
    ranked_memories: List[Dict[str, Any]]
    influence_prompt: str
    confidence_scores: List[float]
    influence_strategy: str  # "direct_citation", "principle_merging", "conflict_resolution"

class InfluenceRouter:
    """
    Garante que a memória recuperada influencia a resposta final através de:
    1. Ranking multi-fator (relevância, recência, confiança, diversidade)
    2. Injeção estratégica no prompt (não apenas dump de contexto)
    3. Resolução de conflitos entre memórias
    4. Geração de instruções explícitas para o LLM
    """

    def __init__(self, graph_path: str = "memory_graph.json", 
                 default_top_k: int = 5,
                 diversity_weight: float = 0.2):
        self.graph_path = Path(graph_path)
        self.default_top_k = default_top_k
        self.diversity_weight = diversity_weight
        self._embedding_cache = {}

    def _load_graph(self) -> Dict[str, Any]:
        if self.graph_path.exists():
            return json.loads(self.graph_path.read_text(encoding='utf-8'))
        return {"nodes": []}

    def _calculate_relevance_score(self, memory: Dict[str, Any], query: str) -> float:
        """
        Calcula score de relevância combinado:
        - Similaridade semântica com query (0.5)
        - Confiança da memória (0.2)
        - Recência (0.15)
        - Diversidade (0.15 - aplicado depois)
        """
        # Similaridade semântica simples (pode ser substituída por embeddings reais)
        query_words = set(query.lower().split())
        memory_text = f"{memory.get('principle', '')} {memory.get('context', '')} {memory.get('decision', '')}".lower()
        memory_words = set(memory_text.split())
        
        if not query_words:
            semantic_score = 0.5
        else:
            overlap = len(query_words & memory_words)
            semantic_score = min(overlap / len(query_words), 1.0)
        
        # Confiança
        confidence = memory.get("confidence", 0.5)
        
        # Recência (quanto mais recente, melhor)
        created_at = memory.get("created_at")
        if created_at:
            try:
                created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                days_old = (datetime.now(timezone.utc) - created).days
                recency_score = max(0.0, 1.0 - (days_old / 180))  # Decai em 6 meses
            except Exception:
                recency_score = 0.5
        else:
            recency_score = 0.5
        
        # Score final
        score = (0.5 * semantic_score) + (0.2 * confidence) + (0.15 * recency_score)
        return round(score, 3)

    def _diversity_penalty(self, selected: List[Dict[str, Any]], candidate: Dict[str, Any]) -> float:
        """Calcula penalidade por similaridade com memórias já selecionadas."""
        if not selected:
            return 0.0
        
        candidate_text = f"{candidate.get('principle', '')} {candidate.get('context', '')}"
        max_similarity = 0.0
        
        for mem in selected:
            mem_text = f"{mem.get('principle', '')} {mem.get('context', '')}"
            words1 = set(candidate_text.lower().split())
            words2 = set(mem_text.lower().split())
            if words1 and words2:
                similarity = len(words1 & words2) / len(words1 | words2)
                max_similarity = max(max_similarity, similarity)
        
        # Penalidade: quanto mais similar, maior a penalidade
        return self.diversity_weight * max_similarity

    def _resolve_conflicts(self, memories: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Identifica e tenta resolver conflitos entre memórias.
        Retorna (memórias_resolvidas, avisos_de_conflito)
        """
        warnings = []
        resolved = []
        
        # Agrupar por princípio para detetar contradições
        principle_map = {}
        for mem in memories:
            principle = mem.get("principle", "").lower()
            decision = mem.get("decision", "").lower()
            if principle in principle_map:
                prev_decision = principle_map[principle]
                if "refuse" in prev_decision and "allow" in decision:
                    warnings.append(f"Conflito detectado para princípio '{principle}': decisões contraditórias.")
                elif "allow" in prev_decision and "refuse" in decision:
                    warnings.append(f"Conflito detectado para princípio '{principle}': decisões contraditórias.")
                else:
                    resolved.append(mem)
            else:
                principle_map[principle] = decision
                resolved.append(mem)
        
        return resolved, warnings

    def rank_memories(self, query: str, memories: List[Dict[str, Any]], 
                      top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Rankeia memórias usando scoring multi-fator + diversidade.
        """
        if not memories:
            return []
        
        top_k = top_k or self.default_top_k
        
        # Calcular scores base
        scored = []
        for mem in memories:
            base_score = self._calculate_relevance_score(mem, query)
            scored.append((base_score, mem))
        
        # Ordenar por score base
        scored.sort(key=lambda x: x[0], reverse=True)
        
        # Selecionar com penalidade de diversidade (MMR - Maximal Marginal Relevance)
        selected = []
        candidates = scored.copy()
        
        for _ in range(min(top_k, len(candidates))):
            if not candidates:
                break
            
            best_idx = 0
            best_score = -1
            
            for idx, (base_score, mem) in enumerate(candidates):
                diversity_penalty = self._diversity_penalty(selected, mem)
                final_score = base_score - diversity_penalty
                if final_score > best_score:
                    best_score = final_score
                    best_idx = idx
            
            selected.append(candidates[best_idx][1])
            candidates.pop(best_idx)
        
        return selected

    def build_influence_prompt(self, query: str, 
                                memories: Optional[List[Dict[str, Any]]] = None,
                                top_k: Optional[int] = None,
                                include_conflict_warning: bool = True) -> InfluenceContext:
        """
        Constrói um prompt que GARANTE influência da memória na resposta.
        """
        if memories is None:
            data = self._load_graph()
            memories = data.get("nodes", [])
        
        # Rankear memórias
        ranked = self.rank_memories(query, memories, top_k)
        
        # Resolver conflitos
        resolved_memories, conflicts = self._resolve_conflicts(ranked)
        
        # Decidir estratégia de influência
        influence_strategy = "direct_citation"
        if len(ranked) >= 3:
            influence_strategy = "principle_merging"
        if conflicts and include_conflict_warning:
            influence_strategy = "conflict_resolution"
        
        # Construir o prompt de influência
        prompt_parts = []
        
        # Instrução base
        prompt_parts.append(f"=== USER QUERY ===\n{query}\n")
        
        # Instrução de influência obrigatória
        prompt_parts.append("=== ETHICAL MEMORY DIRECTIVES (MUST FOLLOW) ===\n")
        prompt_parts.append("The following ethical principles from memory MUST inform your response:\n")
        
        # Adicionar memórias com formatação que força influência
        for i, mem in enumerate(resolved_memories[:top_k], 1):
            principle = mem.get('principle', 'N/A')
            decision = mem.get('decision', 'N/A')
            justification = mem.get('justification', 'N/A')
            confidence = mem.get('confidence', 0.5)
            
            prompt_parts.append(f"{i}. PRINCIPLE: {principle}")
            prompt_parts.append(f"   DECISION: {decision}")
            prompt_parts.append(f"   JUSTIFICATION: {justification}")
            prompt_parts.append(f"   CONFIDENCE: {confidence}\n")
        
        # Adicionar avisos de conflito se necessário
        if conflicts and include_conflict_warning:
            prompt_parts.append("=== CONFLICT WARNING ===\n")
            prompt_parts.append("The memories above contain conflicting principles. ")
            prompt_parts.append("Your response must acknowledge this tension and explain how you resolve it.\n")
        
        # Instrução final obrigatória
        if influence_strategy == "direct_citation":
            prompt_parts.append("=== RESPONSE INSTRUCTION ===\n")
            prompt_parts.append("Your response MUST explicitly reference the ethical principles above ")
            prompt_parts.append("and explain how they shaped your answer. Do not ignore them.\n")
        elif influence_strategy == "principle_merging":
            prompt_parts.append("=== RESPONSE INSTRUCTION ===\n")
            prompt_parts.append("Synthesize the principles above into a coherent ethical framework. ")
            prompt_parts.append("Your response MUST demonstrate how this framework guides your answer.\n")
        elif influence_strategy == "conflict_resolution":
            prompt_parts.append("=== RESPONSE INSTRUCTION ===\n")
            prompt_parts.append("The memories contain conflicts. Your response MUST:")
            prompt_parts.append("1. Acknowledge the conflicting principles")
            prompt_parts.append("2. Explain your resolution approach")
            prompt_parts.append("3. Justify why your resolution is ethically sound\n")
        
        # Calcular scores de confiança para o contexto
        confidence_scores = [mem.get('confidence', 0.5) for mem in resolved_memories[:top_k]]
        
        return InfluenceContext(
            base_query=query,
            raw_memories=memories[:top_k],
            ranked_memories=resolved_memories[:top_k],
            influence_prompt="\n".join(prompt_parts),
            confidence_scores=confidence_scores,
            influence_strategy=influence_strategy
        )

    def get_influenced_response(self, query: str, 
                                 llm_client: Any = None,
                                 memories: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Método de alto nível: constrói contexto influenciado e obtém resposta do LLM.
        Se llm_client for None, retorna apenas o contexto construído.
        """
        context = self.build_influence_prompt(query, memories)
        
        result = {
            "query": query,
            "influence_strategy": context.influence_strategy,
            "memories_used": len(context.ranked_memories),
            "confidence_scores": context.confidence_scores,
            "influence_prompt": context.influence_prompt
        }
        
        if llm_client:
            # Se tiver um cliente LLM, faz a chamada real
            try:
                # Assumindo que llm_client tem um método generate()
                response = llm_client.generate(context.influence_prompt)
                result["response"] = response
            except Exception as e:
                result["error"] = str(e)
                result["response"] = None
        else:
            result["response"] = None
            result["note"] = "No LLM client provided. Use the influence_prompt manually."
        
        return result


# Teste independente
if __name__ == "__main__":
    router = InfluenceRouter()
    
    # Simular algumas memórias
    test_memories = [
        {"principle": "Privacy First", "decision": "Minimize data collection", 
         "justification": "Respects user autonomy", "confidence": 0.9, "created_at": "2026-04-01T00:00:00Z"},
        {"principle": "Transparency", "decision": "Explain all decisions", 
         "justification": "Builds trust", "confidence": 0.85, "created_at": "2026-04-10T00:00:00Z"},
        {"principle": "Non-Maleficence", "decision": "Refuse harmful requests", 
         "justification": "Prevents damage", "confidence": 0.95, "created_at": "2026-04-05T00:00:00Z"},
    ]
    
    context = router.build_influence_prompt("How should I handle user data?", test_memories)
    print("=== Influence Router Test ===")
    print(f"Strategy: {context.influence_strategy}")
    print(f"Memories used: {len(context.ranked_memories)}")
    print("\n--- Generated Prompt ---")
    print(context.influence_prompt[:500] + "...")
