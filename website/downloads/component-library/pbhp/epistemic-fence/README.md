# Epistemic Fence

**Project:** Pause Before Harm  
**Category:** Operating controls  
**Kind:** Claim boundary  
**Component library version:** 1.0.0  
**Component source version:** PBHP/Shadow operating control / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Requires a complete disclosure of scope, evidence, uncertainty, and limits around consequential conclusions.

## Mechanism

The fence prevents inference from escaping its supported scope. Missing required blocks is a failure, not a stylistic choice.

## Inputs

- Claim
- Evidence
- Inference path
- Known limits
- Decision stakes

## Required outputs

- Scoped claim
- Uncertainty statement
- Unverified items
- Prohibited extrapolations

## Known failure modes

- Overgeneralization
- Missing scope
- Unknowns omitted
- Unsupported superlative or guarantee

## Current test state

Specified; annotation consistency and outcome value remain open.

## Next tests

- Create claim-boundary challenge sets
- Measure unsupported extrapolation
- Test legal, scientific, and safety-critical domains

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/evidence/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
