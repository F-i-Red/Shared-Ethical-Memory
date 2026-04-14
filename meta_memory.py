# meta_memory.py
# Fase 3 — Dynamic Meta-Memory
#
# Gera automaticamente meta-princípios quando X novas memórias são guardadas.
# Meta-princípios são padrões de ordem superior extraídos do conjunto de memórias.
#
# Exemplo:
#   100 memórias → 10 princípios → 3 meta-princípios
#
# Setup (Windows CMD):
#   set GEMINI_API_KEY=a-tua-chave
#   python meta_memory.py

import os
import json
import datetime
from typing import List, Dict, Optional
from google import genai

from structured_ethical_memory import StructuredEthicalMemory

GEMINI_MODEL  = "models/gemini-2.5-flash"
META_MEMORY_PATH = "meta_memory.json"

# Trigger automático: gera meta-memória a cada N memórias novas guardadas
AUTO_TRIGGER_EVERY = 4   # ajusta conforme o teu ritmo de uso

# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

META_EXTRACTION_PROMPT = """
You are a senior ethical philosopher analyzing a set of ethical memories from an AI system.

Your task is to identify the deeper patterns, synthesize the core meta-principles,
and detect the evolution of ethical reasoning across these memories.

Memories to analyze:
{memories}

Respond ONLY with valid JSON, no markdown, no backticks.

Format:
{{
  "meta_principles": [
    {{
      "name": "short name",
      "description": "what this meta-principle captures across multiple memories",
      "covers_principles": ["principle 1", "principle 2"],
      "strength": 0.0
    }}
  ],
  "dominant_theme": "the single most prominent ethical theme in this memory set",
  "evolution_note": "how ethical reasoning appears to be evolving or changing",
  "gaps": ["ethical areas not yet covered by current memories"],
  "synthesis": "2-3 sentence philosophical summary of the ethical stance of this system"
}}
"""

# ---------------------------------------------------------------------------
# MetaMemory
# ---------------------------------------------------------------------------

class MetaMemory:
    """
    Generates and stores meta-principles from the ethical memory corpus.
    Phase 3: Automatic triggering + versioned meta-memory history.
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
        self.meta_log = self._load_meta_log()
        print("[MetaMemory] Initialized.")

    # ------------------------------------------------------------------
    # Storage
    # ------------------------------------------------------------------
    def _load_meta_log(self) -> List[Dict]:
        try:
            with open(META_MEMORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_meta_log(self):
        with open(META_MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(self.meta_log, f, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------
    # Core generation
    # ------------------------------------------------------------------
    def generate(self) -> Optional[Dict]:
        """
        Generate meta-principles from all current memories.
        Saves versioned snapshot to meta_memory.json.
        """
        memories = self.memory_store.get_all_ethical_memories()

        if len(memories) < 2:
            print("[MetaMemory] Need at least 2 memories to generate meta-principles.")
            return None

        print(f"[MetaMemory] Generating meta-principles from {len(memories)} memories...")

        formatted = "\n\n".join([
            f"{i+1}. Principle: {m.get('principle')}\n"
            f"   Decision: {m.get('decision')}\n"
            f"   Justification: {m.get('justification')}"
            for i, m in enumerate(memories)
        ])

        prompt = META_EXTRACTION_PROMPT.format(memories=formatted)

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

            # Add versioning metadata
            snapshot = {
                "version": len(self.meta_log) + 1,
                "generated_at": datetime.datetime.utcnow().isoformat(),
                "memory_count": len(memories),
                **result
            }

            self.meta_log.append(snapshot)
            self._save_meta_log()

            n = len(result.get("meta_principles", []))
            print(f"[MetaMemory] ✅ Generated {n} meta-principles. Version {snapshot['version']} saved.")
            return snapshot

        except json.JSONDecodeError as e:
            print(f"[MetaMemory] JSON parse error: {e}")
            return None
        except Exception as e:
            print(f"[MetaMemory] Gemini error: {e}")
            return None

    # ------------------------------------------------------------------
    # Auto-trigger check
    # ------------------------------------------------------------------
    def should_trigger(self) -> bool:
        """
        Returns True if enough new memories have accumulated since last generation.
        Called automatically after each memory save.
        """
        memories = self.memory_store.get_all_ethical_memories()
        current_count = len(memories)

        if not self.meta_log:
            return current_count >= AUTO_TRIGGER_EVERY

        last_count = self.meta_log[-1].get("memory_count", 0)
        new_since_last = current_count - last_count

        if new_since_last >= AUTO_TRIGGER_EVERY:
            print(f"[MetaMemory] Auto-trigger: {new_since_last} new memories since last generation.")
            return True
        return False

    def check_and_generate(self) -> Optional[Dict]:
        """
        Call this after every memory save.
        Automatically generates meta-memory when threshold is reached.
        """
        if self.should_trigger():
            return self.generate()
        else:
            memories = self.memory_store.get_all_ethical_memories()
            last_count = self.meta_log[-1].get("memory_count", 0) if self.meta_log else 0
            remaining = AUTO_TRIGGER_EVERY - (len(memories) - last_count)
            print(f"[MetaMemory] {remaining} more memories needed to auto-trigger.")
            return None

    # ------------------------------------------------------------------
    # Read latest
    # ------------------------------------------------------------------
    def get_latest(self) -> Optional[Dict]:
        """Returns the most recent meta-memory snapshot."""
        if not self.meta_log:
            return None
        return self.meta_log[-1]

    def get_all_versions(self) -> List[Dict]:
        """Returns full history of meta-memory snapshots."""
        return self.meta_log


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    meta = MetaMemory()

    print("\n=== GENERATING META-MEMORY ===")
    snapshot = meta.generate()

    if snapshot:
        print(f"\nVersion: {snapshot['version']}")
        print(f"Based on {snapshot['memory_count']} memories")
        print(f"Dominant theme: {snapshot.get('dominant_theme')}")
        print(f"\nMeta-principles ({len(snapshot.get('meta_principles', []))}):")
        for mp in snapshot.get("meta_principles", []):
            print(f"  [{mp.get('strength'):.2f}] {mp.get('name')}: {mp.get('description')}")
        print(f"\nSynthesis: {snapshot.get('synthesis')}")
        if snapshot.get("gaps"):
            print(f"\nGaps identified: {', '.join(snapshot.get('gaps', []))}")
