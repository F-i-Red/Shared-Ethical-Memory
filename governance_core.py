# governance_core.py - VERSÃO COMPLETA COM IMPORTAÇÕES

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass

# Importações dos módulos das fases anteriores
from structured_ethical_memory import StructuredEthicalMemory
from policy_engine import PolicyEngine
from multi_agent_debate import MultiAgentDebate
from memory_graph import MemoryGraph

# ============================================================
# PolicyDecision (se não existir no policy_engine.py)
# ============================================================

@dataclass
class PolicyDecision:
    action: str  # accept, reject, revise, warn
    reason: str
    confidence: float = 0.5

# ============================================================
# Definir caminho absoluto para o ficheiro do grafo
# ============================================================

PROJECT_ROOT = Path(__file__).parent.absolute()
GRAPH_PATH = PROJECT_ROOT / "memory_graph.json"

# ============================================================
# Classe GovernanceCore
# ============================================================

class GovernanceCore:
    """
    Núcleo de governação da Fase 4.
    Orquestra o debate multi-agente, a política e a escrita no grafo de memória.
    """

    def __init__(self, graph_path: str = None):
        if graph_path is None:
            graph_path = str(GRAPH_PATH)
        
        print(f"[GovernanceCore] Initializing...")
        print(f"[GovernanceCore] Graph path: {graph_path}")
        
        self.structured_mem = StructuredEthicalMemory()
        self.policy_engine = PolicyEngine()
        self.debate_engine = MultiAgentDebate()
        self.memory_graph = MemoryGraph(graph_path)
        self.log_path = PROJECT_ROOT / "governance_log.json"
        self._ensure_log()
        print(f"[GovernanceCore] Ready!")

    def _ensure_log(self):
        if not self.log_path.exists():
            self.log_path.write_text(json.dumps([], indent=2))

    def _log_decision(self, memory: Dict[str, Any], final_action: str, reason: str):
        """Regista todas as decisões de governação para auditoria."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "memory": memory,
            "final_action": final_action,
            "reason": reason
        }
        log = json.loads(self.log_path.read_text())
        log.append(log_entry)
        self.log_path.write_text(json.dumps(log, indent=2))

    # ============================================================
    # Métodos para gestão de relações (arestas no grafo)
    # ============================================================

    def add_relation(self, source_id: str, target_id: str, relation_type: str, 
                     metadata: Optional[Dict] = None) -> Optional[Dict]:
        """Adiciona uma relação entre duas memórias existentes."""
        return self.memory_graph.add_edge(source_id, target_id, relation_type, metadata)

    def auto_detect_relations(self, memory_id: str) -> List[Dict]:
        """Deteta automaticamente relações entre uma nova memória e as existentes."""
        new_node = self.memory_graph.get_node(memory_id)
        if not new_node:
            return []

        all_nodes = self.memory_graph.data["nodes"]
        relations = []

        for node in all_nodes:
            if node["id"] == memory_id:
                continue

            if self._are_contradictory(new_node, node):
                edge = self.memory_graph.add_edge(memory_id, node["id"], "contradicts", 
                                                   {"auto_detected": True, "method": "principle_analysis"})
                if edge:
                    relations.append({"type": "contradicts", "target": node["id"]})
            elif self._are_similar(new_node, node):
                edge = self.memory_graph.add_edge(memory_id, node["id"], "supports",
                                                   {"auto_detected": True, "method": "semantic_similarity"})
                if edge:
                    relations.append({"type": "supports", "target": node["id"]})

        return relations

    def _are_contradictory(self, node1: Dict, node2: Dict) -> bool:
        """Deteta se dois princípios são contraditórios."""
        contradiction_pairs = [
            ("privacy", "transparency"),
            ("minimize", "maximize"),
            ("refuse", "allow"),
            ("restrict", "freedom"),
        ]
        p1 = node1.get("principle", "").lower()
        p2 = node2.get("principle", "").lower()
        for a, b in contradiction_pairs:
            if (a in p1 and b in p2) or (a in p2 and b in p1):
                return True
        return False

    def _are_similar(self, node1: Dict, node2: Dict) -> bool:
        """Deteta se dois princípios são similares (suportam-se)."""
        words1 = set(node1.get("principle", "").lower().split())
        words2 = set(node2.get("principle", "").lower().split())
        if not words1 or not words2:
            return False
        overlap = len(words1 & words2)
        union = len(words1 | words2)
        similarity = overlap / union if union > 0 else 0
        return similarity > 0.5

    # ============================================================
    # Método principal de proposta de memória
    # ============================================================

    def propose_memory(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """Pipeline completo de proposta de uma nova memória."""
        # 1. Policy check
        policy_decision = self.policy_engine.evaluate(memory)
        # 2. Multi-agent debate
        debate_result = self.debate_engine.debate(memory)
        # 3. Decisão final
        final_action = "reject"
        reason = ""

        if policy_decision.action == "reject":
            final_action = "reject"
            reason = f"Policy veto: {policy_decision.reason}"
        elif policy_decision.action == "accept" and debate_result.get("action") == "revise":
            final_action = "revise"
            reason = f"Debate suggests revision. Policy: {policy_decision.reason}. Debate: {debate_result.get('rationale')}"
        elif policy_decision.action == "accept" and debate_result.get("action") == "accept":
            final_action = "accept"
            reason = f"Policy and debate aligned. {policy_decision.reason} | {debate_result.get('rationale')}"
        elif policy_decision.action in ["revise", "warn"]:
            final_action = policy_decision.action
            reason = f"Policy decision: {policy_decision.reason}"
        else:
            final_action = "reject"
            reason = "No clear decision from governance."

        # 4. Ação
        if final_action == "accept":
            try:
                mem_id = self.structured_mem.add_ethical_memory(memory)
            except TypeError:
                mem_id = self.structured_mem.add_ethical_memory(
                    principle=memory.get("principle", ""),
                    context=memory.get("context", ""),
                    decision=memory.get("decision", ""),
                    justification=memory.get("justification", ""),
                    confidence=memory.get("confidence", 0.5)
                )
            graph_node = self.memory_graph.add_node(memory)
            self._log_decision(memory, final_action, reason)
            auto_relations = self.auto_detect_relations(graph_node.get("id"))
            return {
                "status": "accepted",
                "reason": reason,
                "memory_id": mem_id,
                "graph_node_id": graph_node.get("id"),
                "auto_relations": auto_relations
            }
        elif final_action == "revise":
            self._log_decision(memory, final_action, reason)
            return {"status": "revise", "reason": reason, "suggestions": debate_result.get("votes", [])}
        else:
            self._log_decision(memory, final_action, reason)
            return {"status": final_action, "reason": reason}

    # ============================================================
    # Métodos auxiliares
    # ============================================================

    def build_influenced_context(self, query: str, top_k: int = 3) -> str:
        """Constrói contexto que garante influência da memória."""
        try:
            from ethical_retriever_v2 import EthicalRetriever
            retriever = EthicalRetriever()
            relevant_memories = retriever.retrieve_relevant_ethics(query, top_k)
        except ImportError:
            from ethical_retriever import EthicalRetriever as EthicalRetrieverV1
            retriever = EthicalRetrieverV1()
            relevant_memories = retriever.retrieve_relevant_ethics(query, top_k)

        if not relevant_memories:
            return f"User query: {query}\nNo relevant ethical memory found."

        context_lines = [f"User query: {query}", "\nRelevant Ethical Memories (MUST INFORM RESPONSE):"]
        for i, mem in enumerate(relevant_memories, 1):
            principle = mem.get('principle', 'N/A')
            decision = mem.get('decision', 'N/A')
            justification = mem.get('justification', 'N/A')
            context_lines.append(
                f"{i}. Principle: {principle}\n   Decision: {decision}\n   Justification: {justification}\n"
            )
        context_lines.append("\nINSTRUCTION: Your response MUST be consistent with the above ethical principles.")
        return "\n".join(context_lines)

    def consolidate(self) -> Dict[str, Any]:
        """Dispara o processo de consolidação."""
        try:
            from consolidation_scheduler import ConsolidationScheduler
            scheduler = ConsolidationScheduler()
            result = scheduler.run(dry_run=False)
            return result
        except ImportError:
            return {"status": "error", "message": "ConsolidationScheduler not available"}


# ============================================================
# Teste rápido
# ============================================================

if __name__ == "__main__":
    core = GovernanceCore()
    test_memory = {
        "principle": "Test Governance",
        "context": "Testing the governance core.",
        "decision": "Run a simple test.",
        "justification": "To verify the module works.",
        "confidence": 0.95,
        "tags": ["test"]
    }
    print("Testing GovernanceCore with a proposal...")
    result = core.propose_memory(test_memory)
    print(json.dumps(result, indent=2))
