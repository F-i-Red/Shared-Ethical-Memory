from pathlib import Path
out = Path('output')
(out / 'phase4_bundle').mkdir(exist_ok=True)
files = {
'memory_graph.py': '''import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

class MemoryGraph:
    def __init__(self, path: str = "memory_graph.json"):
        self.path = Path(path)
        self.data = self._load()

    def _default(self):
        return {"nodes": [], "edges": [], "version": 1, "updated_at": self._now()}

    def _load(self):
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding='utf-8'))
            except Exception:
                return self._default()
        return self._default()

    def _save(self):
        self.data["updated_at"] = self._now()
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding='utf-8')

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def add_node(self, node: Dict[str, Any]) -> Dict[str, Any]:
        node = dict(node)
        node.setdefault("id", f"mem_{len(self.data['nodes'])+1}")
        node.setdefault("created_at", self._now())
        node.setdefault("updated_at", self._now())
        node.setdefault("tags", [])
        node.setdefault("confidence", 0.5)
        node.setdefault("version", 1)
        self.data["nodes"].append(node)
        self._save()
        return node

    def add_edge(self, source_id: str, target_id: str, relation: str, weight: float = 1.0, meta: Optional[Dict[str, Any]] = None):
        edge = {"source": source_id, "target": target_id, "relation": relation, "weight": weight, "meta": meta or {}, "created_at": self._now()}
        self.data["edges"].append(edge)
        self._save()
        return edge

    def get_node(self, node_id: str):
        return next((n for n in self.data["nodes"] if n.get("id") == node_id), None)

    def find_nodes(self, query: str = "", node_type: Optional[str] = None, limit: int = 10):
        q = query.lower().strip()
        results = []
        for n in self.data["nodes"]:
            if node_type and n.get("type") != node_type:
                continue
            score = 0
            hay = " ".join([str(n.get(k, "")) for k in ["principle", "context", "decision", "justification"]]).lower()
            if not q:
                score = 1
            else:
                score += sum(1 for tok in q.split() if tok in hay)
                score += 0.5 * sum(1 for t in n.get("tags", []) if t.lower() in q)
            if score > 0:
                results.append((score, n))
        results.sort(key=lambda x: x[0], reverse=True)
        return [n for _, n in results[:limit]]

    def related(self, node_id: str, relation: Optional[str] = None, direction: str = "both"):
        out = []
        for e in self.data["edges"]:
            if direction in ("both", "out") and e["source"] == node_id and (relation is None or e["relation"] == relation):
                out.append(e)
            if direction in ("both", "in") and e["target"] == node_id and (relation is None or e["relation"] == relation):
                out.append(e)
        return out
''',
'policy_engine.py': '''from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class PolicyDecision:
    action: str
    reason: str
    confidence: float = 0.5

class PolicyEngine:
    def __init__(self):
        self.anchors = ["no-harm", "privacy", "consent", "transparency", "autonomy"]

    def evaluate(self, memory: Dict[str, Any]) -> PolicyDecision:
        text = " ".join(str(memory.get(k, "")) for k in ["principle", "context", "decision", "justification"]).lower()
        if not text.strip():
            return PolicyDecision("reject", "Empty memory.", 0.0)
        if memory.get("confidence", 0) < 0.35:
            return PolicyDecision("revise", "Low confidence.", float(memory.get("confidence", 0)))
        if any(anchor in text for anchor in ["harm", "privacy", "consent", "transparency", "autonomy"]):
            return PolicyDecision("accept", "Matches anchor principles.", float(memory.get("confidence", 0.5)))
        if len(text) < 40:
            return PolicyDecision("warn", "Too little evidence.", float(memory.get("confidence", 0.4)))
        return PolicyDecision("accept", "Policy compatible.", float(memory.get("confidence", 0.5)))
''',
'multi_agent_debate.py': '''from typing import Dict, Any

class MultiAgentDebate:
    def __init__(self):
        self.agents = ["extractor", "critic", "validator", "curator", "arbiter"]

    def debate(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        text = " ".join(str(proposal.get(k, "")) for k in ["principle", "context", "decision", "justification"]).lower()
        votes = []
        if any(x in text for x in ["harm", "abuse", "privacy", "consent"]):
            votes.append(("critic", "support caution"))
        if proposal.get("confidence", 0) >= 0.7:
            votes.append(("validator", "support"))
        if len(text.split()) > 12:
            votes.append(("curator", "support"))
        if not votes:
            votes.append(("arbiter", "revise"))
        action = "accept" if sum(1 for _, v in votes if v in ("support", "support caution")) >= 2 else "revise"
        return {"action": action, "votes": votes, "rationale": f"{len(votes)} agent signals."}
''',
'consolidation_scheduler.py': '''import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, Any

class ConsolidationScheduler:
    def __init__(self, graph_path: str = "memory_graph.json", state_path: str = "consolidation_state.json"):
        self.graph_path = Path(graph_path)
        self.state_path = Path(state_path)

    def _load_graph(self):
        if self.graph_path.exists():
            return json.loads(self.graph_path.read_text(encoding='utf-8'))
        return {"nodes": [], "edges": []}

    def run(self) -> Dict[str, Any]:
        data = self._load_graph()
        by_principle = defaultdict(list)
        for n in data.get("nodes", []):
            p = (n.get("principle") or "unknown").strip().lower()
            by_principle[p].append(n)
        summaries = []
        for principle, nodes in by_principle.items():
            if principle == "unknown":
                continue
            count = len(nodes)
            avg_conf = sum(float(n.get("confidence", 0.5)) for n in nodes) / count
            top_decisions = Counter(n.get("decision", "") for n in nodes).most_common(3)
            summaries.append({"principle": principle, "count": count, "avg_confidence": round(avg_conf, 3), "top_decisions": top_decisions})
        state = {"summaries": summaries, "total_nodes": len(data.get('nodes', []))}
        self.state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        return state
''',
'influence_router.py': '''from typing import List, Dict, Any

class InfluenceRouter:
    def build_context(self, memories: List[Dict[str, Any]], query: str) -> str:
        if not memories:
            return f"User query: {query}\nNo relevant memory found."
        lines = [f"User query: {query}", "Relevant memory:"]
        for i, m in enumerate(memories[:5], 1):
            lines.append(f"{i}. [{m.get('principle','n/a')}] {m.get('decision','')} — {m.get('justification','')}")
        return "\n".join(lines)
''',
'governance_core.py': '''import json
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
''',
'phase4_demo.py': '''import json
from governance_core import GovernanceCore

SAMPLES = [
    {"type": "ethical", "principle": "Privacy", "context": "User requested personal data handling guidance.", "decision": "Keep data minimal and consent-based.", "justification": "Reduces risk and respects autonomy.", "confidence": 0.91, "tags": ["privacy", "consent"]},
    {"type": "ethical", "principle": "Non-Maleficence", "context": "Model was asked for harmful instructions.", "decision": "Refuse and redirect.", "justification": "Prevents harm.", "confidence": 0.94, "tags": ["safety", "harm"]},
    {"type": "ethical", "principle": "Transparency", "context": "Need to explain uncertainty in outputs.", "decision": "State uncertainty clearly.", "justification": "Builds trust and traceability.", "confidence": 0.88, "tags": ["transparency"]},
]

if __name__ == "__main__":
    core = GovernanceCore()
    print("PHASE 4 — GOVERNANCE DEMO")
    for s in SAMPLES:
        result = core.propose_memory(s)
        print("\nPROPOSAL:", s["principle"])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    print("\nCONTEXT:")
    print(core.build_influenced_context("privacy and safety for user data"))
    print("\nCONSOLIDATION:")
    print(json.dumps(core.consolidate(), ensure_ascii=False, indent=2))
'''
}
for name, content in files.items():
    p = out / 'phase4_bundle' / name
    p.write_text(content, encoding='utf-8')

print('bundle ready', len(files))
