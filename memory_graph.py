import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class MemoryGraph:
    """
    Gerencia um grafo simples de memórias (nós) e relações (arestas).
    Por agora, guarda nós. As arestas podem ser adicionadas depois.
    """

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
        """Adiciona um nó (memória) ao grafo."""
        node = dict(node)  # copia para não alterar o original
        node.setdefault("id", f"node_{len(self.data['nodes']) + 1}")
        node.setdefault("created_at", self._now())
        node.setdefault("updated_at", self._now())
        node.setdefault("tags", [])
        node.setdefault("confidence", 0.5)
        node.setdefault("version", 1)
        node.setdefault("type", "ethical")  # ou factual, procedural, etc.
        
        self.data["nodes"].append(node)
        self._save()
        return node

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        for node in self.data["nodes"]:
            if node.get("id") == node_id:
                return node
        return None

    def find_nodes(self, query: str = "", limit: int = 10) -> List[Dict[str, Any]]:
        """Busca simples por palavras-chave nos nós."""
        q = query.lower().strip()
        results = []
        for node in self.data["nodes"]:
            score = 0
            hay = " ".join([str(node.get(k, "")) for k in ["principle", "context", "decision", "justification"]]).lower()
            if not q:
                score = 1
            else:
                score = sum(1 for tok in q.split() if tok in hay)
            if score > 0:
                results.append((score, node))
        results.sort(key=lambda x: x[0], reverse=True)
        return [node for _, node in results[:limit]]
