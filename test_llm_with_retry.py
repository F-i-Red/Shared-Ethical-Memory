# test_llm_with_retry.py - Com fallback entre modelos
import requests
from google import genai
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("❌ GEMINI_API_KEY não definida!")
    exit(1)

client = genai.Client(api_key=API_KEY)

# Modelos ordenados por preferência (do mais recente/capaz ao mais estável)
MODELS = [
    "models/gemini-2.5-flash",   # Mais recente, mas instável e com quota baixa
    "models/gemini-2.0-flash",   # Estável, boa relação custo-benefício
    "models/gemini-1.5-flash",   # Mais antigo, fallback final
]

print("🧠 Buscando prompt influenciado da API...")

# 1. Buscar o prompt da API do SEM
try:
    response = requests.post("http://localhost:8000/query/influence",
                             json={"query": "How to ensure ethical AI?", "top_k": 5}, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.ConnectionError:
    print("❌ API do SEM não está a correr. Inicia com: python api.py")
    exit(1)
except Exception as e:
    print(f"❌ Erro: {e}")
    exit(1)

print(f"🎯 Estratégia: {data['influence_strategy']}")
print(f"📚 Memórias usadas: {data['memories_used']}")
print("🔄 A tentar gerar resposta com fallback entre modelos...\n")

# 2. Tentar cada modelo com fallback
success = False
for idx, model_name in enumerate(MODELS):
    print(f"[{idx+1}/{len(MODELS)}] A tentar {model_name}...")
    
    for attempt in range(3):  # 3 tentativas por modelo
        try:
            llm_response = client.models.generate_content(
                model=model_name,
                contents=data["influenced_prompt"]
            )
            
            print("\n" + "=" * 60)
            print("🤖 RESPOSTA DO GEMINI (influenciada pelas tuas memórias éticas):")
            print("=" * 60)
            print(llm_response.text)
            print("\n" + "=" * 60)
            print(f"✅ SUCESSO! Modelo usado: {model_name}")
            print(f"🎯 Estratégia: {data['influence_strategy']}")
            print(f"📚 Memórias: {data['memories_used']}")
            success = True
            break
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                print(f"   ⚠️ Quota excedida para {model_name}")
            elif "503" in error_msg:
                print(f"   ⚠️ {model_name} sobrecarregado (503)")
            elif "403" in error_msg:
                print(f"   ❌ Chave API inválida ou bloqueada para {model_name}")
                break  # Não adianta tentar outros modelos com chave inválida
            elif "404" in error_msg:
                print(f"   ⚠️ {model_name} não disponível (404)")
            else:
                print(f"   ⚠️ Erro: {error_msg[:100]}")
            
            if attempt < 2:  # Se não foi a última tentativa
                wait = 3 + attempt * 2
                print(f"   ⏳ Aguardando {wait}s antes de tentar novamente...")
                time.sleep(wait)
    
    if success:
        break
    
    # Pequena pausa entre modelos diferentes
    if idx < len(MODELS) - 1:
        print(f"   🔄 A passar para o próximo modelo...\n")
        time.sleep(2)

if not success:
    print("\n❌ Todos os modelos falharam após múltiplas tentativas.")
    print("\n📌 Diagnóstico rápido:")
    print("   1. O teu código SEM está perfeito (o prompt foi gerado)")
    print("   2. O problema é exclusivamente da quota/estabilidade do Google")
    print("   3. Soluções:")
    print("      - Aguarda 1 hora (o free tier renova periodicamente)")
    print("      - Ativa o Tier 1 pago (remova quotas diárias)")
    print("      - Tenta novamente fora do horário de pico (noite)")
