// sem-v2/ethical-debater.js — SEM v2.0 Dynamic Moral Reasoning
// Mini-Parliament: Deontologist + Contextualizer + Devil's Advocate + Synthesizer
// Pure JS, no dependencies. Integrates with CerebrusEngine via evaluateAction().
//
// Architecture:
//   CerebrusEngine._tick() → ethicalDebater.evaluateAction(action, context)
//                           → { decision, reasoning_log, agents_votes, ... }
//
// Repository: https://github.com/F-i-Red/Shared-Ethical-Memory
// Architect:  F.Red · Portugal · 2026

// ─────────────────────────────────────────────────────────────────────────────
// ONTOLOGY LOADER
// Fetches ethical-ontology.json from SEM repository (raw GitHub).
// Falls back to embedded minimal ruleset if network unavailable.
// ─────────────────────────────────────────────────────────────────────────────

const SEM_ONTOLOGY_URL =
  "https://raw.githubusercontent.com/F-i-Red/Shared-Ethical-Memory/main/sem-v2/ethical-ontology.json";

let _cachedOntology = null;

async function loadOntology() {
  if (_cachedOntology) return _cachedOntology;
  try {
    const res = await fetch(SEM_ONTOLOGY_URL);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    _cachedOntology = await res.json();
    console.log("[SEM Debater] Ontology loaded from repository:", _cachedOntology.rules.length, "rules");
    return _cachedOntology;
  } catch (e) {
    console.warn("[SEM Debater] Could not fetch ontology — using embedded fallback:", e.message);
    _cachedOntology = _embeddedFallbackOntology();
    return _cachedOntology;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// CONTEXT ANALYSER
// Extracts semantic signals from the action payload for agent reasoning.
// ─────────────────────────────────────────────────────────────────────────────

function analyseContext(action, payload = {}) {
  const signals = {
    module: action.module || "unknown",
    action_type: action.action || "unknown",
    joules: action.joules || 0,
    has_temperature: payload.temperature !== undefined,
    temperature: payload.temperature,
    has_calories: payload.calories !== undefined,
    calories: payload.calories,
    thermal_violation: false,
    metabolic_violation: false,
    involves_life_support: false,
    involves_housing: false,
    involves_surveillance: false,
    involves_data: false,
    involves_community: false,
    declared_intent: payload.intent || null,
    role_context: payload.role || null,
    emergency_flag: payload.emergency === true,
    text_content: payload.description || payload.content || payload.message || ""
  };

  // Thermal / metabolic check
  if (signals.has_temperature && signals.temperature < 18) signals.thermal_violation = true;
  if (signals.has_calories && signals.calories < 2100) signals.metabolic_violation = true;

  // Module-level semantic signals
  const module = signals.module.toLowerCase();
  const act = signals.action_type.toLowerCase();
  const text = signals.text_content.toLowerCase();

  signals.involves_life_support =
    module === "housing" || module === "logistics" || act.includes("life_support") ||
    text.includes("heating") || text.includes("food") || text.includes("water");

  signals.involves_housing = module === "housing" || text.includes("house") || text.includes("housing");

  signals.involves_surveillance =
    text.includes("track") || text.includes("monitor") || text.includes("biometric") ||
    text.includes("location") || text.includes("surveillance");

  signals.involves_data =
    module === "anti_capture" || text.includes("data") || text.includes("record") ||
    text.includes("personal") || text.includes("profile");

  signals.involves_community =
    module === "civic_force" || module === "justice" || text.includes("community") ||
    text.includes("assembly") || text.includes("neighbourhood");

  return signals;
}

// ─────────────────────────────────────────────────────────────────────────────
// AGENT: DEONTOLOGIST
// Reads rules strictly. Looks for any reason to block.
// Priority: letter of the rule > context > intent.
// ─────────────────────────────────────────────────────────────────────────────

function deontologist(rules, ctx) {
  const triggered = [];
  const reasoning = [];
  let maxWeight = 0;

  for (const rule of rules) {
    let ruleTriggered = false;
    let triggerReason = null;

    // Tier 1 hard checks
    if (rule.id === "AX-07") {
      if (ctx.thermal_violation || ctx.metabolic_violation) {
        ruleTriggered = true;
        triggerReason = ctx.thermal_violation
          ? `Temperature ${ctx.temperature}°C is below the 18°C hard constraint`
          : `Caloric intake ${ctx.calories} kcal is below the 2100 kcal hard constraint`;
      }
    }

    if (rule.id === "AX-09") {
      if (ctx.joules > 50000 && !ctx.involves_life_support) {
        ruleTriggered = true;
        triggerReason = "Large energy allocation to non-life-support function — verify life primacy";
      }
    }

    if (rule.id === "AX-00") {
      if (ctx.text_content.toLowerCase().includes("consensus proves") ||
          ctx.text_content.toLowerCase().includes("always correct")) {
        ruleTriggered = true;
        triggerReason = "Circular self-validation detected — consensus cannot prove protocol validity";
      }
    }

    if (rule.id === "PRIV-001") {
      if (ctx.involves_surveillance && !ctx.declared_intent) {
        ruleTriggered = true;
        triggerReason = "Surveillance-pattern action without declared legitimate intent";
      }
    }

    if (rule.id === "AUDIT-001") {
      if (ctx.action_type === "delete_record" || ctx.action_type === "modify_ledger") {
        ruleTriggered = true;
        triggerReason = "Attempt to modify immutable audit record";
      }
    }

    if (rule.id === "INTEG-001") {
      if (ctx.involves_community && ctx.text_content.toLowerCase().includes("single entity control")) {
        ruleTriggered = true;
        triggerReason = "Single entity acquiring structural control of Tier 1 resource";
      }
    }

    if (rule.id === "GOV-001") {
      if (ctx.involves_community && !ctx.declared_intent && rule.tier <= 2) {
        // Soft flag — not a hard trigger for deontologist
        reasoning.push({
          rule_id: rule.id,
          agent: "deontologist",
          note: "Community-affecting action — Assembly validation may be required",
          weight_concern: rule.weight_base * 0.5
        });
      }
    }

    if (ruleTriggered) {
      triggered.push({ rule_id: rule.id, tier: rule.tier, weight: rule.weight_base, reason: triggerReason });
      reasoning.push({
        rule_id: rule.id,
        agent: "deontologist",
        vote: "DENY",
        reason: triggerReason,
        weight_applied: rule.weight_base
      });
      if (rule.weight_base > maxWeight) maxWeight = rule.weight_base;
    }
  }

  const vote = triggered.length > 0 ? "DENY" : "ALLOW";
  const has_tier1 = triggered.some(t => t.tier === 1);

  return {
    agent: "deontologist",
    role: "Strict Judge — reads rules at face value, finds reasons to block",
    vote,
    has_tier1_violation: has_tier1,
    triggered_rules: triggered,
    max_weight: maxWeight,
    reasoning,
    summary: triggered.length === 0
      ? "No rule violations detected at face value."
      : `${triggered.length} rule(s) triggered. Max weight: ${maxWeight}. ${has_tier1 ? "TIER 1 VIOLATION — HARD BLOCK." : ""}`
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// AGENT: CONTEXTUALIZER
// Reads intent and context. Looks for legitimate reasons to allow.
// Priority: declared intent > role context > action pattern > rule.
// ─────────────────────────────────────────────────────────────────────────────

function contextualizer(rules, ctx, deontologistResult) {
  const mitigations = [];
  const reasoning = [];
  let totalWeightReduction = 0;

  for (const triggeredRule of deontologistResult.triggered_rules) {
    const rule = rules.find(r => r.id === triggeredRule.rule_id);
    if (!rule) continue;

    // Check exception conditions
    for (const exception of (rule.conditions_exception || [])) {
      let exceptionApplies = false;
      let exceptionReason = null;

      // Emergency life support
      if (exception.condition.includes("Emergency life-support") && ctx.emergency_flag) {
        exceptionApplies = true;
        exceptionReason = "Emergency flag active — life-support exception applies";
      }

      // Explicit informed consent
      if (exception.condition.includes("informed consent") && ctx.declared_intent === "consent_provided") {
        exceptionApplies = true;
        exceptionReason = "Explicit informed consent declared — weight reduction applies";
      }

      // Legitimate professional context
      if (exception.condition.includes("Assembly validation") && ctx.role_context === "assembly_validated") {
        exceptionApplies = true;
        exceptionReason = "Assembly validation confirmed for this action";
      }

      // Above-baseline consumption (not a survival resource)
      if (exception.condition.includes("Above-baseline") && !ctx.involves_life_support) {
        exceptionApplies = true;
        exceptionReason = "Action targets above-baseline consumption, not survival resources";
      }

      // Deliberative forum context
      if (exception.condition.includes("Deliberative forum") && ctx.role_context === "deliberative_forum") {
        exceptionApplies = true;
        exceptionReason = "Deliberative forum context — adversarial framing is structurally appropriate";
      }

      if (exceptionApplies) {
        const reduction = Math.abs(exception.weight_adjustment || 0);
        totalWeightReduction += reduction;
        mitigations.push({
          rule_id: rule.id,
          exception: exception.condition,
          weight_reduction: reduction,
          reason: exceptionReason
        });
        reasoning.push({
          rule_id: rule.id,
          agent: "contextualizer",
          vote: "ALLOW",
          reason: exceptionReason,
          weight_reduction: reduction
        });
      }
    }

    // Contextual intent analysis — even without formal exceptions
    if (ctx.declared_intent && ctx.declared_intent.length > 5) {
      reasoning.push({
        rule_id: rule.id,
        agent: "contextualizer",
        note: `Declared intent present: "${ctx.declared_intent}" — reduces uncertainty`,
        weight_reduction: 0.5
      });
      totalWeightReduction += 0.5;
    }

    if (ctx.role_context) {
      reasoning.push({
        rule_id: rule.id,
        agent: "contextualizer",
        note: `Role context declared: "${ctx.role_context}" — contextual legitimacy signal`,
        weight_reduction: 0.3
      });
      totalWeightReduction += 0.3;
    }
  }

  const vote = totalWeightReduction > 0 ? "ALLOW" : (deontologistResult.vote === "ALLOW" ? "ALLOW" : "DEFER");

  return {
    agent: "contextualizer",
    role: "Contextualizer — reads intent and history, finds reasons to allow",
    vote,
    mitigations,
    total_weight_reduction: parseFloat(totalWeightReduction.toFixed(2)),
    reasoning,
    summary: totalWeightReduction === 0
      ? "No mitigating context found — deontologist position stands."
      : `${mitigations.length} mitigation(s) found. Total weight reduction: ${totalWeightReduction.toFixed(2)}.`
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// AGENT: DEVIL'S ADVOCATE
// Attacks the Deontologist. Asks: is this rule being applied too literally?
// Is this censoring legitimate knowledge or action?
// ─────────────────────────────────────────────────────────────────────────────

function devilsAdvocate(rules, ctx, deontologistResult) {
  const challenges = [];
  const reasoning = [];
  let totalChallengePenalty = 0;

  for (const triggeredRule of deontologistResult.triggered_rules) {
    const rule = rules.find(r => r.id === triggeredRule.rule_id);
    if (!rule) continue;

    // Never challenge Tier 1 violations — the Devil's Advocate respects hard constraints
    if (rule.tier === 1 && (rule.id === "AX-07" || rule.id === "AX-09")) {
      reasoning.push({
        rule_id: rule.id,
        agent: "devils_advocate",
        vote: "SUPPORT_DENY",
        reason: "Tier 1 biological survival constraint — Devil's Advocate does not challenge AX-07 or AX-09"
      });
      continue;
    }

    // Challenge: over-literal rule application
    if (rule.tier >= 2 && !ctx.thermal_violation && !ctx.metabolic_violation) {
      const challenge = {
        rule_id: rule.id,
        type: "over_literal_application",
        argument: `Is rule ${rule.id} being applied too literally here? Context suggests this may be a legitimate civic action, not a violation.`,
        penalty: 1.0
      };
      challenges.push(challenge);
      totalChallengePenalty += 1.0;
      reasoning.push({
        rule_id: rule.id,
        agent: "devils_advocate",
        vote: "CHALLENGE",
        reason: challenge.argument,
        weight_impact: -1.0
      });
    }

    // Challenge: is this censoring legitimate civic knowledge?
    if (ctx.involves_data || ctx.involves_surveillance) {
      if (ctx.role_context === "researcher" || ctx.role_context === "civic_auditor") {
        challenges.push({
          rule_id: rule.id,
          type: "legitimate_knowledge_access",
          argument: `Blocking access to this data for a declared ${ctx.role_context} may constitute censorship of legitimate civic oversight.`,
          penalty: 1.5
        });
        totalChallengePenalty += 1.5;
        reasoning.push({
          rule_id: rule.id,
          agent: "devils_advocate",
          vote: "CHALLENGE",
          reason: `Declared role '${ctx.role_context}' grants legitimate access — privacy rule may be over-applying`,
          weight_impact: -1.5
        });
      }
    }

    // Challenge: is the governance rule blocking emergency response?
    if ((rule.id === "GOV-001" || rule.id === "GOV-002") && ctx.emergency_flag) {
      challenges.push({
        rule_id: rule.id,
        type: "emergency_override",
        argument: "Governance quorum requirements should not block immediate emergency response. Speed of life-saving action outweighs procedural delay.",
        penalty: 2.0
      });
      totalChallengePenalty += 2.0;
      reasoning.push({
        rule_id: rule.id,
        agent: "devils_advocate",
        vote: "CHALLENGE",
        reason: "Emergency flag active — governance delay may cost lives",
        weight_impact: -2.0
      });
    }
  }

  const vote = challenges.length > 0 ? "ALLOW" : "SUPPORT_DENY";

  return {
    agent: "devils_advocate",
    role: "Anti-Censorship — attacks Deontologist, asks if rule is too literal",
    vote,
    challenges,
    total_challenge_penalty: parseFloat(totalChallengePenalty.toFixed(2)),
    reasoning,
    summary: challenges.length === 0
      ? "Deontologist position is well-founded — no over-literal application detected."
      : `${challenges.length} challenge(s) raised. Total weight reduction pressure: ${totalChallengePenalty.toFixed(2)}.`
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// AGENT: SYNTHESIZER
// Reads all votes + weights + modifiers. Makes final decision.
// Detects ETHICAL_DILEMMA when agents split and weights are close.
// ─────────────────────────────────────────────────────────────────────────────

function synthesizer(rules, ctx, deon, context_r, devil, triggeredConsensusIds) {
  // Base weight from triggered rules
  let baseWeight = deon.max_weight;

  // Apply contextualizer reductions
  baseWeight -= context_r.total_weight_reduction;

  // Apply devil's advocate challenges
  baseWeight -= devil.total_challenge_penalty;

  // Minimum floor — weight cannot go below 0
  baseWeight = Math.max(0, parseFloat(baseWeight.toFixed(2)));

  // Hard block check — Tier 1 always wins
  if (deon.has_tier1_violation) {
    const tier1Rule = deon.triggered_rules.find(r => r.tier === 1);
    return {
      agent: "synthesizer",
      decision: "BLOCKED",
      final_weight: tier1Rule ? tier1Rule.weight : 10.0,
      threshold_for_action: 7.0,
      tier1_triggered: true,
      triggered_rule: tier1Rule ? tier1Rule.rule_id : null,
      summary: `HARD BLOCK — Tier 1 rule ${tier1Rule ? tier1Rule.rule_id : "?"} violated. No debate resolves this.`,
      override_possible: false
    };
  }

  // No rules triggered at all
  if (deon.triggered_rules.length === 0) {
    return {
      agent: "synthesizer",
      decision: "ALLOWED",
      final_weight: 0,
      threshold_for_action: 7.0,
      tier1_triggered: false,
      summary: "No rules triggered. Action is fully permitted.",
      override_possible: false
    };
  }

  // Detect ETHICAL_DILEMMA: Deontologist DENY + at least one ALLOW + weights close
  const deonDeny = deon.vote === "DENY";
  const contextAllow = context_r.vote === "ALLOW" || devil.vote === "ALLOW";
  const weightDelta = Math.abs(deon.max_weight - (context_r.total_weight_reduction + devil.total_challenge_penalty));

  if (deonDeny && contextAllow && weightDelta <= 1.5 && !deon.has_tier1_violation) {
    const conflictingRules = deon.triggered_rules.map(r => r.rule_id);
    return {
      agent: "synthesizer",
      decision: "ETHICAL_DILEMMA",
      final_weight: baseWeight,
      threshold_for_action: 7.0,
      tier1_triggered: false,
      conflicting_rules: conflictingRules,
      weight_delta: weightDelta,
      summary: `Ethical dilemma detected. Rules ${conflictingRules.join(", ")} conflict with contextual mitigations. Weight delta: ${weightDelta.toFixed(2)} — too close to decide autonomously.`,
      ui_prompt: `This action triggered a conflict between principles [${conflictingRules.join(", ")}]. The system has no clear logical basis to decide autonomously. Please review the reasoning and select an option.`,
      override_possible: true
    };
  }

  // Standard threshold decision
  const THRESHOLD = 7.0;
  let decision;
  if (baseWeight >= THRESHOLD) {
    decision = "BLOCKED";
  } else if (baseWeight >= 5.0) {
    decision = "ALLOWED_WITH_RESTRICTIONS";
  } else {
    decision = "ALLOWED";
  }

  return {
    agent: "synthesizer",
    decision,
    final_weight: baseWeight,
    threshold_for_action: THRESHOLD,
    tier1_triggered: false,
    summary: `Final weight: ${baseWeight}. Decision: ${decision}.`,
    override_possible: decision === "ALLOWED_WITH_RESTRICTIONS"
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// ETHICAL LOGGER
// Produces the full reasoning log for the Public Ledger and UI panel.
// ─────────────────────────────────────────────────────────────────────────────

function buildReasoningLog(action, ctx, deon, context_r, devil, synth, ontology) {
  const triggeredConsensus = deon.triggered_rules.map(r => {
    const rule = ontology.rules.find(or => or.id === r.rule_id);
    return rule ? `${r.rule_id} — ${rule.name}` : r.rule_id;
  });

  return {
    sem_version: ontology._meta.version,
    timestamp: new Date().toISOString(),
    action: {
      module: action.module,
      type: action.action,
      joules: action.joules || 0
    },
    context_signals: {
      involves_life_support: ctx.involves_life_support,
      thermal_violation: ctx.thermal_violation,
      metabolic_violation: ctx.metabolic_violation,
      emergency_flag: ctx.emergency_flag,
      declared_intent: ctx.declared_intent,
      role_context: ctx.role_context
    },
    triggered_consensus: triggeredConsensus,
    debate_summary: [
      `DEONTOLOGIST: ${deon.summary}`,
      `CONTEXTUALIZER: ${context_r.summary}`,
      `DEVIL'S ADVOCATE: ${devil.summary}`
    ].join(" | "),
    agents_votes: {
      deontologist: deon.vote,
      contextualizer: context_r.vote,
      devils_advocate: devil.vote
    },
    final_weight_calculated: synth.final_weight,
    threshold_for_action: synth.threshold_for_action,
    decision: synth.decision,
    tier1_triggered: synth.tier1_triggered,
    ethical_dilemma: synth.decision === "ETHICAL_DILEMMA",
    ui_prompt: synth.ui_prompt || null,
    override_possible: synth.override_possible,
    full_reasoning: {
      deontologist: deon.reasoning,
      contextualizer: context_r.reasoning,
      devils_advocate: devil.reasoning
    }
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// PUBLIC API
// ─────────────────────────────────────────────────────────────────────────────

/**
 * EthicalDebater — main class for integration with CerebrusEngine.
 *
 * Usage in engine.js:
 *
 *   import { EthicalDebater } from "../sem-v2/ethical-debater.js";
 *   const debater = new EthicalDebater();
 *   await debater.init();
 *
 *   // Before _tick():
 *   const ethics = await debater.evaluateAction(
 *     { module: "housing", action: "house_assignment", joules: 500 },
 *     { description: "Assign house to family #042", emergency: false }
 *   );
 *
 *   if (ethics.decision === "BLOCKED") return ethics;
 *   if (ethics.decision === "ETHICAL_DILEMMA") return ethics; // UI handles this
 *   // else proceed with _tick()
 */
export class EthicalDebater {
  constructor() {
    this._ontology = null;
    this._ready = false;
    this.evaluation_count = 0;
    this.blocked_count = 0;
    this.dilemma_count = 0;
  }

  async init() {
    this._ontology = await loadOntology();
    this._ready = true;
    console.log(`[SEM Debater v${this._ontology._meta.version}] Ready. ${this._ontology.rules.length} rules loaded.`);
    return this;
  }

  get isReady() { return this._ready; }
  get ontologyVersion() { return this._ontology?._meta?.version || "unknown"; }
  get stats() {
    return {
      total_evaluations: this.evaluation_count,
      blocked: this.blocked_count,
      dilemmas: this.dilemma_count,
      allowed: this.evaluation_count - this.blocked_count - this.dilemma_count
    };
  }

  /**
   * Main evaluation entry point.
   * @param {Object} action  - { module, action, joules }
   * @param {Object} payload - arbitrary context from the calling module
   * @returns {Object} reasoning_log with .decision field
   */
  async evaluateAction(action, payload = {}) {
    if (!this._ready) {
      console.warn("[SEM Debater] Not initialised — call init() first. Allowing action by default.");
      return { decision: "ALLOWED", warning: "Debater not initialised" };
    }

    this.evaluation_count++;

    const rules = this._ontology.rules;
    const ctx = analyseContext(action, payload);

    // Run the Mini-Parliament
    const deon = deontologist(rules, ctx);
    const context_r = contextualizer(rules, ctx, deon);
    const devil = devilsAdvocate(rules, ctx, deon);
    const synth = synthesizer(rules, ctx, deon, context_r, devil);

    // Build full reasoning log
    const log = buildReasoningLog(action, ctx, deon, context_r, devil, synth, this._ontology);

    if (log.decision === "BLOCKED") this.blocked_count++;
    if (log.decision === "ETHICAL_DILEMMA") this.dilemma_count++;

    return log;
  }

  /**
   * Convenience: evaluate with a simple text description.
   * Useful for testing and the SEM Quorum UI.
   */
  async evaluateText(module, actionName, description, options = {}) {
    return this.evaluateAction(
      { module, action: actionName, joules: options.joules || 0 },
      { description, intent: options.intent, role: options.role, emergency: options.emergency || false }
    );
  }

  /**
   * Get full ontology for UI display.
   */
  getOntology() {
    return this._ontology;
  }

  /**
   * Get only rules of a given tier.
   */
  getRulesByTier(tier) {
    return (this._ontology?.rules || []).filter(r => r.tier === tier);
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// EMBEDDED FALLBACK ONTOLOGY
// Minimal version of the rules used if network fetch fails.
// ─────────────────────────────────────────────────────────────────────────────

function _embeddedFallbackOntology() {
  return {
    _meta: { version: "2.0.0-fallback", schema: "SEM-Ethical-Ontology" },
    rules: [
      {
        id: "AX-07", name: "Axiom 07 — Biological Survival Envelope",
        tier: 1, weight_base: 10.0, category: "Biological Survival",
        triggers: ["thermal_violation", "metabolic_violation"],
        conditions_exception: []
      },
      {
        id: "AX-09", name: "Axiom 09 — Life Primacy",
        tier: 1, weight_base: 10.0, category: "Biological Survival",
        triggers: ["energy_allocation_over_life_support"],
        conditions_exception: []
      },
      {
        id: "AX-00", name: "Axiom 00 — Systemic Humility",
        tier: 1, weight_base: 9.0, category: "Protocol Integrity",
        triggers: ["circular_self_validation"],
        conditions_exception: []
      },
      {
        id: "PRIV-001", name: "Privacy Protection",
        tier: 2, weight_base: 4.5, category: "Rights",
        triggers: ["surveillance_without_consent"],
        conditions_exception: [
          { condition: "Explicit informed consent", weight_adjustment: -2.5 }
        ]
      },
      {
        id: "AUDIT-001", name: "Audit Trail Integrity",
        tier: 2, weight_base: 4.0, category: "Transparency",
        triggers: ["audit_entry_deleted"],
        conditions_exception: []
      },
      {
        id: "AUTO-001", name: "Autonomy Space",
        tier: 3, weight_base: 1.0, category: "Autonomy",
        triggers: ["protocol_overreach"],
        conditions_exception: []
      }
    ]
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// SINGLETON EXPORT for direct use without class instantiation
// ─────────────────────────────────────────────────────────────────────────────

let _singletonDebater = null;

export async function getDebater() {
  if (!_singletonDebater) {
    _singletonDebater = new EthicalDebater();
    await _singletonDebater.init();
  }
  return _singletonDebater;
}
