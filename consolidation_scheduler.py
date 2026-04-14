# consolidation_scheduler.py
# Gerencia o ciclo de vida da memória: consolidação, pruning e esquecimento controlado

import json
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict

@dataclass
class ConsolidationReport:
    """Relatório detalhado da operação de consolidação."""
    timestamp: str
    nodes_before: int
    nodes_after: int
    nodes_removed: int
    nodes_merged: int
    new_meta_memories: List[Dict[str, Any]]
    semantic_clusters: List[Dict[str, Any]]
    decay_summary: Dict[str, Any]

class ConsolidationScheduler:
    """
    Responsável por:
    1. Detetar memórias redundantes ou obsoletas (pruning)
    2. Agrupar memórias semanticamente similares (clustering)
    3. Gerar memórias de meta-nível a partir de clusters
    4. Aplicar decay temporal (memórias antigas perdem peso)
    5. Garantir que princípios âncora nunca são apagados
    """

    def __init__(self, graph_path: str = "memory_graph.json", 
                 anchor_principles: Optional[List[str]] = None):
        self.graph_path = Path(graph_path)
        self.anchor_principles = anchor_principles or [
            "no-harm", "non-maleficence", "privacy", "consent", 
            "transparency", "autonomy", "human-dignity"
        ]
        self.decay_days_threshold = 90  # Memórias com mais de 90 dias sem uso são candidatas a decay
        self.confidence_threshold = 0.3   # Abaixo disso, pode ser removido
        self.similarity_threshold = 0.85  # Acima disso, considera para merge

    def _load_graph(self) -> Dict[str, Any]:
        if self.graph_path.exists():
            return json.loads(self.graph_path.read_text(encoding='utf-8'))
        return {"nodes": [], "edges": []}

    def _save_graph(self, data: Dict[str, Any]):
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.graph_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    def _calculate_node_age_days(self, node: Dict[str, Any]) -> float:
        """Calcula idade do nó em dias."""
        created_at = node.get("created_at")
        if not created_at:
            return 0.0
        try:
            created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            delta = now - created
            return delta.days
        except Exception:
            return 0.0

    def _calculate_node_relevance(self, node: Dict[str, Any]) -> float:
        """
        Calcula relevância combinada: 
        - Confiança (peso 0.4)
        - Recência (peso 0.3) 
        - Uso (peso 0.3 - simulado por enquanto)
        """
        confidence = node.get("confidence", 0.5)
        age_days = self._calculate_node_age_days(node)
        recency_score = max(0.0, 1.0 - (age_days / self.decay_days_threshold))
        usage_score = node.get("access_count", 0) / 10.0  # Simples: cada 10 acessos = 1.0
        usage_score = min(usage_score, 1.0)
        
        relevance = (0.4 * confidence) + (0.3 * recency_score) + (0.3 * usage_score)
        return round(relevance, 3)

    def _simple_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calcula similaridade simples baseada em palavras-chave."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union if union > 0 else 0.0

    def _is_anchor(self, node: Dict[str, Any]) -> bool:
        """Verifica se o nó é um princípio âncora (nunca pode ser removido)."""
        principle = node.get("principle", "").lower()
        return any(anchor in principle for anchor in self.anchor_principles)

    def run(self, dry_run: bool = False) -> Dict[str, Any]:
        """
        Executa o pipeline completo de consolidação.
        Se dry_run=True, apenas simula e retorna relatório sem alterar dados.
        """
        data = self._load_graph()
        nodes = data.get("nodes", [])
        
        if not nodes:
            return {"status": "no_nodes", "message": "Graph is empty."}
        
        report = ConsolidationReport(
            timestamp=datetime.now(timezone.utc).isoformat(),
            nodes_before=len(nodes),
            nodes_after=0,
            nodes_removed=0,
            nodes_merged=0,
            new_meta_memories=[],
            semantic_clusters=[],
            decay_summary={}
        )
        
        # PASSO 1: Identificar nós para remoção (decay + baixa confiança)
        nodes_to_keep = []
        nodes_to_remove = []
        
        for node in nodes:
            if self._is_anchor(node):
                nodes_to_keep.append(node)
                continue
            
            relevance = self._calculate_node_relevance(node)
            if relevance < self.confidence_threshold:
                nodes_to_remove.append(node)
            else:
                nodes_to_keep.append(node)
        
        report.nodes_removed = len(nodes_to_remove)
        report.decay_summary = {
            "removed_low_relevance": report.nodes_removed,
            "confidence_threshold": self.confidence_threshold,
            "decay_days_threshold": self.decay_days_threshold
        }
        
        # PASSO 2: Detetar clusters semânticos para possível merge
        clusters = []
        used = set()
        
        for i, node1 in enumerate(nodes_to_keep):
            if i in used:
                continue
            cluster = [node1]
            text1 = f"{node1.get('principle', '')} {node1.get('context', '')}"
            
            for j, node2 in enumerate(nodes_to_keep[i+1:], i+1):
                if j in used:
                    continue
                text2 = f"{node2.get('principle', '')} {node2.get('context', '')}"
                similarity = self._simple_semantic_similarity(text1, text2)
                
                if similarity >= self.similarity_threshold:
                    cluster.append(node2)
                    used.add(j)
            
            if len(cluster) > 1:
                clusters.append(cluster)
                used.add(i)
            elif i not in used:
                clusters.append([node1])
                used.add(i)
        
        # PASSO 3: Processar clusters (merge ou manter)
        merged_nodes = []
        merge_count = 0
        
        for cluster in clusters:
            if len(cluster) > 1:
                # Merge: criar nó consolidado
                merged_node = self._merge_nodes(cluster)
                merged_nodes.append(merged_node)
                merge_count += len(cluster) - 1
            else:
                merged_nodes.append(cluster[0])
        
        report.nodes_merged = merge_count
        report.nodes_after = len(merged_nodes)
        
        # PASSO 4: Gerar meta-memórias a partir de clusters grandes
        meta_memories = []
        for cluster in clusters:
            if len(cluster) >= 3:
                meta = self._generate_meta_memory(cluster)
                if meta:
                    meta_memories.append(meta)
        
        report.new_meta_memories = meta_memories
        
        # PASSO 5: Atualizar grafo (se não for dry run)
        if not dry_run:
            # Adicionar meta-memórias como novos nós
            for meta in meta_memories:
                meta["type"] = "meta_memory"
                meta["created_at"] = datetime.now(timezone.utc).isoformat()
                merged_nodes.append(meta)
            
            data["nodes"] = merged_nodes
            data["last_consolidation"] = report.timestamp
            data["consolidation_stats"] = {
                "nodes_removed": report.nodes_removed,
                "nodes_merged": report.nodes_merged,
                "meta_generated": len(meta_memories)
            }
            self._save_graph(data)
        
        # Calcular clusters semânticos para relatório (amostra)
        report.semantic_clusters = [
            {
                "size": len(c),
                "principles": [n.get("principle", "unknown")[:50] for n in c[:3]]
            }
            for c in clusters if len(c) > 1
        ][:5]  # Limitar a 5 para não poluir o relatório
        
        return asdict(report)
    
    def _merge_nodes(self, nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Faz merge de múltiplos nós semanticamente similares."""
        # Pegar o nó com maior confiança como base
        base_node = max(nodes, key=lambda n: n.get("confidence", 0))
        
        # Agregar princípios
        principles = list(set(n.get("principle", "") for n in nodes if n.get("principle")))
        base_node["principle"] = " | ".join(principles[:3])  # Máximo 3 princípios
        
        # Média das confianças
        avg_confidence = sum(n.get("confidence", 0) for n in nodes) / len(nodes)
        base_node["confidence"] = round(avg_confidence, 3)
        
        # Marcar como merged
        base_node["merged_from"] = [n.get("id") for n in nodes if n.get("id")]
        base_node["merged_at"] = datetime.now(timezone.utc).isoformat()
        base_node["version"] = base_node.get("version", 1) + 1
        
        return base_node
    
    def _generate_meta_memory(self, cluster: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Gera uma memória de meta-nível a partir de um cluster."""
        if not cluster:
            return None
        
        principles = [n.get("principle", "") for n in cluster if n.get("principle")]
        contexts = [n.get("context", "") for n in cluster if n.get("context")]
        
        # Identificar tema comum (palavras mais frequentes)
        all_words = " ".join(principles + contexts).lower().split()
        word_freq = Counter(all_words)
        common_words = [w for w, c in word_freq.most_common(5) if len(w) > 3 and c >= 2]
        
        meta_principle = f"Meta: {', '.join(common_words[:3])} (consolidated from {len(cluster)} memories)"
        
        return {
            "principle": meta_principle,
            "context": f"Generated from consolidation of {len(cluster)} related memories.",
            "decision": "This meta-memory represents a higher-level pattern.",
            "justification": f"Semantic similarity threshold: {self.similarity_threshold}. Common themes: {', '.join(common_words[:5])}",
            "confidence": round(sum(n.get("confidence", 0) for n in cluster) / len(cluster), 3),
            "type": "meta_memory",
            "source_cluster_size": len(cluster)
        }

    def get_consolidation_status(self) -> Dict[str, Any]:
        """Retorna estatísticas atuais sem executar consolidação."""
        data = self._load_graph()
        nodes = data.get("nodes", [])
        
        anchor_count = sum(1 for n in nodes if self._is_anchor(n))
        low_relevance_count = sum(1 for n in nodes if not self._is_anchor(n) and self._calculate_node_relevance(n) < self.confidence_threshold)
        
        return {
            "total_nodes": len(nodes),
            "anchor_nodes": anchor_count,
            "low_relevance_candidates": low_relevance_count,
            "last_consolidation": data.get("last_consolidation"),
            "consolidation_stats": data.get("consolidation_stats", {})
        }


# Execução independente para teste
if __name__ == "__main__":
    scheduler = ConsolidationScheduler()
    print("=== Consolidation Scheduler Test ===")
    print("Status before:", scheduler.get_consolidation_status())
    print("\nRunning consolidation (dry run)...")
    report = scheduler.run(dry_run=True)
    print(f"Would remove {report['nodes_removed']} nodes, merge {report['nodes_merged']} nodes.")
    print(f"Would generate {len(report['new_meta_memories'])} meta-memories.")
