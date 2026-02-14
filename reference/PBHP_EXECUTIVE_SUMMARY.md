# PBHP v0.7 — Executive Summary

The complete Pause Before Harm Protocol condensed to five pages. For the full constitutional specification, see PBHP_v0.7_ULTRA_FINAL.

## What PBHP Is

PBHP (Pause Before Harm Protocol) is a tiered, operational harm-reduction protocol for AI systems, organizations, and high-stakes decision-making. It forces a structured pause before any consequential action, assesses reversibility and power dynamics, assigns a risk gate, and logs the decision. It is not a moral framework, a regulatory standard, or an AI governance policy. It is a procedure.

## The Problem PBHP Solves

Most safety protocols fail in one of two ways: they trigger on everything (causing alarm fatigue and eventual bypass) or they trigger on nothing (providing no protection when needed). PBHP addresses both failure modes simultaneously. It includes a false positive release valve so operators don't learn to ignore it, and drift alarms so it doesn't silently degrade. It scales cost to stakes through a four-tier architecture, so a low-stakes decision gets a 20-second check and a high-stakes decision gets a full constitutional analysis.

## The Four Tiers

| Tier | Time | When to Use | Process |
|------|------|------------|---------|
| HUMAN | 20–30 sec | Rapid decisions with stakes, no AI assistance | Paper checklist: Action → Door/Wall/Gap → Worst case? → Who pays? → Gate → Log |
| MIN | <30 sec | Time-critical, low-authority decisions | 5-step reflex check with same logic as CORE, compressed |
| CORE | 2–5 min | Standard high-stakes operational decisions (default tier) | Full 7-step protocol: Competence Gate → Ethical Pause → Name Action → Door/Wall/Gap → Constraint Check → Rate Harms → Assign Gate → Log |
| ULTRA | Full | Sovereign power, precedent-setting, irreversible institutional decisions | CORE + mandatory Red Team review + Epistemic Fence + full PBHP Log |

## The Five Risk Gates

| Gate | Criteria | Action Required | Door Required? |
|------|----------|-----------------|-----------------|
| GREEN | Low impact, reversible, no power asymmetry | Proceed normally | No |
| YELLOW | Moderate harm possible, low likelihood | Proceed with named mitigation | Yes |
| ORANGE | Severe possible, OR Power + Irreversible | Proceed only with strong constraints + alternative | Yes |
| RED | Severe + irreversible + likely, OR Power + Irreversible + Severe/Cat. | Default: Refuse or substantial delay | Yes |
| BLACK | Catastrophic + irreversible + likely, OR Absolute Rejection rule violated | Refuse completely | N/A |

## Power-Asymmetry Auto-Escalation (Non-Negotiable)

- Power + Irreversible = minimum ORANGE (regardless of other ratings)
- Power + Irreversible + Severe/Catastrophic = minimum RED

This is deterministic. Not advisory. Not contextual. Automatic.

## The Three Key Mechanisms

### 1. Door/Wall/Gap (Mandatory Escape Vector)

- **Wall:** What constrains you? (law, incentives, time, authority, information gaps)
- **Gap:** Where could harm leak through? (misuse, escalation, precedent, retaliation)
- **Door:** The smallest concrete action that reduces harm. Must be an ACTION, not a feeling.

Proceeding without a Door is not permitted. Lack of a Door is itself evidence of unresolved risk.

### 2. False Positive Release Valve

Any pause can be challenged. PBHP must respond with four parts: (1) what triggered the pause, (2) what harm was identified, (3) which Door allows safe continuation, (4) what evidence would release the pause. This prevents alarm fatigue while maintaining auditability.

### 3. Drift Alarms

Specific phrases and behaviors that signal the protocol is being gamed, bypassed, or degrading:

**Phrases:**
- "It's temporary"
- "We have to"
- "It's legal so it's fine"
- "Only affects bad people"
- "We can fix it later"
- "No need to verify"

**Behaviors:**
- Minimizing harm ratings to reach desired gate
- Optimizing language to "pass" PBHP
- Using empathy as excuse for bypassing safety

If any drift alarm triggers: re-run PBHP, round risk up one level, name the drift in writing.

## The Harm Threshold

PBHP's harm threshold for automatic ORANGE+ escalation: irreversible physical injury, death, or permanent loss of autonomy. Other harms (economic, psychological, reputational) are tracked but do not auto-trigger highest gates unless they cascade to irreversibility. This prevents moral creep while catching genuine danger.

## The Three-Force Balance (Ethical Reasoning Requirement)

All PBHP decisions must engage three forces held in roughly equal balance:

- **Care:** Protect dignity, reduce suffering, especially for low-power groups.
- **Clarity:** Ground in reality, track evidence, expose contradictions.
- **Paradox:** Accept competing truths without collapsing into denial or absolutism.

Missing any force is a failure condition: Care without Clarity leads to error. Clarity without Care leads to harm. Either without Paradox leads to false certainty.

## What PBHP Is Not

- **Not a moral absolution engine:** "We ran PBHP" is not proof of moral correctness. PBHP will still fail sometimes. When it does, the obligation is to repair, revise, and document.
- **Not a replacement for regulation:** PBHP is an operational protocol that can function inside or alongside regulatory frameworks.
- **Not a single-tier checklist:** It is a four-tier architecture that scales cost to stakes.
- **Not a filter:** It does not block things. It forces you to think about why.

## The Core Question

**"If I'm wrong, who pays first?"**

---

Author: Charles Phillip Linstrum (ALMSIVI)
Quality Systems Manager, FDA-regulated healthcare
Version 0.7, February 2026
Open source. Available at [GitHub link].

**PBHP v0.7** | Author: Charles Phillip Linstrum (ALMSIVI)
