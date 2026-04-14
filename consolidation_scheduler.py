import json
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
