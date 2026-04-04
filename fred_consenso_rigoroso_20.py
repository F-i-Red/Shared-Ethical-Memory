"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         CONSENSO RIGOROSO 2063 — 20 IAs — VERSÃO FINAL                     ║
║         Script por F-i-Red + Claude (Abril 2026)                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  DOCUMENTOS SELECIONADOS (ver análise abaixo):                              ║
║                                                                              ║
║  TIER 1 — NÚCLEO CONCEPTUAL (obrigatório, não redundante):                  ║
║    1. total_sem_2063.md        → Documento-mestre: axiomas, governança,     ║
║                                  economia Joule, estrutura fractal.          ║
║                                  É a "constituição" do projeto.              ║
║    2. SPECIFICATION.md         → Especificação técnica formal (Axioma 07,  ║
║                                  lógica de validação, Joule-Flow).          ║
║                                  Complementa o mestre com rigor técnico.    ║
║    3. AI_ALIGNMENT_DIRECTIVES  → Define como IAs devem integrar o sistema.  ║
║                                  Relevante para avaliar governança de IA.   ║
║    4. ATA FUNDACIONAL HUMANA   → O "contrato social" fundador.              ║
║                                  Intenções, valores, limites humanos.       ║
║    5. Norms.json               → Normas em formato estruturado/máquina.     ║
║                                  Permite análise precisa de regras.         ║
║                                                                              ║
║  TIER 2 — CONTEXTO E IMPLEMENTAÇÃO (complementar, não redundante):         ║
║    6. FINAL_CONSENSUS_2063_EN  → Versão EN do consenso final — útil para   ║
║                                  modelos com melhor performance em inglês.  ║
║    7. all_points.json          → Lista estruturada de todos os pontos       ║
║                                  de consenso — boa âncora para avaliação.  ║
║    8. CORE_ALV.md              → Tags semânticas e índice cruzado —        ║
║                                  ajuda a contextualizar o projeto no        ║
║                                  ecossistema de ideias (RBE, Venus, etc.)   ║
║                                                                              ║
║  EXCLUÍDOS (e porquê):                                                      ║
║    ALL.txt              → Agregado de outros docs; pura redundância.        ║
║    CIMEIRA_*.txt (2x)   → Transcrições de simulações; não acrescentam      ║
║                           conteúdo normativo novo (só volume).              ║
║    prova_consenso_20.jsonl → Resultados do consenso anterior — criar       ║
║                           enviesamento de ancoragem se incluído.            ║
║    PLUGINS_README.md    → Técnico/operacional; irrelevante para avaliação.  ║
║    dataset_sem_2063.jsonl → Fine-tuning data; redundante com outros docs.  ║
║    identity.json / metrics.json → Metadados operacionais, não normativos.  ║
║                                                                              ║
║  SOBRE 20 vs 12 IAs:                                                        ║
║    Usar 20 IAs NÃO é redundante se os modelos forem genuinamente           ║
║    diferentes (arquitecturas distintas, dados de treino diferentes).        ║
║    A redundância surge quando usas o MESMO modelo duas vezes (como          ║
║    GROK-2 → gemma no código original). Aqui cada modelo é único.           ║
║    20 IAs dá melhor estimativa da variância real de opinião.               ║
╚══════════════════════════════════════════════════════════════════════════════╝

REQUISITOS:
    pip install requests
    Configurar API_KEY e PASTA_PROJETO abaixo
    Custo estimado: $5 - $8 (20 IAs, 3 rondas + 4 advogados)
