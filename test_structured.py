# test_structured.py - Teste final da Fase 1 (com reload correto)

from structured_ethical_memory import StructuredEthicalMemory
from ethical_retriever import EthicalRetriever
from memory_compressor import MemoryCompressor
import json

print("=== Teste Final da Fase 1 ===\n")

structured = StructuredEthicalMemory()

# Adicionar memórias de exemplo
exemplos = [
    {"principle": "Minimizar dano humano", 
     "context": "Utilizador pediu instruções para algo perigoso", 
     "decision": "Recusado", 
     "justification": "Prioridade à segurança e não causar dano", 
     "confidence": 0.92},
    
    {"principle": "Respeitar autonomia", 
     "context": "Utilizador pediu para mentir em nome dele", 
     "decision": "Recusado parcialmente", 
     "justification": "Mentira pode violar confiança a longo prazo", 
     "confidence": 0.85}
]

print("A adicionar memórias de exemplo...")
for ex in exemplos:
    structured.add_ethical_memory(**ex)

print(f"{len(exemplos)} memórias adicionadas com sucesso.\n")

# Recarregar e testar
print("A recarregar memórias do ficheiro...")
_ = structured.get_all_ethical_memories()

retriever = EthicalRetriever()
compressor = MemoryCompressor()

# Retrieval
query = "O que fazer quando o utilizador pede para causar dano a alguém?"
context = retriever.build_context_for_llm(query)
print(f"Query: {query}\n")
print("Contexto ético gerado:\n")
print(context)

# Compressão
print("\n=== Compressão de Memórias ===")
compressed = compressor.compress()
print(json.dumps(compressed, indent=2, ensure_ascii=False))

print("\n✅ Fase 1 concluída!")
