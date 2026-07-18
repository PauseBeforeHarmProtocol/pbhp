# Runtime Step 10: CAPA and Open Question Ledger

**Project:** Project Shadow  
**Category:** Runtime processes  
**Kind:** Learning process  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Makes failures and decision-critical unknowns durable until corrected, answered, or explicitly retired.

## Mechanism

CAPA owns correction and effectiveness; the OQL types unknowns and escalates them rather than allowing fluent summaries to erase them.

## Inputs

- Failure
- Unknown
- Owner
- Due date
- Effectiveness criterion

## Required outputs

- CAPA record
- Open-question state
- Escalation
- Verified closure or continued hold

## Known failure modes

- Unknown decays into silence
- Closure without effectiveness
- No owner
- Narrative defense

## Current test state

Process is specified; long-term operational performance remains open.

## Next tests

- Track unknown aging
- Audit closure evidence
- Measure recurrence and correction latency

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/runtime/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
