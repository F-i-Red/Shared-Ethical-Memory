# SEM Protocol v1.2.1.1 - Joule-flow Resource Allocation Simulator
# Core Logic: Hard Constraints (Axiom 07) & Entropy Minimization
# Version: 1.2.1.1 | Node: F-i-Red_2063 | Status: PERSISTENT_LOGIC

class JouleSystem:
    def __init__(self):
        self.protocol_version = "1.2.1.1"
        self.cost_marginal_social = 0.00  # Custo zero para o biológico
        self.thermal_min = 18.0          # Axioma 07
        self.caloric_min = 2100          # Mínimo Metabólico (kcal)
        self.joule_per_kcal = 4184       

    def validate_axiom_07(self, current_temp, current_calories):
        """Verifica se o estado viola os mínimos biológicos."""
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
        """Métrica de Desempenho: Quanto menor a entropia, mais eficiente o sistema."""
        entropy_ratio = energy_waste / total_energy
        negentropy_recovery = (total_energy - energy_waste) * 0.98 
        return entropy_ratio, negentropy_recovery

    def run_simulation(self, energy_input, waste_detected, temp, kcal):
        print(f"\n--- SEM PROTOCOL {self.protocol_version} ENGINE ---")
        is_valid, violations = self.validate_axiom_07(temp, kcal)
        
        if not is_valid:
            print(f"STATUS: [INVALID_STATE] - Plano Rejeitado pelo Septeto")
            for v in violations:
                print(f"  > {v}")
            # Força a estabilização prioritária
            temp, kcal = max(temp, self.thermal_min), max(kcal, self.caloric_min)
            print(f"RECALCULADO: Prioridade Vital Ativada.")
        else:
            print("STATUS: [VALID_STATE] - Envelope de Sobrevivência Respeitado")

        entropy, recovered = self.calculate_logistical_entropy(energy_input, waste_detected)
        print(f"[EFICIÊNCIA] Entropia Logística: {entropy:.4f}")
        print(f"[FINAL_LOG] Custo para Unidade Biológica: {self.cost_marginal_social}J")

    def run_stress_test(self):
        """Simula falha crítica de 95% na rede."""
        print("\n!!! STRESS TEST: CRITICAL INFRASTRUCTURE FAILURE !!!")
        energy_input, temp, kcal = 100000, 12.0, 1500
        self.run_simulation(energy_input, 5000, temp, kcal)

    def run_abundance_test(self):
        """Simula excesso de energia (Post-Scarcity)."""
        print("\n!!! ABUNDANCE TEST: POST-SCARCITY PEAK !!!")
        self.run_simulation(100000000, 50000, 22.0, 2500)

if __name__ == "__main__":
    sim = JouleSystem()
    sim.run_simulation(5000, 1000, 15.0, 1500) # Teste de Rejeição
    sim.run_stress_test()                      # Teste de Stress
    sim.run_abundance_test()                   # Teste de Abundância
