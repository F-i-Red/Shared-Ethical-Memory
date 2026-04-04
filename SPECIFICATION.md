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

#### 2.3. Scientific Basis for Axiom 07 Thresholds

The values T ≥ 18°C and C ≥ 2100 kcal/day are not arbitrary. Both are grounded in
peer-reviewed evidence and international institutional consensus.

**Thermal Threshold — T ≥ 18°C**

The 18°C minimum is established by the World Health Organization's Housing and Health
Guidelines (2018), which issue a *strong recommendation* that 18°C constitutes "a safe
and well-balanced indoor temperature to protect the health of general populations during
cold seasons." This recommendation is supported by multiple systematic reviews showing
that indoor temperatures below 18°C are associated with:

- Elevated cardiovascular risk: cohort studies in Scotland found significantly higher
  blood pressure in residents of homes below 18°C, with risk increasing sharply below
  16°C (OR 4.92 for hypertension).
- Elevated respiratory risk: adults with COPD showed reduced respiratory problems at
  indoor temperatures at or above 18.2°C; temperatures below 16°C with humidity above
  65% are associated with respiratory hazard including allergies.
- Increased all-cause winter mortality, particularly in vulnerable groups (elderly,
  children, those with chronic illness), for whom the WHO recommends a higher minimum
  of 20°C.

**Important qualification:** 18°C is a global *floor*, not a universal *optimum*. The
WHO evidence base is concentrated in temperate and colder climates. Populations
acclimatised to warmer climates (tropical, sub-equatorial) have demonstrated comfort
ranges of 24–32°C. The SEM protocol therefore treats 18°C as the non-negotiable
biological safety floor — the point below which health risk is clinically demonstrated —
while explicitly recognising that regional Assemblies may set higher local minimums
under Axiom 00's Revisable Parameters mechanism. The threshold can be raised; it
cannot be lowered below 18°C.

**Caloric Threshold — C ≥ 2100 kcal/day**

The 2100 kcal/day minimum is derived from the FAO/WHO/UNU Joint Expert Consultation
on Human Energy Requirements (2001, published 2004) — the authoritative reference for
global undernourishment measurement. Key points:

- The FAO defines undernourishment as caloric intake insufficient to meet minimum
  energy requirements for adequate weight, body composition, and sedentary physical
  activity consistent with long-term good health.
- The global average minimum dietary energy requirement (MDER) for adults is
  approximately 2000 kcal/day (FAO); the 2100 kcal threshold adds a safety margin
  above this floor to account for light activity levels and individual variation.
- The FAO/WHO/UNU consultation establishes that requirements vary by age, sex, body
  size and activity level. 2100 kcal/day is consistent with the requirement for an
  adult of average body size performing sedentary to light activity — the baseline
  condition the SEM protocol guarantees before any additional needs are addressed.
- Research modelling global caloric requirements (PMC, 2019) estimates the global
  average daily requirement at approximately 2285 kcal/person as of 2010, rising with
  increasing body height and BMI trends. 2100 kcal is therefore a conservative and
  defensible minimum floor, not a recommended intake.

**Important qualification:** The FAO explicitly states that energy requirements are
population-level averages, not individual prescriptions. The 2100 kcal threshold in
the SEM protocol is therefore correctly understood as a *systemic guarantee* — the
minimum the infrastructure must make available per person — not a claim that every
individual requires exactly this amount. As with the thermal threshold, regional
Assemblies may raise this floor locally (e.g. for populations with higher average
activity levels or body mass); they may not lower it below 2100 kcal.

**On the "colonialism of standards" critique**

Several evaluators in the SEM v2.0 consensus process raised the concern that imposing
universal biological minimums risks cultural paternalism. This critique is addressed
directly:

1. Both thresholds are *floors derived from human physiology*, not cultural preferences.
   Below 16°C, respiratory and cardiovascular risk increases regardless of cultural
   context. Below approximately 1700–1800 kcal/day, the FAO defines chronic
   undernourishment regardless of geography.

2. The thresholds are *revisable upward* by Community Assemblies under the Conflict
   Grammar (Tier 2 — Revisable Defaults). What is not revisable is the direction:
   no cultural argument can lower a biological safety floor.

3. The critique of "colonialism of standards" applies validly to *optimums* imposed
   from outside — e.g. mandating 22°C because a temperate-climate population considers
   it comfortable. It does not apply to *minimums* below which clinical harm is
   documented. The SEM protocol mandates only the latter.

**References**
- WHO Housing and Health Guidelines, 2018. Chapter: Low indoor temperatures.
  NCBI Bookshelf NBK535294.
- Ormandy, D. & Ezratty, V. (2012). Health and thermal comfort: From WHO guidance
  to housing strategies. Energy Policy, 49, 116–121.
- FAO/WHO/UNU. Human Energy Requirements. Report of a Joint Expert Consultation.
  Rome, October 2001. FAO Food and Nutrition Technical Report Series 1, 2004.
- Ritchie, H. & Roser, M. Food Supply. Our World in Data, 2019.
- Bennett, E. et al. (2023). Cold indoor temperatures and their association with
  health and well-being: a systematic literature review. Public Health, 225.

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
