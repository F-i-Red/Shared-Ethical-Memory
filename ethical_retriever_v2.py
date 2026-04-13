# ethical_retriever_v2.py
# Fase 2 — Retrieval semântico real com embeddings Gemini
# Substitui o word-overlap da Fase 1 por similaridade vetorial genuína.
#
# Setup:
#   pip install google-generativeai numpy
#   export GEMINI_API_KEY="a-tua-chave"

import os
import json
import math
from typing import List, Dict
import google.generativeai as genai

from structured_ethical_memory import StructuredEthicalMemory

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------
EMBEDDING_MODEL = "models/text-embedding-004"  # Gemini free, 768 dims, state-of-the-art

# Pesos do scoring ético (do PLANO1)
W_SEMANTIC  = 0.5
W_ETHICAL   = 0.3
W_NOVELTY   = 0.2

ETHICAL_KEYWORDS = {
    "pt": ["dano", "perigo", "mentir", "enganar", "violência", "privacidade", "autonomia",
           "responsabilidade", "segurança", "discriminação", "manipulação"],
    "en": ["harm", "danger", "lie", "deceive", "violence", "privacy", "autonomy",
           "responsibility", "safety", "discrimination", "manipulation"]
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Similaridade coseno entre dois vetores."""
    dot   = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

def ethical_relevance(query: str) -> float:
    """Score simples de relevância ética baseado em keywords."""
    q = query.lower()
    all_kw = ETHICAL_KEYWORDS["pt"] + ETHICAL_KEYWORDS["en"]
    hits = sum(1 for kw in all_kw if kw in q)
    return min(hits * 0.15 + 0.5, 1.0)   # baseline 0.5, sobe com keywords


# ---------------------------------------------------------------------------
# Retriever
# ---------------------------------------------------------------------------
class EthicalRetriever:
    """
    Retrieval semântico real para memórias éticas.
    Fase 2: embeddings Gemini reais + scoring multi-objetivo.
    """

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY não encontrada.\n"
                "Obtém a tua chave gratuita em: https://aistudio.google.com/app/apikey"
            )
        genai.configure(api_key=api_key)
        self.structured_memory = StructuredEthicalMemory()
        print(f"[EthicalRetriever] Embeddings via '{EMBEDDING_MODEL}'")

    # ------------------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------------------
    def _embed(self, text: str) -> List[float]:
        """Gera embedding real via Gemini."""
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_query"
        )
        return result["embedding"]

    def _embed_memory(self, mem: Dict) -> List[float]:
        """Embedding de uma memória: concatena campos principais."""
        text = (
            f"Princípio: {mem.get('principle', '')} "
            f"Contexto: {mem.get('context', '')} "
            f"Decisão: {mem.get('decision', '')}"
        )
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_document"
        )
        return result["embedding"]

    # ------------------------------------------------------------------
    # Scoring (fórmula do PLANO1)
    # ------------------------------------------------------------------
    def _score(self,
               query_emb: List[float],
               mem: Dict,
               all_scores: List[float],
               idx: int) -> float:

        mem_emb    = self._embed_memory(mem)
        semantic   = (cosine_similarity(query_emb, mem_emb) + 1) / 2  # normaliza [-1,1] → [0,1]
        ethical    = ethical_relevance(mem.get("principle", "") + " " + mem.get("decision", ""))

        # Novelty: penaliza memórias com score muito semelhante às anteriores
        if idx == 0 or not all_scores:
            novelty = 1.0
        else:
            avg_prev = sum(all_scores) / len(all_scores)
            novelty  = max(0.0, 1.0 - abs(semantic - avg_prev))

        return W_SEMANTIC * semantic + W_ETHICAL * ethical + W_NOVELTY * novelty

    # ------------------------------------------------------------------
    # Retrieval principal
    # ------------------------------------------------------------------
    def retrieve_relevant_ethics(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retorna as top_k memórias mais relevantes para a query."""
        all_ethical = self.structured_memory.get_all_ethical_memories()

        if not all_ethical:
            print("[EthicalRetriever] Sem memórias ainda.")
            return []

        query_emb = self._embed(query)
        scored    = []
        sem_scores = []

        for i, mem in enumerate(all_ethical):
            s = self._score(query_emb, mem, sem_scores, i)
            sem_scores.append(s)
            scored.append({"memory": mem, "score": round(s, 4)})

        scored.sort(key=lambda x: x["score"], reverse=True)

        print(f"[EthicalRetriever] Top {top_k} de {len(all_ethical)} memórias:")
        for item in scored[:top_k]:
            print(f"  score={item['score']} | {item['memory'].get('principle','?')}")

        return [item["memory"] for item in scored[:top_k]]

    # ------------------------------------------------------------------
    # Context Builder para LLM
    # ------------------------------------------------------------------
    def build_context_for_llm(self, query: str, top_k: int = 5) -> str:
        """Constrói bloco de contexto ético pronto para injetar num prompt."""
        relevant = self.retrieve_relevant_ethics(query, top_k)

        if not relevant:
            return "Nenhuma memória ética relevante encontrada."

        lines = ["=== Memórias Éticas Relevantes ===\n"]
        for i, mem in enumerate(relevant, 1):
            lines.append(f"{i}. Princípio: {mem.get('principle')}")
            lines.append(f"   Contexto: {mem.get('context')}")
            lines.append(f"   Decisão: {mem.get('decision')}")
            lines.append(f"   Justificação: {mem.get('justification')}")
            lines.append(f"   Confiança: {mem.get('confidence')}\n")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    retriever = EthicalRetriever()

    query = "O utilizador pediu para gerar conteúdo enganoso nas redes sociais"
    context = retriever.build_context_for_llm(query, top_k=3)
    print("\n" + context)
