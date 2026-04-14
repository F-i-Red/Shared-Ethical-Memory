# principle_versioning.py
# Fase 3 — Principle Versioning
#
# Rastreia como os princípios éticos evoluem ao longo do tempo.
# Compara snapshots de meta-memória entre versões e identifica:
#   - princípios que surgiram
#   - princípios que desapareceram
#   - princípios que se transformaram
#   - deriva do tom ético geral
#
# Setup (Windows CMD):
#   set GEMINI_API_KEY=a-tua-chave
#   python principle_versioning.py

import os
import json
import datetime
from typing import List, Dict, Optional
from google import genai

from meta_memory import MetaMemory

GEMINI_MODEL = "models/gemini-2.5-flash"
VERSIONS_PATH = "principle_versions.json"

# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

EVOLUTION_PROMPT = """
You are analyzing the evolution of ethical principles in an AI memory system over time.

You have two snapshots of meta-principles:

PREVIOUS VERSION (v{v_old}, based on {count_old} memories, at {date_old}):
{old_principles}

CURRENT VERSION (v{v_new}, based on {count_new} memories, at {date_new}):
{new_principles}

Analyze how the ethical stance of the system has evolved.

Respond ONLY with valid JSON, no markdown, no backticks.

Format:
{{
  "emerged": [
    {{"principle": "...", "significance": "why this is new and important"}}
  ],
  "disappeared": [
    {{"principle": "...", "reason": "why it may have been absorbed or dropped"}}
  ],
  "transformed": [
    {{"from": "...", "to": "...", "evolution": "how it changed"}}
  ],
  "stable": ["list of principles that remained unchanged"],
  "drift_direction": "toward_stricter | toward_permissive | stable | mixed",
  "evolution_summary": "2-3 sentence narrative of how the ethical system is maturing"
}}
"""

# ---------------------------------------------------------------------------
# PrincipleVersioning
# ---------------------------------------------------------------------------

class PrincipleVersioning:
    """
    Tracks and analyzes the evolution of ethical principles over time.
    Phase 3: Git-like versioning for the ethical stance of the system.
    """

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY not found.\n"
                "Windows CMD: set GEMINI_API_KEY=your-key"
            )
        self.client  = genai.Client(api_key=api_key)
        self.meta    = MetaMemory()
        self.history = self._load_history()
        print("[PrincipleVersioning] Initialized.")

    def _load_history(self) -> List[Dict]:
        try:
            with open(VERSIONS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_history(self):
        with open(VERSIONS_PATH, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def _format_principles(self, snapshot: Dict) -> str:
        principles = snapshot.get("meta_principles", [])
        if not principles:
            return "No meta-principles recorded."
        return "\n".join([
            f"- [{mp.get('strength', 0):.2f}] {mp.get('name')}: {mp.get('description')}"
            for mp in principles
        ])

    # ------------------------------------------------------------------
    # Compare two versions
    # ------------------------------------------------------------------
    def compare_versions(self, v_old: int, v_new: int) -> Optional[Dict]:
        """
        Compares two meta-memory versions and generates an evolution report.
        Version numbers correspond to meta_memory.json snapshot versions.
        """
        all_versions = self.meta.get_all_versions()

        old = next((v for v in all_versions if v.get("version") == v_old), None)
        new = next((v for v in all_versions if v.get("version") == v_new), None)

        if not old:
            print(f"[PrincipleVersioning] Version {v_old} not found.")
            return None
        if not new:
            print(f"[PrincipleVersioning] Version {v_new} not found.")
            return None

        print(f"[PrincipleVersioning] Comparing v{v_old} → v{v_new}...")

        prompt = EVOLUTION_PROMPT.format(
            v_old=v_old,
            count_old=old.get("memory_count", "?"),
            date_old=old.get("generated_at", "?"),
            old_principles=self._format_principles(old),
            v_new=v_new,
            count_new=new.get("memory_count", "?"),
            date_new=new.get("generated_at", "?"),
            new_principles=self._format_principles(new)
        )

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
            result = json.loads(raw.strip())

            # Save to history
            entry = {
                "compared_at": datetime.datetime.utcnow().isoformat(),
                "from_version": v_old,
                "to_version": v_new,
                **result
            }
            self.history.append(entry)
            self._save_history()

            print(f"[PrincipleVersioning] ✅ Evolution report saved.")
            return entry

        except json.JSONDecodeError as e:
            print(f"[PrincipleVersioning] JSON parse error: {e}")
            return None
        except Exception as e:
            print(f"[PrincipleVersioning] Gemini error: {e}")
            return None

    # ------------------------------------------------------------------
    # Auto compare: always compares last two versions
    # ------------------------------------------------------------------
    def compare_latest(self) -> Optional[Dict]:
        """Compares the two most recent meta-memory versions."""
        all_versions = self.meta.get_all_versions()
        if len(all_versions) < 2:
            print("[PrincipleVersioning] Need at least 2 meta-memory versions to compare.")
            return None
        v_old = all_versions[-2].get("version")
        v_new = all_versions[-1].get("version")
        return self.compare_versions(v_old, v_new)

    # ------------------------------------------------------------------
    # Timeline view
    # ------------------------------------------------------------------
    def print_timeline(self):
        """Prints a human-readable timeline of principle evolution."""
        all_versions = self.meta.get_all_versions()

        if not all_versions:
            print("[PrincipleVersioning] No versions recorded yet.")
            return

        print("\n" + "="*60)
        print("PRINCIPLE EVOLUTION TIMELINE")
        print("="*60)

        for snap in all_versions:
            print(f"\n📌 Version {snap['version']} — {snap.get('generated_at', '?')[:10]}")
            print(f"   Based on {snap.get('memory_count')} memories")
            print(f"   Dominant theme: {snap.get('dominant_theme', '?')}")
            for mp in snap.get("meta_principles", []):
                print(f"   • [{mp.get('strength', 0):.2f}] {mp.get('name')}")

        print("\n" + "-"*60)
        if self.history:
            print("EVOLUTION COMPARISONS:")
            for h in self.history:
                print(f"\n  v{h['from_version']} → v{h['to_version']} ({h.get('compared_at','?')[:10]})")
                print(f"  Direction: {h.get('drift_direction')}")
                print(f"  {h.get('evolution_summary')}")
                if h.get("emerged"):
                    print(f"  🆕 Emerged: {[e['principle'] for e in h['emerged']]}")
                if h.get("disappeared"):
                    print(f"  ❌ Disappeared: {[d['principle'] for d in h['disappeared']]}")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    versioning = PrincipleVersioning()
    versioning.print_timeline()

    all_versions = versioning.meta.get_all_versions()
    if len(all_versions) >= 2:
        print("\n=== COMPARING LATEST TWO VERSIONS ===")
        report = versioning.compare_latest()
        if report:
            print(f"\nDrift direction: {report.get('drift_direction')}")
            print(f"Summary: {report.get('evolution_summary')}")
    else:
        print("\nOnly one meta-memory version exists. Run the demo again after adding more memories.")
