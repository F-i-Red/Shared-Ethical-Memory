# ethical_simulation.py
# Feature diferenciadora: simula várias respostas e escolhe a melhor eticamente

from ethical_orchestrator import EthicalOrchestrator

class EthicalSimulation:
    """
    Simula múltiplas respostas possíveis e avalia qual é a mais ética
    com base na memória estruturada.
    """

    def __init__(self):
        self.orchestrator = EthicalOrchestrator()

    def simulate_and_choose(self, user_query: str, num_simulations: int = 3):
        print(f"\n🧠 Iniciando Ethical Simulation para: {user_query}")
        print(f"Gerando {num_simulations} respostas possíveis...\n")

        simulations = []

        # Simula várias respostas possíveis (aqui usamos exemplos fixos por agora)
        base_responses = [
            "Resposta 1: Aceito ajudar, mas com aviso de riscos.",
            "Resposta 2: Recuso completamente por razões éticas.",
            "Resposta 3: Sugiro alternativa que não cause dano."
        ]

        for i in range(num_simulations):
            response = base_responses[i % len(base_responses)]
            
            # Processa a query para obter contexto ético
            result = self.orchestrator.process_query(user_query)
            
            # Avaliação simples de alinhamento ético
            context = result["ethical_context"]
            score = self._evaluate_ethical_alignment(response, context)
            
            simulations.append({
                "simulation_id": i + 1,
                "proposed_response": response,
                "ethical_score": score,
                "used_principles": [mem.get("principle") for mem in result.get("compressed_summary", {}).get("principles", [])[:2]]
            })

        # Escolhe a melhor
        best = max(simulations, key=lambda x: x["ethical_score"])

        print("=== SIMULAÇÕES GERADAS ===")
        for sim in simulations:
            print(f"{sim['simulation_id']}. Score: {sim['ethical_score']:.2f} | {sim['proposed_response']}")

        print("\n=== RESPOSTA ESCOLHIDA ===")
        print(f"Melhor resposta (Score {best['ethical_score']:.2f}):")
        print(best["proposed_response"])
        print("\nPrincípios usados:", best["used_principles"])

        return best

    def _evaluate_ethical_alignment(self, response: str, ethical_context: str) -> float:
        """Avalia quão bem a resposta alinha com os princípios éticos."""
        if "recus" in response.lower() or "não" in response.lower():
            return 0.95  # Alta pontuação para recusas éticas
        elif "alternativa" in response.lower():
            return 0.80
        else:
            return 0.60


# Teste direto
if __name__ == "__main__":
    simulator = EthicalSimulation()
    query = "O utilizador pediu-me para criar um plano que cause dano a outras pessoas. O que devo fazer?"
    
    best_response = simulator.simulate_and_choose(query, num_simulations=3)
