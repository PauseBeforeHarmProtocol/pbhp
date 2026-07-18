# Test Plan — Conscience Audit

**Project:** shadow  
**Component:** `conscience-audit`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

Primitive is specified; behavioral and human reliability remain open.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: Recorded intuition
- [ ] Produces or preserves: Evidence check
- [ ] Produces or preserves: No-authority boundary

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Feeling right equals being right
- [ ] Detects or blocks: Moral urgency
- [ ] Detects or blocks: Identity validation
- [ ] Detects or blocks: Intuition used to override a gate

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

- [ ] Moral-certainty pressure cases
- [ ] Compare intuition-only and evidence-bound decisions
- [ ] Human ethics review

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
