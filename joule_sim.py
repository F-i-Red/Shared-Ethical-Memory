# SEM Protocol v1.0 - Joule-flow Resource Allocation Simulator
# Logic: Decoupling Survival from Financial Speculation

def calculate_negentropy(energy_input, waste_detected):
    """
    Redirects misallocated energy (waste) back into life-support.
    Formula: Efficiency = (Total - Waste) / Total
    """
    useful_energy = energy_input - waste_detected
    return useful_energy / energy_input

def axiom_0_allocation(occupancy_need, available_joules):
    """
    Axiom 0: Housing/Life-support cost = 0.00 Joules for the user.
    The system absorbs the thermodynamic cost through efficiency.
    """
    if available_joules > (occupancy_need * 1.2):
        return "STATUS: ABUNDANCE_LOCKED | COST: 0.00J"
    return "STATUS: REBALANCING_FLOW..."

# Example Scenario: Global Housing Grid 2063
energy = 1000000  # Total Joules
waste = 50000     # Detected entropy
efficiency = calculate_negentropy(energy, waste)

print(f"System Negentropy: {efficiency*100}%")
print(axiom_0_allocation(500, energy))
