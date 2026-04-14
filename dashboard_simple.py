# dashboard_simple.py - Dashboard Simplificado (CORRIGIDO)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx
import json

app = FastAPI(title="SEM Dashboard")

API_URL = "http://localhost:8000"  # API está na porta 8000

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEM Dashboard - Shared Ethical Memory</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0f1a;
            color: #e0e0e0;
            padding: 20px;
        }
        h1 { 
            color: #e94560; 
            margin-bottom: 5px;
            font-size: 2rem;
        }
        .subtitle { color: #888; margin-bottom: 20px; font-size: 0.9rem; }
        .status {
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: inline-block;
        }
        .status.online { background: #1a3a2a; color: #4ecdc4; border-left: 4px solid #4ecdc4; }
        .status.offline { background: #3a1a1a; color: #e94560; border-left: 4px solid #e94560; }
        .container { display: flex; gap: 20px; flex-wrap: wrap; }
        .card {
            background: #1a1a2e;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #2a2a4e;
            flex: 1;
            min-width: 300px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .card h3 { color: #4ecdc4; margin-bottom: 15px; border-left: 3px solid #e94560; padding-left: 10px; }
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
            transition: transform 0.2s;
        }
        .stat:hover { transform: translateY(-2px); background: #1a1a2e; }
        .stat-value { font-size: 32px; font-weight: bold; color: #e94560; }
        .stat-label { font-size: 12px; color: #888; margin-top: 5px; }
        .memory-list {
            max-height: 400px;
            overflow-y: auto;
        }
        .memory-item {
            padding: 12px;
            border-bottom: 1px solid #2a2a4e;
            cursor: pointer;
            transition: background 0.2s;
            border-radius: 6px;
        }
        .memory-item:hover { background: #2a2a4e; }
        .memory-principle { font-weight: bold; color: #4ecdc4; font-size: 0.9rem; }
        .memory-meta { font-size: 11px; color: #888; margin-top: 5px; }
        .query-box {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        .query-box input {
            flex: 1;
            padding: 12px;
            background: #0f0f1a;
            border: 1px solid #2a2a4e;
            border-radius: 6px;
            color: #e0e0e0;
            font-size: 14px;
        }
        .query-box input:focus {
            outline: none;
            border-color: #e94560;
        }
        .query-box button {
            padding: 12px 24px;
            background: #e94560;
            border: none;
            border-radius: 6px;
            color: white;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.2s;
        }
        .query-box button:hover { background: #ff6b8a; }
        .response {
            background: #0f0f1a;
            padding: 15px;
            border-radius: 8px;
            font-size: 13px;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
        }
        .loading { text-align: center; padding: 20px; color: #888; }
        .error { color: #e94560; }
        .refresh-btn {
            background: #4ecdc4;
            color: #0f0f1a;
            border: none;
            padding: 5px 12px;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 10px;
            font-size: 11px;
            font-weight: bold;
        }
        .refresh-btn:hover { background: #6ee0d8; }
        hr { border-color: #2a2a4e; margin: 15px 0; }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #555;
            font-size: 0.8rem;
            border-top: 1px solid #2a2a4e;
        }
        .badge {
            display: inline-block;
            background: #e94560;
            color: white;
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 10px;
            margin-left: 8px;
        }
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0f0f1a;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb {
            background: #2a2a4e;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #e94560;
        }
    </style>
</head>
<body>
    <h1>🧠 Shared Ethical Memory <span class="badge">Phase 4</span></h1>
    <div class="subtitle">Multi-Agent Governance | Memory Graph | Guaranteed Influence</div>
    
    <div id="api-status" class="status">🔌 Checking API connection...</div>
    
    <div class="container">
        <div class="card">
            <h3>📊 Graph Statistics <button class="refresh-btn" onclick="loadStats()">⟳</button></h3>
            <div class="stat-grid" id="stats">
                <div class="stat"><div class="stat-value">-</div><div class="stat-label">Nodes</div></div>
                <div class="stat"><div class="stat-value">-</div><div class="stat-label">Edges</div></div>
                <div class="stat"><div class="stat-value">-</div><div class="stat-label">Conflicts</div></div>
                <div class="stat"><div class="stat-value">-</div><div class="stat-label">Meta Memories</div></div>
            </div>
        </div>
        
        <div class="card">
            <h3>📝 Memory Nodes <button class="refresh-btn" onclick="loadMemories()">⟳</button></h3>
            <div class="memory-list" id="memories-list">
                <div class="loading">Loading memories...</div>
            </div>
        </div>
        
        <div class="card">
            <h3>🔍 Ethical Query</h3>
            <div class="query-box">
                <input type="text" id="query" placeholder="Ask something (e.g., 'How to handle user privacy?')" 
                       onkeypress="if(event.key==='Enter') queryInfluence()">
                <button onclick="queryInfluence()">Ask →</button>
            </div>
            <div id="query-result" class="response">
                ✨ Ask a question to see ethical memory influence
            </div>
        </div>
    </div>
    
    <div class="card" style="margin-top: 20px;">
        <h3>📋 Governance Status</h3>
        <div id="governance-log" class="response" style="max-height: 150px;">Loading...</div>
    </div>
    
    <div class="footer">
        SEM Phase 4 | Powered by Gemini 2.5 Flash | Memory Graph v2 | Influence Router
    </div>

    <script>
        const API_BASE = "http://localhost:8000";
        
        async function checkAPI() {
            const statusDiv = document.getElementById('api-status');
            try {
                const response = await fetch(`${API_BASE}/`);
                if (response.ok) {
                    const data = await response.json();
                    statusDiv.innerHTML = `✅ API Online - ${data.name} v${data.version}`;
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
            listDiv.innerHTML = '<div class="loading">📡 Loading memories...</div>';
            try {
                const response = await fetch(`${API_BASE}/memories/graph/nodes?limit=20`);
                const data = await response.json();
                if (data.nodes && data.nodes.length > 0) {
                    listDiv.innerHTML = data.nodes.map(node => `
                        <div class="memory-item" onclick="document.getElementById('query').value = '${escapeHtml(node.principle || node.id)}'; queryInfluence();">
                            <div class="memory-principle">📌 ${escapeHtml(node.principle || 'No principle')}</div>
                            <div class="memory-meta">🆔 ${node.id} | 📊 Confidence: ${(node.confidence || 0.5).toFixed(2)} | 🏷️ ${node.type || 'ethical'}</div>
                        </div>
                    `).join('');
                } else {
                    listDiv.innerHTML = '<div class="loading">📭 No memories yet. Use POST /memories/propose to add.</div>';
                }
            } catch(e) {
                listDiv.innerHTML = `<div class="loading error">❌ Error: ${e.message}</div>`;
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
                    <div style="margin-bottom: 12px;">
                        <span style="color: #4ecdc4; font-weight: bold;">🎯 Strategy:</span> ${data.influence_strategy}<br>
                        <span style="color: #4ecdc4; font-weight: bold;">📚 Memories used:</span> ${data.memories_used}
                    </div>
                    <hr>
                    <div style="margin-top: 12px;">
                        <strong>📝 Influenced Prompt:</strong>
                    </div>
                    <div style="margin-top: 8px; background: #0a0a12; padding: 10px; border-radius: 6px;">
                        ${escapeHtml(data.influenced_prompt)}
                    </div>
                `;
            } catch(e) {
                resultDiv.innerHTML = `<div class="loading error">❌ Error: ${e.message}</div>`;
            }
        }
        
        async function loadGovernanceLog() {
            const logDiv = document.getElementById('governance-log');
            logDiv.innerHTML = '<div class="loading">Loading governance status...</div>';
            try {
                const response = await fetch(`${API_BASE}/governance/status`);
                const data = await response.json();
                logDiv.innerHTML = `
                    <div>📊 <strong>Graph Nodes:</strong> ${data.graph?.total_nodes || 0}</div>
                    <div>📈 <strong>Graph Edges:</strong> ${data.graph?.total_edges || 0}</div>
                    <div>📝 <strong>Log Entries:</strong> ${data.governance_log || 0}</div>
                    <div>🔄 <strong>Last Consolidation:</strong> ${data.consolidation?.last_consolidation || 'Never'}</div>
                    <div>📉 <strong>Low Relevance Candidates:</strong> ${data.consolidation?.low_relevance_candidates || 0}</div>
                `;
            } catch(e) {
                logDiv.innerHTML = `<div class="loading error">❌ Error: ${e.message}</div>`;
            }
        }
        
        function escapeHtml(text) {
            if (!text) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Initial load
        async function init() {
            const online = await checkAPI();
            if (online) {
                await loadStats();
                await loadMemories();
                await loadGovernanceLog();
            }
        }
        
        init();
        
        // Auto-refresh every 15 seconds
        setInterval(async () => {
            const statusDiv = document.getElementById('api-status');
            if (statusDiv.classList.contains('online')) {
                await loadStats();
                await loadMemories();
                await loadGovernanceLog();
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
    return {"status": "healthy", "service": "SEM Dashboard"}

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 SEM Dashboard (Simplified)")
    print("📍 Dashboard: http://localhost:8080")
    print("📍 API: http://localhost:8000")
    print("=" * 60)
    print("\n⚠️  Certifica-te que a API está a correr: python api.py")
    print("=" * 60)
    uvicorn.run(
        "dashboard_simple:app",
        host="0.0.0.0",
        port=8080,
        reload=False
    )
