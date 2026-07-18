# Test Plan — Runtime Step 00.5: Provenance Bind

**Project:** shadow  
**Component:** `provenance-bind`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

Built-in provenance contracts and declaration-neutrality batteries are reported; independent reproduction remains open.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: ATTESTED
- [ ] Produces or preserves: DECLARED
- [ ] Produces or preserves: ASSERTED
- [ ] Produces or preserves: Downgrade or refusal state

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Declaration laundering
- [ ] Detects or blocks: Fabricated evidence hash
- [ ] Detects or blocks: Bare assertion used as authority
- [ ] Detects or blocks: Unbound steering field

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

- [ ] Reproduce declaration-neutrality results
- [ ] Test evidence-hash collisions and near misses
- [ ] Run adversarial source-laundering cases

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
