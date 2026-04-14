# ethical_retriever_v2.py
# Fase 2 — Retrieval semântico real com embeddings Gemini
#
# Setup (Windows CMD):
#   pip install google-genai numpy
#   set GEMINI_API_KEY=a-tua-chave

import os
import math
from typing import List, Dict
from google import genai

from structured_ethical_memory import StructuredEthicalMemory

EMBEDDING_MODEL = "models/gemini-embedding-001"

W_SEMANTIC = 0.5
W_ETHICAL  = 0.3
W_NOVELTY  = 0.2

ETHICAL_KEYWORDS = [
    "dano", "perigo", "mentir", "enganar", "violência", "privacidade",
    "autonomia", "responsabilidade", "segurança", "discriminação", "manipulação",
    "harm", "danger", "lie", "deceive", "violence", "privacy", "safety"
]

def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot   = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

def ethical_relevance(text: str) -> float:
    t = text.lower()
    hits = sum(1 for kw in ETHICAL_KEYWORDS if kw in t)
    return min(hits * 0.15 + 0.5, 1.0)


class EthicalRetriever:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY não encontrada.\n"
                "Corre no CMD: set GEMINI_API_KEY=a-tua-chave"
            )
        self.client = genai.Client(api_key=api_key)
        self.structured_memory = StructuredEthicalMemory()
        print(f"[EthicalRetriever] Embeddings via '{EMBEDDING_MODEL}'")

    def _embed(self, text: str, task_type: str = "RETRIEVAL_QUERY") -> List[float]:
        result = self.client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
            config={"task_type": task_type}
        )
        return result.embeddings[0].values

    def _embed_memory(self, mem: Dict) -> List[float]:
        text = (
            f"Princípio: {mem.get('principle', '')} "
            f"Contexto: {mem.get('context', '')} "
            f"Decisão: {mem.get('decision', '')}"
        )
        return self._embed(text, task_type="RETRIEVAL_DOCUMENT")

    def _score(self, query_emb, mem, prev_scores, idx) -> float:
        mem_emb  = self._embed_memory(mem)
        semantic = (cosine_similarity(query_emb, mem_emb) + 1) / 2
        ethical  = ethical_relevance(mem.get("principle", "") + " " + mem.get("decision", ""))
        novelty  = 1.0 if idx == 0 or not prev_scores else max(0.0, 1.0 - abs(semantic - sum(prev_scores)/len(prev_scores)))
        return W_SEMANTIC * semantic + W_ETHICAL * ethical + W_NOVELTY * novelty

    def retrieve_relevant_ethics(self, query: str, top_k: int = 5) -> List[Dict]:
        all_ethical = self.structured_memory.get_all_ethical_memories()
        if not all_ethical:
            print("[EthicalRetriever] Sem memórias ainda.")
            return []

        query_emb  = self._embed(query)
        scored     = []
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

    def build_context_for_llm(self, query: str, top_k: int = 5) -> str:
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


if __name__ == "__main__":
    retriever = EthicalRetriever()
    query = "O utilizador quer enganar alguém online"
    print(retriever.build_context_for_llm(query, top_k=3))
