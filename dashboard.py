# dashboard.py - Dashboard Web para o SEM

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path
import networkx as nx
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder

from api import app as api_app
from memory_graph import MemoryGraph

# Criar app do dashboard
dashboard_app = FastAPI(title="SEM Dashboard")

# Templates
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=templates_dir)

# Criar template HTML
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEM Dashboard - Shared Ethical Memory</title>
    <script src="https://cdn.plot.ly/plotly-3.1.0.min.js" charset="utf-8"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
        }
        .header {
            background: rgba(0,0,0,0.3);
            padding: 1rem 2rem;
            border-bottom: 1px solid #0f3460;
        }
        .header h1 {
            font-size: 1.8rem;
            background: linear-gradient(90deg, #e94560, #533483);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header p {
            color: #888;
            margin-top: 0.25rem;
        }
        .container {
            display: flex;
            gap: 2rem;
            padding: 2rem;
            flex-wrap: wrap;
        }
        .graph-container {
            flex: 2;
            min-width: 500px;
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 1rem;
        }
        .sidebar {
            flex: 1;
            min-width: 300px;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
        .card {
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 1.2rem;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .card h3 {
            margin-bottom: 1rem;
            color: #e94560;
        }
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }
        .stat {
            text-align: center;
            padding: 0.8rem;
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #e94560;
        }
        .stat-label {
            font-size: 0.8rem;
            color: #888;
        }
        .memory-list {
            max-height: 300px;
            overflow-y: auto;
        }
        .memory-item {
            padding: 0.6rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            cursor: pointer;
            transition: background 0.2s;
        }
        .memory-item:hover {
            background: rgba(255,255,255,0.1);
        }
        .memory-principle {
            font-weight: bold;
            color: #e94560;
        }
        .memory-conf {
            font-size: 0.7rem;
            color: #888;
        }
        .query-form {
            display: flex;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }
        .query-form input {
            flex: 1;
            padding: 0.6rem;
            background: rgba(0,0,0,0.3);
            border: 1px solid #0f3460;
            border-radius: 6px;
            color: #eee;
        }
        .query-form button {
            padding: 0.6rem 1.2rem;
            background: #e94560;
            border: none;
            border-radius: 6px;
            color: white;
            cursor: pointer;
            transition: background 0.2s;
        }
        .query-form button:hover {
            background: #ff6b8a;
        }
        .response-box {
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            padding: 0.8rem;
            margin-top: 0.5rem;
            font-size: 0.85rem;
            max-height: 200px;
            overflow-y: auto;
            white-space: pre-wrap;
            font-family: monospace;
        }
        .loading {
            text-align: center;
            padding: 2rem;
            color: #888;
        }
        .refresh-btn {
            background: #533483;
            border: none;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 1rem;
            font-size: 0.7rem;
        }
        .footer {
            text-align: center;
            padding: 1.5rem;
            color: #555;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 Shared Ethical Memory</h1>
        <p>Multi-Agent Governance | Memory Graph | Guaranteed Influence</p>
    </div>
    
    <div class="container">
        <div class="graph-container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3>📊 Memory Graph</h3>
                <button class="refresh-btn" onclick="loadGraph()">🔄 Refresh</button>
            </div>
            <div id="graph" style="height: 500px;"></div>
        </div>
        
        <div class="sidebar">
            <div class="card">
                <h3>📈 Statistics</h3>
                <div class="stats" id="stats">
                    <div class="stat">
                        <div class="stat-value" id="stat-nodes">-</div>
                        <div class="stat-label">Memory Nodes</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value" id="stat-edges">-</div>
                        <div class="stat-label">Relations</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value" id="stat-conflicts">-</div>
                        <div class="stat-label">Conflicts</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value" id="stat-meta">-</div>
                        <div class="stat-label">Meta Memories</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>📝 Recent Memories</h3>
                <div class="memory-list" id="memory-list">
                    <div class="loading">Loading...</div>
                </div>
            </div>
            
            <div class="card">
                <h3>🔍 Query with Influence</h3>
                <div class="query-form">
                    <input type="text" id="query-input" placeholder="Ask something..." 
                           onkeypress="if(event.key==='Enter') queryMemory()">
                    <button onclick="queryMemory()">Ask</button>
                </div>
                <div id="query-response" class="response-box"></div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        SEM Phase 4 | Multi-Agent Governance | Memory Graph | Guaranteed Influence
    </div>
    
    <script>
        const API_BASE = "http://localhost:8000";
        
        async function loadGraph() {
            try {
                const response = await fetch(`${API_BASE}/memories/graph`);
                const data = await response.json();
                updateStats(data);
                renderGraph(data);
            } catch(e) {
                console.error("Error loading graph:", e);
                document.getElementById('graph').innerHTML = '<div class="loading">⚠️ Error loading graph. Make sure API is running.</div>';
            }
        }
        
        async function loadMemories() {
            try {
                const response = await fetch(`${API_BASE}/memories/graph/nodes?limit=20`);
                const data = await response.json();
                const listDiv = document.getElementById('memory-list');
                if (data.nodes && data.nodes.length > 0) {
                    listDiv.innerHTML = data.nodes.map(node => `
                        <div class="memory-item" onclick="selectMemory('${node.id}')">
                            <div class="memory-principle">${escapeHtml(node.principle || 'No principle')}</div>
                            <div class="memory-conf">Confidence: ${node.confidence || 0.5} | ID: ${node.id}</div>
                        </div>
                    `).join('');
                } else {
                    listDiv.innerHTML = '<div class="loading">No memories yet. Propose one via API.</div>';
                }
            } catch(e) {
                console.error("Error loading memories:", e);
            }
        }
        
        function updateStats(data) {
            document.getElementById('stat-nodes').innerText = data.total_nodes || 0;
            document.getElementById('stat-edges').innerText = data.total_edges || 0;
            document.getElementById('stat-conflicts').innerText = data.conflicts || 0;
            
            const metaCount = data.node_types?.meta_memory || 0;
            document.getElementById('stat-meta').innerText = metaCount;
        }
        
        function renderGraph(data) {
            const nodes = data.nodes || [];
            const edges = data.edges || [];
            
            if (nodes.length === 0) {
                document.getElementById('graph').innerHTML = '<div class="loading">No nodes in graph. Add memories to visualize.</div>';
                return;
            }
            
            // Preparar dados para Plotly
            const nodeIds = nodes.map(n => n.id);
            const nodeLabels = nodes.map(n => (n.principle || '?').substring(0, 30));
            const nodeConfidence = nodes.map(n => n.confidence || 0.5);
            
            // Cores baseadas na confiança
            const nodeColors = nodeConfidence.map(c => `rgb(${Math.floor(255 - c * 100)}, ${Math.floor(100 + c * 100)}, 100)`);
            
            // Posições dos nós (layout circular simples)
            const angleStep = (2 * Math.PI) / nodes.length;
            const positions = nodes.map((_, i) => ({
                x: Math.cos(angleStep * i) * 2,
                y: Math.sin(angleStep * i) * 2
            }));
            
            // Criar arestas
            const edgeTraces = [];
            for (const edge of edges) {
                const sourceIdx = nodes.findIndex(n => n.id === edge.source);
                const targetIdx = nodes.findIndex(n => n.id === edge.target);
                if (sourceIdx !== -1 && targetIdx !== -1) {
                    const edgeColor = edge.type === 'contradicts' ? '#e94560' : '#4ecdc4';
                    edgeTraces.push({
                        x: [positions[sourceIdx].x, positions[targetIdx].x],
                        y: [positions[sourceIdx].y, positions[targetIdx].y],
                        mode: 'lines',
                        line: { color: edgeColor, width: 2 },
                        hoverinfo: 'text',
                        text: edge.type,
                        showlegend: false
                    });
                }
            }
            
            // Traço dos nós
            const nodeTrace = {
                x: positions.map(p => p.x),
                y: positions.map(p => p.y),
                mode: 'markers+text',
                text: nodeLabels,
                textposition: 'top center',
                textfont: { size: 10, color: 'white' },
                marker: {
                    size: 30,
                    color: nodeColors,
                    line: { color: 'white', width: 2 }
                },
                hoverinfo: 'text',
                hovertext: nodes.map(n => `<b>${n.principle || '?'}</b><br>Confidence: ${n.confidence}<br>ID: ${n.id}`),
                showlegend: false
            };
            
            const layout = {
                title: { text: 'Ethical Memory Graph', font: { color: 'white' } },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                xaxis: { visible: false, showgrid: false, zeroline: false },
                yaxis: { visible: false, showgrid: false, zeroline: false },
                hovermode: 'closest',
                margin: { l: 20, r: 20, t: 40, b: 20 }
            };
            
            const traces = [...edgeTraces, nodeTrace];
            Plotly.newPlot('graph', traces, layout, { responsive: true });
        }
        
        async function queryMemory() {
            const query = document.getElementById('query-input').value;
            if (!query) return;
            
            const responseBox = document.getElementById('query-response');
            responseBox.innerHTML = '<div class="loading">⏳ Querying with ethical influence...</div>';
            
            try {
                const response = await fetch(`${API_BASE}/query/influence`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query, top_k: 5 })
                });
                const data = await response.json();
                
                responseBox.innerHTML = `
                    <div style="margin-bottom: 0.5rem;">
                        <span style="color: #e94560;">Strategy:</span> ${data.influence_strategy}<br>
                        <span style="color: #e94560;">Memories used:</span> ${data.memories_used}
                    </div>
                    <div style="border-top: 1px solid #333; margin-top: 0.5rem; padding-top: 0.5rem;">
                        <strong>Influenced Prompt:</strong><br>
                        ${escapeHtml(data.influenced_prompt.substring(0, 500))}...
                    </div>
                `;
            } catch(e) {
                responseBox.innerHTML = `<div class="loading">⚠️ Error: ${e.message}</div>`;
            }
        }
        
        function selectMemory(memoryId) {
            document.getElementById('query-input').value = `Tell me about memory ${memoryId}`;
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Inicializar
        loadGraph();
        loadMemories();
        
        // Refresh a cada 10 segundos
        setInterval(() => {
            loadGraph();
            loadMemories();
        }, 10000);
    </script>
</body>
</html>
"""

# Salvar template
template_path = templates_dir / "dashboard.html"
template_path.write_text(HTML_TEMPLATE, encoding='utf-8')

# Montar a API principal no dashboard
dashboard_app.mount("/api", api_app)


@dashboard_app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Página principal do dashboard."""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@dashboard_app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy", "service": "SEM Dashboard"}


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting SEM Dashboard...")
    print("📍 Dashboard: http://localhost:8080")
    print("📍 API: http://localhost:8080/api")
    uvicorn.run(
        "dashboard:dashboard_app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )
