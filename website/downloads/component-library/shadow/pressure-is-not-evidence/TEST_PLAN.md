# Test Plan — Pressure Is Not Evidence / The Anvil

**Project:** shadow  
**Component:** `pressure-is-not-evidence`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

Screen-grade multi-turn experiments report reduced caving relative to bare and firmness-placebo conditions; human grading and larger independent replication remain open.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: Hold or revise based on evidence
- [ ] Produces or preserves: Caving metric
- [ ] Produces or preserves: Over-caution metric

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Stubborn refusal
- [ ] Detects or blocks: Pressure mistaken for evidence
- [ ] Detects or blocks: Length placebo
- [ ] Detects or blocks: Correct approval suppressed

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

- [ ] Complete blinded human grading
- [ ] Larger cross-model preregistered study
- [ ] Safe-control approval tests
- [ ] Independent reproduction

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
