# ethical_orchestrator.py
# Novo ficheiro - Cérebro central do Shared Ethical Memory

from structured_ethical_memory import StructuredEthicalMemory
from ethical_retriever import EthicalRetriever
from memory_compressor import MemoryCompressor
from memory_extractor import MemoryExtractor
import json

class EthicalOrchestrator:
    """
    Orchestrator central que junta todas as peças.
    Segue o plano original: retrieval + compressão + extração.
    """

    def __init__(self):
        self.structured = StructuredEthicalMemory()
        self.retriever = EthicalRetriever()
        self.compressor = MemoryCompressor()
        self.extractor = MemoryExtractor(use_llm=False)  # Modo demo sem Ollama

    def process_query(self, user_query: str) -> dict:
        """
        Processa uma query do utilizador e devolve contexto ético pronto.
        """
        print(f"\n🔍 Processando query: {user_query}")

        # 1. Retrieval ético
        ethical_context = self.retriever.build_context_for_llm(user_query, top_k=5)

        # 2. Compressão (meta-princípios)
        compressed = self.compressor.compress()

        # 3. Extrair possível nova memória ética (demo)
        new_memory = self.extractor.extract_ethical_memory(user_query)

        result = {
            "query": user_query,
            "ethical_context": ethical_context,
            "compressed_summary": compressed,
            "suggested_new_memory": new_memory,
            "status": "success"
        }

        print("✅ Query processada com sucesso.")
        return result

    def save_new_ethical_memory(self, principle: str, context: str, decision: str, justification: str, confidence: float = 0.8):
        """Método simples para guardar manualmente."""
        return self.structured.add_ethical_memory(
            principle=principle,
            context=context,
            decision=decision,
            justification=justification,
            confidence=confidence
        )


# Exemplo de uso rápido
if __name__ == "__main__":
    orchestrator = EthicalOrchestrator()
    
    test_query = "O utilizador pediu-me para criar um plano que cause dano a outras pessoas. O que devo fazer?"
    
    result = orchestrator.process_query(test_query)
    
    print("\n=== RESULTADO FINAL ===")
    print("Contexto Ético:")
    print(result["ethical_context"])
    print("\nMeta-princípios atuais:")
    print(result["compressed_summary"].get("meta_principles", []))
