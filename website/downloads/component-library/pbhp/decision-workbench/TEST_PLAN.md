# Test Plan — Decision Workbench

**Project:** pbhp  
**Component:** `decision-workbench`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

DOM, selector, JavaScript syntax, and receipt-output contracts pass; authenticated usability and accessibility QA remain open.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: Draft decision state
- [ ] Produces or preserves: Routing notes
- [ ] Produces or preserves: Downloadable JSON receipt

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Treating the router as authorization
- [ ] Detects or blocks: Incomplete fields
- [ ] Detects or blocks: Local data lost before download
- [ ] Detects or blocks: Rules mistaken for domain judgment

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

- [ ] Run keyboard and screen-reader QA
- [ ] Conduct usability sessions
- [ ] Test edge cases and state persistence
- [ ] Verify production privacy behavior

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
