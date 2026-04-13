# structured_ethical_memory.py
# Novo ficheiro - não altera nada do código antigo

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

# Vamos usar o teu EthicalMemoryStore existente para guardar as memórias estruturadas
from ethical_memory_store import EthicalMemoryStore, load_json, save_json


class StructuredEthicalMemory:
    """
    Camada estruturada para memórias éticas.
    Segue o plano: principle, context, decision, justification, confidence.
    Tudo é guardado usando o teu EthicalMemoryStore (nada é apagado).
    """

    def __init__(self,
                 active_path: str = "structured_ethical_memories.json",
                 archive_path: str = "structured_ethical_archive.json",
                 llm_model: str = "mistral",
                 llm_endpoint: str = "http://localhost:11434/api/chat"):

        self.store = EthicalMemoryStore(
            active_path=active_path,
            archive_path=archive_path,
            llm_model=llm_model,
            llm_endpoint=llm_endpoint
        )

    def add_ethical_memory(self,
                           principle: str,
                           context: str,
                           decision: str,
                           justification: str,
                           confidence: float = 0.8,
                           extra_tags: List[str] = None) -> str:
        """
        Adiciona uma memória ética bem estruturada.
        """
        if extra_tags is None:
            extra_tags = []

        memory_data = {
            "type": "ethical",
            "principle": principle.strip(),
            "context": context.strip(),
            "decision": decision.strip(),
            "justification": justification.strip(),
            "confidence": float(confidence),
            "tags": extra_tags,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "structured_v1"
        }

        # Guarda como texto JSON bonito para o LLM conseguir ler facilmente
        text_for_storage = json.dumps(memory_data, ensure_ascii=False, indent=2)

        # Usa o teu store existente (nada muda no código antigo)
        mem_id = self.store.save_memory(
            text=text_for_storage,
            embedding=[0.0] * 1536,  # placeholder - podes melhorar depois com embeddings reais
            extra_metadata={
                "structured": True,
                "principle": principle[:100]  # resumo para busca rápida
            }
        )

        print(f"[StructuredEthicalMemory] Memória ética guardada com ID: {mem_id}")
        return mem_id

    def get_all_ethical_memories(self) -> List[Dict]:
        """Devolve todas as memórias éticas ativas (bem estruturadas)."""
        ethical_list = []
        for mem in self.store.active_memories:
            try:
                data = json.loads(mem["text"])
                if data.get("type") == "ethical":
                    ethical_list.append(data)
            except:
                pass  # ignora memórias antigas que não são estruturadas
        return ethical_list

    def search_by_principle(self, keyword: str) -> List[Dict]:
        """Busca simples por palavra no princípio."""
        results = []
        for mem in self.get_all_ethical_memories():
            if keyword.lower() in mem.get("principle", "").lower():
                results.append(mem)
        return results
