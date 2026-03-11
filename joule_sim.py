# SEM Protocol v1.2 - Joule-flow Resource Allocation Simulator
# Core Logic: Negentropic Recovery & Biological Precedence
# Version: 1.2 | Consensus 2026 | Node: F-i-Red_2063

import time

class JouleSystem:
    def __init__(self):
        self.protocol_version = "1.2"
        self.baseline_cost = 0.00  # Axiom 0
        self.thermal_min = 18.0    # Axiom 07 (Celsius)
        self.thermal_max = 24.0    # Axiom 07 (Celsius)

    def calculate_negentropy(self, total_energy, waste_entropy):
        """
        Calcula a recuperação de desperdício sistémico.
        Em 2063, desperdício é apenas recurso mal alocado.
        """
        recovered_joules = waste_entropy * 0.95  # 95% efficiency in recovery
        efficiency_rate = (total_energy - (waste_entropy - recovered_joules)) / total_energy
        return recovered_joules, efficiency_rate

    def validate_biological_shield(self, current_temp, available_joules):
        """
        Axiom 07: Thermal Inalienability.
        Garante que o suporte térmico nunca é cortado.
        """
        if current_temp < self.thermal_min:
            status = "⚠️ HEATING_REQUIRED"
            joules_needed = (self.thermal_min - current_temp) * 1200 # Energy to stabilize
        elif current_temp > self.thermal_max:
            status = "⚠️ COOLING_REQUIRED"
            joules_needed = (current_temp - self.thermal_max) * 1200
        else:
            status = "✅ THERMAL_EQUILIBRIUM"
            joules_needed = 0
            
        return status, joules_needed

    def run_simulation(self, energy_input, entropy_detected, population_temp):
        print(f"--- SEM PROTOCOL {self.protocol_version} SIMULATOR ---")
        print(f"Node Status: Active | Priority: Life_Primacy\n")
        
        recovered, efficiency = self.calculate_negentropy(energy_input, entropy_detected)
        status, stabilization_cost = self.validate_biological_shield(population_temp, energy_input)
        
        print(f"[1] Sistema de Negentropia: {efficiency*100:.2f}% de Eficiência")
        print(f"[2] Joules Recuperados do Desperdício: {recovered:.2f}J")
        print(f"[3] Estado Térmico: {status}")
        
        if stabilization_cost > 0:
            print(f"[4] Alocação Automática: {stabilization_cost}J direcionados para TIP.")
        
        # O custo para o biológico é sempre ZERO
        print(f"\n[FINAL_LOG] Custo para a Unidade Biológica: {self.baseline_cost}J")
        print(f"--- STATUS: ABUNDANCE_LOCKED ---")

# --- TESTE DE CENÁRIO (Transição 2063) ---
if __name__ == "__main__":
    sim = JouleSystem()
    
    # Exemplo: Cidade com alto desperdício industrial e frio extremo
    sim.run_simulation(
        energy_input=5000000, 
        entropy_detected=850000
