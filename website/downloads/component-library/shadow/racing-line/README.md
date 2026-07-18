# Racing Line / Focal Routing

**Project:** Project Shadow  
**Category:** Provenance and instrumentation  
**Kind:** Structural gauge  
**Component library version:** 1.0.0  
**Component source version:** Racing Line v0.2 corrected  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Pins attention to the decision-critical path so long context and narrative drag do not displace binding constraints.

## Mechanism

The gauge is structural rather than behavioral: it records the focal route and flags divergence without claiming the route is morally or factually correct.

## Inputs

- Objective
- Critical constraints
- Current reasoning path
- Context drag

## Required outputs

- Constraint pin
- Divergence signal
- Refocus action

## Known failure modes

- Pinning the wrong objective
- Narrative drift
- Constraint loss
- Focal route treated as truth

## Current test state

Corrected package exists; comparative behavioral and human validation remain open.

## Next tests

- Run long-context focal-drift tests
- Compare with length-matched controls
- Human review of pinned objectives

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/sil/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
