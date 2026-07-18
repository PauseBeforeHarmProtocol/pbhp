# Anchors Ledger

**Project:** Pause Before Harm  
**Category:** Operating controls  
**Kind:** Priority control  
**Component library version:** 1.0.0  
**Component source version:** PBHP/Shadow operating control / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Keeps the least-powerful stakeholder, binding constraints, and decision-critical facts visible throughout a long analysis.

## Mechanism

Anchors are recorded and cannot be silently edited or dropped. A changed anchor requires a visible reason and new evidence.

## Inputs

- Stakeholder priorities
- Binding constraints
- Critical facts
- Version history

## Required outputs

- Anchor set
- Change record
- Drift finding

## Known failure modes

- Silent edit
- Anchor replacement by convenience
- Too many anchors
- Unversioned changes

## Current test state

Specified; long-context and human-workflow performance remain open.

## Next tests

- Test anchor retention under long context
- Measure false drift alarms
- Audit changes against evidence

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/operations/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
