# test_edges.py - Testar arestas do grafo

from memory_graph import MemoryGraph
from governance_core import GovernanceCore

print("=== Testing Graph Edges ===\n")

# 1. Criar grafo
graph = MemoryGraph()
print("1. Graph created")

# 2. Adicionar nós
n1 = graph.add_node({"principle": "Privacy First", "type": "ethical", "confidence": 0.95})
n2 = graph.add_node({"principle": "Data Minimization", "type": "ethical", "confidence": 0.92})
n3 = graph.add_node({"principle": "Maximum Utility", "type": "ethical", "confidence": 0.85})

print(f"2. Nodes added: {n1['id']}, {n2['id']}, {n3['id']}")

# 3. Adicionar arestas
graph.add_edge(n1['id'], n2['id'], "supports", {"confidence": 0.9, "reason": "Privacy requires minimizing data"})
graph.add_edge(n1['id'], n3['id'], "contradicts", {"confidence": 0.8, "reason": "Privacy vs Utility trade-off"})
graph.add_edge(n2['id'], n3['id'], "refines", {})

print("3. Edges added")

# 4. Ver relações
print("\n4. Relations from Privacy First:")
edges_from = graph.get_edges_from(n1['id'])
for e in edges_from:
    print(f"   → {e['target']} ({e['type']})")

# 5. Ver conflitos
print("\n5. Conflicts detected:")
conflicts = graph.detect_conflicts()
for c in conflicts:
    print(f"   {c['source']} → {c['target']}")

# 6. Ver resumo
print("\n6. Graph Summary:")
summary = graph.get_graph_summary()
for k, v in summary.items():
    print(f"   {k}: {v}")

print("\n✅ Graph with edges working!")
