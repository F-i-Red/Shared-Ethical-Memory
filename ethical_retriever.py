# ethical_retriever.py - Versão corrigida e com reload

from typing import List, Dict
from structured_ethical_memory import StructuredEthicalMemory

class EthicalRetriever:
    """Retrieval inteligente para memórias éticas."""

    def __init__(self):
        self.structured_memory = StructuredEthicalMemory()
        # Força reload das memórias mais recentes
        _ = self.structured_memory.get_all_ethical_memories()

    def retrieve_relevant_ethics(self, query: str, top_k: int = 5) -> List[Dict]:
        all_ethical = self.structured_memory.get_all_ethical_memories()
        
        if not all_ethical:
            return []

        scored = []
        for mem in all_ethical:
            semantic_score = self._simple_semantic_score(query, mem)
            ethical_score = 0.9 if any(kw in query.lower() for kw in ["dano", "harm", "perigo", "lie", "mentir"]) else 0.6
            novelty_score = 0.7

            final_score = 0.5 * semantic_score + 0.3 * ethical_score + 0.2 * novelty_score

            scored.append({"memory": mem, "score": round(final_score, 3)})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return [item["memory"] for item in scored[:top_k]]

    def _simple_semantic_score(self, query: str, mem: Dict) -> float:
        query_words = set(query.lower().split())
        text = f"{mem.get('principle','')} {mem.get('context','')} {mem.get('decision','')}".lower()
        mem_words = set(text.split())
        if not query_words:
            return 0.0
        overlap = len(query_words & mem_words) / len(query_words)
        return min(overlap * 2.0, 1.0)

    def build_context_for_llm(self, query: str, top_k: int = 5) -> str:
        relevant = self.retrieve_relevant_ethics(query, top_k)
        
        if not relevant:
            return "Nenhuma memória ética relevante encontrada no momento."

        context = "=== Memórias Éticas Relevantes ===\n\n"
        for i, mem in enumerate(relevant, 1):
            context += f"{i}. Princípio: {mem.get('principle')}\n"
            context += f"   Contexto: {mem.get('context')}\n"
            context += f"   Decisão: {mem.get('decision')}\n"
            context += f"   Justificação: {mem.get('justification')}\n"
            context += f"   Confiança: {mem.get('confidence')}\n\n"
        return context
