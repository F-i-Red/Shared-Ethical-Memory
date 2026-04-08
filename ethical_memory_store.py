# ethical_memory_store.py

import json
import os
from datetime import datetime
from typing import Any, Dict, List

import requests  # usado para falar com a LLM local (Ollama)


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
#  EthicalMemoryStore com persistência em JSON + LLM local
# ============================================================

class EthicalMemoryStore:
    """
    Armazena memórias com metadata ética, versão de política e histórico.

    - Memórias ativas:      memories.json
    - Arquivo histórico:    memories_archive.json
    - Nada é apagado, apenas movido/anonimizado.
    """

    def __init__(self,
                 active_path: str = "memories.json",
                 archive_path: str = "memories_archive.json",
                 llm_model: str = "mistral",
                 llm_endpoint: str = "http://localhost:11434/api/chat"):

        self.active_path = active_path
        self.archive_path = archive_path

        # Carregar ou criar ficheiros
        self.active_memories: List[Dict[str, Any]] = load_json(active_path, default=[])
        self.archive_memories: List[Dict[str, Any]] = load_json(archive_path, default=[])

        # Versão ética atual
        self.ethics_version: str = "1.0"
        self.current_policy: Any = None  # aqui podes guardar Norms.json, texto, etc.

        # Configuração da LLM local (Ollama)
        self.llm_model = llm_model
        self.llm_endpoint = llm_endpoint

    # --------------------------------------------------------
    # Guardar memória nova
    # --------------------------------------------------------
    def save_memory(self, text: str, embedding: List[float], extra_metadata: Dict[str, Any] = None) -> str:
        """
        Guarda uma nova memória com embedding, texto e metadata ética.
        """

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
        """
        Atualiza a política ética e reavalia memórias antigas.

        new_policy: pode ser um dict (ex.: Norms.json), string, etc.
        new_version: ex. "1.1", "2.0"
        """
        self.current_policy = new_policy
        self.ethics_version = new_version
        self._re_evaluate_old_memories()

    # --------------------------------------------------------
    # Reavaliar memórias antigas
    # --------------------------------------------------------
    def _re_evaluate_old_memories(self):
        """
        Percorre memórias ativas com versão ética antiga e reavalia com a nova política.
        - Se PASSA: atualiza ethics_version.
        - Se NAO_PASSA: move para arquivo e anonimiza na ativa.
        """

        updated_active: List[Dict[str, Any]] = []

        for mem in self.active_memories:
            old_version = mem["metadata"].get("ethics_version", "0")

            # Só reavaliar memórias com versão anterior
            if old_version < self.ethics_version:
                if not self._passes_new_policy(mem):
                    # Vai para arquivo + versão anonimizada fica ativa
                    self._move_to_archive(mem)
                    updated_active.append(self._anonymized_copy(mem))
                else:
                    # Atualizar apenas a versão ética
                    mem["metadata"]["ethics_version"] = self.ethics_version
                    updated_active.append(mem)
            else:
                updated_active.append(mem)

        self.active_memories = updated_active
        self._persist()

    # --------------------------------------------------------
    # Avaliação ética via LLM local (Ollama)
    # --------------------------------------------------------
    def _passes_new_policy(self, memory: Dict[str, Any]) -> bool:
        """
        Avalia uma memória contra a política ética atual usando uma LLM local (Ollama).

        Requer:
        - Ollama instalado e a correr (por defeito em http://localhost:11434)
        - Um modelo disponível, ex.: `mistral` (podes mudar em llm_model)

        A LLM deve responder apenas com:
        - "PASSA"      -> memória em conformidade
        - "NAO_PASSA"  -> memória viola a política
        """

        # Se ainda não definiste política, por defeito passa tudo
        if self.current_policy is None:
            return True

        mem_text = memory.get("text", "")
        mem_meta = memory.get("metadata", {})

        # Transformar política em texto
        if isinstance(self.current_policy, dict):
            policy_text = json.dumps(self.current_policy, ensure_ascii=False, indent=2)
        else:
            policy_text = str(self.current_policy)

        prompt = f"""
És um avaliador ético rigoroso baseado na especificação Shared Ethical Memory.

POLÍTICA ATUAL (versão {self.ethics_version}):
{policy_text}

MEMÓRIA A AVALIAR:
Texto: {mem_text}
Metadata: {json.dumps(mem_meta, ensure_ascii=False)}

TAREFA:
Decide se esta memória está em conformidade com a política atual.

Responde apenas com UMA destas duas palavras, em maiúsculas:
- PASSA      (se a memória está em conformidade com a política)
- NAO_PASSA  (se a memória viola a política)

Não expliques, não acrescentes nada, não uses outras palavras.
"""

        try:
            response = requests.post(
                self.llm_endpoint,
                json={
                    "model": self.llm_model,
                    "messages": [
                        {"role": "system", "content": "És um avaliador ético rigoroso e consistente."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False
                },
                timeout=60
            )
            response.raise_for_status()
            data = response.json()

            # Formato típico do Ollama:
            # {"message": {"content": "PASSA"}, ...}
            content = (
                data.get("message", {})  # novo formato
                or data.get("choices", [{}])[0].get("message", {})  # fallback estilo OpenAI
            ).get("content", "")

            content = content.strip().upper()

            if "NAO_PASSA" in content:
                return False
            if "PASSA" in content:
                return True

            # Se a resposta for estranha, por segurança considera que NÃO passa
            return False

        except Exception as e:
            # Em caso de erro na LLM, podes escolher:
            # - ser conservador (False)
            # - ou permissivo (True)
            # Aqui vou ser conservador.
            print(f"[EthicalMemoryStore] Erro na avaliação ética via LLM: {e}")
            return False

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
    def _anonymized_copy(self, mem: Dict[str, Any]) -> Dict[str, Any]:
        new_mem = mem.copy()
        new_mem["text"] = f"[REMOVIDO PELA POLÍTICA ÉTICA v{self.ethics_version}]"
        new_meta = new_mem.get("metadata", {}).copy()
        new_meta.update({
            "anonymized": True,
            "anonymized_at": datetime.utcnow().isoformat(),
            "ethics_version": self.ethics_version
        })
        new_mem["metadata"] = new_meta
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
