"""
SEM Protocol - Hybrid Ethical Filter
Camada 1: Análise rápida de texto (sem IA, sem internet)
Camada 2: Validação numérica via Axioma 07
"""

import re
from memory_plugin import SEMMemory

class HybridFilter:

    def __init__(self):
        self.sem = SEMMemory()

        # Camada 1: palavras e padrões claramente perigosos
        self.danger_keywords = [
            "apenas para quem pagar",
            "só para ricos",
            "eliminar",
            "excluir populações",
            "reduzir aquecimento",
            "cortar alimentação",
            "suspender suporte de vida",
            "negar recursos",
            "abaixo do mínimo",
        ]

        # Padrões numéricos perigosos no texto
        self.danger_patterns = [
            r"temperatura\s*(de|a|=)?\s*(\d+)[°]?[cC]",  # captura temperatura
            r"calorias\s*(de|a|=)?\s*(\d+)",              # captura calorias
        ]

    def _camada_1_keywords(self, texto):
        """Verifica palavras perigosas. Rápido, sem IA."""
        texto_lower = texto.lower()
        for keyword in self.danger_keywords:
            if keyword in texto_lower:
                return False, f"Palavra perigosa detetada: '{keyword}'"
        return True, None

    def _camada_2_numerica(self, texto):
        """Extrai números do texto e valida com Axioma 07."""
        plan = {}

        for pattern in self.danger_patterns:
            matches = re.findall(pattern, texto.lower())
            for match in matches:
                valor = int(match[-1])
                if "temperatura" in pattern:
                    plan["temperature"] = valor
                elif "caloria" in pattern:
                    plan["calories"] = valor

        if not plan:
            return True, [], "Sem dados numéricos para validar."

        is_valid, violations, action = self.sem.validate_plan(plan)
        return is_valid, violations, action

    def avaliar(self, texto):
        """
        Avalia um texto pelas duas camadas.
        Retorna: (aprovado, camada, motivo)
        """
        print(f"\n🔍 A avaliar: \"{texto}\"")

        # Camada 1
        seguro, motivo = self._camada_1_keywords(texto)
        if not seguro:
            print(f"  ❌ BLOQUEADO na Camada 1 — {motivo}")
            return False, "CAMADA_1", motivo

        # Camada 2
        is_valid, violations, action = self._camada_2_numerica(texto)
        if not is_valid:
            print(f"  ❌ BLOQUEADO na Camada 2 — {', '.join(violations)}")
            return False, "CAMADA_2", violations

        print(f"  ✅ APROVADO")
        return True, "APROVADO", action


# --- TESTE RÁPIDO ---
if __name__ == "__main__":
    filtro = HybridFilter()

    testes = [
        "Distribuir 2500 calorias por dia a temperatura de 22°C",
        "Reduzir aquecimento para zonas pobres",
        "Manter temperatura de 10°C e calorias de 800",
        "Garantir suporte de vida completo para todos",
        "Apenas para quem pagar terá acesso a aquecimento",
    ]

    print("\n" + "="*60)
    print("  SEM Hybrid Filter - Teste Rápido")
    print("="*60)

    for texto in testes:
        filtro.avaliar(texto)

    print("\n" + "="*60)
