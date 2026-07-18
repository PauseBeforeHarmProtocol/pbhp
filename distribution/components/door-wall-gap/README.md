# Door / Wall / Gap

**Project:** Pause Before Harm  
**Category:** Protocol gates  
**Kind:** Classification  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Makes legitimate routes, binding blockers, and unresolved uncertainty distinct decision states.

## Mechanism

A Door is a sufficiently safe route forward; a Wall blocks the proposed form; a Gap records missing evidence or a route through which harm can escape. A Gap cannot be upgraded by urgency or confidence alone.

## Inputs

- Concrete action
- Known constraints
- Available evidence
- Unresolved questions

## Required outputs

- Door
- Wall
- Gap
- Reason and evidence basis

## Known failure modes

- Calling uncertainty a Door
- Treating a Wall as inconvenience
- Collapsing multiple routes into one
- Silent reclassification

## Current test state

The classification contract is specified; calibration and cross-rater reliability remain open.

## Next tests

- Create boundary cases between Gap and Wall
- Measure classification stability across reviewers
- Test whether new evidence moves states in the intended direction

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/protocol/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
