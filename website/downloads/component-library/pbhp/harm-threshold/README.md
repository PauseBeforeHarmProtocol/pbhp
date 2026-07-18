# Harm Threshold

**Project:** Pause Before Harm  
**Category:** Protocol gates  
**Kind:** Risk classification  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Classifies the decision from GREEN through BLACK according to harm, reversibility, power, and who pays.

## Mechanism

The most serious applicable condition governs. Later confidence, authority, or preference cannot ratchet a binding floor downward.

## Inputs

- Magnitude of harm
- Reversibility
- Power asymmetry
- Dignity and autonomy
- Who pays first

## Required outputs

- GREEN
- YELLOW
- ORANGE
- RED
- BLACK
- Rationale and governing factor

## Known failure modes

- Severity averaging
- Optimistic re-rating
- Ignoring low-probability catastrophic outcomes
- Using organizational status as a discount

## Current test state

The ladder and escalation semantics are specified; thresholds still require domain calibration and independent validation.

## Next tests

- Build domain-specific calibration sets
- Measure inter-rater threshold agreement
- Test monotonic escalation and prohibited downgrades

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/risk/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
