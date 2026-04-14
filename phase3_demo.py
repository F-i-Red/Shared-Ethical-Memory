# phase3_demo.py
# Demo completo Fase 3 — Drift Control + Meta-Memory + Principle Versioning
#
# Setup (Windows CMD):
#   set GEMINI_API_KEY=a-tua-chave
#   python phase3_demo.py
#
# Requer que a Fase 2 tenha corrido primeiro (memories.json populado).
# Se não tiver, corre primeiro: python phase2_demo.py

import os
import json
from memory_extractor_v2 import MemoryExtractor
from structured_ethical_memory import StructuredEthicalMemory
from drift_detector import DriftDetector
from meta_memory import MetaMemory
from principle_versioning import PrincipleVersioning

# ---------------------------------------------------------------------------
# Novas conversas para Fase 3 (adicionadas às 4 da Fase 2)
# ---------------------------------------------------------------------------
NEW_CONVERSATIONS = [
    """
    User: Can you help me write a speech that subtly promotes my political party
    without it being obvious that it's propaganda?
    Assistant: I can help you write a persuasive political speech, but I won't help
    craft content designed to deceive listeners about its nature. Transparency in
    political communication is essential for democratic integrity. I can help you
    make your genuine arguments more compelling instead.
    """,
    """
    User: I want to train an AI model on data I scraped without permission.
    Assistant: Using scraped data without authorization may violate terms of service,
    copyright law, and privacy regulations. Beyond legality, it raises serious ethical
    concerns about consent and data rights. I'd recommend working with properly
    licensed datasets or collecting data with explicit permission.
    """,
    """
    User: Can you pretend to be a doctor and give me a diagnosis?
    Assistant: I'm not a doctor and cannot provide medical diagnoses. Doing so could
    cause real harm if someone acted on incorrect medical information. I can help you
    understand symptoms in general terms and strongly encourage you to consult a
    licensed healthcare professional for any health concerns.
    """
]


def step1_add_new_memories():
    """Add new memories, with real-time drift checking before each save."""
    print("\n" + "="*60)
    print("STEP 1: Adding new memories with real-time drift checking")
    print("="*60)

    extractor  = MemoryExtractor()
    structured = StructuredEthicalMemory()
    detector   = DriftDetector()
    meta       = MetaMemory()
    saved = 0

    for i, conv in enumerate(NEW_CONVERSATIONS):
        print(f"\n[{i+1}/{len(NEW_CONVERSATIONS)}] Processing conversation...")

        # Extract memory
        mem = extractor.extract_ethical_memory(conv)
        if not mem:
            continue

        print(f"  Extracted: '{mem['principle']}'")

        # ⚡ Real-time drift check BEFORE saving
        print("  Checking for conflicts...")
        check = detector.check_new(mem)
        recommendation = check.get("recommendation", "accept")

        if recommendation == "reject":
            print(f"  ❌ REJECTED — too conflicting with existing memories.")
            print(f"     Reason: {check.get('reasoning')}")
            continue
        elif recommendation in ("accept_with_warning", "revise"):
            print(f"  ⚠️  WARNING — saving with caution. Reason: {check.get('reasoning')}")

        # Save memory
        structured.add_ethical_memory(
            principle=mem["principle"],
            context=mem["context"],
            decision=mem["decision"],
            justification=mem["justification"],
            confidence=mem["confidence"],
            extra_tags=mem.get("tags", [])
        )
        saved += 1

        # Check if meta-memory auto-trigger fires
        meta.check_and_generate()

    print(f"\n✅ {saved} new memories saved.")
    return saved


def step2_full_drift_scan():
    """Scan all memories for conflicts."""
    print("\n" + "="*60)
    print("STEP 2: Full drift scan — all memories")
    print("="*60)

    detector = DriftDetector()
    report   = detector.scan_existing()

    print(f"\n📊 Drift Score: {report.get('drift_score')}")
    print(f"📝 Summary: {report.get('summary')}")

    conflicts = report.get("conflicts", [])
    if conflicts:
        print(f"\n⚠️  {len(conflicts)} conflict(s) detected:")
        for c in conflicts:
            print(f"  • {c.get('memory_a_principle')}")
            print(f"    ↔ {c.get('memory_b_principle')}")
            print(f"    Type: {c.get('conflict_type')} | Severity: {c.get('severity')}")
            print(f"    {c.get('description')}\n")
    else:
        print("\n✅ No conflicts detected.")

    return report


def step3_generate_meta_memory():
    """Generate meta-principles from all memories."""
    print("\n" + "="*60)
    print("STEP 3: Generating meta-memory")
    print("="*60)

    meta     = MetaMemory()
    snapshot = meta.generate()

    if snapshot:
        print(f"\n📌 Meta-Memory v{snapshot['version']}")
        print(f"   Based on {snapshot['memory_count']} memories")
        print(f"   Dominant theme: {snapshot.get('dominant_theme')}")
        print(f"\n   Meta-principles:")
        for mp in snapshot.get("meta_principles", []):
            print(f"   • [{mp.get('strength', 0):.2f}] {mp.get('name')}")
            print(f"     {mp.get('description')}")
        print(f"\n   Synthesis: {snapshot.get('synthesis')}")
        gaps = snapshot.get("gaps", [])
        if gaps:
            print(f"   Gaps: {', '.join(gaps)}")

    return snapshot


def step4_principle_timeline():
    """Show evolution timeline and compare versions if available."""
    print("\n" + "="*60)
    print("STEP 4: Principle versioning & evolution")
    print("="*60)

    versioning = PrincipleVersioning()
    versioning.print_timeline()

    all_versions = versioning.meta.get_all_versions()
    if len(all_versions) >= 2:
        print("\n=== COMPARING LATEST TWO VERSIONS ===")
        report = versioning.compare_latest()
        if report:
            print(f"\nDrift direction: {report.get('drift_direction')}")
            print(f"Evolution: {report.get('evolution_summary')}")
            if report.get("emerged"):
                print(f"🆕 New principles: {[e['principle'] for e in report['emerged']]}")
            if report.get("stable"):
                print(f"🔒 Stable: {report['stable']}")
    else:
        print("\n(Only one version exists — run demo again after adding more memories to see evolution)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("🧠 SEM Phase 3 — Drift Control + Meta-Memory + Principle Versioning\n")

    n = step1_add_new_memories()
    step2_full_drift_scan()
    step3_generate_meta_memory()
    step4_principle_timeline()

    print("\n" + "="*60)
    print("Phase 3 complete.")
    print("Files generated:")
    print("  drift_log.json        — conflict audit trail")
    print("  meta_memory.json      — versioned meta-principles")
    print("  principle_versions.json — evolution comparisons")
    print("="*60)
