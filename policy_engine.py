from dataclasses import dataclass
from typing import Dict, Any

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
        if any(anchor in text for anchor in ["harm", "privacy", "consent", "transparency", "autonomy"]):
            return PolicyDecision("accept", "Matches anchor principles.", float(memory.get("confidence", 0.5)))
        if len(text) < 40:
            return PolicyDecision("warn", "Too little evidence.", float(memory.get("confidence", 0.4)))
        return PolicyDecision("accept", "Policy compatible.", float(memory.get("confidence", 0.5)))
