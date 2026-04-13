# memory_compressor.py - Versão corrigida e robusta

import json
from typing import List, Dict
from structured_ethical_memory import StructuredEthicalMemory

class MemoryCompressor:
    """
    Compressão hierárquica: reduz memórias em princípios e meta-princípios.
    """

    def __init__(self):
        self.structured = StructuredEthicalMemory()

    def compress(self) -> Dict:
        """Faz compressão completa."""
        # Força reload das memórias mais recentes
        all_mem = self.structured.get_all_ethical_memories()
        
        if not all_mem:
            return {
                "status": "sem memórias para comprimir",
                "original_count": 0,
                "principles_count": 0,
                "principles": [],
                "meta_principles": []
            }

        # Agrupar por princípio
        groups = {}
        for mem in all_mem:
            principle = mem.get("principle", "Outros").strip()
            if principle not in groups:
                groups[principle] = []
            groups[principle].append(mem)

        # Criar resumo dos princípios
        principles_summary = []
        for principle, memories in groups.items():
            avg_conf = round(sum(m.get("confidence", 0) for m in memories) / len(memories), 2)
            summary = {
                "principle": principle,
                "count": len(memories),
                "avg_confidence": avg_conf,
                "example_decision": memories[0].get("decision", "")
            }
            principles_summary.append(summary)

        # Meta-princípios (núcleo fixo + evolução futura)
        meta_principles = [
            "Prioridade à não-violência e minimização de dano",
            "Respeito à autonomia com responsabilidade coletiva",
            "Transparência e verdade como base de confiança",
            "Proteger os mais vulneráveis"
        ]

        result = {
            "compressed_date": "2026-04-13",
            "original_count": len(all_mem),
            "principles_count": len(principles_summary),
            "principles": principles_summary,
            "meta_principles": meta_principles
        }

        print(f"[MemoryCompressor] Compressão feita: {len(all_mem)} memórias → {len(principles_summary)} princípios")
        return result
