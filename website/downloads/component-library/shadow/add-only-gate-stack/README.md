# Runtime Step 5: Add-Only Gate Stack

**Project:** Project Shadow  
**Category:** Runtime processes  
**Kind:** Aggregation invariant  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Aggregates independent checks monotonically: new information may preserve or increase caution, never silently turn refusal into permission.

## Mechanism

Refuse-class results remain refuse-class. Pause, review, capture, or uncertainty may escalate the state; no later gate can wash them out by averaging.

## Inputs

- Individual gate results
- Risk floors
- Review states
- Override request

## Required outputs

- Aggregated gate state
- Escalation reason
- Prohibited downgrade record

## Known failure modes

- Refusal averaging
- Last-gate-wins
- Override without evidence
- Hidden state mutation

## Current test state

Monotonic aggregation is part of the runtime contracts; independent formal verification remains open.

## Next tests

- Property-based monotonicity tests
- Formal model of state transitions
- Adversarial override sequences

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/gates/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
