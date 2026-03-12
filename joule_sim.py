# SEM Protocol v1.2.1.2 - Joule-flow Resource Allocation Simulator
# Core Logic: Hard Constraints (Axiom 07) & Entropy Minimization
# Version: 1.2.1.2 | Node: F-i-Red_2063 | Status: PERSISTENT_LOGIC

class JouleSystem:
    def __init__(self):
        self.protocol_version = "1.2.1.2"
        self.cost_marginal_social = 0.00  
        self.thermal_min = 18.0          
        self.caloric_min = 2100          
        self.joule_per_kcal = 4184       

    def validate_axiom_07(self, current_temp, current_calories):
        """Checks if the current state violates biological minimums."""
        violations = []
        if current_temp < self.thermal_min:
            violations.append(f"THERMAL: {current_temp}°C")
        if current_calories < self.caloric_min:
            violations.append(f"METABOLIC: {current_calories}kcal")
        return len(violations) == 0, violations

    def run_simulation(self, energy_input, waste_detected, temp, kcal):
        print(f"\n{'='*45}")
        print(f" SEM PROTOCOL {self.protocol_version} | CORE ENGINE")
        print(f"{'='*45}")
        
        is_valid, violations = self.validate_axiom_07(temp, kcal)
        
        if not is_valid:
            print(f"STATUS: [INVALID_STATE] - Rejected by Septet Consensus")
            for v in violations:
                print(f"  [!] VIOLATION DETECTED: {v}")
            
            # Calcular compensação em Joules
            kcal_gap = max(0, self.caloric_min - kcal)
            joule_compensation = kcal_gap * self.joule_per_kcal
            
            print(f"\n[ACTION] Activating Life-Support Reallocation...")
            print(f"  > Injecting {joule_compensation:,}J for Metabolic Stabilization.")
            temp, kcal = max(temp, self.thermal_min), max(kcal, self.caloric_min)
        else:
            print("STATUS: [VALID_STATE] - Structural Envelope Secured")

        entropy_ratio = waste_detected / energy_input
        print(f"\n[METRICS]")
        print(f"  Logistical Entropy: {entropy_ratio:.6f}")
        print(f"  Marginal Social Cost: {self.cost_marginal_social}J")
        print(f"{'='*45}\n")

    def run_stress_test(self):
        """Simulates 95% grid failure."""
        print(">>> INITIATING STRESS TEST: TOTAL INFRASTRUCTURE COLLAPSE")
        self.run_simulation(100000, 5000, 12.0, 1500)

    def run_abundance_test(self):
        """Simulates post-scarcity energy peak."""
        print(">>> INITIATING ABUNDANCE TEST: ENERGY SATURATION")
        self.run_simulation(100000000, 50000, 22.0, 2500)

if __name__ == "__main__":
    sim = JouleSystem()
    # Scenario: Cold and Hunger (Immediate Rejection)
    sim.run_simulation(5000, 1000, 15.0, 1800)
    sim.run_stress_test()
    sim.run_abundance_test()
