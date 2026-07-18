# Test Plan — Compression Honesty

**Project:** pbhp  
**Component:** `compression-honesty`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

Specified; controlled evaluation of information loss remains open.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: Compressed output
- [ ] Produces or preserves: No-drops list
- [ ] Produces or preserves: Omissions disclosure

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Caveat stripping
- [ ] Detects or blocks: Refusal softened into advice
- [ ] Detects or blocks: Adverse evidence omitted
- [ ] Detects or blocks: Summary treated as source

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

- [ ] Build compression fidelity tests
- [ ] Score preservation of blockers and evidence states
- [ ] Test extreme length constraints

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
