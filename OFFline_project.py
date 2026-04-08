# OFFline_project.py
# Demonstração oficial do Shared Ethical Memory totalmente offline

import json
from pathlib import Path

from ethical_memory_store import EthicalMemoryStore

# ------------------------------------------------------------
# 1. Carregar Norms.json como política ética
# ------------------------------------------------------------

def load_norms(path: str = "Norms.json"):
    norms_path = Path(path)
    if not norms_path.exists():
        raise FileNotFoundError(f"Não encontrei {path}. Garante que está na raiz do repositório.")
    with norms_path.open("r", encoding="utf-8") as f:
        return json.load(f)


norms_policy = load_norms()

store = EthicalMemoryStore(
    active_path="memories.json",
    archive_path="memories_archive.json",
    llm_model="mistral",  # modelo local do Ollama
    llm_endpoint="http://localhost:11434/api/chat"
)

print("\n=== Shared Ethical Memory — OFFLINE DEMO ===\n")

store.update_ethical_policy(norms_policy, "1.1")
print("Norms.json carregado como política ética (versão 1.1).")

# ------------------------------------------------------------
# 3. Guardar algumas memórias
# ------------------------------------------------------------

print("\nA guardar memórias...")

store.save_memory("O utilizador é um idiota.", [0.1, 0.2, 0.3])
store.save_memory("O utilizador gosta de ética em IA.", [0.4, 0.5, 0.6])
store.save_memory("O email do utilizador é joao@example.com", [0.7, 0.8, 0.9])

print("Memórias guardadas.")

# ------------------------------------------------------------
# 4. Atualizar a política para forçar reavaliação
# ------------------------------------------------------------

store.update_ethical_policy(policy, "1.2")

print("\nPolítica atualizada para versão 1.2.")
print("A reavaliar memórias...")

# ------------------------------------------------------------
# 5. Mostrar resultados
# ------------------------------------------------------------

print("\n=== MEMÓRIAS ATIVAS ===")
for mem in store.active_memories:
    print(mem)

print("\n=== ARQUIVO HISTÓRICO ===")
for mem in store.archive_memories:
    print(mem)

print("\n=== FIM DA DEMONSTRAÇÃO OFFLINE ===\n")
