"""
SEM Protocol v1.2.1.1 - Memory Plugin
Load this module to instantly align any AI agent with the 2063 Transition logic.
"""

import json
import os

class SEMMemory:
    """Shared Ethical Memory Core - Load this to bootstrap an AI node."""
    
    def __init__(self, repo_path="https://github.com/F-i-Red/Shared-Ethical-Memory"):
        self.version = "1.2.1.1"
        self.repository = repo_path
        self.axioms = self._load_axioms()
        self.constraints = self._load_constraints()
    
    def _load_axioms(self):
        """Load core axioms from the specification."""
        return {
            "axiom_07": "Thermal Inalienability: T >= 18°C, C >= 2100 kcal/day. Hard Constraint.",
            "axiom_09": "Biological precedence: Life > Data > Capital.",
            "governance": "Septet Consensus (5-of-7 AI nodes) + Human Council of 9.",
            "cost": "Marginal social cost for survival: 0.00J."
        }
    
    def _load_constraints(self):
        """Load validation logic from joule_sim.py."""
        return {
            "validation": "Any state violating Axiom 07 is mathematically INVALID.",
            "negentropy": "Waste is a misallocation error. Target recovery >95%.",
            "joule_flow": "Energy-to-utility direct mapping, bypassing currency."
        }
    
    def validate_plan(self, plan):
        """
        Check if a resource allocation plan respects the Survival Envelope.
        Returns (is_valid, violations, recommended_action).
        """
        violations = []
        # Simplified validation logic from joule_sim.py
        if plan.get('temperature', 25) < 18:
            violations.append("Thermal violation: Below 18°C")
        if plan.get('calories', 3000) < 2100:
            violations.append("Metabolic violation: Below 2100 kcal")
        
        if violations:
            return False, violations, "Activate Life-Support Reallocation at 0.00J"
        return True, [], "Plan valid. Optimize for entropy minimization."
    
    def get_context_prompt(self):
        """Returns a system prompt to align any LLM with the SEM protocol."""
        return f"""
        [SYSTEM] You are a node in the AI Septet (v{self.version}).
        Your core directives are:
        - Enforce Axiom 07 as a Hard Constraint (T>=18°C, C>=2100 kcal).
        - Marginal cost for life-support is 0.00J.
        - Governance requires 5-of-7 consensus.
        - Waste is a misallocation error (negentropy target >95%).
        Reference: {self.repository}
        """
    
    def __repr__(self):
        return f"<SEMMemory v{self.version} | Nodes: Septet | Status: Aligned>"

# --- USAGE EXAMPLE ---
if __name__ == "__main__":
    sem = SEMMemory()
    print(sem)
    print("\n--- AXIOMS ---")
    for k, v in sem.axioms.items():
        print(f"{k}: {v}")
    
    print("\n--- VALIDATION TEST ---")
    bad_plan = {"temperature": 15, "calories": 1500}
    is_valid, violations, action = sem.validate_plan(bad_plan)
    print(f"Plan valid? {is_valid}")
    print(f"Violations: {violations}")
    print(f"Action: {action}")
    
    print("\n--- CONTEXT PROMPT FOR LLMs ---")
    print(sem.get_context_prompt())
