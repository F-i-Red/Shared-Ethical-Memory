# governance_core.py - VERSÃO CORRIGIDA (compatível com a Fase 1)

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

# Assumindo que os módulos das fases anteriores estão na mesma pasta
from structured_ethical_memory import StructuredEthicalMemory
from policy_engine import PolicyEngine, PolicyDecision
from multi_agent_debate import MultiAgentDebate
from memory_graph import MemoryGraph

class GovernanceCore:
    """
    Núcleo de governação da Fase 4.
    Orquestra o debate multi-agente, a política e a escrita no grafo de memória.
    """

    def __init__(self, graph_path: str = "memory_graph.json"):
        self.structured_mem = StructuredEthicalMemory()  # Base da Fase 1
        self.policy_engine = PolicyEngine()
        self.debate_engine = MultiAgentDebate()
        self.memory_graph = MemoryGraph(graph_path)  # Novo para a Fase 4
        self.log_path = Path("governance_log.json")
        self._ensure_log()

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

    def propose_memory(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pipeline completo de proposta de uma nova memória:
        1. Avaliação pela Policy Engine.
        2. Debate multi-agente.
        3. Decisão final (com regras de desempate).
        4. Se aprovada, escreve no grafo e na memória estruturada.
        """
        # 1. Policy check
        policy_decision: PolicyDecision = self.policy_engine.evaluate(memory)
        
        # 2. Multi-agent debate
        debate_result = self.debate_engine.debate(memory)
        
        # 3. Decisão final (lógica simples de desempate)
        final_action = "reject"
        reason = ""
        
        # Se a política rejeita, é rejeição imediata
        if policy_decision.action == "reject":
            final_action = "reject"
            reason = f"Policy veto: {policy_decision.reason}"
        # Se a política aceita, mas o debate sugere revisão, vamos para revise
        elif policy_decision.action == "accept" and debate_result.get("action") == "revise":
            final_action = "revise"
            reason = f"Debate suggests revision. Policy: {policy_decision.reason}. Debate: {debate_result.get('rationale')}"
        # Se a política aceita e o debate também, aceitamos
        elif policy_decision.action == "accept" and debate_result.get("action") == "accept":
            final_action = "accept"
            reason = f"Policy and debate aligned. {policy_decision.reason} | {debate_result.get('rationale')}"
        # Se a política é revise ou warn, seguimos a política
        elif policy_decision.action in ["revise", "warn"]:
            final_action = policy_decision.action
            reason = f"Policy decision: {policy_decision.reason}"
        else:
            # Fallback: rejeitar se algo correu mal
            final_action = "reject"
            reason = "No clear decision from governance."

        # 4. Ação
        if final_action == "accept":
            # Escreve na memória estruturada (Fase 1) - formato corrigido
            try:
                # Tentar usar o formato de dicionário primeiro
                mem_id = self.structured_mem.add_ethical_memory(memory)
            except TypeError:
                # Se falhar, tentar o formato posicional
                mem_id = self.structured_mem.add_ethical_memory(
                    principle=memory.get("principle", ""),
                    context=memory.get("context", ""),
                    decision=memory.get("decision", ""),
                    justification=memory.get("justification", ""),
                    confidence=memory.get("confidence", 0.5)
                )
            
            # Escreve no grafo (Fase 4)
            graph_node = self.memory_graph.add_node(memory)
            self._log_decision(memory, final_action, reason)
            return {
                "status": "accepted",
                "reason": reason,
                "memory_id": mem_id,
                "graph_node_id": graph_node.get("id")
            }
        elif final_action == "revise":
            self._log_decision(memory, final_action, reason)
            return {"status": "revise", "reason": reason, "suggestions": debate_result.get("votes", [])}
        else:  # reject ou warn
            self._log_decision(memory, final_action, reason)
            return {"status": final_action, "reason": reason}

    def build_influenced_context(self, query: str, top_k: int = 3) -> str:
        """
        Interface para o InfluenceRouter (Fase 4).
        Por agora, uma implementação simples que garante influência.
        """
        try:
            from ethical_retriever_v2 import EthicalRetriever
            retriever = EthicalRetriever()
            relevant_memories = retriever.retrieve_relevant_ethics(query, top_k)
        except ImportError:
            # Fallback para o retriever da Fase 1
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
        """Dispara o processo de consolidação (esquecimento e sumarização)."""
        try:
            from consolidation_scheduler import ConsolidationScheduler
            scheduler = ConsolidationScheduler()
            result = scheduler.run(dry_run=False)
            return result
        except ImportError:
            return {"status": "error", "message": "ConsolidationScheduler not available"}


# Pequeno teste se correres este ficheiro diretamente
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
