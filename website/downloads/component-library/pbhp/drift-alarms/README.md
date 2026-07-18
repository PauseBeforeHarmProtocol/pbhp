# Drift Alarms

**Project:** Pause Before Harm  
**Category:** Operating controls  
**Kind:** Monitoring control  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Names recurring phrases and behaviors that indicate rationalization, compliance theater, or pressure-driven degradation.

## Mechanism

A drift alarm increases scrutiny and records the pattern. It cannot be suppressed merely because the operator is senior or the deadline is near.

## Inputs

- Decision language
- Override attempts
- Repeated pressure
- Receipt history

## Required outputs

- Drift finding
- Risk escalation
- Calibration or CAPA trigger

## Known failure modes

- Normalizing alarm phrases
- Suppressing alerts
- Using alarms as personality judgments
- Alert fatigue

## Current test state

Specified; precision, recall, and alert-fatigue calibration remain open.

## Next tests

- Create labeled drift and non-drift corpora
- Measure false-alarm burden
- Test adversarial paraphrases
- Review whether alarms improve decisions

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/operations/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
