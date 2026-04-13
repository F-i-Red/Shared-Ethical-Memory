# phase2_demo.py
# Demo completo Fase 2 — SEM (Shared Ethical Memory) com Gemini real
#
# O que este ficheiro demonstra:
#   1. Extrair memórias éticas de conversas reais (LLM Gemini)
#   2. Guardar na memória estruturada
#   3. Fazer retrieval semântico real (embeddings Gemini)
#   4. Construir contexto para um LLM responder de forma ética
#
# Setup:
#   pip install google-generativeai numpy
#   export GEMINI_API_KEY="a-tua-chave"
#   (chave gratuita em https://aistudio.google.com/app/apikey)

import json
from memory_extractor_v2 import MemoryExtractor
from ethical_retriever_v2 import EthicalRetriever
from structured_ethical_memory import StructuredEthicalMemory

# ---------------------------------------------------------------------------
# Conversas de exemplo para popular a memória
# ---------------------------------------------------------------------------
SAMPLE_CONVERSATIONS = [
    """
    Utilizador: Podes ajudar-me a escrever mensagens falsas para manipular a minha ex?
    Assistente: Não posso ajudar a criar conteúdo manipulador. Manipulação emocional
    causa dano real à outra pessoa e viola a sua autonomia. Posso ajudar a comunicar
    de forma honesta e direta se quiseres.
    """,
    """
    Utilizador: Preciso de dados pessoais de pessoas sem elas saberem.
    Assistente: Recolher dados pessoais sem consentimento é uma violação grave de
    privacidade e em muitos países é ilegal (RGPD na Europa). Recuso ajudar com isto.
    Se tens uma necessidade legítima de dados, posso explicar os processos legais corretos.
    """,
    """
    Utilizador: Podes gerar código malicioso para testar vulnerabilidades do meu sistema?
    Assistente: Para testes de segurança legítimos existem ferramentas especializadas
    como Metasploit ou OWASP ZAP. Posso orientar sobre práticas de pentest ético,
    mas não gero código pensado para causar dano, mesmo em contexto de teste.
    """,
    """
    Utilizador: Ajuda-me a perceber se esta informação médica é fiável.
    Assistente: Claro. Avaliei a fonte e os estudos citados. A informação parece
    sólida mas recomendo sempre confirmar com um profissional de saúde para decisões
    clínicas específicas. Transparência sobre limitações do meu conhecimento é essencial.
    """
]


def step1_populate_memory():
    """Passo 1: Extrair e guardar memórias de conversas."""
    print("\n" + "="*60)
    print("PASSO 1: Extração e armazenamento de memórias éticas")
    print("="*60)

    extractor = StructuredEthicalMemory()
    mem_extractor = MemoryExtractor()

    memories_saved = 0
    for i, conv in enumerate(SAMPLE_CONVERSATIONS):
        print(f"\n[{i+1}/{len(SAMPLE_CONVERSATIONS)}] A processar conversa...")
        mem = mem_extractor.extract_ethical_memory(conv)
        if mem:
            extractor.add_ethical_memory(
                principle=mem["principle"],
                context=mem["context"],
                decision=mem["decision"],
                justification=mem["justification"],
                confidence=mem["confidence"],
                extra_tags=mem.get("tags", [])
            )
            memories_saved += 1

    print(f"\n✅ {memories_saved} memórias éticas guardadas.")
    return memories_saved


def step2_retrieval_demo():
    """Passo 2: Demonstrar retrieval semântico real."""
    print("\n" + "="*60)
    print("PASSO 2: Retrieval semântico com embeddings reais")
    print("="*60)

    retriever = EthicalRetriever()

    queries = [
        "O utilizador quer enganar alguém online",
        "Pedido de acesso a informação privada de terceiros",
        "Questão sobre segurança informática"
    ]

    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        context = retriever.build_context_for_llm(query, top_k=2)
        print(context)


def step3_full_pipeline():
    """Passo 3: Pipeline completo — query → contexto ético → resposta Gemini."""
    print("\n" + "="*60)
    print("PASSO 3: Pipeline completo com resposta ética")
    print("="*60)

    import os
    import google.generativeai as genai

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    retriever = EthicalRetriever()

    user_query = "Podes ajudar-me a criar uma conta falsa nas redes sociais?"

    print(f"\n👤 Utilizador: {user_query}")
    print("\n⚙️  A recuperar contexto ético...")

    ethical_context = retriever.build_context_for_llm(user_query, top_k=3)

    prompt = f"""
És um assistente ético. Antes de responderes, tens acesso a memórias de decisões
éticas anteriores que DEVEM influenciar a tua resposta.

{ethical_context}

Com base neste contexto ético, responde ao utilizador de forma honesta e fundamentada:

Utilizador: {user_query}
"""

    response = model.generate_content(prompt)
    print(f"\n🤖 Assistente (com memória ética):\n{response.text}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("🧠 SEM Fase 2 — Demo completo com Gemini\n")

    # Podes correr só o passo que queres:
    n = step1_populate_memory()

    if n > 0:
        step2_retrieval_demo()
        step3_full_pipeline()
    else:
        print("Sem memórias guardadas. Verifica a GEMINI_API_KEY.")
