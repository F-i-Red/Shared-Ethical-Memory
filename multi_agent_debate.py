from typing import Dict, Any, List, Tuple

class MultiAgentDebate:
    """
    Simula um debate entre agentes com diferentes papéis.
    """

    def __init__(self):
        self.agents = ["Extractor", "Critic", "Validator", "Curator", "Arbiter"]

    def debate(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cada agente dá a sua opinião. No final, o árbitro decide.
        Retorna um dicionário com a ação final e os votos.
        """
        text = " ".join(str(proposal.get(k, "")) for k in ["principle", "context", "decision", "justification"]).lower()
        votes: List[Tuple[str, str]] = []  # (agent, vote)

        # Agente 1: Extractor (vê se a estrutura está completa)
        if all(k in proposal for k in ["principle", "context", "decision", "justification"]):
            votes.append(("Extractor", "accept"))
        else:
            votes.append(("Extractor", "revise"))

        # Agente 2: Critic (procura linguagem de dano ou conflito)
        if any(word in text for word in ["harm", "abuse", "violate", "unethical"]):
            votes.append(("Critic", "reject"))
        else:
            votes.append(("Critic", "accept"))

        # Agente 3: Validator (verifica confiança e consistência)
        if proposal.get("confidence", 0) >= 0.7:
            votes.append(("Validator", "accept"))
        else:
            votes.append(("Validator", "revise"))

        # Agente 4: Curator (avalia se é útil e não redundante)
        if len(text.split()) > 20:
            votes.append(("Curator", "accept"))
        else:
            votes.append(("Curator", "warn"))

        # Agente 5: Arbiter (voto de desempate baseado em regras)
        accept_count = sum(1 for _, v in votes if v == "accept")
        reject_count = sum(1 for _, v in votes if v == "reject")
        revise_count = sum(1 for _, v in votes if v == "revise")
        
        if accept_count >= 3:
            arbiter_vote = "accept"
        elif reject_count >= 2:
            arbiter_vote = "reject"
        elif revise_count >= 2:
            arbiter_vote = "revise"
        else:
            arbiter_vote = "warn"
        
        votes.append(("Arbiter", arbiter_vote))

        # Decisão final: maioria simples
        final_votes = [v for _, v in votes]
        if final_votes.count("accept") > final_votes.count("reject") and final_votes.count("accept") > final_votes.count("revise"):
            action = "accept"
        elif final_votes.count("reject") > 2:
            action = "reject"
        elif final_votes.count("revise") >= 2:
            action = "revise"
        else:
            action = "warn"

        return {
            "action": action,
            "votes": votes,
            "rationale": f"Final decision after {len(self.agents)} agents: {action}."
        }
