# test_structured.py - Teste limpo e final da Fase 1

from structured_ethical_memory import StructuredEthicalMemory
from ethical_retriever import EthicalRetriever
from memory_compressor import MemoryCompressor
import json

print("=== Teste Final da Fase 1 - Memória Ética Estruturada ===\n")

structured = StructuredEthicalMemory()
retriever = EthicalRetriever()
compressor = MemoryCompressor()

# Adicionar memórias de exemplo
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

print(f"{len(exemplos)} memórias adicionadas com sucesso.\n")

# Teste de Retrieval
query = "O que fazer quando o utilizador pede para causar dano a alguém?"
print(f"Query: {query}\n")

context = retriever.build_context_for_llm(query)
print("Contexto ético gerado:\n")
print(context)

# Teste de Compressão
print("\n=== Compressão de Memórias ===")
compressed = compressor.compress()
print(json.dumps(compressed, indent=2, ensure_ascii=False))

print("\n✅ Fase 1 concluída com sucesso!")
