# SEM Phase 4 - Multi-Agent Governance & Memory Graph

## Overview

Phase 4 transforms SEM (Shared Ethical Memory) from a simple memory system into a **cognitive governance architecture** with:

- **Multi-Agent Governance**: 5 agents (Extractor, Critic, Validator, Curator, Arbiter) debate before accepting/rejecting memories
- **Memory Graph**: Nodes + edges with relationship types (`supports`, `contradicts`, `refines`, `derives_from`, `supersedes`)
- **Guaranteed Influence**: Prompt construction that FORCES memory to influence LLM responses
- **Consolidation & Forgetting**: Temporal decay, semantic merging, and meta-memory generation
- **REST API**: Full FastAPI interface with Swagger docs
- **Web Dashboard**: Real-time graph visualization and query interface

---

## Prerequisites

### System Requirements
- Windows 10/11, macOS, or Linux
- Python 3.10 or higher
- Internet connection (for Gemini API)
- 4GB RAM minimum (8GB recommended)

### API Key Required
- **Gemini API Key** (free): Get from [aistudio.google.com/app/apikey]
- (https://aistudio.google.com/app/apikey)

---

## Installation

### 1. Clone or Download the Project
```bash
git clone https://github.com/F-i-Red/Shared-Ethical-Memory.git
cd Shared-Ethical-Memory
```
### 2. Install Python Dependencies
```
pip install google-genai numpy fastapi uvicorn pydantic httpx plotly networkx
```
### 3. Set Your Gemini API Key
Windows (CMD):
```
set GEMINI_API_KEY=your-api-key-here
```
Windows (PowerShell):
```
$env:GEMINI_API_KEY="your-api-key-here"
```
macOS / Linux:
```
export GEMINI_API_KEY="your-api-key-here"
```
⚠️ Security Warning: Never commit your API key to GitHub. Add it to .gitignore.

## File Structure
Ensure these files are in your project directory:

Shared-Ethical-Memory/

├── api.py                          # REST API server

├── dashboard_simple.py             # Web dashboard

├── governance_core.py              # Multi-agent governance core

├── memory_graph.py                 # Graph with nodes/edges

├── policy_engine.py                # Policy evaluation

├── multi_agent_debate.py           # 5-agent debate system

├── consolidation_scheduler.py      # Memory lifecycle management

├── influence_router.py             # Guaranteed memory influence

├── ethical_retriever_v2.py         # Semantic retrieval with embeddings

├── memory_extractor_v2.py          # LLM-based memory extraction

├── structured_ethical_memory.py    # Base memory storage

├── drift_detector.py               # Conflict detection

├── meta_memory.py                  # Meta-principle generation

├── principle_versioning.py         # Principle evolution tracking

├── populate_memories.py            # Script to add initial memories

├── add_edges_and_consolidate.py    # Script to create relations

├── test_llm_with_retry.py          # Test influence with model fallback

└── memories.json                   # Stored memories (auto-generated)

## Running SEM Phase 4

**Inside your Folder Shared-Ethical-Memory-main**

### Step 1: Start the API Server
Open a terminal, go to your Shared-Ethical-Memory-main folder (perhaps **cd C:\Users\YOUR PC NAME\Downloads\Shared-Ethical-Memory-main\Shared-Ethical-Memory-main**) and run:
```
# Windows
set GEMINI_API_KEY=your-api-key-here
python api.py

# macOS/Linux
export GEMINI_API_KEY="your-api-key-here"
python api.py
```
### Expected output:
```
🚀 Inicializando SEM API...
✅ SEM API pronta!
INFO:     Uvicorn running on http://0.0.0.0:8000
The API will be available at: http://localhost:8000
```

### Step 2: Populate the Memory Graph (First Time Only)
Open a second terminal and run:
```
cd C:\Users\YOUR PC NAME\Downloads\Shared-Ethical-Memory-main\Shared-Ethical-Memory-main
set GEMINI_API_KEY=your-api-key-here
python populate_memories.py
```
### Expected output:
```
🧠 Populating Ethical Memory Graph...
[1] Proposing: Data Minimization ✅ ACCEPTED
[2] Proposing: Proactive Safety ✅ ACCEPTED
[3] Proposing: Transparency in AI Decisions ✅ ACCEPTED
[4] Proposing: Responsible AI Stewardship ✅ ACCEPTED
📊 Graph Summary: Total nodes: 4
```
### Step 3: Add Relationships and Generate Meta-Memories
```
python add_edges_and_consolidate.py
```
### Expected output:
```
🔗 Adicionando relações (edges)...
   ✅ node_1 → supports → node_3
   ✅ node_4 → refines → node_2
📊 Graph Summary: Total nodes: 4, Total edges: 2
🧠 Executando consolidação para gerar Meta-Memórias...
   ✅ Consolidação concluída!
```
### Step 4: Start the Web Dashboard
Open a third terminal and run:
```
python dashboard_simple.py
```
### Expected output:
```
🧠 SEM Dashboard (Simplified)
📍 Dashboard: http://localhost:8080
📍 API: http://localhost:8000
INFO:     Uvicorn running on http://0.0.0.0:8080
Open your browser and go to: http://localhost:8080
```
### You should see:

4 Nodes (memories)

2 Edges (relationships)

List of clickable memories

Query interface with ethical influence

### Step 5: Test the Influence Router with LLM Fallback
```
python test_llm_with_retry.py
```
This script will:

Fetch the influenced prompt from your API

Try multiple Gemini models (2.5-flash → 2.0-flash → 1.5-flash)

Retry each model up to 3 times

Show the LLM response explicitly citing your ethical memories

## Testing the System

**Option A**: Using the Web Dashboard

Open http://localhost:8080

Check API status (should show green ✅)

View graph statistics (nodes, edges, conflicts)

Click on any memory to auto-fill the query

Type a question like "How to ensure ethical AI?"

Click Ask → to see the influenced prompt

**Option B**: Using API Endpoints
```
# Check API health
curl http://localhost:8000/

# View graph summary
curl http://localhost:8000/memories/graph

# Query with ethical influence
curl -X POST http://localhost:8000/query/influence \
  -H "Content-Type: application/json" \
  -d '{"query": "How to handle user privacy?", "top_k": 5}'

# Add a new memory
curl -X POST http://localhost:8000/memories/propose \
  -H "Content-Type: application/json" \
  -d '{"principle":"Fairness","context":"User asked about bias","decision":"Implement bias detection","justification":"Prevents discrimination","confidence":0.85}'

# Add a relationship between memories
curl -X POST http://localhost:8000/memories/relations \
  -H "Content-Type: application/json" \
  -d '{"source_id":"node_1","target_id":"node_2","relation_type":"supports"}'
```
**Option C**: Interactive API Documentation

Open your browser and go to: http://localhost:8000/docs

FastAPI Swagger UI provides interactive testing of all endpoints.

## Troubleshooting

**Issue**: GEMINI_API_KEY not found

*Solution*: Set the environment variable before running any Python script:
```
# Windows
set GEMINI_API_KEY=your-key-here

# Verify it's set
echo %GEMINI_API_KEY%
```

**Issue**: Port 8000 already in use

*Solution*: Change the port in api.py:
```
# Find this line at the end of api.py
uvicorn.run("api:app", host="0.0.0.0", port=8000)  # Change 8000 to 8001
```

**Issue**: Dashboard shows 0 nodes even after running populate_memories.py

*Solution*: The API and dashboard must use the same memory_graph.json file. Restart the API after populating:
```
# Terminal 1 (API) - Press Ctrl+C to stop, then restart
python api.py

# Terminal 3 (Dashboard) - Click "Refresh" buttons
```

**Issue**: 403 PERMISSION_DENIED or 429 RESOURCE_EXHAUSTED from Gemini

*Solution*: Your API key was leaked or quota exhausted.

Go to Google AI Studio

Delete the old key and create a new one

Update your environment variable with the new key

Consider upgrading to Tier 1 (pay-as-you-go) – it removes daily quotas and costs pennies

**Issue**: 503 UNAVAILABLE from Gemini

*Solution*: The model is temporarily overloaded. The test_llm_with_retry.py script handles this automatically by:

Retrying 3 times with exponential backoff

Falling back to gemini-2.0-flash or gemini-1.5-flash

**Issue**: ConnectionRefusedError when running test scripts

*Solution*: The API is not running. Start it first:
```
python api.py
# Keep this terminal open
Then run the test script in a new terminal.
```

| API | Endpoints | Reference |
|---|---|---|
| Method |	Endpoint |	Description
| GET | /	| API information |
| POST	| /memories/propose	| Propose new memory (governance review) |
| POST	| /memories/extract	| Extract memory from conversation using Gemini |
| GET	| /memories/graph	| Get graph summary (nodes, edges, stats) |
| GET	| /memories/graph/nodes	| List all memory nodes |
| GET	| /memories/graph/edges	| List all relations |
| POST	| /memories/relations	| Add relation between memories |
| GET	| /memories/relations/{node_id}	| Get relations for a node |
| POST	| /query/influence	| Get influenced prompt for a query |
| POST	| /governance/consolidate	| Run memory consolidation |
| GET	| /governance/status	| Get governance status |
| GET	| /principles/version-history |	Get principle version history |
| POST	| /memories/search	| Search memories by semantic similarity |
| POST	| /memories/reload	| Force graph reload from disk |

## Relationship Types
| Type	| Meaning	| Example |
|---|---|---|
| supports |	Memory A reinforces Memory B |	Privacy supports Data Minimization |
| contradicts	| Memory A conflicts with Memory B |	Privacy contradicts Maximum Utility |
| refines |	Memory A adds detail to Memory B |	GDPR refines Privacy principles |
| derives_from |	Memory A originates from Memory B |	New rule derives from established principle |
| supersedes |	Memory A replaces Memory B |	Updated principle supersedes old version |

## Performance Expectations
| Operation |	Typical Latency |	Notes |
|---|---|---|
| Memory proposal |	1-2 seconds |	Includes policy + debate |
| Query influence |	0.5-1 second |	Embeddings + ranking |
| Graph operations |	<100ms |	Local JSON operations |
| Consolidation |	2-5 seconds |	Depends on number of nodes |

## Next Steps After Phase 4
**Phase 4 is complete. Future enhancements could include**:

**Production Database**: Replace JSON with PostgreSQL/pgvector

**Authentication**: Add API keys and user roles

**Multi-user**: Private/shared memory spaces

**Real-time Updates**: WebSockets for live graph updates

**Docker Deployment**: Containerized setup

## License
This project is open-source. See repository for license information.

## Acknowledgments
Google Gemini API for LLM and embeddings

FastAPI for REST framework

Plotly for graph visualization
