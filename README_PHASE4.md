# SEM Phase 4 - Multi-Agent Governance & Memory Graph

## Overview

Phase 4 transforms SEM (Shared Ethical Memory) from a simple memory system into a **cognitive governance architecture** with:

- **Multi-Agent Governance**: 5 agents (Extractor, Critic, Validator, Curator, Arbiter) debate before accepting/rejecting memories
- **Memory Graph**: Nodes + edges with relationship types (supports, contradicts, refines, derives_from, supersedes)
- **Guaranteed Influence**: Prompt construction that FORCES memory to influence LLM responses
- **Consolidation & Forgetting**: Temporal decay, semantic merging, and meta-memory generation
- **REST API**: Full FastAPI interface with Swagger docs
- **Web Dashboard**: Real-time graph visualization and query interface

## Architecture

┌─────────────────────────────────────────────────────────────────┐

│ PHASE 4 ARCHITECTURE │

├─────────────────────────────────────────────────────────────────┤

│ │

│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │

│ │ Web UI │ │ REST API │ │ Dashboard │ │

│ │ (Port 8080) │◄──►│ (Port 8000) │ │ (Plotly) │ │

│ └──────────────┘ └──────┬───────┘ └──────────────┘ │

│ │ │

│ ▼ │

│ ┌──────────────────────────────────────────────────────────┐ │

│ │ GOVERNANCE CORE │ │

│ │ ┌────────────┐ ┌────────────┐ ┌────────────────────┐ │ │

│ │ │ Policy │ │ Multi- │ │ Memory │ │ │

│ │ │ Engine │ │ Agent │ │ Graph │ │ │

│ │ │ │ │ Debate │ │ │ │ │

│ │ └────────────┘ └────────────┘ └────────────────────┘ │ │

│ └──────────────────────────────────────────────────────────┘ │

│ │ │

│ ▼ │

│ ┌──────────────────────────────────────────────────────────┐ │

│ │ STORAGE LAYER │ │

│ │ ┌────────────┐ ┌────────────┐ ┌────────────────────┐ │ │

│ │ │ Structured │ │ Memory │ │ Governance │ │ │

│ │ │ Memory │ │ Graph │ │ Log │ │ │

│ │ │ (JSON) │ │ (JSON) │ │ (JSON) │ │ │

│ │ └────────────┘ └────────────┘ └────────────────────┘ │ │

│ └──────────────────────────────────────────────────────────┘ │

│ │

└─────────────────────────────────────────────────────────────────┘

## Prerequisites

### System Requirements
- Windows 10/11, macOS, or Linux
- Python 3.10 or higher
- Internet connection (for Gemini API)
- 4GB RAM minimum (8GB recommended)

