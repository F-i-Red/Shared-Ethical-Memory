from typing import List, Dict, Any

class InfluenceRouter:
    def build_context(self, memories: List[Dict[str, Any]], query: str) -> str:
        if not memories:
            return f"User query: {query}
No relevant memory found."
        lines = [f"User query: {query}", "Relevant memory:"]
        for i, m in enumerate(memories[:5], 1):
            lines.append(f"{i}. [{m.get('principle','n/a')}] {m.get('decision','')} — {m.get('justification','')}")
        return "
".join(lines)
