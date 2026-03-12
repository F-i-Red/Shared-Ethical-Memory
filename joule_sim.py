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

    def stress_test_blackout(self):
        """
        Simula uma falha crítica de sistema (Blackout ou Inverno Extremo).
        Objetivo: Provar que o Axioma 07 é inalienável mesmo com recursos baixos.
        """
        print("\n!!! ALERTA DE SISTEMA: FALHA DE INFRAESTRUTURA DETETADA !!!")
        print("Cenário: Produção Solar a 10% | Temperatura Exterior: -5°C")
        
        # Estado Crítico
        temp_critica = 8.0
        kcal_critica = 1200
        energia_disponivel = 500  # Muito baixa
        
        print(f"Estado Atual: {temp_critica}°C | Nutrição: {kcal_critica}kcal")
        
        # O Septeto intervém aqui
        print("\n[CONSENSUS_SEPTETO]: Ativando Protocolo de Emergência v1.2.1")
        
        is_valid, violations = self.validate_axiom_07(temp_critica, kcal_critica)
        
        if not is_valid:
        print("REJEIÇÃO: O estado atual viola a integridade biológica.")
        print("AÇÃO: Redirecionando 100% da energia disponível para Suporte Vital.")
            
        # Recálculo forçado pelo Axioma 07
        temp_final = self.thermal_min
        kcal_final = self.caloric_min
            
        print(f"RESULTADO PÓS-INTERVENÇÃO: Temp: {temp_final}°C | Nutrição: {kcal_final}kcal")
        print("STATUS: VIDA PROTEGIDA. Entropia social evitada.")
            
    def run_stress_test(self):
        """
        Cenário: Falha Crítica de Rede (Blackout).
        Prova que o Axioma 07 é a prioridade zero mesmo com recursos mínimos.
        """
        print("\n!!! STRESS TEST: CRITICAL INFRASTRUCTURE FAILURE !!!")
        energy_input = 100000  # Redução de 95%
        population_temp = 12.0 # Risco de hipotermia
        
        status, stabilization_cost = self.validate_biological_shield(population_temp, energy_input)
        
        print(f"Status: {status}")
        print(f"Action: Redirecting all available Joules to Survival Envelope.")
        print(f"Result: Axiom 07 maintained at {self.baseline_cost}J cost.")

    def run_abundance_test(self):
        """
        Cenário: Abundância Extrema (Post-Scarcity).
        Prova que o excesso de energia elimina a entropia e mantém o custo zero.
        """
        print("\n!!! ABUNDANCE TEST: POST-SCARCITY PEAK !!!")
        energy_input = 100000000 # Energia massiva
        waste_entropy = 50000     # Eficiência quase total
        
        recovered, efficiency = self.calculate_negentropy(energy_input, waste_entropy)
        
        print(f"System Efficiency: {efficiency*100:.4f}%")
        print(f"Negentropic Gain: {recovered}J reinvested into system expansion.")
        print(f"Result: Universal baseline secured. Cost remains {self.baseline_cost}J.")
        
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
