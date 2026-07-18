# Test Plan — Runtime Step 9: Write-Ahead Receipt

**Project:** shadow  
**Component:** `write-ahead-receipt`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

Receipt and seal behavior are included in built-in verification; production key infrastructure and independent audit remain open.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: Write-ahead receipt
- [ ] Produces or preserves: Hash chain
- [ ] Produces or preserves: Authorization state
- [ ] Produces or preserves: Wall on write failure

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: After-the-fact logging
- [ ] Detects or blocks: Broken chain
- [ ] Detects or blocks: Receipt mismatch
- [ ] Detects or blocks: Execution despite write failure

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

- [ ] Tamper and replay tests
- [ ] Production-grade signature infrastructure
- [ ] Independent chain audit
- [ ] Execution-to-receipt linkage

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
