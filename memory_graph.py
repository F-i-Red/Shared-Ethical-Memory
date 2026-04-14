import json
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
