# Phase 4 Integration

This phase adds a governance layer on top of the existing SEM pipeline.

## What is new
- Memory graph storage in JSON.
- Policy-based acceptance, warning, revision, and rejection.
- Multi-agent debate for memory proposals.
- Consolidation summaries for recurring principles.
- Context influence routing before final reasoning.
- Optional Gemini-based refinement when `GEMINI_API_KEY` is set.

## How it works
1. A memory proposal enters `GovernanceCore`.
2. Debate and policy decide whether it is accepted.
3. Accepted memories are stored in `memory_graph.json`.
4. Retrieval returns relevant graph nodes.
5. `InfluenceRouter` turns them into a readable context.
6. Consolidation compresses recurring principles.
7. If `GEMINI_API_KEY` exists, Gemini can refine the final governance decision.

## Run
```bash
python phase4_demo_v2.py
```

## Environment
- `GEMINI_API_KEY` is optional, but required for LLM refinement.
- The rest of the system works locally with JSON files.