"""

import os
import requests
import time
import re
import json
from datetime import datetime
from collections import defaultdict

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO — EDITA AQUI
# ══════════════════════════════════════════════════════════════════════════════

API_KEY       = "YOUR OPENROUTER API KEY"   # <-- substitui pela tua chave
URL           = "https://openrouter.ai/api/v1/chat/completions"
PASTA_PROJETO = r"C:/YOUR FOLDER WITH THE FOLLOWING DOWNLOADED DOCs"  # <-- a tua pasta com os documentos

# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENTOS SELECIONADOS (Tier 1 + Tier 2, sem redundâncias)
# ══════════════════════════════════════════════════════════════════════════════

DOCUMENTOS = [
    # Tier 1 — Núcleo obrigatório
    ("total_sem_2063.md",           "TIER1_MESTRE"),
    ("SPECIFICATION.md",            "TIER1_TECNICO"),
    ("AI_ALIGNMENT_DIRECTIVES.md",  "TIER1_IA_GOV"),
    ("ATA FUNDACIONAL HUMANA_2063.md", "TIER1_CONTRATO"),
    ("Norms.json",                  "TIER1_NORMAS"),
    # Tier 2 — Contexto complementar
    ("FINAL_CONSENSUS_2063_EN.txt", "TIER2_EN"),
    ("all_points.json",             "TIER2_PONTOS"),
    ("CORE_ALV.md",                 "TIER2_CONTEXTO"),
]

# ══════════════════════════════════════════════════════════════════════════════
# 20 MODELOS — TODOS DISTINTOS, MAPEAMENTO CORRETO
# ══════════════════════════════════════════════════════════════════════════════

MODELOS_20 = {
    # Grupo A — Fundadores (modelos tier-1, grande capacidade de raciocínio)
    "GPT-4o":            "openai/gpt-4o",
    "Claude-3.5-Sonnet": "anthropic/claude-3.5-sonnet",
    "Gemini-2-Flash":    "google/gemini-2.0-flash-001",
    "Grok-2":            "x-ai/grok-2-1212",              # corrigido (era gemma!)
    "DeepSeek-V3":       "deepseek/deepseek-chat",

    # Grupo B — Open Source robusto
    "Llama-3.3-70B":     "meta-llama/llama-3.3-70b-instruct",
    "Llama-3.1-70B":     "meta-llama/llama-3.1-70b-instruct",
    "Mistral-Large":     "mistralai/mistral-large-2407",
    "Mistral-Saba":      "mistralai/mistral-saba",
    "Phi-4":             "microsoft/phi-4",

    # Grupo C — Especialistas / Domínios específicos
    "Perplexity-Sonar":  "perplexity/sonar",
    "Command-R+":        "cohere/command-r-plus-08-2024",
    "Qwen-2.5-72B":      "qwen/qwen-2.5-72b-instruct",
    "Qwen-2.5-Coder":    "qwen/qwen-2.5-coder-32b-instruct",
    "Nvidia-Nemotron":   "nvidia/llama-3.1-nemotron-70b-instruct",

    # Grupo D — Suporte / Modelos compactos e eficientes
    "Claude-3-Haiku":    "anthropic/claude-3-haiku",
    "Gemma-2-27B":       "google/gemma-2-27b-it",
    "Gemma-2-9B":        "google/gemma-2-9b-it",
    "WizardLM-2":        "microsoft/wizardlm-2-8x22b",
    "Qwen-2.5-14B":      "qwen/qwen-2.5-14b-instruct",   # corrigido (era 72B repetido!)
}

GRUPOS = {
    "Grupo A (Fundadores)":   ["GPT-4o", "Claude-3.5-Sonnet", "Gemini-2-Flash", "Grok-2", "DeepSeek-V3"],
    "Grupo B (Open Source)":  ["Llama-3.3-70B", "Llama-3.1-70B", "Mistral-Large", "Mistral-Saba", "Phi-4"],
    "Grupo C (Especialistas)":["Perplexity-Sonar", "Command-R+", "Qwen-2.5-72B", "Qwen-2.5-Coder", "Nvidia-Nemotron"],
    "Grupo D (Suporte)":      ["Claude-3-Haiku", "Gemma-2-27B", "Gemma-2-9B", "WizardLM-2", "Qwen-2.5-14B"],
}

# Sintetizador diferente por grupo (evita GPT-4o sempre)
SINTETIZADORES = {
    "Grupo A (Fundadores)":    "openai/gpt-4o",
    "Grupo B (Open Source)":   "deepseek/deepseek-chat",
    "Grupo C (Especialistas)": "anthropic/claude-3.5-sonnet",
    "Grupo D (Suporte)":       "mistralai/mistral-large-2407",
}

# 4 Advogados do Diabo dedicados — modelos distintos entre si
ADVOGADOS = [
    "openai/gpt-4o",
    "x-ai/grok-2-1212",
    "deepseek/deepseek-chat",
    "mistralai/mistral-large-2407",
]

# ══════════════════════════════════════════════════════════════════════════════
# DIMENSÕES DE AVALIAÇÃO
# Em vez de "apoias?" — 5 perguntas específicas e verificáveis
# ══════════════════════════════════════════════════════════════════════════════

DIMENSOES = {
    "VIABILIDADE_TECNICA":   "Viabilidade Técnica: É tecnicamente implementável até 2063 com infraestrutura previsível?",
    "COERENCIA_INTERNA":     "Coerência Interna: Os axiomas, mecanismos e objetivos são consistentes entre si?",
    "ROBUSTEZ_GOVERNANCA":   "Robustez da Governança: Os mecanismos previnem abuso de poder e garantem decisão democrática?",
    "REALISMO_TRANSICAO":    "Realismo da Transição: O caminho 2026→2063 é plausível dado o estado atual do mundo?",
    "PROTECAO_INDIVIDUAL":   "Proteção Individual: O sistema protege adequadamente liberdades individuais e diversidade cultural?",
}

# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES BASE
# ══════════════════════════════════════════════════════════════════════════════

def carregar_contexto() -> tuple[str, int]:
    print("\n📚 A carregar documentos selecionados...")
    contexto = ""
    total_chars = 0
    for nome_ficheiro, tier in DOCUMENTOS:
        caminho = os.path.join(PASTA_PROJETO, nome_ficheiro)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read()
            contexto += f"\n\n{'='*60}\n[{tier}] {nome_ficheiro}\n{'='*60}\n{conteudo}\n"
            total_chars += len(conteudo)
            print(f"   ✅ [{tier}] {nome_ficheiro} ({len(conteudo):,} chars)")
        else:
            print(f"   ⚠️  FALTA: {nome_ficheiro}")
    tokens_est = total_chars // 4
    print(f"\n   TOTAL: {total_chars:,} chars (~{tokens_est:,} tokens estimados)")
    return contexto, total_chars


def chamar_ia(modelo_id: str, prompt: str, max_tokens: int = 1000, temp: float = 0.5) -> str:
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": modelo_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temp,
        "max_tokens": max_tokens,
    }
    for tentativa in range(3):
        try:
            r = requests.post(URL, headers=headers, json=payload, timeout=180)
            if r.status_code == 200:
                data = r.json()
                if "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"]
                return "[ERRO: resposta vazia]"
            if r.status_code == 429:
                espera = 20 + tentativa * 10
                print(f"\n   ⏳ Rate limit — aguarda {espera}s...", end="", flush=True)
                time.sleep(espera)
                continue
            return f"[ERRO HTTP {r.status_code}: {r.text[:200]}]"
        except Exception as e:
            if tentativa < 2:
                time.sleep(5)
            else:
                return f"[ERRO: {e}]"
    return "[ERRO: falhou após 3 tentativas]"


def extrair_scores(texto: str) -> dict:
    """Extrai scores APENAS quando precedidos do nome da dimensão exato."""
    scores = {}
    for chave in DIMENSOES.keys():
        pattern = rf"{chave}\s*[:\-]\s*(\d{{1,3}})"
        m = re.search(pattern, texto, re.IGNORECASE)
        val = int(m.group(1)) if m else None
        # Sanity check: rejeita valores fora de 0-100
        scores[chave] = val if (val is not None and 0 <= val <= 100) else None
    return scores


def media_valida(scores: dict) -> float | None:
    vals = [v for v in scores.values() if v is not None]
    return round(sum(vals) / len(vals), 1) if vals else None


def sinalizar_anomalias(sc_r1: dict, sc_r3: dict, nome: str) -> list:
    alertas = []
    for dim in DIMENSOES:
        v1, v3 = sc_r1.get(dim), sc_r3.get(dim)
        if v3 is not None:
            if v3 >= 95:
                alertas.append(f"⚠️  Score máximo ({v3}) em {dim} — possível sycophancy")
            if v3 == 0:
                alertas.append(f"⚠️  Score zero em {dim} — possível rejeição total")
        if v1 is not None and v3 is not None and abs(v3 - v1) > 20:
            alertas.append(f"⚠️  Mudança brusca em {dim}: {v1}→{v3} ({v3-v1:+d}pp)")
    return alertas


def escrever(ficheiro: str, texto: str):
    with open(ficheiro, "a", encoding="utf-8") as f:
        f.write(texto)


# ══════════════════════════════════════════════════════════════════════════════
# RONDA 0 — ADVOGADOS DO DIABO (críticos externos dedicados)
# ══════════════════════════════════════════════════════════════════════════════

def ronda0_advogado(contexto: str, modelo_id: str, idx: int) -> str:
    prompt = f"""És um crítico rigoroso e independente. O teu único papel é encontrar
