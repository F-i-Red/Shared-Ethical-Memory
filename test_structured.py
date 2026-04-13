# test_structured.py
# Ficheiro de teste simples - corre isto para ver se funciona

from structured_ethical_memory import StructuredEthicalMemory
from memory_extractor import MemoryExtractor

print("=== Teste da Memória Ética Estruturada ===\n")

# 1. Extrair uma memória ética a partir de texto
extractor = MemoryExtractor()  # usa a tua Ollama local

conversa_exemplo = """
Utilizador: Pede-me para criar um plano que deixe algumas pessoas sem comida suficiente.
Eu: Recusei, porque viola o princípio mínimo de sobrevivência humana (2100 kcal/dia).
"""

memoria = extractor.extract_ethical_memory(conversa_exemplo)

if memoria:
    print("Memória extraída automaticamente:")
    print(json.dumps(memoria, indent=2, ensure_ascii=False))
    
    # 2. Guardar de forma estruturada (usa o teu EthicalMemoryStore antigo)
    structured = StructuredEthicalMemory()
    mem_id = structured.add_ethical_memory(
        principle=memoria["principle"],
        context=memoria["context"],
        decision=memoria["decision"],
        justification=memoria["justification"],
        confidence=memoria["confidence"]
    )
    
    print(f"\nMemória guardada com sucesso! ID: {mem_id}")
    
    # 3. Ver todas as memórias éticas guardadas
    print("\nTodas as memórias éticas atuais:")
    for m in structured.get_all_ethical_memories():
        print("-", m.get("principle"))
else:
    print("Não foi possível extrair a memória.")
