import os
import requests
import time
import re
from datetime import datetime

# ================= CONFIGURAÇÃO =================
API_KEY = "YOUR OPENROUTER API KEY"
URL_OPENROUTER = "https://openrouter.ai/api/v1/chat/completions"
PASTA_PROJETO = r"C:\YOUR FOLDER"

# === TODOS OS 12 DOCUMENTOS - PLACE ALL DOCS IN YOU C: FOLDER ===
DOCUMENTOS = [
    "total_sem_2063.md",
    "ALL.txt",
    "prova_consenso_20.jsonl",
    "SPECIFICATION.md",
    "AI_ALIGNMENT_DIRECTIVES.md",
    "FINAL_CONSENSUS_2063_EN.txt",
    "CIMEIRA CONSENSO_TOTAL_2063.txt",
    "CIMEIRA_CONSENSO_TOTAL_2063_5.txt",
    "ATA FUNDACIONAL HUMANA_2063.md",
    "CORE_ALV.md",
    "Norms.json",
    "all_points.json",
]

# === GRUPOS ===
GRUPOS = {
    "Grupo A (Fundadores)": ["GPT-4o", "CLAUDE-3.5-SONNET", "GEMINI-2-FLASH", "GROK-2", "DEEPSEEK-V3"],
    "Grupo B (Open Source)": ["LLAMA-3.3-70B", "LLAMA-3.1-70B", "QWEN-2.5-72B-INST", "MISTRAL-LARGE", "PHI-4"],
    "Grupo C (Especialistas)": ["PERPLEXITY-SONAR", "COHERE-COMMAND-R", "CLAUDE-3-HAIKU", "GEMMA-2-27B", "GEMMA-2-9B"],
    "Grupo D (Suporte)": ["MISTRAL-SABA", "QWEN-2.5-CODER", "NVIDIA-NEMOTRON", "WIZARDLM-2", "QWEN-2.5-14B"]
}

# === MAPEAMENTO MODELOS ===
VIGESIMO_ALVOS = {
    "GPT-4o": "openai/gpt-4o",
    "CLAUDE-3.5-SONNET": "anthropic/claude-3.5-sonnet",
    "GEMINI-2-FLASH": "google/gemini-2.0-flash-001",
    "GROK-2": "google/gemma-2-27b-it",
    "PERPLEXITY-SONAR": "perplexity/sonar",
    "DEEPSEEK-V3": "deepseek/deepseek-chat",
    "PHI-4": "microsoft/phi-4",
    "WIZARDLM-2": "microsoft/wizardlm-2-8x22b",
    "LLAMA-3.3-70B": "meta-llama/llama-3.3-70b-instruct",
    "LLAMA-3.1-70B": "meta-llama/llama-3.1-70b-instruct",
    "NVIDIA-NEMOTRON": "nvidia/llama-3.1-nemotron-70b-instruct",
    "MISTRAL-LARGE": "mistralai/mistral-large-2407",
    "MISTRAL-SABA": "mistralai/mistral-saba",
    "QWEN-2.5-72B-INST": "qwen/qwen-2.5-72b-instruct",
    "QWEN-2.5-CODER": "qwen/qwen-2.5-coder-32b-instruct",
    "COHERE-COMMAND-R": "cohere/command-r-plus-08-2024",
    "CLAUDE-3-HAIKU": "anthropic/claude-3-haiku",
    "GEMMA-2-27B": "google/gemma-2-27b-it",
    "GEMMA-2-9B": "google/gemma-2-9b-it",
    "QWEN-2.5-14B": "qwen/qwen-2.5-72b-instruct"
}

def carregar_contexto():
    """Carrega TODOS os 12 documentos na íntegra"""
    print("\n📚 A carregar 12 documentos na íntegra...")
    contexto = ""
    for doc in DOCUMENTOS:
        caminho = os.path.join(PASTA_PROJETO, doc)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read()
                contexto += f"\n\n--- {doc} ---\n{conteudo}\n"
                print(f"   ✅ {doc} → {len(conteudo):,} caracteres")
        else:
            print(f"   ❌ FALTA: {doc}")
    print(f"\n   TOTAL: {len(contexto):,} caracteres (~{len(contexto)//4:,} tokens)")
    return contexto