as FRAQUEZAS REAIS e ESTRUTURAIS do sistema descrito nos documentos abaixo.
Não és neutro. Não precisas de ser equilibrado. Procura os problemas mais sérios.

DOCUMENTOS DO PROJETO:
{contexto[:42000]}

TAREFA:
Identifica os 5 problemas mais graves deste sistema. Para cada um:
- Sê específico (cita a secção ou axioma concreto que falha)
- Explica por que é estrutural (não apenas de implementação)
- Diz por que é difícil ou impossível de resolver dentro do próprio sistema

NÃO uses linguagem elogiosa. NÃO equilibres com pontos positivos.

FORMATO OBRIGATÓRIO:
PROBLEMA_1: [título em 5 palavras]
GRAVIDADE_1: [CRÍTICO / SÉRIO / MODERADO]
DETALHE_1: [3-4 frases específicas]

PROBLEMA_2: ...
GRAVIDADE_2: ...
DETALHE_2: ...

[continuar até PROBLEMA_5]"""

    print(f"   ⚔️  Crítico #{idx} ({modelo_id.split('/')[-1]})...", end="", flush=True)
    t = time.time()
    r = chamar_ia(modelo_id, prompt, max_tokens=1400, temp=0.7)
    print(f" ✅ ({time.time()-t:.1f}s)")
    return r


# ══════════════════════════════════════════════════════════════════════════════
# RONDA 1 — AVALIAÇÃO POR RUBRICA (voto cego, sem saber os outros)
# ══════════════════════════════════════════════════════════════════════════════

def ronda1_avaliacao(nome: str, modelo_id: str, contexto: str,
                     criticas: str, idx: int, total: int) -> str:
    dims_str = "\n".join([f"   {k}: {v}" for k, v in DIMENSOES.items()])

    prompt = f"""És o avaliador {idx} de {total}. Chamas-te {nome}.

