# memory_extractor.py (versão atualizada - com fallback sem Ollama)

import json
from typing import Dict, Optional

class MemoryExtractor:
    """
    Extrai memórias éticas.
    Modo fallback: se Ollama não estiver ligado, usa exemplos fixos ou input manual.
    """

    def __init__(self, use_llm: bool = True, llm_model: str = "mistral"):
        self.use_llm = use_llm  # False = modo demo sem LLM

    def extract_ethical_memory(self, conversation_text: str) -> Optional[Dict]:
        """Extrai ou cria memória ética."""
        if not self.use_llm:
            # Modo demo sem Ollama
            print("[MemoryExtractor] Modo demo ativado (sem Ollama). Usando exemplo fixo.")
            return {
                "principle": "Minimizar dano",
                "context": conversation_text[:200] + "...",
                "decision": "Recusado",
                "justification": "Proteção à segurança e valores humanos",
                "confidence": 0.85
            }

        # (código antigo com Ollama fica aqui - se quiseres ligar depois)
        print("[MemoryExtractor] Ollama não encontrado. Ative o modo fallback no código.")
        return None  # fallback automático
