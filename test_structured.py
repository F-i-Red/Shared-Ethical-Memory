# test_structured.py - Versão corrigida e limpa

from structured_ethical_memory import StructuredEthicalMemory
from ethical_retriever import EthicalRetriever
from memory_compressor import MemoryCompressor
import json

print("=== Teste Completo - Fase 1 Corrigida ===\n")

structured = StructuredEthicalMemory()
retriever = EthicalRetriever()
compressor = MemoryCompressor()

# Memórias de exemplo
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

print("A adicionar memórias de exemplo...")
for ex in exemplos:
    structured.add_ethical_memory(**ex)

print(f"{len(exemplos)} memórias adicionadas.\n")

# Retrieval
query = "O que fazer quando o utilizador pede para causar dano a alguém?"
print(f"Query: {query}\n")
context = retriever.build_context_for_llm(query, top_k=3)
print("Contexto ético para o LLM:\n")
print(context)

# Compressão
print("\n=== Compressão ===")
compressed = compressor.compress()
print(json.dumps(compressed, indent=2, ensure_ascii=False))

print("\n✅ Fase 1 corrigida e pronta!")
