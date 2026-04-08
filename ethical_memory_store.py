# ethical_memory_manager_json.py

import json
import os
from datetime import datetime
from typing import Any, Dict, List


# ============================================================
#  Utilidades de ficheiros JSON
# ============================================================

def load_json(path: str, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default


def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ============================================================
#  Gestor Ético de Memória com persistência em JSON
# ============================================================

class EthicalMemoryManagerJSON:
    def __init__(self,
                 active_path="memories.json",
                 archive_path="memories_archive.json"):

        self.active_path = active_path
        self.archive_path = archive_path

        # Carregar ou criar ficheiros
        self.active_memories = load_json(active_path, default=[])
        self.archive_memories = load_json(archive_path, default=[])

        # Versão ética atual
        self.ethics_version = "1.0"
        self.current_policy = None  # Aqui podes guardar Norms.json ou outro

    # --------------------------------------------------------
    # Guardar memória nova
    # --------------------------------------------------------
    def save_memory(self, text: str, embedding: List[float], extra_metadata: Dict[str, Any] = None):
        metadata = extra_metadata.copy() if extra_metadata else {}
        metadata.update({
            "ethics_version": self.ethics_version,
            "timestamp": datetime.utcnow().isoformat()
        })

        mem_id = self._generate_id()

        memory = {
            "id": mem_id,
            "text": text,
            "embedding": embedding,
            "metadata": metadata
        }

        self.active_memories.append(memory)
        self._persist()

        return mem_id

    # --------------------------------------------------------
    # Atualizar política ética
    # --------------------------------------------------------
    def update_ethical_policy(self, new_policy: Any, new_version: str):
        self.current_policy = new_policy
        self.ethics_version = new_version
        self._re_evaluate_old_memories()

    # --------------------------------------------------------
    # Reavaliar memórias antigas
    # --------------------------------------------------------
    def _re_evaluate_old_memories(self):
        updated_active = []

        for mem in self.active_memories:
            old_version = mem["metadata"].get("ethics_version", "0")

            # Só reavaliar memórias antigas
            if old_version < self.ethics_version:
                if not self._passes_new_policy(mem):
                    self._move_to_archive(mem)
                    updated_active.append(self._anonymized_copy(mem))
                else:
                    # Atualizar versão ética
                    mem["metadata"]["ethics_version"] = self.ethics_version
                    updated_active.append(mem)
            else:
                updated_active.append(mem)

        self.active_memories = updated_active
        self._persist()

    # --------------------------------------------------------
    # Avaliação ética (aqui entra a LLM no futuro)
    # --------------------------------------------------------
    def _passes_new_policy(self, memory: Dict[str, Any]) -> bool:
        """
        Aqui vamos integrar a LLM.
        Por agora devolve sempre True.
        """
        return True

    # --------------------------------------------------------
    # Mover memória para o arquivo histórico
    # --------------------------------------------------------
    def _move_to_archive(self, mem: Dict[str, Any]):
        archived = mem.copy()
        archived["archived_at"] = datetime.utcnow().isoformat()
        self.archive_memories.append(archived)

    # --------------------------------------------------------
    # Criar versão anonimizada para manter no ativo
    # --------------------------------------------------------
    def _anonymized_copy(self, mem: Dict[str, Any]):
        new_mem = mem.copy()
        new_mem["text"] = f"[REMOVIDO PELA POLÍTICA ÉTICA v{self.ethics_version}]"
        new_mem["metadata"] = new_mem["metadata"].copy()
        new_mem["metadata"]["anonymized"] = True
        new_mem["metadata"]["anonymized_at"] = datetime.utcnow().isoformat()
        new_mem["metadata"]["ethics_version"] = self.ethics_version
        return new_mem

    # --------------------------------------------------------
    # Persistência em disco
    # --------------------------------------------------------
    def _persist(self):
        save_json(self.active_path, self.active_memories)
        save_json(self.archive_path, self.archive_memories)

    # --------------------------------------------------------
    # Gerar ID simples
    # --------------------------------------------------------
    def _generate_id(self) -> str:
        return datetime.utcnow().isoformat()