### API Key Required
- **Gemini API Key** (free): Get from [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

## Installation

### 1. Clone or Download the Project

```bash
git clone https://github.com/F-i-Red/Shared-Ethical-Memory.git
cd Shared-Ethical-Memory
```

## 2. Install Python Dependencies
```
pip install google-genai numpy fastapi uvicorn pydantic httpx plotly networkx
```

## 3. Set Your Gemini API Key
### Windows (CMD):
```
set GEMINI_API_KEY=your-api-key-here
```

### Windows (PowerShell):
```
$env:GEMINI_API_KEY="your-api-key-here"
```
### macOS / Linux:
```
export GEMINI_API_KEY="your-api-key-here"
```

## File Structure
Ensure these files are in your project directory:

Shared-Ethical-Memory/
├── api.py                      # REST API server
├── dashboard_simple.py         # Web dashboard
├── governance_core.py          # Multi-agent governance core
├── memory_graph.py             # Graph with edges/nodes
├── policy_engine.py            # Policy evaluation
├── multi_agent_debate.py       # 5-agent debate system
├── consolidation_scheduler.py  # Memory lifecycle management
├── influence_router.py         # Guaranteed memory influence
├── ethical_retriever_v2.py     # Semantic retrieval with embeddings
├── memory_extractor_v2.py      # LLM-based memory extraction
├── structured_ethical_memory.py # Base memory storage
├── drift_detector.py           # Conflict detection
├── meta_memory.py              # Meta-principle generation
├── principle_versioning.py     # Principle evolution tracking
└── memories.json               # Stored memories (auto-generated)

# Running SEM Phase 4

## Step 1: Start the API Server

### Open a terminal and run:

```
# Windows
set GEMINI_API_KEY=your-api-key-here
python api.py

# macOS/Linux
export GEMINI_API_KEY="your-api-key-here"
python api.py
```
## Expected output:

🚀 Inicializando SEM API...
[EthicalRetriever] Embeddings via 'models/gemini-embedding-001'
[MemoryExtractor] Gemini 'models/gemini-2.5-flash' iniciado.
✅ SEM API pronta!
INFO:     Uvicorn running on http://0.0.0.0:8000

### The API will be available at: http://localhost:8000

## Step 2: Start the Web Dashboard

### Open a second terminal and run:
```
# Windows
python dashboard_simple.py

# macOS/Linux
python dashboard_simple.py
```
## Expected output:
```
============================================================
🚀 SEM Dashboard (Simplified)
📍 Dashboard: http://localhost:8080
📍 API: http://localhost:8000
============================================================
INFO:     Uvicorn running on http://0.0.0.0:8080
```

The dashboard will be available at: http://localhost:8080

Step 3: Verify Both Services
Service	URL	Status
API	http://localhost:8000	✅ Should show JSON response
Dashboard	http://localhost:8080	✅ Should show web interface
API Docs	http://localhost:8000/docs	✅ FastAPI Swagger UI
Testing the System
Option A: Using the Web Dashboard
Open http://localhost:8080

Check API status (should show ✅ green)

View graph statistics and memory nodes

Type a query like: "How should we handle user data privacy?"

Click "Ask →" to see the influenced prompt

Option B: Using API Endpoints
### 1. Check API Health
```
curl http://localhost:8000/
```
### 2. Propose a New Memory
```
curl -X POST http://localhost:8000/memories/propose \
  -H "Content-Type: application/json" \
  -d '{
    "principle": "Data Minimization",
    "context": "User asked about data storage practices",
    "decision": "Store only essential data for 30 days",
    "justification": "Reduces privacy risk and respects user autonomy",
    "confidence": 0.92,
    "tags": ["privacy", "data"]
  }'
```

### 3. Query with Ethical Influence
```
curl -X POST http://localhost:8000/query/influence \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How to handle user privacy concerns?",
    "top_k": 5
  }'
```

### 4. View Memory Graph
```
curl http://localhost:8000/memories/graph
```

### 5. View Governance Status
```
curl http://localhost:8000/governance/status
```

### Option C: Using Python Test Script
Create test_phase4.py:
```
import requests
import json

BASE_URL = "http://localhost:8000"

# Test API health
print("1. Testing API health...")
r = requests.get(f"{BASE_URL}/")
print(f"   Status: {r.status_code}")
print(f"   Response: {r.json()['name']} v{r.json()['version']}\n")

# Propose a memory
print("2. Proposing a memory...")
memory = {
    "principle": "Transparency First",
    "context": "User asked for explanation of AI decision",
    "decision": "Provide clear, human-readable explanation",
    "justification": "Builds trust and enables accountability",
    "confidence": 0.88,
    "tags": ["transparency", "trust"]
}
r = requests.post(f"{BASE_URL}/memories/propose", json=memory)
print(f"   Status: {r.status_code}")
print(f"   Response: {json.dumps(r.json(), indent=2)}\n")

# Query with influence
print("3. Querying with ethical influence...")
query = {"query": "How to be transparent with users?", "top_k": 3}
r = requests.post(f"{BASE_URL}/query/influence", json=query)
result = r.json()
print(f"   Strategy: {result['influence_strategy']}")
print(f"   Memories used: {result['memories_used']}")
print(f"   Prompt preview: {result['influenced_prompt'][:200]}...\n")

print("✅ All tests passed!")
```

### Run it:
```
python test_phase4.py
```

## API Endpoints Reference
Method	Endpoint	Description
GET	/	API information
POST	/memories/propose	Propose new memory (governance review)
POST	/memories/extract	Extract memory from conversation using Gemini
GET	/memories/graph	Get graph summary (nodes, edges, stats)
GET	/memories/graph/nodes	List all memory nodes
GET	/memories/graph/edges	List all relations
POST	/memories/relations	Add relation between memories
GET	/memories/relations/{node_id}	Get relations for a node
POST	/query/influence	Get influenced prompt for a query
POST	/governance/consolidate	Run memory consolidation
GET	/governance/status	Get governance status
GET	/principles/version-history	Get principle version history
POST	/memories/search	Search memories by semantic similarity

## Relationship Types
Type	Meaning	Example
supports	Memory A reinforces Memory B	Privacy supports Data Minimization
contradicts	Memory A conflicts with Memory B	Privacy contradicts Maximum Utility
refines	Memory A adds detail to Memory B	GDPR refines Privacy principles
derives_from	Memory A originates from Memory B	New rule derives from established principle
supersedes	Memory A replaces Memory B	Updated principle supersedes old version


## Troubleshooting
### Issue: "GEMINI_API_KEY not found"
Solution: Set the environment variable before running:
```
# Windows
set GEMINI_API_KEY=your-key-here

# Verify it's set
echo %GEMINI_API_KEY%
```

### Issue: Port 8000 already in use
Solution: Change the port in api.py:
```
# Find this line at the end of api.py
uvicorn.run("api:app", host="0.0.0.0", port=8000)  # Change 8000 to 8001
```

## Issue: Dashboard can't connect to API
Solution: Ensure API is running first, then dashboard. Check both terminals:
```
# Terminal 1 - Should show API running
python api.py

# Terminal 2 - Should show dashboard running
python dashboard_simple.py
```

## Issue: Rate limit errors from Gemini
Solution: The free tier has 5 requests/minute. Add delays between calls or upgrade to paid tier.

## Issue: ImportError: cannot import name 'EthicalRetrieverV2'
Solution: The correct import is EthicalRetriever (without V2):
```
from ethical_retriever_v2 import EthicalRetriever
```

### Performance Expectations
Operation	Typical Latency	Notes
Memory proposal	1-2 seconds	Includes policy + debate
Query influence	0.5-1 second	Embeddings + ranking
Graph operations	<100ms	Local JSON operations
Consolidation	2-5 seconds	Depends on number of nodes

## Next Steps After Phase 4
Phase 4 is complete. Future enhancements could include:

Production Database: Replace JSON with PostgreSQL/pgvector

Authentication: Add API keys and user roles

Multi-user: Private/shared memory spaces

Real-time Updates: WebSockets for live graph updates

Docker Deployment: Containerized setup

## License
This project is open-source. See repository for license information.

# Acknowledgments
Google Gemini API for LLM and embeddings

FastAPI for REST framework

Plotly for graph visualization






## Environment
- `GEMINI_API_KEY` is optional, but required for LLM refinement.
- The rest of the system works locally with JSON files.
