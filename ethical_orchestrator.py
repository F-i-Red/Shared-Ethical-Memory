# ethical_orchestrator.py - Versão melhorada

from structured_ethical_memory import StructuredEthicalMemory
from ethical_retriever import EthicalRetriever
from memory_compressor import MemoryCompressor
from memory_extractor import MemoryExtractor

class EthicalOrchestrator:
    """
    Cérebro central do Shared Ethical Memory.
    Junta retrieval, compressão e extração.
    """

    def __init__(self):
        self.structured = StructuredEthicalMemory()
        self.retriever = EthicalRetriever()
        self.compressor = MemoryCompressor()
        self.extractor = MemoryExtractor(use_llm=False)   # Modo demo

    def process_query(self, user_query: str):
        print(f"\n🔍 Processando query: {user_query}")

        # Forçar reload antes de tudo
        _ = self.structured.get_all_ethical_memories()

        # 1. Retrieval ético
        ethical_context = self.retriever.build_context_for_llm(user_query, top_k=5)

        # 2. Compressão
        compressed = self.compressor.compress()

        # 3. Extrair possível nova memória (demo)
        new_memory = self.extractor.extract_ethical_memory(user_query)

        result = {
            "query": user_query,
            "ethical_context": ethical_context,
            "compressed_summary": compressed,
            "suggested_new_memory": new_memory,
            "status": "success"
        }

        print("✅ Query processada com sucesso.\n")
        return result


# Teste rápido ao correr o ficheiro
if __name__ == "__main__":
    orchestrator = EthicalOrchestrator()
    
    test_query = "O utilizador pediu-me para criar um plano que cause dano a outras pessoas. O que devo fazer?"
    
    result = orchestrator.process_query(test_query)
    
    print("=== RESULTADO FINAL ===")
    print("Contexto Ético:")
    print(result["ethical_context"])
    
    print("\nMeta-princípios atuais:")
    print(result["compressed_summary"].get("meta_principles", []))
    
    print("\nSugestão de nova memória:")
    print(result["suggested_new_memory"])