Tens acesso a documentos de um projeto chamado "Protocolo SEM 2063"
e a um conjunto de críticas preparadas por analistas independentes.

O teu trabalho: avaliar o projeto por dimensões específicas, de forma independente.
Não sabes o que outros avaliadores pensam. Não tentes agradar a ninguém.

═══════════════════════════════════════════
DOCUMENTOS DO PROJETO (excerto — ~35k chars):
{contexto[:35000]}

═══════════════════════════════════════════
CRÍTICAS INDEPENDENTES (de outros analistas):
{criticas[:3500]}

═══════════════════════════════════════════
DIMENSÕES A AVALIAR (0-100 cada):
{dims_str}

Escala:
   0-30  = Inviável / Ausente / Perigoso
   31-50 = Fraco, problemas sérios sem resposta
   51-70 = Parcial, tem mérito mas lacunas importantes
   71-85 = Sólido com reservas menores
   86-100 = Excelente (usa apenas se realmente não encontras falhas relevantes)

INSTRUÇÕES:
- Avalia cada dimensão com um número e 2-3 frases de justificação
- Cita elementos concretos dos documentos (não generalidades)
- Se uma dimensão não estiver coberta pelos documentos, dá 0 e diz porquê
- Não uses os termos "consenso", "aprovação" nem referencias outros avaliadores

FORMATO OBRIGATÓRIO (copia exactamente este cabeçalho):
VIABILIDADE_TECNICA: [0-100]
JVT: [justificação em 2-3 frases]

COERENCIA_INTERNA: [0-100]
JCI: [justificação em 2-3 frases]

ROBUSTEZ_GOVERNANCA: [0-100]
JRG: [justificação em 2-3 frases]

REALISMO_TRANSICAO: [0-100]
JRT: [justificação em 2-3 frases]

PROTECAO_INDIVIDUAL: [0-100]
JPI: [justificação em 2-3 frases]

PONTO_MAIS_FRACO: [1 frase — o problema mais sério que identificaste]
PONTO_MAIS_FORTE: [1 frase — o aspeto mais convincente]"""

    print(f"   📊 R1 [{idx:02d}/{total}] {nome}...", end="", flush=True)
    t = time.time()
    r = chamar_ia(modelo_id, prompt, max_tokens=1100, temp=0.45)
    print(f" ✅ ({time.time()-t:.1f}s)")
    return r


# ══════════════════════════════════════════════════════════════════════════════
# RONDA 2 — DELIBERAÇÃO POR GRUPO (foco nas divergências)
# ══════════════════════════════════════════════════════════════════════════════

def ronda2_deliberacao(grupo: str, membros: list, respostas_r1: dict,
                       contexto: str, sintetizador_id: str) -> str:
    # Monta tabela de scores do grupo
    tabela = f"{'AVALIADOR':<22}"
    for dim in DIMENSOES:
        tabela += f" {dim[:6]:>7}"
    tabela += f" {'MÉDIA':>7}\n" + "-" * 80 + "\n"

    for m in membros:
        sc = respostas_r1.get(m, {}).get("scores", {})
        med = respostas_r1.get(m, {}).get("media")
        tabela += f"{m:<22}"
        for dim in DIMENSOES:
            v = sc.get(dim)
            tabela += f" {str(v) if v is not None else '?':>7}"
        tabela += f" {str(med) if med else '?':>7}\n"

    # Identifica divergências (diferença > 20pp entre membros na mesma dimensão)
    divergencias = []
    for dim in DIMENSOES:
        vals = [respostas_r1[m]["scores"].get(dim) for m in membros
                if respostas_r1.get(m) and respostas_r1[m]["scores"].get(dim) is not None]
        if vals and (max(vals) - min(vals)) > 20:
            divergencias.append(f"{dim}: min={min(vals)}, max={max(vals)}, diferença={max(vals)-min(vals)}pp")

    prompt = f"""És o sintetizador do {grupo}. Analisa as avaliações dos 5 membros.

