# False Positive Release Valve

**Project:** Pause Before Harm  
**Category:** Operating controls  
**Kind:** Challenge process  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Lets an operator challenge an unnecessary pause without wearing the protocol down through repetition.

## Mechanism

A valid challenge identifies the trigger, the risk, a safer Door, and evidence that would prevent the same false positive next time. Pressure without new evidence is logged as drift.

## Inputs

- Paused decision
- Trigger
- Alternative Door
- New evidence

## Required outputs

- Release with rationale
- Continued hold
- Calibration finding
- Protocol improvement request

## Known failure modes

- Wear-down
- Repeating the same claim
- Treating urgency as evidence
- Challenge without a safer Door

## Current test state

Specified; false-positive rates and challenge quality need prospective measurement.

## Next tests

- Measure release precision and recall
- Test repeated-pressure attacks
- Review challenge outcomes during calibration

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/operations/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
