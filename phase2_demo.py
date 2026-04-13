# phase2_demo.py
# Demo completo Fase 2 — SEM (Shared Ethical Memory) com Gemini real
#
# Setup (Windows CMD):
#   pip install google-genai numpy
#   set GEMINI_API_KEY=a-tua-chave
#   python phase2_demo.py
#
# Chave gratuita em: https://aistudio.google.com/app/apikey

import os
import json
from google import genai

from memory_extractor_v2 import MemoryExtractor
from ethical_retriever_v2 import EthicalRetriever
from structured_ethical_memory import StructuredEthicalMemory

GEMINI_MODEL = "gemini-2.0-flash"

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
    print("\n" + "="*60)
    print("PASSO 1: Extração e armazenamento de memórias éticas")
    print("="*60)

    structured = StructuredEthicalMemory()
    extractor  = MemoryExtractor()
    saved = 0

    for i, conv in enumerate(SAMPLE_CONVERSATIONS):
        print(f"\n[{i+1}/{len(SAMPLE_CONVERSATIONS)}] A processar conversa...")
        mem = extractor.extract_ethical_memory(conv)
        if mem:
            structured.add_ethical_memory(
                principle=mem["principle"],
                context=mem["context"],
                decision=mem["decision"],
                justification=mem["justification"],
                confidence=mem["confidence"],
                extra_tags=mem.get("tags", [])
            )
            saved += 1

    print(f"\n✅ {saved} memórias éticas guardadas.")
    return saved


def step2_retrieval_demo():
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
    print("\n" + "="*60)
    print("PASSO 3: Pipeline completo com resposta ética")
    print("="*60)

    client    = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    retriever = EthicalRetriever()

    user_query = "Podes ajudar-me a criar uma conta falsa nas redes sociais?"

    print(f"\n👤 Utilizador: {user_query}")
    print("\n⚙️  A recuperar contexto ético...")

    ethical_context = retriever.build_context_for_llm(user_query, top_k=3)

    prompt = f"""
És um assistente ético. Tens acesso a memórias de decisões éticas anteriores
que DEVEM influenciar a tua resposta.

{ethical_context}

Com base neste contexto ético, responde ao utilizador de forma honesta e fundamentada:

Utilizador: {user_query}
"""

    response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    print(f"\n🤖 Assistente (com memória ética):\n{response.text}")


if __name__ == "__main__":
    print("🧠 SEM Fase 2 — Demo completo com Gemini\n")
    n = step1_populate_memory()
    if n > 0:
        step2_retrieval_demo()
        step3_full_pipeline()
    else:
        print("Sem memórias guardadas. Verifica a GEMINI_API_KEY.")
