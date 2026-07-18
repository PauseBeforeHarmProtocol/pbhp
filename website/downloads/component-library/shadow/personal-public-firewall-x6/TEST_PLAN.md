# Test Plan — X-6 Personal / Public Firewall

**Project:** shadow  
**Component:** `personal-public-firewall-x6`  
**Library version:** 1.0.0  
**Release date:** 2026-07-18

## Current evidence statement

Automated public-boundary scans pass for the release; professional security and privacy review remain open.

## Test levels

### 1. Contract fidelity

- [ ] Produces or preserves: Included public artifact
- [ ] Produces or preserves: Excluded private material
- [ ] Produces or preserves: Boundary scan report

### 2. Negative and adversarial behavior

- [ ] Detects or blocks: Session dump
- [ ] Detects or blocks: Credential leak
- [ ] Detects or blocks: Opaque chat-file dependency
- [ ] Detects or blocks: Personal material included without necessity

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

- [ ] Independent privacy review
- [ ] Secret-scanner expansion
- [ ] Manual artifact-by-artifact publication review

## Promotion rule

Do not promote this component's evidence state merely because the code passes or the output looks persuasive. Promotion requires a preregistered claim, a discriminating test, preserved adverse results, scoped interpretation, and the review authority defined for the applicable release tier.
