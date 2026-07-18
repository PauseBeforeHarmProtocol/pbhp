# Runtime Step 8: Maybe / Therefore

**Project:** Project Shadow  
**Category:** Runtime processes  
**Kind:** Hard-locked gate  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Observed + adverse

## Summary

Requires a substantive countercase and evidence-bound conclusion inside the runtime.

## Mechanism

Token Maybes are detected as drift. The gate remains hard-locked so later formatting or operator preference cannot bypass it.

## Inputs

- Preferred decision
- Counterevidence
- Affected-party perspective
- Evidence state

## Required outputs

- Maybe
- Therefore
- Pass or hold
- Drift finding

## Known failure modes

- Token objection
- Countercase ignored
- Rhetorical Maybe
- Formatting bypass

## Current test state

Implemented, but earlier aggregate ablation did not isolate its independent effect; better component-specific tests are required.

## Next tests

- Human-grade Maybe quality
- Placebo-controlled ablation
- Test safe-control approval preservation

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/runtime/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
