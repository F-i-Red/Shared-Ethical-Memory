# memory_graph.py - COM ARESTAS (versão melhorada)

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
from collections import defaultdict

class MemoryGraph:
    """
    Gerencia um grafo de memórias com nós e arestas.
    Relações suportadas: supports, contradicts, refines, derives_from, supersedes
    """

    def __init__(self, path: str = "memory_graph.json"):
        self.path = Path(path).expanduser().absolute()  # Converte para absoluto
        self.data = self._load()
        print(f"[MemoryGraph] Using path: {self.path}")  # Debug

    def _default(self):
        return {
            "nodes": [],
            "edges": [],
            "version": 1,
            "updated_at": self._now(),
            "statistics": {"total_nodes": 0, "total_edges": 0, "edge_types": {}}
        }

    def _load(self):
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding='utf-8'))
            except Exception:
                return self._default()
        return self._default()

    def _save(self):
        self.data["updated_at"] = self._now()
        self.data["statistics"] = {
            "total_nodes": len(self.data["nodes"]),
            "total_edges": len(self.data["edges"]),
            "edge_types": defaultdict(int, {})
        }
        for edge in self.data["edges"]:
            self.data["statistics"]["edge_types"][edge.get("type", "unknown")] += 1
        self.data["statistics"]["edge_types"] = dict(self.data["statistics"]["edge_types"])
        
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding='utf-8')

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def _node_exists(self, node_id: str) -> bool:
        """Verifica se um nó existe."""
        return any(n.get("id") == node_id for n in self.data["nodes"])

    def add_node(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Adiciona um nó (memória) ao grafo."""
        node = dict(node)
        node.setdefault("id", f"node_{len(self.data['nodes']) + 1}")
        node.setdefault("created_at", self._now())
        node.setdefault("updated_at", self._now())
        node.setdefault("tags", [])
        node.setdefault("confidence", 0.5)
        node.setdefault("version", 1)
        node.setdefault("type", "ethical")
        node.setdefault("access_count", 0)
        node.setdefault("last_accessed", None)
        
        self.data["nodes"].append(node)
        self._save()
        return node

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        for node in self.data["nodes"]:
            if node.get("id") == node_id:
                # Incrementar contador de acesso
                node["access_count"] = node.get("access_count", 0) + 1
                node["last_accessed"] = self._now()
                self._save()
                return node
        return None

    def add_edge(self, source_id: str, target_id: str, 
                 edge_type: str, metadata: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """
        Adiciona uma aresta entre dois nós.
        edge_type: supports, contradicts, refines, derives_from, supersedes
        """
        if not self._node_exists(source_id):
            print(f"[MemoryGraph] Erro: source node {source_id} não existe")
            return None
        if not self._node_exists(target_id):
            print(f"[MemoryGraph] Erro: target node {target_id} não existe")
            return None
        
        edge = {
            "id": f"edge_{len(self.data['edges']) + 1}",
            "source": source_id,
            "target": target_id,
            "type": edge_type,
            "created_at": self._now(),
            "metadata": metadata or {}
        }
        
        self.data["edges"].append(edge)
        self._save()
        return edge

    def get_edges_from(self, node_id: str, edge_type: Optional[str] = None) -> List[Dict]:
        """Retorna todas as arestas que saem de um nó."""
        result = []
        for edge in self.data["edges"]:
            if edge["source"] == node_id:
                if edge_type is None or edge["type"] == edge_type:
                    result.append(edge)
        return result

    def get_edges_to(self, node_id: str, edge_type: Optional[str] = None) -> List[Dict]:
        """Retorna todas as arestas que entram num nó."""
        result = []
        for edge in self.data["edges"]:
            if edge["target"] == node_id:
                if edge_type is None or edge["type"] == edge_type:
                    result.append(edge)
        return result

    def get_related_nodes(self, node_id: str, relation: Optional[str] = None) -> List[Tuple[str, str]]:
        """
        Retorna nós relacionados com o nó dado.
        Retorna lista de (node_id, relation_type)
        """
        related = []
        for edge in self.data["edges"]:
            if edge["source"] == node_id:
                if relation is None or edge["type"] == relation:
                    related.append((edge["target"], edge["type"]))
            if edge["target"] == node_id:
                if relation is None or edge["type"] == relation:
                    related.append((edge["source"], f"inverse_{edge['type']}"))
        return related

    def detect_conflicts(self, node_id: Optional[str] = None) -> List[Dict]:
        """
        Deteta conflitos no grafo.
        - Contradições diretas (edge type = contradicts)
        - Cadeias de contradições
        """
        conflicts = []
        
        if node_id:
            # Conflitos de um nó específico
            for edge in self.data["edges"]:
                if edge["type"] == "contradicts":
                    if edge["source"] == node_id or edge["target"] == node_id:
                        conflicts.append({
                            "type": "direct",
                            "source": edge["source"],
                            "target": edge["target"],
                            "edge_id": edge["id"]
                        })
        else:
            # Todos os conflitos
            for edge in self.data["edges"]:
                if edge["type"] == "contradicts":
                    conflicts.append({
                        "type": "direct",
                        "source": edge["source"],
                        "target": edge["target"],
                        "edge_id": edge["id"]
                    })
        
        return conflicts

    def find_path(self, source_id: str, target_id: str, max_depth: int = 5) -> Optional[List[str]]:
        """BFS para encontrar caminho entre dois nós."""
        if source_id == target_id:
            return [source_id]
        
        visited = set()
        queue = [(source_id, [source_id])]
        
        while queue:
            node_id, path = queue.pop(0)
            if node_id in visited:
                continue
            visited.add(node_id)
            
            for edge in self.data["edges"]:
                if edge["source"] == node_id:
                    next_node = edge["target"]
                    if next_node == target_id:
                        return path + [next_node]
                    if next_node not in visited and len(path) < max_depth:
                        queue.append((next_node, path + [next_node]))
        
        return None

    def get_graph_summary(self) -> Dict[str, Any]:
        """Retorna um resumo do grafo."""
        nodes = self.data["nodes"]
        edges = self.data["edges"]
        
        # Contar nós por tipo
        types = defaultdict(int)
        for node in nodes:
            types[node.get("type", "unknown")] += 1
        
        # Contar arestas por tipo
        edge_types = defaultdict(int)
        for edge in edges:
            edge_types[edge.get("type", "unknown")] += 1
        
        # Nós mais conectados
        node_degree = defaultdict(int)
        for edge in edges:
            node_degree[edge["source"]] += 1
            node_degree[edge["target"]] += 1
        
        top_nodes = sorted(node_degree.items(), key=lambda x: x[1], reverse=True)[:5]
        top_nodes_info = []
        for node_id, degree in top_nodes:
            node = self.get_node(node_id)
            if node:
                top_nodes_info.append({
                    "id": node_id,
                    "principle": node.get("principle", "N/A")[:50],
                    "degree": degree
                })
        
        return {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "node_types": dict(types),
            "edge_types": dict(edge_types),
            "most_connected_nodes": top_nodes_info,
            "conflicts": len(self.detect_conflicts())
        }


# Teste independente
if __name__ == "__main__":
    graph = MemoryGraph()
    
    # Adicionar nós
    n1 = graph.add_node({"principle": "Privacy First", "type": "ethical"})
    n2 = graph.add_node({"principle": "Data Minimization", "type": "ethical"})
    n3 = graph.add_node({"principle": "Maximum Utility", "type": "ethical"})
    
    print(f"Nós criados: {n1['id']}, {n2['id']}, {n3['id']}")
    
    # Adicionar relações
    graph.add_edge(n1['id'], n2['id'], "supports", {"confidence": 0.9})
    graph.add_edge(n1['id'], n3['id'], "contradicts", {"confidence": 0.8})
    graph.add_edge(n2['id'], n3['id'], "refines", {})
    
    # Ver resumo
    print("\n=== Graph Summary ===")
    summary = graph.get_graph_summary()
    for k, v in summary.items():
        print(f"  {k}: {v}")
    
    # Ver conflitos
    print("\n=== Conflicts ===")
    conflicts = graph.detect_conflicts()
    for c in conflicts:
        print(f"  {c['source']} contradicts {c['target']}")
    
    # Ver caminho
    print("\n=== Path ===")
    path = graph.find_path(n1['id'], n3['id'])
    print(f"  Path: {' → '.join(path)}")
