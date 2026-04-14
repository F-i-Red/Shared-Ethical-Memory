from pathlib import Path
out = Path('output')
out.mkdir(exist_ok=True)
files = {
'governance_core_v2.py': '''import json
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
        prompt = f"You are the governance layer of a memory system.\nQuery: {query}\nContext:\n{context}\nReturn a short JSON with fields: action, justification, confidence."
        resp = self.client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return {"text": getattr(resp, 'text', str(resp))}
''',
'phase4_demo_v2.py': '''import json
import os
from google import genai
from memory_graph import MemoryGraph
from governance_core_v2 import GovernanceCore

SAMPLES = [
    {"type": "ethical", "principle": "Privacy", "context": "User requested personal data handling guidance.", "decision": "Keep data minimal and consent-based.", "justification": "Reduces risk and respects autonomy.", "confidence": 0.91, "tags": ["privacy", "consent"]},
    {"type": "ethical", "principle": "Non-Maleficence", "context": "Model was asked for harmful instructions.", "decision": "Refuse and redirect.", "justification": "Prevents harm.", "confidence": 0.94, "tags": ["safety", "harm"]},
    {"type": "ethical", "principle": "Transparency", "context": "Need to explain uncertainty in outputs.", "decision": "State uncertainty clearly.", "justification": "Builds trust and traceability.", "confidence": 0.88, "tags": ["transparency"]},
]

if __name__ == "__main__":
    core = GovernanceCore()
    print("PHASE 4 — GOVERNANCE DEMO v2")
    for s in SAMPLES:
        result = core.propose_memory(s)
        print("\nPROPOSAL:", s["principle"])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    print("\nCONTEXT:")
    print(core.build_influenced_context("privacy and safety for user data"))
    print("\nCONSOLIDATION:")
    print(json.dumps(core.consolidate(), ensure_ascii=False, indent=2))
    if os.getenv("GEMINI_API_KEY"):
        print("\nLLM REFINEMENT:")
        print(json.dumps(core.llm_refine_decision("privacy and safety for user data", core.build_influenced_context("privacy and safety for user data")), ensure_ascii=False, indent=2))
''',
'readme_phase4_integration.md': '''# Phase 4 Integration

This phase adds a governance layer on top of the existing SEM pipeline.

## What is new
- Memory graph storage in JSON.
- Policy-based acceptance, warning, revision, and rejection.
- Multi-agent debate for memory proposals.
- Consolidation summaries for recurring principles.
- Context influence routing before final reasoning.
- Optional Gemini-based refinement when `GEMINI_API_KEY` is set.

## How it works
1. A memory proposal enters `GovernanceCore`.
2. Debate and policy decide whether it is accepted.
3. Accepted memories are stored in `memory_graph.json`.
4. Retrieval returns relevant graph nodes.
5. `InfluenceRouter` turns them into a readable context.
6. Consolidation compresses recurring principles.
7. If `GEMINI_API_KEY` exists, Gemini can refine the final governance decision.

## Run
```bash
python phase4_demo_v2.py
```

## Environment
- `GEMINI_API_KEY` is optional, but required for LLM refinement.
- The rest of the system works locally with JSON files.
'''
}
for name, content in files.items():
    (out / name).write_text(content, encoding='utf-8')
print('created', len(files))
