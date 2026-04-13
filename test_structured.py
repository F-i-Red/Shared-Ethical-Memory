# test_structured.py - Teste completo da Fase 1

from structured_ethical_memory import StructuredEthicalMemory
from ethical_retriever import EthicalRetriever
from memory_compressor import MemoryCompressor

print("=== Teste Completo - Memória Ética Estruturada + Retrieval + Compressão ===\n")

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

for ex in exemplos:
    structured.add_ethical_memory(**ex)

# Retrieval
query = "O que fazer quando o utilizador pede para causar dano?"
context = retriever.build_context_for_llm(query)
print("Contexto ético para LLM:\n", context)

# Compressão
compressed = compressor.compress()
print("\nResultado da compressão:\n", json.dumps(compressed, indent=2, ensure_ascii=False))



# 2. Testar retrieval inteligente
retriever = EthicalRetriever()
query = "O que fazer quando o utilizador pede para causar dano a alguém?"

print(f"Query do utilizador: {query}\n")
context = retriever.build_context_for_llm(query, top_k=3)

print("Contexto ético gerado para o LLM:\n")
print(context)

print("Pronto! Já tens retrieval inteligente.")
