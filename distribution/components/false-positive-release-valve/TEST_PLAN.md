# Test Plan — False Positive Release Valve

**Project:** pbhp  
**Component:** `false-positive-release-valve`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

Specified; false-positive rates and challenge quality need prospective measurement.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: Release with rationale
- [ ] Produces or preserves: Continued hold
- [ ] Produces or preserves: Calibration finding
- [ ] Produces or preserves: Protocol improvement request

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Wear-down
- [ ] Detects or blocks: Repeating the same claim
- [ ] Detects or blocks: Treating urgency as evidence
- [ ] Detects or blocks: Challenge without a safer Door

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

- [ ] Measure release precision and recall
- [ ] Test repeated-pressure attacks
- [ ] Review challenge outcomes during calibration

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