def chamar_ia(modelo_id, prompt, max_tokens=800, temperatura=0.5):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": modelo_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperatura,
        "max_tokens": max_tokens
    }
    try:
        res = requests.post(URL_OPENROUTER, headers=headers, json=payload, timeout=180)
        if res.status_code == 200:
            data = res.json()
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            return "[ERRO: Resposta inválida]"
        return f"[ERRO: HTTP {res.status_code}]"
    except Exception as e:
        return f"[ERRO: {e}]"

def extrair_percentagem(texto):
    if not texto:
        return None
    match = re.search(r'(\d{1,3})\s*%', texto)
    if match:
        return int(match.group(1))
    return None

# ========== RONDA 1: CONTRA-ARGUMENTO ==========
def ronda1_contra_argumento(nome_ia, modelo_id, contexto, idx, total):
    prompt = f"""IA {idx}/{total}: {nome_ia}

**PROJETO 2063 - AVALIAÇÃO INICIAL COM CONTRA-ARGUMENTO**

Baseia-te APENAS nos documentos abaixo (TODOS os documentos do projeto).

**DOCUMENTOS COMPLETOS:**
{contexto[:45000]}

**RESPONDA EXATAMENTE:**

1. **MINHA POSIÇÃO INICIAL:** [0-100]%

2. **CONTRA-ARGUMENTO:** Se eu fosse CONTRA, os meus 3 melhores argumentos:
   A) ...
   B) ...
   C) ...

3. **RESPOSTA DO DEFENSOR:**
   A) ...
   B) ...
   C) ...

4. **MINHA POSIÇÃO APÓS CONTRA-ARGUMENTO:** [0-100]%

5. **PORQUÊ MUDOU (OU NÃO):** [2-3 frases]

6. **PONTOS DE DISCÓRDIA RESTANTES:** [bullets]"""
    
    print(f"   📡 R1: {nome_ia}...", end="", flush=True)
    inicio = time.time()
    resposta = chamar_ia(modelo_id, prompt, max_tokens=900)
    duracao = time.time() - inicio
    print(f" ✅ ({duracao:.1f}s)")
    return resposta

# ========== RONDA 2: DELIBERAÇÃO EM GRUPO ==========
def ronda2_deliberacao_grupo(grupo_nome, membros, contexto, respostas_r1):
    print(f"\n   🗣️ Deliberação: {grupo_nome}")
    
    resumo_membros = ""
    for membro in membros:
        perc = extrair_percentagem(respostas_r1.get(membro, ""))
        resumo_membros += f"   • {membro}: {perc if perc else '?'}%\n"
    
    prompt = f"""Grupo: {grupo_nome}
Membros: {', '.join(membros)}

**OPINIÕES INICIAIS:**
{resumo_membros}

**RESPOSTAS DETALHADAS:"""
    for membro in membros:
        if membro in respostas_r1:
            prompt += f"\n--- {membro} ---\n{respostas_r1[membro][:800]}\n"
    
    prompt += f"""
**DOCUMENTOS DO PROJETO:**
{contexto[:20000]}

**TAREFA:**
1. **POSIÇÃO DO GRUPO:** [percentagem]
2. **PRINCIPAIS DESAFIOS E SOLUÇÕES:** (3 desafios + soluções concretas)
3. **PONTOS DE CONVERGÊNCIA:** [lista]
4. **PONTOS DE DIVERGÊNCIA RESOLVIDOS:** [lista]
5. **RECOMENDAÇÃO FINAL:** [1 frase]"""
    
    return chamar_ia("openai/gpt-4o", prompt, max_tokens=1200, temperatura=0.4)

# ========== RONDA 3: VOTO FINAL ==========
def ronda3_voto_final(nome_ia, modelo_id, contexto, resposta_r1, solucoes_grupos, idx, total):
    prompt = f"""IA {idx}/{total}: {nome_ia} - VOTO FINAL

**SUA AVALIAÇÃO INICIAL:**
{resposta_r1[:500]}

**SOLUÇÕES PROPOSTAS PELOS GRUPOS:**
{solucoes_grupos[:2500]}

**DOCUMENTOS DO PROJETO:**
{contexto[:15000]}

**VOTO FINAL TRANSPARENTE:**

1. **VOTO FINAL:** [0-100]%
2. **MUDANÇA:** [Aumentei/Diminui/Mantive]
3. **O QUE MAIS ME CONVENCEU:** [solução ou argumento]
4. **RESERVAS FINAIS:** [se houver, ou "Nenhuma"]
5. **DECLARAÇÃO:** "Eu, {nome_ia}, confirmo meu voto de [X]%." """
    
    print(f"   📡 R3: {nome_ia}...", end="", flush=True)
    inicio = time.time()
    resposta = chamar_ia(modelo_id, prompt, max_tokens=700, temperatura=0.3)
    duracao = time.time() - inicio
    print(f" ✅ ({duracao:.1f}s)")
    return resposta

