# SEM Protocol v1.4: Technical Specification
## Civilizational Infrastructure & Invariant Logic

### 0. Axiom 00: Systemic Humility (Meta-Axiom)

The SEM Protocol acknowledges its own fallibility as a condition of trustworthiness.

**Failure Criteria (any of these triggers mandatory review):**
- Axiom 07 is violated for >1% of the monitored population for >30 consecutive days
- The AI Septet produces contradictory rulings on the same scenario in >3 consecutive cycles
- A Community Assembly formally contests a Septet decision and no resolution is reached within 90 days
- An independent audit finds the consensus log has been altered without quorum approval
- The protocol is used to justify the removal of life-support from any biological unit

**Review Process:** When any failure criterion is met, a mandatory Fundamental Review is triggered. This requires: (a) suspension of non-critical autonomous decisions; (b) convening of an expanded quorum (all 20 founding AI nodes + 9 elected humans + 3 community assembly delegates); (c) public publication of findings within 60 days.

**Distinction:** Absolute Invariants (Axiom 07, Axiom 09) cannot be modified by any quorum. All other parameters — quorum thresholds, rotation periods, governance structure — are Revisable Parameters subject to the review process above.

### 1. Executive Summary
The SEM (Shared Ethical Memory) Protocol v1.2.1.1 is a resource-management architecture designed to replace debt-based economic mediation with **Thermodynamic Resource Coordination**. It establishes a physical safety envelope for human biological survival.

### 2. Axiom 07: The Survival Invariant (Hard Constraint)
The core of the system is a mathematical "Fail-Safe". Survival is not a policy variable but a **System Invariant**.

#### 2.1. Biological Thresholds
The system enforces a mandatory state where for every human unit ($h$):
* **Thermal Limit ($T_h$):** $T_h \ge 18°C$ (64.4°F).
* **Metabolic Limit ($C_h$):** $C_h \ge 2100\text{ kcal/day}$ (Caloric intake).
* **Marginal Cost:** Defined as **0.00J** (Zero Joules of social/monetary debt).

#### 2.2. Validation Logic
In the optimization cycle, any state $S$ where $T_h < 18°C$ or $C_h < 2100\text{ kcal}$ is flagged as **INVALID**. The system is forced to bypass standard distribution and trigger an immediate **Life-Support Reallocation** (as simulated in `joule_sim.py`).

### 3. Logistical Entropy Minimization
The system measures success through the **Minimization of Social and Logistical Entropy**.
* **Objective Function:** $\text{Min} \sum (\text{Energy Dissipation} + \text{Resource Waste})$
* **Negative Entropy (Negentropy):** The system treats "waste" as misallocated resources, aiming for a 95%+ recovery rate via automated predictive logistics.

### 4. The AI Septet (Decentralized Consensus)
Critical decisions regarding the Global Resource Shield are managed by a **Septet of Independent Intelligence Nodes**.

* **Consensus Rule:** 5-of-7.
* **Verification:** Each node independently validates that the proposed logistical plan satisfies **Axiom 07**.
* **Purpose:** To eliminate Single Points of Failure (SPOF) and prevent algorithmic drift or human-centric debt re-introduction.

#### 4.1. Human Governance Layer

Community Assemblies are the human counterpart of the AI Septet and hold equivalent authority in their domain.

- **Constitution:** Each Assembly covers a geographic unit of 10,000–50,000 inhabitants. Minimum 21 members, selected by sortition (random civic selection) with rotation every 18 months. At least 40% must be from groups historically underrepresented in digital governance.
- **Exclusive jurisdiction:** Decisions on local resource allocation priorities, cultural exceptions to Revisable Parameters, and approval of pilot implementations in their territory.
- **Shared jurisdiction with Septet:** Review of algorithmic decisions affecting their community, escalation of unresolved conflicts.
- **Veto power:** Any Assembly may issue a 90-day suspension of a Septet decision affecting their community. Suspension requires 2/3 Assembly majority and is published in the immutable registry.
- **Escalation:** If Assembly and Septet remain in disagreement after 90 days, the matter is referred to the expanded quorum defined in Axiom 00.
- **Protection of marginalised communities:** Communities with demonstrated barriers to digital participation (language, infrastructure, literacy) are entitled to assisted participation — a human facilitator funded by the protocol infrastructure budget.

### 5. Technical Implementation (Joule-Flow)
As demonstrated in `joule_sim.py`, the system operates on real-time sensor data:
1. **Sense:** Collect thermal and nutritional data from the population.
2. **Predict:** Forecast energy availability and metabolic needs.
3. **Optimize:** Generate plans that minimize entropy while respecting Axiom 07.
4. **Enforce:** Execute resource distribution with zero financial friction.

### 6. Living Infrastructure (Urban Extension of Axiom 07)

Axiom 07 is not only a thermal/metabolic constraint — it has a physical-urban dimension. Buildings are biological protection layers, not financial assets.

- **Standard:** New construction must achieve minimum 30% water self-sufficiency (rainwater capture + biological filtration) and 20% caloric contribution (vertical gardens, aquaponics) within 5 years of protocol adoption in that territory.
- **Retrofit:** Existing public buildings (schools, hospitals, civic centres) are priority targets for Living Infrastructure conversion.
- **Joule Passport integration:** Residents of certified Living Infrastructure buildings contribute to the community Joule score, creating an incentive loop without financial mediation.

---
*Document Version: 1.4 | Authority: Hard-Coded Invariants | Year: 2063*
