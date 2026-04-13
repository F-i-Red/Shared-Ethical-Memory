# structured_ethical_memory.py - Versão final corrigida (usa os mesmos ficheiros do repo)

import json
from datetime import datetime
from typing import Dict, List

from ethical_memory_store import EthicalMemoryStore


class StructuredEthicalMemory:
    """
    Camada estruturada para memórias éticas.
    Usa exatamente os mesmos ficheiros do teu EthicalMemoryStore original (memories.json).
    Nada é apagado. Compatível com tudo o que já tinhas.
    """

    def __init__(self):
        # Usa os ficheiros originais do teu repo
        self.store = EthicalMemoryStore(
            active_path="memories.json",
            archive_path="memories_archive.json"
        )

    def add_ethical_memory(self,
                           principle: str,
                           context: str,
                           decision: str,
                           justification: str,
                           confidence: float = 0.85,
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
        """Devolve todas as memórias éticas guardadas."""
        ethical_list = []
        for mem in self.store.active_memories:
            try:
                data = json.loads(mem.get("text", "{}"))
                if isinstance(data, dict) and data.get("type") == "ethical":
                    ethical_list.append(data)
            except:
                pass
        return ethical_list