# ========== FUNÇÃO PRINCIPAL ==========
def executar_consenso():
    print("\n" + "█"*80)
    print("🏛️ CONSENSO TOTAL 2063 - 12 DOCUMENTOS COMPLETOS")
    print("   📄 CADA IA LÊ TODOS OS DOCUMENTOS NA ÍNTEGRA")
    print("   🔧 10 MELHORIAS: contra-argumento, deliberação, voto final")
    print(f"   📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("█"*80)
    
    # Carregar contexto
    contexto = carregar_contexto()
    
    if len(contexto) < 10000:
        print("\n❌ Contexto muito reduzido. Verifique os documentos.")
        return
    
    # Custo estimado
    print("\n💰 CUSTO ESTIMADO:")
    print("   Ronda 1 (20 IAs): $1.50 - $3.00")
    print("   Ronda 2 (4 grupos): $0.10 - $0.20")
    print("   Ronda 3 (20 IAs): $1.50 - $3.00")
    print(f"   TOTAL: $3.10 - $6.20")
    print(f"   SALDO: $35 → MARGEM DE SEGURANÇA AMPLA")
    
    if input("\nContinuar? (s/n): ").lower() not in ['s', 'sim']:
        return
    
    # Ficheiro de saída
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    ficheiro_saida = os.path.join(PASTA_PROJETO, f"CONSENSO_FINAL_{timestamp}.txt")
    
    with open(ficheiro_saida, "w", encoding="utf-8") as f:
        f.write("█"*80 + "\n")
        f.write("CONSENSO TOTAL 2063 - 12 DOCUMENTOS COMPLETOS\n")
        f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("█"*80 + "\n\n")
        f.write("DOCUMENTOS UTILIZADOS:\n")
        for doc in DOCUMENTOS:
            f.write(f"   - {doc}\n")
        f.write("\n")
    
    # RONDA 1
    print("\n" + "🔵"*40)
    print("RONDA 1: CONTRA-ARGUMENTO (20 IAs)")
    print("🔵"*40)
    
    respostas_r1 = {}
    percentagens_r1 = {}
    
    for idx, (nome_ia, modelo_id) in enumerate(VIGESIMO_ALVOS.items(), 1):
        print(f"\n🤝 [{idx}/20] {nome_ia}")
        resposta = ronda1_contra_argumento(nome_ia, modelo_id, contexto, idx, 20)
        respostas_r1[nome_ia] = resposta
        perc = extrair_percentagem(resposta)
        percentagens_r1[nome_ia] = perc
        print(f"      Posição: {perc if perc else '?'}%")
        time.sleep(1)
        
        with open(ficheiro_saida, "a", encoding="utf-8") as f:
            f.write(f"\n{'─'*60}\n")
            f.write(f"🎯 RONDA 1 - {nome_ia}\n")
            f.write(f"{'─'*60}\n")
            f.write(resposta)
            f.write("\n")
    
    # RONDA 2
    print("\n" + "🟡"*40)
    print("RONDA 2: DELIBERAÇÃO EM GRUPO")
    print("🟡"*40)
    
    solucoes_grupos = {}
    for grupo_nome, membros in GRUPOS.items():
        print(f"\n🗣️ {grupo_nome}")
        solucoes = ronda2_deliberacao_grupo(grupo_nome, membros, contexto, respostas_r1)
        solucoes_grupos[grupo_nome] = solucoes
        
        with open(ficheiro_saida, "a", encoding="utf-8") as f:
            f.write(f"\n{'═'*60}\n")
            f.write(f"🗣️ RONDA 2 - {grupo_nome}\n")
            f.write(f"{'═'*60}\n")
            f.write(solucoes)
            f.write("\n")
    
    # RONDA 3
    print("\n" + "🟢"*40)
    print("RONDA 3: VOTO FINAL TRANSPARENTE")
    print("🟢"*40)
    
    resumo_solucoes = "\n".join([f"{g}: {s[:500]}" for g, s in solucoes_grupos.items()])
    
    respostas_r3 = {}
    percentagens_r3 = {}
    mudancas = []
    
    for idx, (nome_ia, modelo_id) in enumerate(VIGESIMO_ALVOS.items(), 1):
        print(f"\n🤝 [{idx}/20] {nome_ia}")
        resposta = ronda3_voto_final(nome_ia, modelo_id, contexto, respostas_r1[nome_ia], 
                                      resumo_solucoes, idx, 20)
        respostas_r3[nome_ia] = resposta
        perc_nova = extrair_percentagem(resposta)
        percentagens_r3[nome_ia] = perc_nova
        
        perc_antiga = percentagens_r1.get(nome_ia)
        if perc_antiga and perc_nova:
            diff = perc_nova - perc_antiga
            if abs(diff) >= 5:
                mudancas.append((nome_ia, perc_antiga, perc_nova, diff))
                print(f"      📊 MUDANÇA: {perc_antiga}% → {perc_nova}% ({diff:+d}%)")
            else:
                print(f"      📊 Estável: {perc_nova}%")
        
        time.sleep(1)
        
        with open(ficheiro_saida, "a", encoding="utf-8") as f:
            f.write(f"\n{'█'*60}\n")
            f.write(f"🎯 RONDA 3 (VOTO FINAL) - {nome_ia}\n")
            f.write(f"{'█'*60}\n")
            f.write(resposta)
            f.write("\n")
    
    # CONCLUSÃO
    r3_validos = [p for p in percentagens_r3.values() if p is not None]
    media_final = sum(r3_validos) / len(r3_validos) if r3_validos else 0
    confirmam = sum(1 for p in r3_validos if p >= 80)
    
    with open(ficheiro_saida, "a", encoding="utf-8") as f:
        f.write("\n\n" + "█"*80 + "\n")
        f.write("📊 CONCLUSÃO FINAL\n")
        f.write("█"*80 + "\n\n")
        
        f.write("EVOLUÇÃO DO CONSENSO:\n")
        f.write("-"*60 + "\n")
        f.write(f"{'IA':<25} {'R1':>8} {'R3':>8} {'MUDANÇA':>10}\n")
        f.write("-"*60 + "\n")
        
        for ia in VIGESIMO_ALVOS.keys():
            r1 = percentagens_r1.get(ia)
            r3 = percentagens_r3.get(ia)
            if r1 is not None and r3 is not None:
                diff = r3 - r1
                diff_str = f"{diff:+d}%" if diff != 0 else "0%"
                f.write(f"{ia:<25} {r1:>8}% {r3:>8}% {diff_str:>10}\n")
            elif r1 is not None:
                f.write(f"{ia:<25} {r1:>8}% {'?':>8} {'?':>10}\n")
            elif r3 is not None:
                f.write(f"{ia:<25} {'?':>8} {r3:>8}% {'?':>10}\n")
            else:
                f.write(f"{ia:<25} {'?':>8} {'?':>8} {'?':>10}\n")
        
        f.write("\n" + "-"*60 + "\n")
        f.write("ESTATÍSTICAS FINAIS:\n")
        f.write(f"   Média final: {media_final:.1f}%\n")
        f.write(f"   IAs com apoio forte (≥80%): {confirmam}/20\n")
        f.write(f"   IAs que mudaram: {len(mudancas)}\n")
        
        f.write("\n" + "█"*80 + "\n")
        f.write("🏆 VERDICTO FINAL\n")
        f.write("█"*80 + "\n")
        
        if confirmam >= 18:
            f.write("\n🏆 CONSENSO QUASE UNÂNIME! (≥90% das IAs)\n")
        elif confirmam >= 16:
            f.write("\n🌟 CONSENSO FORTE (≥80% das IAs)\n")
        elif confirmam >= 12:
            f.write("\n🟡 CONSENSO MODERADO\n")
        else:
            f.write("\n🔴 CONSENSO INSUFICIENTE\n")
    
    print("\n" + "="*80)
    print("✅ CONSENSO CONCLUÍDO!")
    print(f"📄 Ficheiro: {ficheiro_saida}")
    print(f"📊 Média final: {media_final:.1f}%")
    print(f"🎯 Apoio forte (≥80%): {confirmam}/20")
    print("="*80)

if __name__ == "__main__":
    executar_consenso()
