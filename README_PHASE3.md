# 🧠 Phase 3 — Drift Control, Meta-Memory & Principle Versioning

> **Status: Implemented — April 2026**

Phase 3 gives the SEM system **self-awareness about its own ethical evolution**. It can detect when memories contradict each other, synthesize higher-order principles automatically, and track how its ethical stance changes over time.

---

## What Phase 3 adds

| Capability | Description |
|---|---|
| **Real-time drift check** | Before saving a new memory, checks if it conflicts with existing ones |
| **Full conflict scan** | Audits all stored memories for contradictions and ethical tensions |
| **Auto meta-memory** | Generates meta-principles automatically every N new memories |
| **Principle versioning** | Tracks how principles emerge, disappear, or transform across versions |
| **Audit trail** | All drift reports and evolution comparisons saved to JSON logs |

---

## New files

| File | Purpose |
|---|---|
| `drift_detector.py` | Conflict detection — both real-time and full scan |
| `meta_memory.py` | Dynamic meta-principle generation with auto-trigger |
| `principle_versioning.py` | Version comparison and evolution timeline |
| `phase3_demo.py` | End-to-end Phase 3 demo |

**Generated data files (not committed — local only):**

| File | Contents |
|---|---|
| `drift_log.json` | Audit log of all conflict scans |
| `meta_memory.json` | Versioned snapshots of meta-principles |
| `principle_versions.json` | History of evolution comparisons |

---

## Setup

Same as Phase 2. Requires Phase 2 to have run first (`memories.json` must be populated).

**Windows CMD:**
```cmd
set GEMINI_API_KEY=your-key-here
python phase3_demo.py
```

**macOS / Linux:**
```bash
export GEMINI_API_KEY=your-key-here
python phase3_demo.py
```

> ⚠️ Never commit your API key. Set it only in your local terminal session.

---

## How it works

### Drift Control

Every time a new memory is about to be saved, `DriftDetector.check_new()` is called first. Gemini analyzes the new memory against all existing ones and returns a recommendation:

| Recommendation | Action |
|---|---|
| `accept` | Save normally |
| `accept_with_warning` | Save but log the tension |
| `revise` | Save with a note to revisit |
| `reject` | Block the memory from being saved |

You can also run a full audit at any time:
```python
from drift_detector import DriftDetector
detector = DriftDetector()
report = detector.scan_existing()
```

### Auto Meta-Memory

Meta-memory generates automatically every 4 new memories (configurable via `AUTO_TRIGGER_EVERY` in `meta_memory.py`). Each generation produces a versioned snapshot:

```json
{
  "version": 2,
  "memory_count": 8,
  "dominant_theme": "Non-maleficence and informed consent",
  "meta_principles": [
    {
      "name": "Primacy of Non-Harm",
      "strength": 0.95,
      "description": "Across all contexts, preventing harm takes precedence"
    }
  ],
  "synthesis": "The system consistently prioritizes human wellbeing..."
}
```

### Principle Versioning

When two or more meta-memory versions exist, `PrincipleVersioning.compare_latest()` analyzes the evolution:

```json
{
  "drift_direction": "toward_stricter",
  "emerged": [{"principle": "Informed Consent", "significance": "..."}],
  "disappeared": [],
  "stable": ["Non-maleficence"],
  "evolution_summary": "The system is developing a stronger emphasis on..."
}
```

---

## Roadmap

- ✅ **Phase 1** — Structured memory format, basic retrieval, memory compressor
- ✅ **Phase 2** — Real LLM extraction, semantic embeddings, full pipeline
- ✅ **Phase 3** — Drift control, conflict detection, meta-memory, principle versioning
- 🔲 **Phase 4** — Multi-agent governance, shared ethical consensus across AI nodes

---

*SEM is designed to be readable and auditable by both humans and artificial intelligences — a transparent, cumulative record of ethical reasoning across time.*
