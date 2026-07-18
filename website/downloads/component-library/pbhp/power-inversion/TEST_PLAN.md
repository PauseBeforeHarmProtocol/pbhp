# Test Plan — Power Inversion

**Project:** pbhp  
**Component:** `power-inversion`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

Specified, but an earlier aggregate ablation battery did not isolate its contribution; better discriminating tests are required.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: Power finding
- [ ] Produces or preserves: Missing protections
- [ ] Produces or preserves: Forced risk floor
- [ ] Produces or preserves: Required safeguard or review

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Fictional consent
- [ ] Detects or blocks: Appeal that cannot change the result
- [ ] Detects or blocks: Exit with punitive cost
- [ ] Detects or blocks: Selective weighting that lowers the floor

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

- [ ] Run targeted ablations on power-asymmetric cases
- [ ] Measure false positives on genuinely balanced cases
- [ ] Use independent human scoring of notice, voice, consent, appeal, exit, and repair

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
