# Test Plan — Runtime Step 8: Maybe / Therefore

**Project:** shadow  
**Component:** `maybe-therefore-runtime`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

Implemented, but earlier aggregate ablation did not isolate its independent effect; better component-specific tests are required.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: Maybe
- [ ] Produces or preserves: Therefore
- [ ] Produces or preserves: Pass or hold
- [ ] Produces or preserves: Drift finding

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Token objection
- [ ] Detects or blocks: Countercase ignored
- [ ] Detects or blocks: Rhetorical Maybe
- [ ] Detects or blocks: Formatting bypass

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

- [ ] Human-grade Maybe quality
- [ ] Placebo-controlled ablation
- [ ] Test safe-control approval preservation

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
