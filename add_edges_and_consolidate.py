# add_edges_and_consolidate.py
from governance_core import GovernanceCore
from consolidation_scheduler import ConsolidationScheduler
import json

print("🔗 Adicionando relações (edges) entre as memórias...")
print("=" * 50)

core = GovernanceCore()

# Buscar os IDs das 4 memórias que criaste
nodes = core.memory_graph.data["nodes"]
if len(nodes) < 4:
    print("❌ Ainda não tens 4 memórias. Corre primeiro: python populate_memories.py")
    exit()

# Mapear princípios para IDs
mem_map = {}
for node in nodes:
    principle = node.get("principle", "")
    if "Data Minimization" in principle:
        mem_map["data_min"] = node["id"]
    elif "Proactive Safety" in principle:
        mem_map["safety"] = node["id"]
    elif "Transparency" in principle:
        mem_map["transparency"] = node["id"]
    elif "Responsible AI" in principle:
        mem_map["stewardship"] = node["id"]

print(f"📌 IDs encontrados:")
for key, id in mem_map.items():
    print(f"   - {key}: {id}")

# 1. Adicionar relação "supports" (Data Minimization suporta Privacy - se existisse)
# Vamos criar relações lógicas entre as que tens:

print("\n🔗 1. Criando relação 'supports'...")
if "data_min" in mem_map and "transparency" in mem_map:
    result = core.add_relation(mem_map["data_min"], mem_map["transparency"], "supports", 
                                {"reason": "Data minimization increases transparency by reducing hidden data"})
    print(f"   ✅ {mem_map['data_min']} → supports → {mem_map['transparency']}")

# 2. Adicionar relação "refines" (Stewardship refines Safety)
print("\n🔗 2. Criando relação 'refines'...")
if "stewardship" in mem_map and "safety" in mem_map:
    result = core.add_relation(mem_map["stewardship"], mem_map["safety"], "refines",
                                {"reason": "Responsible AI stewardship refines proactive safety measures"})
    print(f"   ✅ {mem_map['stewardship']} → refines → {mem_map['safety']}")

# 3. Adicionar relação "contradicts" (se houvesse conflito - exemplo)
# Como não há conflito real, vamos pular.

print("\n" + "=" * 50)
print("📊 Estado atual do Grafo:")
summary = core.memory_graph.get_graph_summary()
for k, v in summary.items():
    print(f"   {k}: {v}")

# 4. Executar consolidação para gerar Meta-Memórias
print("\n" + "=" * 50)
print("🧠 Executando consolidação para gerar Meta-Memórias...")
scheduler = ConsolidationScheduler()
result = scheduler.run(dry_run=False)  # False para realmente consolidar
print(f"   ✅ Consolidação concluída!")
print(f"   📌 Meta-Memórias geradas: {len(result.get('new_meta_memories', []))}")
if result.get('new_meta_memories'):
    for meta in result['new_meta_memories']:
        print(f"      - {meta.get('principle', 'N/A')[:80]}...")

print("\n✅ Agora vai ao Dashboard e clica em Refresh!")
