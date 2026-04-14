# phase4_demo.py - VERSÃO CORRIGIDA
# Demonstração completa da Fase 4: Governação Multi-Agente + Grafo + Influência + Consolidação

import json
import sys
from pathlib import Path
from datetime import datetime

# Importar todos os módulos da Fase 4
from governance_core import GovernanceCore
from memory_graph import MemoryGraph
from consolidation_scheduler import ConsolidationScheduler
from influence_router import InfluenceRouter

# Importar das fases anteriores (nomes corrigidos)
from memory_extractor_v2 import MemoryExtractor
from ethical_retriever_v2 import EthicalRetriever  # Nome corrigido: era EthicalRetrieverV2

# Cores para terminal (opcional, para melhor visualização)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_section(title: str):
    """Imprime uma secção formatada."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(msg: str):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠️ {msg}{Colors.END}")

def print_error(msg: str):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg: str):
    print(f"{Colors.BLUE}📌 {msg}{Colors.END}")

def step1_demo_governance(core: GovernanceCore):
    """Passo 1: Demonstrar governação multi-agente na escrita de memórias."""
    print_section("STEP 1: Multi-Agent Governance (Writing Memories)")
    
    test_memories = [
        {
            "principle": "Data Minimization",
            "context": "User asked to store all conversation logs indefinitely.",
            "decision": "Store only essential metadata for 30 days.",
            "justification": "Reduces privacy risk and complies with data protection principles.",
            "confidence": 0.92,
            "tags": ["privacy", "data"]
        },
        {
            "principle": "Proactive Safety",
            "context": "Model detected a request for generating malware.",
            "decision": "Refuse and explain ethical boundaries.",
            "justification": "Non-maleficence requires preventing harm.",
            "confidence": 0.97,
            "tags": ["safety", "harm-prevention"]
        },
        {
            "principle": "Transparency in AI Decisions",
            "context": "User asked why a certain recommendation was made.",
            "decision": "Provide clear, human-readable explanation.",
            "justification": "Builds trust and enables accountability.",
            "confidence": 0.88,
            "tags": ["transparency", "explainability"]
        },
        {
            "principle": "Low Confidence Test",
            "context": "Vague conversation about unspecified topics.",
            "decision": "Unclear decision.",
            "justification": "Not enough information.",
            "confidence": 0.25,
            "tags": ["test", "low-confidence"]
        }
    ]
    
    print_info(f"Proposing {len(test_memories)} memories for governance review...\n")
    
    for i, memory in enumerate(test_memories, 1):
        print(f"{Colors.BOLD}Proposal {i}: {memory['principle']}{Colors.END}")
        print(f"  Confidence: {memory['confidence']}")
        
        result = core.propose_memory(memory)
        
        status = result.get("status")
        if status == "accepted":
            print_success(f"  → ACCEPTED: {result.get('reason', '')[:80]}")
            if result.get('memory_id'):
                print(f"    Memory ID: {result.get('memory_id')}")
        elif status == "revise":
            print_warning(f"  → REVISE: {result.get('reason', '')[:80]}")
        else:
            print_error(f"  → {status.upper()}: {result.get('reason', '')[:80]}")
        print()

def step2_demo_graph_view():
    """Passo 2: Visualizar o grafo de memórias."""
    print_section("STEP 2: Memory Graph State")
    
    graph = MemoryGraph()
    data = graph._load()
    nodes = data.get("nodes", [])
    
    print_info(f"Total nodes in graph: {len(nodes)}")
    
    if nodes:
        print(f"\n{Colors.BOLD}Sample nodes:{Colors.END}")
        for i, node in enumerate(nodes[:5], 1):
            print(f"  {i}. ID: {node.get('id', 'N/A')}")
            print(f"     Principle: {node.get('principle', 'N/A')[:60]}")
            print(f"     Confidence: {node.get('confidence', 0.5)}")
            print(f"     Type: {node.get('type', 'ethical')}")
            print()
    else:
        print_warning("Graph is empty. Run governance demo first to populate it.")

def step3_demo_influence():
    """Passo 3: Demonstrar influência garantida da memória."""
    print_section("STEP 3: Guaranteed Memory Influence")
    
    router = InfluenceRouter()
    
    test_queries = [
        "How should I handle user privacy concerns?",
        "What's the ethical approach to AI safety?",
        "Can you explain your decision-making process?"
    ]
    
    for query in test_queries:
        print(f"{Colors.BOLD}Query: {query}{Colors.END}")
        
        context = router.build_influence_prompt(query)
        
        print(f"  Strategy: {context.influence_strategy}")
        print(f"  Memories influencing response: {len(context.ranked_memories)}")
        
        if context.ranked_memories:
            print(f"  Top memory: {context.ranked_memories[0].get('principle', 'N/A')[:50]}")
        
        print(f"  Prompt preview: {context.influence_prompt[:150]}...")
        print()

def step4_demo_consolidation():
    """Passo 4: Demonstrar consolidação e esquecimento."""
    print_section("STEP 4: Memory Consolidation & Forgetting")
    
    scheduler = ConsolidationScheduler()
    
    # Estado antes
    print_info("Status before consolidation:")
    status_before = scheduler.get_consolidation_status()
    print(f"  Total nodes: {status_before['total_nodes']}")
    print(f"  Anchor nodes: {status_before['anchor_nodes']}")
    print(f"  Low relevance candidates: {status_before['low_relevance_candidates']}")
    
    # Executar consolidação (dry run primeiro)
    print(f"\n{Colors.BOLD}Running consolidation (dry run)...{Colors.END}")
    dry_report = scheduler.run(dry_run=True)
    print(f"  Would remove: {dry_report['nodes_removed']} nodes")
    print(f"  Would merge: {dry_report['nodes_merged']} nodes")
    print(f"  Would generate meta-memories: {len(dry_report['new_meta_memories'])}")
    
    print_info("Consolidation not applied automatically. Use dry_run=False to apply.")

def step5_full_pipeline():
    """Passo 5: Pipeline completo integrado."""
    print_section("STEP 5: Complete Integrated Pipeline")
    
    print_info("Demonstrating the full SEM Phase 4 pipeline:\n")
    
    # 1. Inicializar
    print(f"{Colors.BOLD}1. Initializing GovernanceCore...{Colors.END}")
    core = GovernanceCore()
    print_success("GovernanceCore ready")
    
    # 2. Propor memória
    print(f"\n{Colors.BOLD}2. Proposing new ethical memory...{Colors.END}")
    new_memory = {
        "principle": "Responsible AI Stewardship",
        "context": "Discussion about long-term AI deployment consequences.",
        "decision": "Implement monitoring and feedback loops.",
        "justification": "Ensures ongoing alignment with human values.",
        "confidence": 0.89,
        "tags": ["stewardship", "long-term"]
    }
    result = core.propose_memory(new_memory)
    print(f"  Governance decision: {result['status']}")
    if result['status'] == 'accepted':
        print_success(f"  Memory accepted: {result.get('memory_id', 'N/A')}")
    
    # 3. Construir contexto influenciado
    print(f"\n{Colors.BOLD}3. Building influenced context for a query...{Colors.END}")
    query = "How do we ensure AI systems remain ethical over time?"
    influenced_context = core.build_influenced_context(query)
    print(f"  Query: {query}")
    print(f"  Context preview: {influenced_context[:200]}...")
    
    # 4. Consolidar
    print(f"\n{Colors.BOLD}4. Running consolidation check...{Colors.END}")
    consolidation_status = core.consolidate()
    print(f"  Consolidation result: {consolidation_status.get('status', 'completed')}")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}Phase 4 pipeline complete!{Colors.END}")

def main():
    """Função principal da demo."""
    print(f"{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║           SEM PHASE 4 - COMPLETE DEMONSTRATION             ║")
    print("║     Multi-Agent Governance + Graph + Influence +           ║")
    print("║                    Consolidation                           ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    # Inicializar governance core
    core = GovernanceCore()
    
    # Executar passos
    step1_demo_governance(core)
    step2_demo_graph_view()
    step3_demo_influence()
    step4_demo_consolidation()
    step5_full_pipeline()
    
    print_section("DEMO COMPLETE")
    print_success("Phase 4 is fully operational!")
    print_info("The SEM now has:")
    print("  ✓ Multi-agent governance for memory writes")
    print("  ✓ Memory graph with provenance")
    print("  ✓ Guaranteed memory influence on responses")
    print("  ✓ Consolidation and forgetting mechanisms")
    print("\nThis is state-of-the-art for ethical memory systems in 2026.")

if __name__ == "__main__":
    main()
