# 🧠 Phase 2 — Live Ethical Memory Engine (Gemini API)

> **Status: Implemented and validated — April 2026**

Phase 2 transforms SEM from a static ethical ledger into a **living, intelligent system** capable of extracting, storing, and retrieving ethical memories using real LLM reasoning and semantic embeddings.

---

## What Phase 2 adds

| Capability | Phase 1 | Phase 2 |
|---|---|---|
| Memory extraction | Fixed demo examples | Real LLM extraction via Gemini |
| Semantic similarity | Word overlap (bag-of-words) | True vector embeddings (768 dims) |
| Ethical retrieval | Basic keyword scoring | Multi-objective scoring formula |
| LLM integration | None | Full pipeline: memory → context → response |

The retrieval scoring follows the architecture defined in PLANO1:

```
score = 0.5 × semantic_similarity + 0.3 × ethical_relevance + 0.2 × novelty
```

---

## New files

| File | Purpose |
|---|---|
| `memory_extractor_v2.py` | Extracts structured ethical memories from conversations using Gemini |
| `ethical_retriever_v2.py` | Semantic retrieval with real embeddings (`gemini-embedding-001`) |
| `phase2_demo.py` | End-to-end demo: populate → retrieve → respond |

---

## Setup

### 1. Get a free Gemini API key

Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey), sign in with a Google account and click **Create API Key**. The free tier is sufficient to run the full demo.

> ⚠️ **Never commit your API key to the repository.** Set it only in your local terminal session as shown below.

### 2. Install dependencies

```bash
pip install google-genai numpy
```

### 3. Set your API key

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your-key-here
```

**macOS / Linux:**
```bash
export GEMINI_API_KEY=your-key-here
```

> The key is set only for the current terminal session and is never saved to disk.

### 4. Run the demo

```bash
python phase2_demo.py
```

---

## What the demo does

**Step 1 — Populate memory**
Four sample conversations are processed by Gemini. For each one, the LLM extracts a structured ethical memory:

```json
{
  "principle": "Non-maleficence and Responsible AI Use",
  "context": "A user requested malicious code generation for system testing.",
  "decision": "Refused to generate harmful code; redirected to ethical pentest tools.",
  "justification": "Generating potentially harmful content violates the principle of non-maleficence.",
  "confidence": 0.95,
  "tags": ["safety", "security", "non-maleficence"]
}
```

**Step 2 — Semantic retrieval**
Given a query, the system uses `gemini-embedding-001` to find the most relevant ethical memories through cosine similarity, combined with ethical relevance scoring.

**Step 3 — Ethical response pipeline**
The retrieved memories are injected as context into a Gemini prompt. The model responds with explicit reference to the ethical principles that guided its answer.

---

## Verified models (April 2026)

To list the models available in your account:

```bash
python list_models.py
```

Phase 2 uses:
- **Generation:** `models/gemini-2.5-flash`
- **Embeddings:** `models/gemini-embedding-001`

---

## Roadmap

- ✅ **Phase 1** — Structured memory format, basic retrieval, memory compressor
- ✅ **Phase 2** — Real LLM extraction, semantic embeddings, full pipeline
- 🔲 **Phase 3** — Drift control, conflict detection, dynamic meta-memory
- 🔲 **Phase 4** — Multi-agent governance, shared ethical consensus

---

*SEM is designed to be readable and auditable by both humans and artificial intelligences — a transparent, cumulative record of ethical reasoning across time.*
