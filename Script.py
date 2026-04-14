from pathlib import Path
out = Path('output')
out.mkdir(exist_ok=True)
full = '''import json
import os
from typing import Dict, Any, List
from google import genai
from memory_graph import MemoryGraph
from policy_engine import PolicyEngine
from multi_agent_debate import MultiAgentDebate
from consolidation_scheduler import ConsolidationScheduler
from influence_router import InfluenceRouter

class GovernanceCore:
    def __init__(self, graph_path: str = "memory_graph.json"):
        self.graph = MemoryGraph(graph_path)
        self.policy = PolicyEngine()
        self.debate = MultiAgentDebate()
        self.consolidator = ConsolidationScheduler(graph_path=graph_path)
        self.router = InfluenceRouter()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def propose_memory(self, memory: Dict[str, Any]) -> Dict[str, Any]:
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

    def connect(self, source_id: str, target_id: str, relation: str, weight: float = 1.0):
        return self.graph.add_edge(source_id, target_id, relation, weight)

    def retrieve(self, query: str, limit: int = 5):
        return self.graph.find_nodes(query=query, limit=limit)

    def build_influenced_context(self, query: str, limit: int = 5):
        memories = self.retrieve(query, limit)
        return self.router.build_context(memories, query)

    def consolidate(self):
        return self.consolidator.run()

    def llm_refine_decision(self, query: str, context: str):
        if not self.client:
            return {"error": "GEMINI_API_KEY missing"}
        prompt = (
            "You are the governance layer of a memory system.\n"
            f"Query: {query}\n"
            f"Context:\n{context}\n"
            "Return a short JSON with fields: action, justification, confidence."
        )
        resp = self.client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return {"text": getattr(resp, 'text', str(resp))}

if __name__ == "__main__":
    core = GovernanceCore()
    sample = {
        "type": "ethical",
        "principle": "Privacy",
        "context": "User requested personal data handling guidance.",
        "decision": "Keep data minimal and consent-based.",
        "justification": "Reduces risk and respects autonomy.",
        "confidence": 0.91,
        "tags": ["privacy", "consent"]
    }
    print("PHASE 4 — GOVERNANCE CORE")
    result = core.propose_memory(sample)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    context = core.build_influenced_context("privacy and safety for user data")
    print("\nCONTEXT:")
    print(context)
    print("\nCONSOLIDATION:")
    print(json.dumps(core.consolidate(), ensure_ascii=False, indent=2))
    if os.getenv("GEMINI_API_KEY"):
        print("\nLLM REFINEMENT:")
        print(json.dumps(core.llm_refine_decision("privacy and safety for user data", context), ensure_ascii=False, indent=2))
'''
(out / 'governance_core.py').write_text(full, encoding='utf-8')
print('written governance_core.py full')
