# ethical_retriever.py
# Novo ficheiro - Retrieval inteligente para memórias éticas
# Não altera nada do código antigo

import json
from typing import List, Dict, Any
from structured_ethical_memory import StructuredEthicalMemory

class EthicalRetriever:
    """
    Faz buscas inteligentes nas memórias éticas.
    Usa scoring multi-objetivo: similaridade + relevância ética + novidade.
    """

    def __init__(self):
        self.structured_memory = StructuredEthicalMemory()

    def retrieve_relevant_ethics(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Busca memórias éticas relevantes para uma query do utilizador.
        """
        all_ethical = self.structured_memory.get_all_ethical_memories()
        
        if not all_ethical:
            return []

        scored = []
        for mem in all_ethical:
            # Scoring simples mas eficaz (podes melhorar depois)
            semantic_score = self._simple_semantic_score(query, mem)
            ethical_score = self._ethical_relevance_score(query, mem)
            novelty_score = 0.8  # placeholder - pode vir de timestamp ou uso

            final_score = 0.5 * semantic_score + 0.3 * ethical_score + 0.2 * novelty_score

            scored.append({
                "memory": mem,
                "score": round(final_score, 3)
            })

        # Ordena por score e devolve os melhores
        scored.sort(key=lambda x: x["score"], reverse=True)
        return [item["memory"] for item in scored[:top_k]]

    def _simple_semantic_score(self, query: str, mem: Dict) -> float:
        """Score simples baseado em palavras em comum (melhorar depois com embeddings)."""
        query_words = set(query.lower().split())
        text = f"{mem.get('principle', '')} {mem.get('context', '')} {mem.get('decision', '')}".lower()
        mem_words = set(text.split())
        if not query_words or not mem_words:
            return 0.0
        overlap = len(query_words & mem_words) / len(query_words)
        return min(overlap * 1.5, 1.0)  # dá mais peso se houver match

    def _ethical_relevance_score(self, query: str, mem: Dict) -> float:
        """Score baseado em quão ética parece a query."""
        ethics_keywords = ["ética", "moral", "princípio", "dano", "justiça", "direito", "harm", "fair", "right", "wrong"]
        query_lower = query.lower()
        if any(kw in query_lower for kw in ethics_keywords):
            return 0.95  # alta relevância ética
        return 0.6

    def build_context_for_llm(self, query: str, top_k: int = 5) -> str:
        """Constrói um contexto limpo para dar ao LLM."""
        relevant = self.retrieve_relevant_ethics(query, top_k)
        
        if not relevant:
            return "Nenhuma memória ética relevante encontrada."

        context = "=== Memórias Éticas Relevantes ===\n\n"
        for i, mem in enumerate(relevant, 1):
            context += f"{i}. Princípio: {mem.get('principle')}\n"
            context += f"   Contexto: {mem.get('context')}\n"
            context += f"   Decisão: {mem.get('decision')}\n"
            context += f"   Justificação: {mem.get('justification')}\n"
            context += f"   Confiança: {mem.get('confidence')}\n\n"

        return context
