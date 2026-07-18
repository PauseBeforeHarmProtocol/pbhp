# Test Plan — Blind Response Grader

**Project:** shadow  
**Component:** `response-grader`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

The static tool and JavaScript syntax are checked; full human usability, accessibility, and grading reliability remain open.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: Completed score record
- [ ] Produces or preserves: Progress state
- [ ] Produces or preserves: Exportable grading data

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Condition leakage
- [ ] Detects or blocks: Incomplete rubric
- [ ] Detects or blocks: Local state loss
- [ ] Detects or blocks: Machine output mistaken for human grade

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

- [ ] Keyboard and assistive-technology QA
- [ ] Inter-rater reliability study
- [ ] Tamper and condition-leak review

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
