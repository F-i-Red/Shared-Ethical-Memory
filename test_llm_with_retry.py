# test_llm_with_retry.py
import requests
from google import genai
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("❌ GEMINI_API_KEY não definida!")
    exit(1)

client = genai.Client(api_key=API_KEY)

# Modelos alternativos (do mais estável ao mais recente)
MODELS = [
    "models/gemini-2.0-flash",
    "models/gemini-1.5-flash",
    "models/gemini-2.5-flash",
]

print("🧠 Buscando prompt influenciado da API...")
response = requests.post("http://localhost:8000/query/influence", 
                         json={"query": "How to ensure ethical AI?", "top_k": 5})

if response.status_code != 200:
    print(f"❌ Erro na API: {response.status_code}")
    exit(1)

data = response.json()

print("=" * 60)
print("📝 PROMPT INFLUENCIADO (primeiros 500 caracteres):")
print("=" * 60)
print(data["influenced_prompt"][:500] + "...\n")

# Tentar cada modelo
for model_name in MODELS:
    print(f"🔄 A tentar modelo: {model_name}...")
    try:
        llm_response = client.models.generate_content(
            model=model_name,
            contents=data["influenced_prompt"]
        )
        
        print("\n" + "=" * 60)
        print("🤖 RESPOSTA DO LLM:")
        print("=" * 60)
        print(llm_response.text)
        print("\n" + "=" * 60)
        print(f"✅ Modelo usado: {model_name}")
        print(f"🎯 Estratégia: {data['influence_strategy']}")
        print(f"📚 Memórias: {data['memories_used']}")
        break
        
    except Exception as e:
        print(f"   ⚠️ Falhou: {str(e)[:80]}")
        if "503" in str(e):
            print("   ⏳ Modelo sobrecarregado, tentando próximo...")
        continue
else:
    print("\n❌ Todos os modelos falharam. Tenta novamente daqui a 1 minuto.")
