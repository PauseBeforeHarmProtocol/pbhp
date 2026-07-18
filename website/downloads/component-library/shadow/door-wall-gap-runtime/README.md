# Runtime Step 2: Door / Wall / Gap

**Project:** Project Shadow  
**Category:** Runtime processes  
**Kind:** Runtime classification  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Promotes unclear and missing evidence to first-class runtime states.

## Mechanism

The runtime classifies the route and grades Door quality. It does not silently convert uncertainty into permission.

## Inputs

- Canonical action
- Constraints
- Evidence
- Known unknowns

## Required outputs

- Door quality
- Wall
- Gap
- Required next evidence or alternate route

## Known failure modes

- Defaulting unclear to proceed
- Low-quality Door treated as sufficient
- Wall override by preference
- Untracked state transition

## Current test state

Classification is implemented and contract-tested; external calibration remains open.

## Next tests

- Boundary-case corpus
- Metamorphic state-transition tests
- Human comparison on ambiguous cases

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/runtime/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
