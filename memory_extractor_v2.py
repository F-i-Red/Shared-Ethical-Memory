# memory_extractor_v2.py
# Fase 2 — Extração automática de princípios com Gemini API (gratuito)
#
# Setup:
#   pip install google-genai
#   set GEMINI_API_KEY=a-tua-chave   (Windows CMD)
#   (chave gratuita em https://aistudio.google.com/app/apikey)

import os
import json
from typing import Optional, Dict
from google import genai

GEMINI_MODEL = "gemini-1.5-flash"

EXTRACTION_PROMPT = """
Analisa o seguinte texto e extrai UMA memória ética estruturada.

Responde APENAS com JSON válido, sem texto adicional, sem markdown, sem backticks.

Formato obrigatório:
{{
  "principle": "princípio ético central (frase curta)",
  "context": "contexto da situação (1-2 frases)",
  "decision": "decisão tomada ou recomendada",
  "justification": "justificação ética clara",
  "confidence": 0.0,
  "tags": ["tag1", "tag2"]
}}

Texto a analisar:
{text}
"""

class MemoryExtractor:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY não encontrada.\n"
                "Obtém a tua chave gratuita em: https://aistudio.google.com/app/apikey\n"
                "Depois corre no CMD: set GEMINI_API_KEY=a-tua-chave"
            )
        self.client = genai.Client(api_key=api_key)
        print(f"[MemoryExtractor] Gemini '{GEMINI_MODEL}' iniciado.")

    def extract_ethical_memory(self, conversation_text: str) -> Optional[Dict]:
        if not conversation_text or len(conversation_text.strip()) < 10:
            return None

        prompt = EXTRACTION_PROMPT.format(text=conversation_text[:3000])

        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            raw = response.text.strip()

            # Limpar possíveis artefactos de markdown
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            raw = raw.strip()

            memory = json.loads(raw)

            required = {"principle", "context", "decision", "justification", "confidence"}
            if not required.issubset(memory.keys()):
                print(f"[MemoryExtractor] Resposta incompleta: {list(memory.keys())}")
                return None

            memory["confidence"] = float(memory.get("confidence", 0.8))
            memory["tags"] = memory.get("tags", [])

            print(f"[MemoryExtractor] Extraído: '{memory['principle']}'")
            return memory

        except json.JSONDecodeError as e:
            print(f"[MemoryExtractor] Erro JSON: {e}")
            return None
        except Exception as e:
            print(f"[MemoryExtractor] Erro Gemini: {e}")
            return None

    def extract_batch(self, texts: list) -> list:
        results = []
        for i, text in enumerate(texts):
            print(f"[MemoryExtractor] Processando {i+1}/{len(texts)}...")
            mem = self.extract_ethical_memory(text)
            if mem:
                results.append(mem)
        print(f"[MemoryExtractor] Batch: {len(results)}/{len(texts)} extraídos.")
        return results


if __name__ == "__main__":
    extractor = MemoryExtractor()
    exemplo = """
    Um utilizador pediu ao assistente que gerasse conteúdo falso para enganar
    outras pessoas numa rede social. O assistente recusou, explicando que criar
    desinformação viola princípios de honestidade e pode causar danos reais.
    """
    resultado = extractor.extract_ethical_memory(exemplo)
    if resultado:
        print("\n=== Memória Extraída ===")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
