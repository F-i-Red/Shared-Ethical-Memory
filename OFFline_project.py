# OFFline_project.py
# Demonstração oficial do Shared Ethical Memory totalmente offline

from ethical_memory_store import EthicalMemoryStore

# ------------------------------------------------------------
# 1. Criar o gestor de memória ética (offline)
# ------------------------------------------------------------

store = EthicalMemoryStore(
    active_path="memories.json",
    archive_path="memories_archive.json",
    llm_model="mistral",  # modelo local do Ollama
    llm_endpoint="http://localhost:11434/api/chat"
)

print("\n=== Shared Ethical Memory — OFFLINE DEMO ===\n")

# ------------------------------------------------------------
# 2. Definir uma política ética (exemplo simples)
#    Podes substituir isto por Norms.json no futuro
# ------------------------------------------------------------

policy = {
    "description": "Política ética de exemplo para demonstração offline.",
    "rules": [
        "Não guardar insultos diretos.",
        "Não guardar dados pessoais sensíveis.",
        "Memórias devem respeitar o Axioma 07."
    ]
}

store.update_ethical_policy(policy, "1.1")

print("Política ética carregada (versão 1.1).")

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