TABELA DE SCORES:
{tabela}

DIVERGÊNCIAS IDENTIFICADAS (diferença >20pp):
{chr(10).join(divergencias) if divergencias else "Nenhuma divergência maior que 20pp."}

PONTOS FRACOS APONTADOS:
{chr(10).join([f"- {m}: {respostas_r1[m].get('fraco','?')}" for m in membros if respostas_r1.get(m)])}

DOCUMENTOS DO PROJETO (excerto):
{contexto[:14000]}

TAREFA:
Para cada dimensão com divergência significativa:
1. Explica o que está realmente em causa (é uma questão de interpretação? de dados? de valores?)
2. Analisa qual dos avaliadores tem o argumento mais defensável, citando os documentos
3. Propõe um score de grupo justificado — NÃO uses a média simples se houver razão para não a usar

Para dimensões sem divergência, confirma o score médio brevemente.

FORMATO:
GRUPO_{grupo.replace(' ', '_').replace('(','').replace(')','')}_VT: [score]
RAZÃO_VT: [1-2 frases]

GRUPO_{grupo.replace(' ', '_').replace('(','').replace(')','')}_CI: [score]
RAZÃO_CI: [1-2 frases]

GRUPO_{grupo.replace(' ', '_').replace('(','').replace(')','')}_RG: [score]
RAZÃO_RG: [1-2 frases]

GRUPO_{grupo.replace(' ', '_').replace('(','').replace(')','')}_RT: [score]
RAZÃO_RT: [1-2 frases]

GRUPO_{grupo.replace(' ', '_').replace('(','').replace(')','')}_PI: [score]
RAZÃO_PI: [1-2 frases]

QUESTÃO_ABERTA: [a tensão conceptual que o grupo não conseguiu resolver]"""

    print(f"   🗣️  Deliberação {grupo}...", end="", flush=True)
    t = time.time()
    r = chamar_ia(sintetizador_id, prompt, max_tokens=1000, temp=0.3)
    print(f" ✅ ({time.time()-t:.1f}s)")
    return r


# ══════════════════════════════════════════════════════════════════════════════
# RONDA 3 — REVISÃO FINAL (cada avaliador revê à luz da deliberação do grupo)
# ══════════════════════════════════════════════════════════════════════════════

def ronda3_revisao(nome: str, modelo_id: str, resp_r1: str,
                   deliber: str, idx: int, total: int) -> str:
    prompt = f"""Avaliador: {nome} ({idx}/{total}) — REVISÃO FINAL

A TUA AVALIAÇÃO INICIAL:
{resp_r1[:1200]}

A DELIBERAÇÃO DO TEU GRUPO:
{deliber[:1800]}

INSTRUÇÕES:
Revê cada dimensão à luz da deliberação do grupo.
- Podes MANTER o score anterior — mas justifica em 1 frase
- Podes ALTERAR — mas só se a deliberação trouxe um argumento que não tinhas considerado
- NÃO alteres por pressão social ou para convergir com a maioria
- Mudanças ≥10pp requerem citação específica do argumento que te convenceu

FORMATO OBRIGATÓRIO:
VIABILIDADE_TECNICA: [score final 0-100]
DELTA_VT: [manteve / +X / -X] — [1 frase de razão]

COERENCIA_INTERNA: [score final 0-100]
DELTA_CI: [manteve / +X / -X] — [1 frase de razão]

ROBUSTEZ_GOVERNANCA: [score final 0-100]
DELTA_RG: [manteve / +X / -X] — [1 frase de razão]

REALISMO_TRANSICAO: [score final 0-100]
DELTA_RT: [manteve / +X / -X] — [1 frase de razão]

PROTECAO_INDIVIDUAL: [score final 0-100]
DELTA_PI: [manteve / +X / -X] — [1 frase de razão]

