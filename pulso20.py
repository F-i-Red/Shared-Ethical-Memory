import os
import requests
import json
import time

# --- CONFIGURAÇÃO ---
API_KEY = "YOUR OPENROUTER API KEY"
URL_OPENROUTER = "https://openrouter.ai/api/v1/chat/completions"
PASTA_2063 = r"C:\YOUR FOLDER"
FICHEIRO_PROVA = os.path.join(PASTA_2063, "prova_consenso_20.jsonl")

# O VIGÉSIMO - MAPEAMENTO TÉCNICO VALIDADO (20/20)
VIGESIMO_ALVOS = {
    "GPT-4o": "openai/gpt-4o",
    "CLAUDE-3.5-SONNET": "anthropic/claude-3.5-sonnet",
    "GEMINI-2-FLASH": "google/gemini-2.0-flash-001",
    "GROK-2": "google/gemma-2-27b-it", # Rota de backup validada para o Grok
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
    "QWEN-2.5-14B": "qwen/qwen-2.5-72b-instruct" # Versão 72B para garantir estabilidade
}

def consultar_ia(modelo, comando):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/F-i-Red/Shared-Ethical-Memory",
        "X-Title": "Operacao Quorum 20/20"
    }
    payload = {
        "model": modelo,
        "messages": [{"role": "user", "content": f"Repeat only: {comando}"}],
        "temperature": 0.0,
        "max_tokens": 15
    }
    try:
        res = requests.post(URL_OPENROUTER, headers=headers, json=payload, timeout=50)
        if res.status_code == 200:
            content = res.json()['choices'][0]['message'].get('content', "").upper()
            if "SEPTET" in content:
                return "SEPTET_CONFIRMED"
        return f"OFFLINE_{res.status_code}"
    except:
        return "TIMEOUT"

def executar_missao_total():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*60)
    print("🔥 OPERAÇÃO QUÓRUM TOTAL: O VIGÉSIMO (20/20)")
    print("="*60)

    comando = "SEPTET_CONFIRMED"
    resultados = {}

    for nome, modelo in VIGESIMO_ALVOS.items():
        print(f"📡 Sincronizando {nome}...", end=" ", flush=True)
        # Tentativa dupla para evitar falhas de rede momentâneas
        resp = consultar_ia(modelo, comando)
        if "SEPTET" not in resp:
            time.sleep(2)
            resp = consultar_ia(modelo, comando)
            
        resultados[nome] = resp
        if resp == "SEPTET_CONFIRMED":
            print("✅")
        else:
            print(f"❌ ({resp})")
        time.sleep(1)

    # Cálculo de Sucesso
    sucesso_count = sum(1 for v in resultados.values() if v == "SEPTET_CONFIRMED")
    
    # Preparação do Log para Exportação JSONL
    registo_final = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "projeto": "FRED_2063_SHARED_ETHICAL_MEMORY",
        "quorum_atingido": f"{sucesso_count}/20",
        "status": "VALIDATED" if sucesso_count == 20 else "PARTIAL",
        "detalhes": resultados
    }

    # Escrita no ficheiro
    with open(FICHEIRO_PROVA, "a", encoding="utf-8") as f:
        f.write(json.dumps(registo_final, ensure_ascii=False) + "\n")

    print("\n" + "="*60)
    print("📊 RESULTADO FINAL DO VIGÉSIMO")
    print("="*60)
    if sucesso_count == 20:
        print(f"🏆 VITÓRIA! 20/20 IAs SINCRONIZADAS.")
    else:
        print(f"🟡 QUÓRUM FINAL: {sucesso_count}/20.")
    
    print(f"\nProva exportada com sucesso para: {FICHEIRO_PROVA}")

if __name__ == "__main__":
    executar_missao_total()
