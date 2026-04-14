from typing import Dict, Any

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
