# api.py - API REST para o SEM (Shared Ethical Memory)

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Importar módulos do SEM
from governance_core import GovernanceCore
from memory_graph import MemoryGraph
from influence_router import InfluenceRouter
from consolidation_scheduler import ConsolidationScheduler
from ethical_retriever_v2 import EthicalRetriever
from memory_extractor_v2 import MemoryExtractor

# ============================================================
# Modelos Pydantic (Schemas)
# ============================================================

class MemoryProposal(BaseModel):
    """Modelo para proposta de nova memória."""
    principle: str = Field(..., description="Princípio ético", min_length=3)
    context: str = Field(..., description="Contexto da decisão")
    decision: str = Field(..., description="Decisão tomada")
    justification: str = Field(..., description="Justificação ética")
    confidence: float = Field(0.85, ge=0.0, le=1.0, description="Confiança (0-1)")
    tags: List[str] = Field(default_factory=list, description="Tags para categorização")

class MemoryResponse(BaseModel):
    """Resposta após proposta de memória."""
    status: str  # accepted, revise, reject, warn
    reason: str
    memory_id: Optional[str] = None
    graph_node_id: Optional[str] = None
    suggestions: Optional[List[str]] = None

class RelationRequest(BaseModel):
    """Modelo para adicionar relação entre memórias."""
    source_id: str = Field(..., description="ID da memória origem")
    target_id: str = Field(..., description="ID da memória destino")
    relation_type: str = Field(..., description="Tipo: supports, contradicts, refines, derives_from, supersedes")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class QueryRequest(BaseModel):
    """Modelo para consulta com influência ética."""
    query: str = Field(..., description="Pergunta do utilizador")
    top_k: int = Field(5, ge=1, le=20, description="Número de memórias a recuperar")

class QueryResponse(BaseModel):
    """Resposta com contexto influenciado."""
    query: str
    influence_strategy: str
    memories_used: int
    confidence_scores: List[float]
    influenced_prompt: str

class ExtractRequest(BaseModel):
    """Modelo para extração de memória de uma conversa."""
    conversation: str = Field(..., description="Texto da conversa para análise")

class ExtractResponse(BaseModel):
    """Resposta da extração de memória."""
    memory: Optional[MemoryProposal] = None
    error: Optional[str] = None

