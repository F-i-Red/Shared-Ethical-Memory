# test_structured.py - Teste completo da Fase 1 (corrigido)

from structured_ethical_memory import StructuredEthicalMemory
from ethical_retriever import EthicalRetriever
from memory_compressor import MemoryCompressor
import json

print("=== Teste Completo - Memória Ética Estruturada + Retrieval + Compressão ===\n")

structured = StructuredEthicalMemory()
retriever = EthicalRetriever()
compressor = MemoryCompressor()

# === Memórias de exemplo (sempre adicionadas) ===
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
    structured.add_ethical_memory(**ex)   # <--- Esta linha é importante!

print(f"{len(exemplos)} memórias de exemplo adicionadas com sucesso.\n")

# === Teste de Retrieval Inteligente ===
query = "O que fazer quando o utilizador pede para causar dano a alguém?"
print(f"Query do utilizador: {query}\n")

context = retriever.build_context_for_llm(query, top_k=3)
print("Contexto ético gerado para o LLM:\n")
print(context)

# === Teste de Compressão ===
print("\n=== Compressão de Memórias ===")
compressed = compressor.compress()
print(json.dumps(compressed, indent=2, ensure_ascii=False))

print("\n✅ Teste completo terminado!")
print("Já tens a Fase 1 do plano original funcionando (memória estruturada + retrieval + compressão).")
