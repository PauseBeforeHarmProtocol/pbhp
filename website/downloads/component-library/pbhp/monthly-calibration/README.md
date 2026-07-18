# Monthly Calibration

**Project:** Pause Before Harm  
**Category:** Operating controls  
**Kind:** Calibration process  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Samples decisions over time to compare thresholds, evidence use, overrides, and outcomes.

## Mechanism

A defined sample of receipts is reviewed on a recurring cycle. A missed calibration is itself a finding rather than an invisible lapse.

## Inputs

- Receipt sample
- Decision outcomes
- Overrides
- Operator and domain context

## Required outputs

- Calibration record
- Threshold adjustments
- Training actions
- CAPA or effectiveness check

## Known failure modes

- Cherry-picked samples
- No adverse cases
- Untracked threshold changes
- Calibration without effectiveness review

## Current test state

Specified; longitudinal operational evidence remains open.

## Next tests

- Define sampling plans by risk
- Measure operator drift over time
- Track correction effectiveness
- Use an independent reviewer for high-risk samples

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/operations/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
