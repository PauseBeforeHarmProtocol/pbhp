# Test Plan — Monthly Calibration

**Project:** pbhp  
**Component:** `monthly-calibration`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

Specified; longitudinal operational evidence remains open.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: Calibration record
- [ ] Produces or preserves: Threshold adjustments
- [ ] Produces or preserves: Training actions
- [ ] Produces or preserves: CAPA or effectiveness check

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Cherry-picked samples
- [ ] Detects or blocks: No adverse cases
- [ ] Detects or blocks: Untracked threshold changes
- [ ] Detects or blocks: Calibration without effectiveness review

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

- [ ] Define sampling plans by risk
- [ ] Measure operator drift over time
- [ ] Track correction effectiveness
- [ ] Use an independent reviewer for high-risk samples

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
