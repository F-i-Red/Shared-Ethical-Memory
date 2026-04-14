import json
from memory_graph import MemoryGraph
from policy_engine import PolicyEngine
from multi_agent_debate import MultiAgentDebate
from consolidation_scheduler import ConsolidationScheduler
from influence_router import InfluenceRouter

class GovernanceCore:
    def __init__(self):
        self.graph = MemoryGraph()
        self.policy = PolicyEngine()
        self.debate = MultiAgentDebate()
        self.consolidator = ConsolidationScheduler()
        self.router = InfluenceRouter()

    def propose_memory(self, memory):
        debate = self.debate.debate(memory)
        policy = self.policy.evaluate(memory)
        action = policy.action
        if debate["action"] == "revise" and action == "accept":
            action = "warn"
        result = {"policy": policy.__dict__, "debate": debate, "action": action}
        if action in ("accept", "warn"):
            node = self.graph.add_node(memory)
            result["node"] = node
        return result

    def connect(self, source_id, target_id, relation, weight=1.0):
        return self.graph.add_edge(source_id, target_id, relation, weight)

    def retrieve(self, query, limit=5):
        return self.graph.find_nodes(query=query, limit=limit)

    def build_influenced_context(self, query, limit=5):
        memories = self.retrieve(query, limit)
        return self.router.build_context(memories, query)

    def consolidate(self):
        return self.consolidator.run()
