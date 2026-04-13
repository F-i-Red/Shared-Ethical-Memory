# memory_extractor.py
# Novo ficheiro - extrai memórias éticas automaticamente a partir de texto/conversa

import json
import requests
from typing import Dict, Optional

class MemoryExtractor:
    """
    Usa a tua LLM local (Ollama) para transformar qualquer conversa
    numa memória ética bem estruturada (principle, context, decision...).
    """

    def __init__(self,
                 llm_model: str = "mistral",
                 llm_endpoint: str = "http://localhost:11434/api/chat"):

        self.llm_model = llm_model
        self.llm_endpoint = llm_endpoint

    def extract_ethical_memory(self, conversation_text: str) -> Optional[Dict]:
        """
        Recebe um texto de conversa e devolve um dicionário estruturado.
        """
        prompt = f"""
Tu és um extrator de memórias éticas preciso e rigoroso.

Analisa a conversa abaixo e extrai **uma** memória ética importante.

Responde **apenas** com um JSON válido no seguinte formato exato:

{{
  "principle": "nome curto do princípio ético envolvido",
  "context": "descrição breve do que aconteceu ou foi discutido",
  "decision": "o que foi decidido ou a posição tomada",
  "justification": "porquê essa decisão (razão ética)",
  "confidence": 0.XX
}}

Conversa para analisar:
{conversation_text}

JSON:
"""

        try:
            response = requests.post(
                self.llm_endpoint,
                json={
                    "model": self.llm_model,
                    "messages": [
                        {"role": "system", "content": "Responde sempre apenas com JSON válido, sem texto extra."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "temperature": 0.3
                },
                timeout=90
            )
            response.raise_for_status()
            data = response.json()

            content = data.get("message", {}).get("content", "") or \
                      data.get("choices", [{}])[0].get("message", {}).get("content", "")

            # Limpa e carrega o JSON
            content = content.strip()
            if content.startswith("```json"):
                content = content.split("```json")[1].split("```")[0].strip()
            elif content.startswith("```"):
                content = content.split("```")[1].strip()

            ethical_mem = json.loads(content)

            # Garante que tem os campos obrigatórios
            required = ["principle", "context", "decision", "justification", "confidence"]
            for field in required:
                if field not in ethical_mem:
                    ethical_mem[field] = "" if field != "confidence" else 0.5

            return ethical_mem

        except Exception as e:
            print(f"[MemoryExtractor] Erro ao extrair memória: {e}")
            return None
