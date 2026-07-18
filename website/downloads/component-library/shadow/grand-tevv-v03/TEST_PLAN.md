# Test Plan — Grand TEVV v0.3

**Project:** shadow  
**Component:** `grand-tevv-v03`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

Built-in checks passed and limited real-target evidence exists, but the 10-case fusion smoke respected the synthetic BLACK floor in only 6/10 cases; independent validation is open.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: Test reports
- [ ] Produces or preserves: Observed and adverse findings
- [ ] Produces or preserves: Validation status
- [ ] Produces or preserves: Release blockers

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Calling built-in checks independent validation
- [ ] Detects or blocks: Mixing version counts
- [ ] Detects or blocks: Hiding adverse results
- [ ] Detects or blocks: Synthetic evidence treated as field outcome

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

- [ ] Independent reproduction
- [ ] Complete human grading
- [ ] Large real-target corpus
- [ ] External benchmark suites
- [ ] Domain-expert evaluation

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