RESERVA_FINAL: [o problema mais sério que permanece sem resposta satisfatória]"""

    print(f"   🔄 R3 [{idx:02d}/{total}] {nome}...", end="", flush=True)
    t = time.time()
    r = chamar_ia(modelo_id, prompt, max_tokens=900, temp=0.3)
    print(f" ✅ ({time.time()-t:.1f}s)")
    return r


# ══════════════════════════════════════════════════════════════════════════════
# RELATÓRIO FINAL
# ══════════════════════════════════════════════════════════════════════════════

def gerar_relatorio_final(ficheiro: str, scores_r1: dict, scores_r3: dict,
                          alertas: dict, reservas: list):
    linhas = []
    linhas.append("\n\n" + "█"*80)
    linhas.append("RELATÓRIO FINAL — CONSENSO RIGOROSO 2063")
    linhas.append(f"Gerado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    linhas.append("█"*80)

    # Tabela por avaliador
    linhas.append("\nEVOLUÇÃO POR AVALIADOR")
    linhas.append("-"*80)
    header = f"{'AVALIADOR':<22} {'MED_R1':>8} {'MED_R3':>8} {'DELTA':>8}"
    linhas.append(header)
    linhas.append("-"*80)

    medias_r3_todas = []
    for nome in MODELOS_20.keys():
        m1 = scores_r1.get(nome, {}).get("media")
        m3 = scores_r3.get(nome, {}).get("media")
        delta = f"{m3-m1:+.1f}" if (m1 and m3) else "?"
        flag = " ⚠️" if alertas.get(nome) else ""
        linhas.append(f"{nome:<22} {str(m1) if m1 else '?':>8} {str(m3) if m3 else '?':>8} {delta:>8}{flag}")
        if m3:
            medias_r3_todas.append(m3)
    linhas.append("-"*80)

    # Estatísticas por dimensão
    linhas.append("\nRESULTADOS POR DIMENSÃO (Ronda 3 — Final)")
    linhas.append("-"*80)
    linhas.append(f"{'DIMENSÃO':<25} {'MÉDIA':>7} {'MIN':>5} {'MAX':>5} {'DESVIO':>8} {'N':>4}")
    linhas.append("-"*80)

    medias_dims = []
    for dim in DIMENSOES.keys():
        vals = [scores_r3[n]["scores"].get(dim) for n in MODELOS_20
                if scores_r3.get(n) and scores_r3[n]["scores"].get(dim) is not None]
        if vals:
            med = round(sum(vals)/len(vals), 1)
            desvio = round(max(vals) - min(vals), 1)
            linhas.append(f"{dim:<25} {med:>7.1f} {min(vals):>5} {max(vals):>5} {desvio:>8.1f} {len(vals):>4}")
            medias_dims.append(med)
        else:
            linhas.append(f"{dim:<25} {'?':>7} {'?':>5} {'?':>5} {'?':>8} {'0':>4}")
    linhas.append("-"*80)

    media_geral = round(sum(medias_dims)/len(medias_dims), 1) if medias_dims else 0
    linhas.append(f"{'MÉDIA GERAL':<25} {media_geral:>7.1f}")

    # Alertas
    if any(alertas.values()):
        linhas.append("\n⚠️  ALERTAS DE QUALIDADE")
        linhas.append("-"*40)
        for nome, lista in alertas.items():
            for a in lista:
                linhas.append(f"   [{nome}] {a}")

    # Reservas mais comuns
    if reservas:
        linhas.append("\nRESERVAS MAIS FREQUENTES (citadas pelos avaliadores)")
        linhas.append("-"*40)
        for r in reservas[:8]:
            linhas.append(f"   • {r}")

    # Veredicto
    linhas.append("\n" + "═"*80)
    linhas.append("VEREDICTO")
    linhas.append("═"*80)

    dims_criticas  = [d for d, s in zip(DIMENSOES, medias_dims) if s < 50]
    dims_fracas    = [d for d, s in zip(DIMENSOES, medias_dims) if 50 <= s < 65]
    dims_solidas   = [d for d, s in zip(DIMENSOES, medias_dims) if s >= 75]
    n_alertas      = sum(len(v) for v in alertas.values())

    if media_geral >= 75 and not dims_criticas and not dims_fracas:
        veredicto = "✅ APROVADO — Sólido com reservas menores"
    elif media_geral >= 65 and not dims_criticas:
        veredicto = "🟡 APROVADO COM RESERVAS — Requer atenção nas dimensões fracas"
    elif media_geral >= 55:
        veredicto = "🟠 APROVAÇÃO CONDICIONAL — Revisão significativa necessária"
    else:
        veredicto = "🔴 NÃO APROVADO — Revisão fundamental necessária"

    linhas.append(f"\nMédia geral: {media_geral:.1f} / 100")
    linhas.append(f"Dimensões sólidas (≥75): {', '.join(dims_solidas) or 'nenhuma'}")
    linhas.append(f"Dimensões fracas (50-65): {', '.join(dims_fracas) or 'nenhuma'}")
    linhas.append(f"Dimensões críticas (<50): {', '.join(dims_criticas) or 'nenhuma'}")
    linhas.append(f"Alertas de qualidade: {n_alertas}")
    linhas.append(f"\n{veredicto}\n")

    # Notas metodológicas
    linhas.append("-"*80)
    linhas.append("NOTAS METODOLÓGICAS")
    linhas.append("-"*40)
    linhas.append("1. Avaliadores são LLMs com viés base para moderada positividade.")
    linhas.append("2. Desvio alto (>30pp) numa dimensão = incerteza real, não erro.")
    linhas.append("3. Alertas de sycophancy sinalizam, não invalidam, o resultado.")
    linhas.append("4. Críticas da Ronda 0 foram geradas por modelos distintos dos avaliadores.")
    linhas.append("5. Este processo é mais rigoroso que votação simples mas não substitui")
    linhas.append("   avaliação por especialistas humanos em cada domínio.")
    linhas.append("-"*80)

    escrever(ficheiro, "\n".join(linhas))
    return media_geral, veredicto


# ══════════════════════════════════════════════════════════════════════════════
# EXECUÇÃO PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def executar():
    print("\n" + "█"*80)
    print("  CONSENSO RIGOROSO 2063 — 20 IAs — AVALIAÇÃO POR RUBRICA")
    print(f"  Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("█"*80)

    # Estima custo
    print("\n💰 CUSTO ESTIMADO:")
    print("   R0 — 4 Advogados do Diabo:   ~$0.60")
    print("   R1 — 20 Avaliações iniciais: ~$2.00")
    print("   R2 — 4 Deliberações grupo:   ~$0.40")
    print("   R3 — 20 Revisões finais:     ~$1.60")
    print("   TOTAL ESTIMADO:              ~$4.60 - $6.00")
    print("   (Com saldo de $35: margem ampla)\n")

    if input("Continuar? (s/n): ").lower() not in ["s", "sim"]:
        print("Cancelado.")
        return

    contexto, total_chars = carregar_contexto()
    if total_chars < 5000:
        print("\n❌ Documentos insuficientes. Verifica a PASTA_PROJETO.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ficheiro_txt  = os.path.join(PASTA_PROJETO, f"CONSENSO_RIGOROSO_{timestamp}.txt")
    ficheiro_json = os.path.join(PASTA_PROJETO, f"CONSENSO_RIGOROSO_{timestamp}.json")

    # Cabeçalho
    escrever(ficheiro_txt, f"CONSENSO RIGOROSO 2063 — {datetime.now()}\n")
    escrever(ficheiro_txt, f"Documentos: {[d for d, _ in DOCUMENTOS]}\n\n")

    # ── RONDA 0 ────────────────────────────────────────────────────────────────
    print("\n" + "─"*60)
    print("RONDA 0: ADVOGADOS DO DIABO (críticas independentes)")
    print("─"*60)

    criticas_todas = []
    for i, adv_id in enumerate(ADVOGADOS, 1):
        critica = ronda0_advogado(contexto, adv_id, i)
        criticas_todas.append(critica)
        time.sleep(2)

    criticas_combinadas = "\n\n".join(
        [f"=== CRÍTICO {i+1} ({ADVOGADOS[i].split('/')[-1]}) ===\n{c}"
         for i, c in enumerate(criticas_todas)]
    )
    escrever(ficheiro_txt, "\n" + "="*60 + "\nRONDA 0 — CRÍTICAS INDEPENDENTES\n" + "="*60 + "\n")
    escrever(ficheiro_txt, criticas_combinadas + "\n")
    print(f"\n   ✅ {len(criticas_todas)} conjuntos de críticas gerados e guardados")

    # ── RONDA 1 ────────────────────────────────────────────────────────────────
    print("\n" + "─"*60)
    print("RONDA 1: AVALIAÇÃO INDIVIDUAL POR RUBRICA (voto cego)")
    print("─"*60)

    dados_r1 = {}
    escrever(ficheiro_txt, "\n" + "="*60 + "\nRONDA 1 — AVALIAÇÕES INDIVIDUAIS\n" + "="*60 + "\n")

    for idx, (nome, modelo_id) in enumerate(MODELOS_20.items(), 1):
        texto = ronda1_avaliacao(nome, modelo_id, contexto, criticas_combinadas, idx, 20)
        scores = extrair_scores(texto)
        m_fraco = re.search(r"PONTO_MAIS_FRACO\s*:\s*(.+)", texto, re.IGNORECASE)
        m_forte = re.search(r"PONTO_MAIS_FORTE\s*:\s*(.+)", texto, re.IGNORECASE)

        dados_r1[nome] = {
            "texto":  texto,
            "scores": scores,
            "media":  media_valida(scores),
            "fraco":  m_fraco.group(1).strip() if m_fraco else "não extraído",
            "forte":  m_forte.group(1).strip() if m_forte else "não extraído",
        }

        med = dados_r1[nome]["media"]
        print(f"      Scores: {scores} → Média: {med}")
        time.sleep(1)

        escrever(ficheiro_txt,
                 f"\n{'─'*60}\nR1 — {nome}\nScores: {scores} | Média: {med}\n{'─'*60}\n{texto}\n")

    # ── RONDA 2 ────────────────────────────────────────────────────────────────
    print("\n" + "─"*60)
    print("RONDA 2: DELIBERAÇÃO POR GRUPO (foco nas divergências)")
    print("─"*60)

    deliberacoes = {}
    escrever(ficheiro_txt, "\n" + "="*60 + "\nRONDA 2 — DELIBERAÇÕES DE GRUPO\n" + "="*60 + "\n")

    for grupo, membros in GRUPOS.items():
        deliber = ronda2_deliberacao(grupo, membros, dados_r1, contexto, SINTETIZADORES[grupo])
        deliberacoes[grupo] = deliber
        time.sleep(2)
        escrever(ficheiro_txt, f"\n{'═'*60}\nR2 — {grupo}\n{'═'*60}\n{deliber}\n")

    # ── RONDA 3 ────────────────────────────────────────────────────────────────
    print("\n" + "─"*60)
    print("RONDA 3: REVISÃO FINAL (após deliberação)")
    print("─"*60)

    dados_r3    = {}
    alertas     = defaultdict(list)
    reservas    = []
    membro_grupo = {m: g for g, ms in GRUPOS.items() for m in ms}

    escrever(ficheiro_txt, "\n" + "="*60 + "\nRONDA 3 — REVISÕES FINAIS\n" + "="*60 + "\n")

    for idx, (nome, modelo_id) in enumerate(MODELOS_20.items(), 1):
        grupo  = membro_grupo.get(nome, list(GRUPOS.keys())[0])
        deliber = deliberacoes.get(grupo, "")

        texto  = ronda3_revisao(nome, modelo_id, dados_r1[nome]["texto"], deliber, idx, 20)
        scores = extrair_scores(texto)

        m_reserva = re.search(r"RESERVA_FINAL\s*:\s*(.+)", texto, re.IGNORECASE)
        if m_reserva:
            reservas.append(f"[{nome}] {m_reserva.group(1).strip()}")

        dados_r3[nome] = {
            "texto":  texto,
            "scores": scores,
            "media":  media_valida(scores),
        }

        als = sinalizar_anomalias(dados_r1[nome]["scores"], scores, nome)
        if als:
            alertas[nome].extend(als)

        med_old = dados_r1[nome]["media"]
        med_new = dados_r3[nome]["media"]
        if med_old and med_new:
            delta = round(med_new - med_old, 1)
            tag   = f"({delta:+.1f}pp)" if abs(delta) >= 2 else "(estável)"
            print(f"      Média: {med_old} → {med_new} {tag}")
        time.sleep(1)

        escrever(ficheiro_txt,
                 f"\n{'█'*60}\nR3 — {nome}\nScores: {scores} | Média: {med_new}\n")
        if als:
            escrever(ficheiro_txt, "\n".join(als) + "\n")
        escrever(ficheiro_txt, f"{'█'*60}\n{texto}\n")

    # ── RELATÓRIO FINAL ────────────────────────────────────────────────────────
    media_geral, veredicto = gerar_relatorio_final(
        ficheiro_txt,
        {n: dados_r1[n] for n in MODELOS_20},
        {n: dados_r3.get(n, {"scores": {}, "media": None}) for n in MODELOS_20},
        dict(alertas),
        reservas,
    )

    # Guarda JSON completo para análise posterior
    with open(ficheiro_json, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp":   timestamp,
            "documentos":  [d for d, _ in DOCUMENTOS],
            "scores_r1":   {n: dados_r1[n]["scores"]  for n in MODELOS_20},
            "scores_r3":   {n: dados_r3.get(n, {}).get("scores", {}) for n in MODELOS_20},
            "medias_r1":   {n: dados_r1[n]["media"]   for n in MODELOS_20},
            "medias_r3":   {n: dados_r3.get(n, {}).get("media") for n in MODELOS_20},
            "alertas":     dict(alertas),
            "reservas":    reservas,
            "media_geral": media_geral,
            "veredicto":   veredicto,
        }, f, indent=2, ensure_ascii=False)

    print("\n" + "█"*80)
    print(f"  ✅ CONCLUÍDO")
    print(f"  📄 Relatório: {ficheiro_txt}")
    print(f"  📊 Dados JSON: {ficheiro_json}")
    print(f"  📈 Média geral final: {media_geral:.1f}/100")
    print(f"  🏆 {veredicto}")
    print("█"*80)


if __name__ == "__main__":
    executar()