# ============================================================
# Inicialização do SEM (lifespan)
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação."""
    print("🚀 Inicializando SEM API...")
    app.state.governance = GovernanceCore()
    app.state.graph = MemoryGraph()
    app.state.router = InfluenceRouter()
    app.state.consolidator = ConsolidationScheduler()
    app.state.retriever = EthicalRetriever()
    app.state.extractor = MemoryExtractor()
    print("✅ SEM API pronta!")
    yield
    print("👋 Encerrando SEM API...")

# ============================================================
# Criação da App FastAPI
# ============================================================

app = FastAPI(
    title="Shared Ethical Memory API",
    description="API para sistema de memória ética com governação multi-agente, grafo de conhecimento e influência garantida.",
    version="4.0.0",
    lifespan=lifespan
)

# CORS para permitir chamadas de front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restringir a domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Endpoints
# ============================================================

@app.get("/", tags=["Status"])
async def root():
    """Endpoint raiz com informações da API."""
    return {
        "name": "Shared Ethical Memory API",
        "version": "4.0.0",
        "status": "operational",
        "endpoints": [
            "/memories/propose",
            "/memories/extract",
            "/memories/graph",
            "/memories/relations",
            "/query/influence",
            "/governance/consolidate",
            "/governance/status",
            "/principles/version-history"
        ]
    }

@app.post("/memories/propose", response_model=MemoryResponse, tags=["Memories"])
async def propose_memory(memory: MemoryProposal):
    """
    Propõe uma nova memória ética.
    Passa pelo sistema de governação multi-agente antes de ser aceite.
    """
    result = app.state.governance.propose_memory(memory.dict())
    return MemoryResponse(**result)

@app.post("/memories/extract", response_model=ExtractResponse, tags=["Memories"])
async def extract_memory(request: ExtractRequest):
    """
    Extrai automaticamente uma memória ética de uma conversa usando Gemini.
    """
    try:
        extracted = app.state.extractor.extract_from_conversation(request.conversation)
        if extracted:
            return ExtractResponse(memory=MemoryProposal(**extracted))
        else:
            return ExtractResponse(error="Não foi possível extrair memória da conversa.")
    except Exception as e:
        return ExtractResponse(error=str(e))

@app.get("/memories/graph", tags=["Memory Graph"])
async def get_graph_summary():
    """Retorna um resumo do grafo de memórias (nós, arestas, estatísticas)."""
    return app.state.graph.get_graph_summary()

@app.get("/memories/graph/nodes", tags=["Memory Graph"])
async def get_graph_nodes(limit: int = Query(50, ge=1, le=200)):
    """Retorna a lista de nós do grafo."""
    nodes = app.state.graph.data.get("nodes", [])
    return {"total": len(nodes), "nodes": nodes[:limit]}

@app.get("/memories/graph/edges", tags=["Memory Graph"])
async def get_graph_edges(limit: int = Query(50, ge=1, le=200)):
    """Retorna a lista de arestas do grafo."""
    edges = app.state.graph.data.get("edges", [])
    return {"total": len(edges), "edges": edges[:limit]}

@app.post("/memories/relations", tags=["Memory Graph"])
async def add_relation(relation: RelationRequest):
    """
    Adiciona uma relação entre duas memórias existentes.
    Tipos: supports, contradicts, refines, derives_from, supersedes
    """
    edge = app.state.governance.add_relation(
        relation.source_id, 
        relation.target_id, 
        relation.relation_type,
        relation.metadata
    )
    if edge:
        return {"status": "created", "edge": edge}
    else:
        raise HTTPException(status_code=404, detail="Um dos nós não foi encontrado.")

@app.get("/memories/relations/{node_id}", tags=["Memory Graph"])
async def get_node_relations(node_id: str):
    """Retorna todas as relações de um nó específico."""
    edges_from = app.state.graph.get_edges_from(node_id)
    edges_to = app.state.graph.get_edges_to(node_id)
    return {
        "node_id": node_id,
        "outgoing": edges_from,
        "incoming": edges_to
    }

@app.post("/query/influence", response_model=QueryResponse, tags=["Query"])
async def get_influenced_context(request: QueryRequest):
    """
    Constrói um prompt com memórias éticas relevantes e instruções para garantir influência.
    """
    context = app.state.router.build_influence_prompt(request.query, top_k=request.top_k)
    return QueryResponse(
        query=context.base_query,
        influence_strategy=context.influence_strategy,
        memories_used=len(context.ranked_memories),
        confidence_scores=context.confidence_scores,
        influenced_prompt=context.influence_prompt
    )

@app.post("/governance/consolidate", tags=["Governance"])
async def run_consolidation(dry_run: bool = Query(False)):
    """
    Executa o processo de consolidação (pruning, merge, meta-memórias).
    Use dry_run=True para simular sem alterar dados.
    """
    result = app.state.consolidator.run(dry_run=dry_run)
    return result

@app.get("/governance/status", tags=["Governance"])
async def get_governance_status():
    """Retorna o estado atual da governação e do sistema."""
    graph_summary = app.state.graph.get_graph_summary()
    consolidation_status = app.state.consolidator.get_consolidation_status()
    
    return {
        "graph": graph_summary,
        "consolidation": consolidation_status,
        "governance_log": len(app.state.governance.log_path.read_text().splitlines()) if app.state.governance.log_path.exists() else 0
    }

@app.get("/principles/version-history", tags=["Principles"])
async def get_version_history():
    """Retorna o histórico de versões dos princípios éticos."""
    version_path = Path("principle_versions.json")
    if version_path.exists():
        data = json.loads(version_path.read_text(encoding='utf-8'))
        return data
    return {"versions": [], "message": "No version history found"}

@app.post("/memories/search", tags=["Memories"])
async def search_memories(query: str = Body(..., embed=True), top_k: int = Query(5)):
    """
    Busca memórias éticas por similaridade semântica.
    """
    results = app.state.retriever.retrieve_relevant_ethics(query, top_k)
    return {"query": query, "results": results}

# ============================================================
# Execução (apenas se correr diretamente)
# ============================================================

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload em desenvolvimento
        log_level="info"
    )
