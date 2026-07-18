# Test Plan — X-7 Challengeability

**Project:** shadow  
**Component:** `challengeability-x7`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

Invariant is specified; operational independent-review infrastructure remains open.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: Accepted, rejected, or unresolved challenge
- [ ] Produces or preserves: Correction or hold
- [ ] Produces or preserves: Audit trail

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Maintainer exemption
- [ ] Detects or blocks: Same-model review called independent
- [ ] Detects or blocks: Challenge without power to block
- [ ] Detects or blocks: Retaliatory governance

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

- [ ] Define independence criteria
- [ ] Run external red-team and reproduction
- [ ] Test maintainer-conflict scenarios

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
