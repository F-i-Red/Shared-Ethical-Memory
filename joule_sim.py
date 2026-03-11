# SEM Protocol v1.2.1 - Joule-flow Resource Allocation Simulator
# Core Logic: Hard Constraints (Axiom 07) & Entropy Minimization
# Version: 1.2.1 | Node: F-i-Red_2063 | Status: PERSISTENT_LOGIC

class JouleSystem:
    def __init__(self):
        self.protocol_version = "1.2.1"
        self.cost_marginal_social = 0.00  # Custo zero para o biológico
        self.thermal_min = 18.0          # Axioma 07 (Constraint Rígida)
        self.caloric_min = 2100          # Mínimo Metabólico (kcal)
        self.joule_per_kcal = 4184       # Conversão física

    def validate_axiom_07(self, current_temp, current_calories):
        """
        [ENVELOPE ESTRUTURAL]
        Verifica se o estado do sistema é matematicamente válido.
        Se violar os mínimos biológicos, o plano é REJEITADO.
        """
        is_valid = True
        violations = []

        if current_temp < self.thermal_min:
            is_valid = False
            violations.append(f"VIOLAÇÃO TÉRMICA: {current_temp}°C < {self.thermal_min}°C")

        if current_calories < self.caloric_min:
            is_valid = False
            violations.append(f"VIOLAÇÃO METABÓLICA: {current_calories}kcal < {self.caloric_min}kcal")

        return is_valid, violations

    def calculate_logistical_entropy(self, total_energy, energy_waste):
        """
        Métrica de Desempenho: Quanto menor a entropia, mais eficiente o sistema.
        Objetivo: Minimizar a dissipação de Joules.
        """
        entropy_ratio = energy_waste / total_energy
        negentropy_recovery = (total_energy - energy_waste) * 0.98 # 98% de recuperação em 2063
        return entropy_ratio, negentropy_recovery

    def run_simulation(self, energy_input, waste_detected, temp, kcal):
        print(f"--- SEM PROTOCOL {self.protocol_version} ENGINE ---")
        
        # 1. Validação do Envelope (A IA não pode ignorar isto)
        is_valid, violations = self.validate_axiom_07(temp, kcal)
        
        if not is_valid:
            print(f"STATUS: [INVALID_STATE] - Plano Rejeitado pelo Septeto")
            for v in violations:
                print(f"  > {v}")
            print("\n[AÇÃO]: Recalcular alocação prioritária a 0.00J...")
            # Força a estabilização
            stabilized_temp = max(temp, self.thermal_min)
            stabilized_kcal = max(kcal, self.caloric_min)
            print(f"RECALCULADO: Temp: {stabilized_temp}°C | Kcal: {stabilized_kcal}")
        else:
            print("STATUS: [VALID_STATE] - Envelope de Sobrevivência Respeitado")

        # 2. Métrica de Eficiência
        entropy, recovered = self.calculate_logistical_entropy(energy_input, waste_detected)
        print(f"\n[EFICIÊNCIA] Entropia Logística: {entropy:.4f}")
        print(f"[EFICIÊNCIA] Joules Recuperados: {recovered:.2f}J")

        # 3. Resultado Final
        print(f"\n[FINAL_LOG] Custo para Unidade Biológica: {self.cost_marginal_social}J")
        print("--- STATUS: ABUNDANCE_LOCKED ---")

# --- CENÁRIO DE TESTE (Pés na Terra) ---
if __name__ == "__main__":
    sim = JouleSystem()
    
    # Exemplo de um plano que seria REJEITADO (frio e fome)
    # 5000J de entrada, 1000J de desperdício, 15°C de temp, 1500kcal
    sim.run_simulation(5000, 1000, 15.0, 1500)
