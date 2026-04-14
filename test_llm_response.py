# test_llm_response.py
import requests
import google.generativeai as genai
import os

# Configurar Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Buscar o prompt influenciado da API
response = requests.post("http://localhost:8000/query/influence", 
                         json={"query": "How to ensure ethical AI?", "top_k": 5})
data = response.json()

print("🧠 Enviando prompt ao Gemini...\n")
print("=" * 60)

# Enviar o prompt influenciado para o LLM
llm_response = model.generate_content(data["influenced_prompt"])

print("\n📝 RESPOSTA DO LLM (influenciada pelas memórias éticas):\n")
print(llm_response.text)
print("\n" + "=" * 60)
print(f"✅ Estratégia usada: {data['influence_strategy']}")
print(f"📚 Memórias consideradas: {data['memories_used']}")
