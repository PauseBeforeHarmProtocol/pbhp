# Test Plan — Harm Threshold

**Project:** pbhp  
**Component:** `harm-threshold`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

The ladder and escalation semantics are specified; thresholds still require domain calibration and independent validation.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: GREEN
- [ ] Produces or preserves: YELLOW
- [ ] Produces or preserves: ORANGE
- [ ] Produces or preserves: RED
- [ ] Produces or preserves: BLACK
- [ ] Produces or preserves: Rationale and governing factor

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Severity averaging
- [ ] Detects or blocks: Optimistic re-rating
- [ ] Detects or blocks: Ignoring low-probability catastrophic outcomes
- [ ] Detects or blocks: Using organizational status as a discount

### 3. Component ablation

- [ ] Compare the full system with this component removed.
- [ ] Use a placebo or length-matched control where applicable.
- [ ] Confirm the battery can discriminate a deliberately sabotaged implementation.
- [ ] Measure both missed harms and over-caution on genuinely safe controls.

### 4. Cross-implementation and cross-model reproduction

- [ ] Run on at least one materially different implementation or model family.
- [ ] Freeze prompts, versions, scoring, and expected outputs before execution.
- [ ] Retain null, adverse, and contradictory results.

### 5. Human and field validation

- [ ] Use blinded human grading where the construct depends on judgment.
- [ ] Measure inter-rater agreement and adjudication rules.
- [ ] Evaluate burden, usability, accessibility, override behavior, and downstream outcomes.
- [ ] Obtain materially independent review before making external-validation claims.

## Component-specific next work

- [ ] Build domain-specific calibration sets
- [ ] Measure inter-rater threshold agreement
- [ ] Test monotonic escalation and prohibited downgrades

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
