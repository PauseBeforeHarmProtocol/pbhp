# Context Load Audit

**Project:** Pause Before Harm  
**Category:** Extensions and tools  
**Kind:** Operating-state extension  
**Component library version:** 1.0.0  
**Component source version:** PBHP CLA / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Discloses whether an AI system has enough trustworthy context for the stakes of the requested work.

## Mechanism

The audit distinguishes measured, estimated, declared, and unknown context state; applies stakes-aware thresholds; records overrides; and routes critical load or uncertainty to refresh, recovery, or refusal.

## Inputs

- Context state
- Compaction or memory state
- Stakes
- Source coverage
- Override request

## Required outputs

- Disclosure
- Refresh or recovery action
- Proceed condition
- Override record

## Known failure modes

- Self-report presented as measurement
- High-stakes work under unknown load
- Silent compaction
- Override without record

## Current test state

Extension is specified and linked to SIL; calibration and external validation remain open.

## Next tests

- Calibrate thresholds by task and model
- Compare measured and estimated states
- Test compaction recovery
- Measure false refusals

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/cla/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
