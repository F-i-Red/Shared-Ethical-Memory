import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass

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
        if any(anchor in text for anchor in self.anchors):
            return PolicyDecision("accept", "Matches anchor principles.", float(memory.get("confidence", 0.5)))
        if len(text) < 40:
            return PolicyDecision("warn", "Too little evidence.", float(memory.get("confidence", 0.4)))
        return PolicyDecision("accept", "Policy compatible.", float(memory.get("confidence", 0.5)))

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

    def find_nodes(self, query: str = "", limit: int = 10):
        q = query.lower().strip()
        results = []
        for n in self.data["nodes"]:
            score = 0
            hay = " ".join([str(n.get(k, "")) for k in ["principle", "context", "decision", "justification"]]).lower()
            if not q:
                score = 1
            else:
                score += sum(1 for tok in q.split() if tok in hay)
            if score > 0:
                results.append((score, n))
        results.sort(key=lambda x: x[0], reverse=True)
        return [n for _, n in results[:limit]]

class InfluenceRouter:
    def build_context(self, memories: List[Dict[str, Any]], query: str) -> str:
        if not memories:
            return f"User query: {query}\\nNo relevant memory found."
        lines = [f"User query: {query}", "Relevant memory:"]
        for i, m in enumerate(memories[:5], 1):
            lines.append(f"{i}. [{m.get('principle','n/a')}] {m.get('decision','')} — {m.get('justification','')}")
        return "\\n".join(lines)

class ConsolidationScheduler:
    def __init__(self, graph_path: str = "memory_graph.json"):
        self.graph_path = Path(graph_path)

    def _load_graph(self):
        if self.graph_path.exists():
            return json.loads(self.graph_path.read_text(encoding='utf-8'))
        return {"nodes": []}

    def run(self) -> Dict[str, Any]:
        data = self._load_graph()
        from collections import defaultdict, Counter
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
            summaries.append({"principle": principle, "count": count, "avg_confidence": round(avg_conf, 3)})
        return {"summaries": summaries, "total_nodes": len(data.get('nodes', []))}

class GovernanceCore:
    def __init__(self):
        self.graph = MemoryGraph()
        self.policy = PolicyEngine()
        self.debate = MultiAgentDebate()
        self.consolidator = ConsolidationScheduler()
        self.router = InfluenceRouter()

    def propose_memory(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        debate = self.debate.debate(memory)
        policy = self.policy.evaluate(memory)
        action = policy.action
        if debate["action"] == "revise" and action == "accept
