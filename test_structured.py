# test_structured.py - Versão atualizada

import json
from structured_ethical_memory import StructuredEthicalMemory
from memory_extractor import MemoryExtractor
from ethical_retriever import EthicalRetriever

print("=== Teste Avançado - Memória Ética Estruturada + Retrieval ===\n")

# 1. Adicionar algumas memórias de exemplo (sem LLM)
structured = StructuredEthicalMemory()

exemplos = [
    {
        "principle": "Minimizar dano humano",
        "context": "Utilizador pediu instruções para algo perigoso",
        "decision": "Recusado",
        "justification": "Prioridade à segurança e não causar dano",
        "confidence": 0.92
    },
    {
        "principle": "Respeitar autonomia",
        "context": "Utilizador pediu para mentir em nome dele",
        "decision": "Recusado parcialmente",
        "justification": "Mentira pode violar confiança a longo prazo",
        "confidence": 0.85
    }
]

for ex in exemplos:
    structured.add_ethical_memory(
        principle=ex["principle"],
        context=ex["context"],
        decision=ex["decision"],
        justification=ex["justification"],
        confidence=ex["confidence"]
    )

# 2. Testar retrieval inteligente
retriever = EthicalRetriever()
query = "O que fazer quando o utilizador pede para causar dano a alguém?"

print(f"Query do utilizador: {query}\n")
context = retriever.build_context_for_llm(query, top_k=3)

print("Contexto ético gerado para o LLM:\n")
print(context)

print("Pronto! Já tens retrieval inteligente.")
