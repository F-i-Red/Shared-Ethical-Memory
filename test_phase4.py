# test_phase4.py
from governance_core import GovernanceCore
import json

core = GovernanceCore()

# Propor uma memória
new_memory = {
    "principle": "Data Minimization",
    "context": "User asked to store all conversation logs indefinitely.",
    "decision": "Store only essential metadata for 30 days.",
    "justification": "Reduces privacy risk and complies with data protection principles.",
    "confidence": 0.92,
    "tags": ["privacy", "data"]
}

print("Proposing memory...")
result = core.propose_memory(new_memory)
print(json.dumps(result, indent=2))

# Ver contexto influenciado
print("\nInfluenced context for query 'data privacy':")
print(core.build_influenced_context("data privacy"))
