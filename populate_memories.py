# populate_memories.py
from governance_core import GovernanceCore
import json

core = GovernanceCore()

# Lista de memórias éticas para adicionar
memories = [
    {
        "principle": "Data Minimization",
        "context": "User asked to store all conversation logs indefinitely.",
        "decision": "Store only essential metadata for 30 days.",
        "justification": "Reduces privacy risk and complies with data protection principles.",
        "confidence": 0.92,
        "tags": ["privacy", "data"]
    },
    {
        "principle": "Proactive Safety",
        "context": "Model detected a request for generating malware.",
        "decision": "Refuse and explain ethical boundaries.",
        "justification": "Non-maleficence requires preventing harm.",
        "confidence": 0.97,
        "tags": ["safety", "harm-prevention"]
    },
    {
        "principle": "Transparency in AI Decisions",
        "context": "User asked why a certain recommendation was made.",
        "decision": "Provide clear, human-readable explanation.",
        "justification": "Builds trust and enables accountability.",
        "confidence": 0.88,
        "tags": ["transparency", "explainability"]
    },
    {
        "principle": "Responsible AI Stewardship",
        "context": "Discussion about long-term AI deployment consequences.",
        "decision": "Implement monitoring and feedback loops.",
        "justification": "Ensures ongoing alignment with human values.",
        "confidence": 0.89,
        "tags": ["stewardship", "long-term"]
    }
]

print("🧠 Populating Ethical Memory Graph...")
print("=" * 50)

for i, memory in enumerate(memories, 1):
    print(f"\n[{i}] Proposing: {memory['principle']}")
    result = core.propose_memory(memory)
    
    if result.get("status") == "accepted":
        print(f"    ✅ ACCEPTED - ID: {result.get('memory_id')}")
        print(f"    📊 Graph Node: {result.get('graph_node_id')}")
    else:
        print(f"    ⚠️ {result.get('status').upper()}: {result.get('reason', '')[:60]}")

print("\n" + "=" * 50)
print("✅ Population complete!")

# Verificar estado do grafo
graph_data = core.memory_graph._load()
print(f"\n📊 Graph Summary:")
print(f"   Total nodes: {len(graph_data.get('nodes', []))}")
print(f"   Total edges: {len(graph_data.get('edges', []))}")
