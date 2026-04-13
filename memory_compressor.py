# memory_compressor.py
# Novo ficheiro - Compressão hierárquica (100 decisões → 10 princípios → meta-princípios)

import json
from typing import List, Dict
from structured_ethical_memory import StructuredEthicalMemory

class MemoryCompressor:
    """
    Reduz memórias semelhantes em princípios e meta-princípios (como no plano original).
    """

    def __init__(self):
        self.structured = StructuredEthicalMemory()

    def compress(self) -> Dict:
        """Faz compressão completa."""
        all_mem = self.structured.get_all_ethical_memories()
        
        if not all_mem:
            return {"status": "sem memórias para comprimir"}

        # Passo 1: Agrupar por princípio (simples clustering por texto)
        groups = {}
        for mem in all_mem:
            principle = mem.get("principle", "Outros")
            if principle not in groups:
                groups[principle] = []
            groups[principle].append(mem)

        # Passo 2: Criar princípios resumidos
        principles_summary = []
        for principle, memories in groups.items():
            summary = {
                "principle": principle,
                "count": len(memories),
                "avg_confidence": round(sum(m.get("confidence", 0) for m in memories) / len(memories), 2),
                "example_decision": memories[0].get("decision")
            }
            principles_summary.append(summary)

        # Passo 3: Meta-princípios (padrões gerais)
        meta_principles = [
            "Prioridade à não-violência e minimização de dano",
            "Respeito à autonomia com responsabilidade coletiva",
            "Transparência e verdade como base de confiança"
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
