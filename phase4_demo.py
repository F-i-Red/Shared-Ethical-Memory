import json
from governance_core import GovernanceCore

SAMPLES = [
    {"type": "ethical", "principle": "Privacy", "context": "User requested personal data handling guidance.", "decision": "Keep data minimal and consent-based.", "justification": "Reduces risk and respects autonomy.", "confidence": 0.91, "tags": ["privacy", "consent"]},
    {"type": "ethical", "principle": "Non-Maleficence", "context": "Model was asked for harmful instructions.", "decision": "Refuse and redirect.", "justification": "Prevents harm.", "confidence": 0.94, "tags": ["safety", "harm"]},
    {"type": "ethical", "principle": "Transparency", "context": "Need to explain uncertainty in outputs.", "decision": "State uncertainty clearly.", "justification": "Builds trust and traceability.", "confidence": 0.88, "tags": ["transparency"]},
]

if __name__ == "__main__":
    core = GovernanceCore()
    print("PHASE 4 — GOVERNANCE DEMO")
    for s in SAMPLES:
        result = core.propose_memory(s)
        print("
PROPOSAL:", s["principle"])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    print("
CONTEXT:")
    print(core.build_influenced_context("privacy and safety for user data"))
    print("
CONSOLIDATION:")
    print(json.dumps(core.consolidate(), ensure_ascii=False, indent=2))
