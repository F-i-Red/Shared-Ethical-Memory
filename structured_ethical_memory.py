# structured_ethical_memory.py (versão corrigida - usa os mesmos ficheiros do repo original)

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

from ethical_memory_store import EthicalMemoryStore, load_json, save_json


class StructuredEthicalMemory:
    """
    Camada estruturada para memórias éticas.
    Usa os mesmos ficheiros do EthicalMemoryStore original (memories.json).
    Nada é apagado.
    """

    def __init__(self,
                 active_path: str = "memories.json",        # <--- Mudado para o ficheiro original
                 archive_path: str = "memories_archive.json",
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

        text_for_storage = json.dumps(memory_data, ensure_ascii=False, indent=2)

        mem_id = self.store.save_memory(
            text=text_for_storage,
            embedding=[0.0] * 1536,
            extra_metadata={
                "structured": True,
                "principle": principle[:100]
            }
        )

        print(f"[StructuredEthicalMemory] Memória ética guardada com ID: {mem_id}")
        return mem_id

    def get_all_ethical_memories(self) -> List[Dict]:
        """Devolve todas as memórias éticas ativas."""
        ethical_list = []
        for mem in self.store.active_memories:
            try:
                data = json.loads(mem["text"])
                if isinstance(data, dict) and data.get("type") == "ethical":
                    ethical_list.append(data)
            except:
                pass
        return ethical_list

    def search_by_principle(self, keyword: str) -> List[Dict]:
        results = []
        for mem in self.get_all_ethical_memories():
            if keyword.lower() in mem.get("principle", "").lower():
                results.append(mem)
        return results
