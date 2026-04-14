# dashboard_simple.py - Dashboard simplificado (HTML puro)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx
import json

app = FastAPI(title="SEM Dashboard Simple")

API_URL = "http://localhost:8000"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEM Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0f1a;
            color: #e0e0e0;
            padding: 20px;
        }
        h1 { color: #e94560; margin-bottom: 10px; }
        .status {
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .status.online { background: #1a3a2a; color: #4ecdc4; }
        .status.offline { background: #3a1a1a; color: #e94560; }
        .container { display: flex; gap: 20px; flex-wrap: wrap; }
        .card {
            background: #1a1a2e;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #2a2a4e;
            flex: 1;
            min-width: 300px;
        }
        .card h3 { color: #4ecdc4; margin-bottom: 15px; }
        .stat-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        .stat {
            background: #0f0f1a;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value { font-size: 28px; font-weight: bold; color: #e94560; }
        .stat-label { font-size: 12px; color: #888; margin-top: 5px; }
        .memory-item {
            padding: 10px;
            border-bottom: 1px solid #2a2a4e;
            cursor: pointer;
        }
        .memory-item:hover { background: #2a2a4e; }
        .memory-principle { font-weight: bold; color: #4ecdc4; }
        .query-box {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        .query-box input {
            flex: 1;
            padding: 10px;
            background: #0f0f1a;
            border: 1px solid #2a2a4e;
            border-radius: 6px;
            color: #e0e0e0;
        }
        .query-box button {
            padding: 10px 20px;
            background: #e94560;
            border: none;
            border-radius: 6px;
            color: white;
            cursor: pointer;
        }
        .query-box button:hover { background: #ff6b8a; }
        .response {
            background: #0f0f1a;
            padding: 15px;
            border-radius: 8px;
            font-size: 13px;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
            font-family: monospace;
        }
        .loading { text-align: center; padding: 20px; color: #888; }
        .error { color: #e94560; }
        .refresh-btn {
            background: #4ecdc4;
            color: #0f0f1a;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 10px;
            font-size: 12px;
        }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        hr { border-color: #2a2a4e; margin: 15px 0; }
    </style>
</head>
<body>
    <h1>🧠 Shared Ethical Memory Dashboard</h1>
    <div id="api-status" class="status">🔌 Checking API connection...</div>
    
    <div class="container">
        <div class="card">
            <h3>📊 Graph Statistics</h3>
            <div class="stat-grid" id="stats">
                <div class="stat"><div class="stat-value">-</div><div class="stat-label">Nodes</div></div>
                <div class="stat"><div class="stat-value">-</div><div class="stat-label">Edges</div></div>
                <div class="stat"><div class="stat-value">-</div><div class="stat-label">Conflicts</div></div>
                <div class="stat"><div class="stat-value">-</div><div class="stat-label">Meta Memories</div></div>
            </div>
        </div>
        
        <div class="card">
            <h3>📝 Memories <button class="refresh-btn" onclick="loadMemories()">⟳</button></h3>
            <div id="memories-list" class="loading">Loading...</div>
        </div>
        
        <div class="card">
            <h3>🔍 Query with Ethical Influence</h3>
            <div class="query-box">
                <input type="text" id="query" placeholder="Ask something..." onkeypress="if(event.key==='Enter') queryInfluence()">
                <button onclick="queryInfluence()">Ask</button>
            </div>
            <div id="query-result" class="response">✨ Ask a question to see ethical memory in action</div>
        </div>
    </div>
    
    <div class="card" style="margin-top: 20px;">
        <h3>📋 Governance Log</h3>
        <div id="governance-log" class="response" style="max-height: 200px;">Loading...</div>
    </div>

    <script>
        const API_BASE = "http://localhost:8000";
        
        async function checkAPI() {
            const statusDiv = document.getElementById('api-status');
            try {
                const response = await fetch(`${API_BASE}/`);
                if (response.ok) {
                    statusDiv.innerHTML = '✅ API Online - SEM is operational';
                    statusDiv.className = 'status online';
                    return true;
                } else {
                    throw new Error('API responded with error');
                }
            } catch(e) {
                statusDiv.innerHTML = '❌ API Offline - Make sure to run: python api.py';
                statusDiv.className = 'status offline';
                return false;
            }
        }
        
        async function loadStats() {
            try {
                const response = await fetch(`${API_BASE}/memories/graph`);
                const data = await response.json();
                document.getElementById('stats').innerHTML = `
                    <div class="stat"><div class="stat-value">${data.total_nodes || 0}</div><div class="stat-label">Nodes</div></div>
                    <div class="stat"><div class="stat-value">${data.total_edges || 0}</div><div class="stat-label">Edges</div></div>
                    <div class="stat"><div class="stat-value">${data.conflicts || 0}</div><div class="stat-label">Conflicts</div></div>
                    <div class="stat"><div class="stat-value">${data.node_types?.meta_memory || 0}</div><div class="stat-label">Meta Memories</div></div>
                `;
            } catch(e) {
                console.error('Error loading stats:', e);
            }
        }
        
        async function loadMemories() {
            const listDiv = document.getElementById('memories-list');
            listDiv.innerHTML = '<div class="loading">Loading memories...</div>';
            try {
                const response = await fetch(`${API_BASE}/memories/graph/nodes?limit=20`);
                const data = await response.json();
                if (data.nodes && data.nodes.length > 0) {
                    listDiv.innerHTML = data.nodes.map(node => `
                        <div class="memory-item" onclick="document.getElementById('query').value = 'Tell me about: ${node.principle || node.id}'; queryInfluence();">
                            <div class="memory-principle">${escapeHtml(node.principle || 'No principle')}</div>
                            <div style="font-size: 11px; color: #888;">ID: ${node.id} | Conf: ${node.confidence || 0.5}</div>
                        </div>
                    `).join('');
                } else {
                    listDiv.innerHTML = '<div class="loading">No memories yet. Use POST /memories/propose to add.</div>';
                }
            } catch(e) {
                listDiv.innerHTML = `<div class="loading error">Error loading memories: ${e.message}</div>`;
            }
        }
        
        async function queryInfluence() {
            const query = document.getElementById('query').value;
            if (!query) {
                alert('Please enter a question');
                return;
            }
            
            const resultDiv = document.getElementById('query-result');
            resultDiv.innerHTML = '<div class="loading">⏳ Querying with ethical influence...</div>';
            
            try {
                const response = await fetch(`${API_BASE}/query/influence`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query, top_k: 5 })
                });
                const data = await response.json();
                
                resultDiv.innerHTML = `
                    <div style="margin-bottom: 10px;">
                        <span style="color: #4ecdc4;">Strategy:</span> ${data.influence_strategy}<br>
                        <span style="color: #4ecdc4;">Memories used:</span> ${data.memories_used}
                    </div>
                    <hr>
                    <div><strong>Influenced Prompt:</strong></div>
                    <div style="margin-top: 8px;">${escapeHtml(data.influenced_prompt)}</div>
                `;
            } catch(e) {
                resultDiv.innerHTML = `<div class="loading error">Error: ${e.message}</div>`;
            }
        }
        
        async function loadGovernanceLog() {
            const logDiv = document.getElementById('governance-log');
            try {
                const response = await fetch(`${API_BASE}/governance/status`);
                const data = await response.json();
                logDiv.innerHTML = `
                    <div>📊 Graph Nodes: ${data.graph?.total_nodes || 0}</div>
                    <div>📈 Graph Edges: ${data.graph?.total_edges || 0}</div>
                    <div>📝 Log Entries: ${data.governance_log || 0}</div>
                    <div>🔄 Last Consolidation: ${data.consolidation?.last_consolidation || 'Never'}</div>
                `;
            } catch(e) {
                logDiv.innerHTML = `<div class="error">Error: ${e.message}</div>`;
            }
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Initial load
        async function init() {
            const online = await checkAPI();
            if (online) {
                loadStats();
                loadMemories();
                loadGovernanceLog();
            }
        }
        
        init();
        
        // Auto-refresh every 15 seconds
        setInterval(() => {
            if (document.getElementById('api-status').classList.contains('online')) {
                loadStats();
                loadMemories();
                loadGovernanceLog();
            }
        }, 15000);
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Página principal do dashboard."""
    return HTML_PAGE

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("🚀 SEM Dashboard (Simplified)")
    print("📍 http://localhost:8080")
    print("=" * 50)
    uvicorn.run(
        "dashboard_simple:dashboard_app",
        host="0.0.0.0",
        port=8080,
        reload=False
    )
