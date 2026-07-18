# Test Plan — Decision States

**Project:** pbhp  
**Component:** `decision-states`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

The state contract is specified; cross-implementation consistency remains open.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: One named decision state
- [ ] Produces or preserves: Conditions attached to the state
- [ ] Produces or preserves: Owner and next action

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Ambiguous advice
- [ ] Detects or blocks: Proceed language inside a refusal
- [ ] Detects or blocks: Mitigations without enforcement
- [ ] Detects or blocks: Delay without a decision-critical evidence request

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

- [ ] Test contradictory outputs
- [ ] Measure state consistency across implementations
- [ ] Verify that downstream systems enforce attached conditions

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
