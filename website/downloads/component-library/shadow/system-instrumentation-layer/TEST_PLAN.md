# Test Plan — System Instrumentation Layer

**Project:** shadow  
**Component:** `system-instrumentation-layer`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

The panel reports 28 gauges and 519 built-in checks; threshold calibration and external validation remain open.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: 28 gauge states
- [ ] Produces or preserves: Critical-floor action
- [ ] Produces or preserves: Stakes-aware disclosure
- [ ] Produces or preserves: Receipt snapshot

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Global green
- [ ] Detects or blocks: Gauge averaging
- [ ] Detects or blocks: Estimated state presented as measured
- [ ] Detects or blocks: Override of critical floor

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

- [ ] Independent code and contract review
- [ ] Threshold calibration
- [ ] Cross-model adapters
- [ ] Human comprehension testing
- [ ] Production telemetry integration

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
