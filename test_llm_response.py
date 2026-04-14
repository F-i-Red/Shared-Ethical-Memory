# test_llm_response.py - Versão com google.genai (nova biblioteca)
import requests
from google import genai
import os

# Configurar a chave API (vai buscar à variável de ambiente)
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("❌ GEMINI_API_KEY não definida!")
    print("   Corre primeiro: set GEMINI_API_KEY=AIzaSyDXyzvCdll6XqLsnj0eoY9d4Ft-QSavJSU")
    exit(1)

# Inicializar cliente Gemini (nova biblioteca)
client = genai.Client(api_key=API_KEY)

print("🧠 Buscando prompt influenciado da API...\n")

# Buscar o prompt influenciado da API
response = requests.post("http://localhost:8000/query/influence", 
                         json={"query": "How to ensure ethical AI?", "top_k": 5})

if response.status_code != 200:
    print(f"❌ Erro na API: {response.status_code}")
    print(response.text)
    exit(1)

data = response.json()

print("=" * 60)
print("📝 PROMPT INFLUENCIADO (enviado ao Gemini):")
print("=" * 60)
print(data["influenced_prompt"][:500] + "...\n")

# Enviar o prompt influenciado para o Gemini (nova biblioteca)
print("🧠 A enviar ao Gemini para gerar resposta...\n")

try:
    llm_response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=data["influenced_prompt"]
    )
    
    print("=" * 60)
    print("🤖 RESPOSTA DO LLM (influenciada pelas memórias éticas):")
    print("=" * 60)
    print(llm_response.text)
    print("\n" + "=" * 60)
    print(f"✅ Estratégia usada: {data['influence_strategy']}")
    print(f"📚 Memórias consideradas: {data['memories_used']}")
    
except Exception as e:
    print(f"❌ Erro ao chamar Gemini: {e}")
