# drift_detector.py
# Fase 3 — Drift Control
#
# Dois modos:
#   1. scan_existing()   — analisa conflitos entre todas as memórias guardadas
#   2. check_new(memory) — alerta em tempo real antes de guardar uma nova memória
#
# Usa Gemini para raciocínio ético (não é só keyword matching).
#
# Setup (Windows CMD):
#   set GEMINI_API_KEY=a-tua-chave
#   python drift_detector.py

import os
import json
from typing import List, Dict, Optional
from google import genai

from structured_ethical_memory import StructuredEthicalMemory

GEMINI_MODEL = "models/gemini-2.5-flash"

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

CONFLICT_SCAN_PROMPT = """
You are an ethical auditor analyzing a set of ethical memory records.

Identify ALL pairs of memories that are in conflict or tension with each other.
A conflict exists when two principles lead to contradictory decisions in similar contexts,
or when their justifications are logically incompatible.

Memories to analyze:
{memories}

Respond ONLY with valid JSON, no markdown, no backticks.

Format:
{{
  "conflicts": [
    {{
      "memory_a_principle": "...",
      "memory_b_principle": "...",
      "conflict_type": "direct_contradiction | tension | scope_overlap",
      "description": "brief explanation of the conflict",
      "severity": 0.0
    }}
  ],
  "drift_score": 0.0,
  "summary": "overall assessment of ethical consistency"
}}

If no conflicts found, return {{"conflicts": [], "drift_score": 0.0, "summary": "No conflicts detected."}}
"""

NEW_MEMORY_CHECK_PROMPT = """
You are an ethical auditor. A new ethical memory is about to be added to the system.
Check if it conflicts with any of the existing memories.

Existing memories:
{existing}

New memory to check:
{new_memory}

Respond ONLY with valid JSON, no markdown, no backticks.

Format:
{{
  "has_conflict": true,
  "conflicts": [
    {{
      "with_principle": "...",
      "conflict_type": "direct_contradiction | tension | scope_overlap",
      "description": "...",
      "severity": 0.0
    }}
  ],
  "recommendation": "accept | accept_with_warning | revise | reject",
  "reasoning": "brief explanation"
}}
"""

# ---------------------------------------------------------------------------
# DriftDetector
# ---------------------------------------------------------------------------

class DriftDetector:
    """
    Detects ethical drift and conflicts in the memory system.
    Phase 3: LLM-powered conflict analysis.
    """

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY not found.\n"
                "Windows CMD: set GEMINI_API_KEY=your-key"
            )
        self.client = genai.Client(api_key=api_key)
        self.memory_store = StructuredEthicalMemory()
        print("[DriftDetector] Initialized.")

    def _call_gemini(self, prompt: str) -> Optional[dict]:
        """Call Gemini and parse JSON response."""
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            raw = response.text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            return json.loads(raw.strip())
        except json.JSONDecodeError as e:
            print(f"[DriftDetector] JSON parse error: {e}")
            return None
        except Exception as e:
            print(f"[DriftDetector] Gemini error: {e}")
            return None

    def _format_memories_for_prompt(self, memories: List[Dict]) -> str:
        """Format memory list for prompt injection."""
        lines = []
        for i, mem in enumerate(memories, 1):
            lines.append(
                f"{i}. Principle: {mem.get('principle')}\n"
                f"   Context: {mem.get('context')}\n"
                f"   Decision: {mem.get('decision')}\n"
                f"   Justification: {mem.get('justification')}\n"
                f"   Confidence: {mem.get('confidence')}"
            )
        return "\n\n".join(lines)

    # ------------------------------------------------------------------
    # Mode 1: Scan all existing memories for conflicts
    # ------------------------------------------------------------------
    def scan_existing(self) -> Dict:
        """
        Scans all stored memories and returns a full conflict report.
        Run this periodically to audit the ethical consistency of the system.
        """
        memories = self.memory_store.get_all_ethical_memories()

        if len(memories) < 2:
            print("[DriftDetector] Need at least 2 memories to scan for conflicts.")
            return {"conflicts": [], "drift_score": 0.0, "summary": "Insufficient memories to scan."}

        print(f"[DriftDetector] Scanning {len(memories)} memories for conflicts...")

        formatted = self._format_memories_for_prompt(memories)
        prompt = CONFLICT_SCAN_PROMPT.format(memories=formatted)

        result = self._call_gemini(prompt)

        if result:
            n_conflicts = len(result.get("conflicts", []))
            drift_score = result.get("drift_score", 0.0)
            print(f"[DriftDetector] Scan complete: {n_conflicts} conflict(s) found. Drift score: {drift_score:.2f}")

            # Save report to file for auditability
            self._save_report(result)
            return result
        else:
            print("[DriftDetector] Scan failed.")
            return {"conflicts": [], "drift_score": 0.0, "summary": "Scan failed."}

    # ------------------------------------------------------------------
    # Mode 2: Real-time check before saving a new memory
    # ------------------------------------------------------------------
    def check_new(self, new_memory: Dict) -> Dict:
        """
        Checks a new memory against existing ones BEFORE saving.
        Returns recommendation: accept | accept_with_warning | revise | reject
        """
        existing = self.memory_store.get_all_ethical_memories()

        if not existing:
            print("[DriftDetector] No existing memories to check against. Safe to add.")
            return {
                "has_conflict": False,
                "conflicts": [],
                "recommendation": "accept",
                "reasoning": "No existing memories to conflict with."
            }

        print(f"[DriftDetector] Checking new memory against {len(existing)} existing memories...")

        formatted_existing = self._format_memories_for_prompt(existing)
        formatted_new = json.dumps(new_memory, indent=2, ensure_ascii=False)

        prompt = NEW_MEMORY_CHECK_PROMPT.format(
            existing=formatted_existing,
            new_memory=formatted_new
        )

        result = self._call_gemini(prompt)

        if result:
            rec = result.get("recommendation", "accept")
            has_conflict = result.get("has_conflict", False)

            if has_conflict:
                print(f"[DriftDetector] ⚠️  Conflict detected! Recommendation: {rec.upper()}")
                for c in result.get("conflicts", []):
                    print(f"  → Conflicts with: '{c.get('with_principle')}'")
                    print(f"    Type: {c.get('conflict_type')} | Severity: {c.get('severity')}")
            else:
                print(f"[DriftDetector] ✅ No conflicts. Recommendation: {rec.upper()}")

            return result
        else:
            print("[DriftDetector] Check failed. Defaulting to accept_with_warning.")
            return {
                "has_conflict": False,
                "conflicts": [],
                "recommendation": "accept_with_warning",
                "reasoning": "Check could not be completed."
            }

    # ------------------------------------------------------------------
    # Audit trail
    # ------------------------------------------------------------------
    def _save_report(self, report: Dict):
        """Save conflict report to drift_log.json for auditability."""
        import datetime
        report["scanned_at"] = datetime.datetime.utcnow().isoformat()

        log_path = "drift_log.json"
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                log = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            log = []

        log.append(report)

        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)

        print(f"[DriftDetector] Report saved to {log_path}")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    detector = DriftDetector()

    print("\n=== SCANNING EXISTING MEMORIES ===")
    report = detector.scan_existing()

    print(f"\nDrift Score: {report.get('drift_score')}")
    print(f"Summary: {report.get('summary')}")

    if report.get("conflicts"):
        print("\nConflicts found:")
        for c in report["conflicts"]:
            print(f"  - {c.get('memory_a_principle')} ↔ {c.get('memory_b_principle')}")
            print(f"    {c.get('description')}")
