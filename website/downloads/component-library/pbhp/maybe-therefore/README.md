# Maybe / Therefore

**Project:** Pause Before Harm  
**Category:** Protocol gates  
**Kind:** Adversarial reasoning gate  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Observed + adverse

## Summary

Requires the strongest honest case against the preferred action before the final decision rationale.

## Mechanism

Maybe articulates why the action could be wrong, unfair, premature, unsafe, or unsupported. Therefore explains why the resulting action state follows. A token objection or straw man fails the gate.

## Inputs

- Preferred action
- Evidence
- Counterevidence
- Affected-party perspective

## Required outputs

- Substantive Maybe
- Evidence-bound Therefore
- Decision state

## Known failure modes

- Ceremonial objection
- Straw man
- Rhetorical flourish
- Therefore that ignores the Maybe

## Current test state

The mechanism is specified and used in behavioral work, but earlier aggregate ablation did not isolate its independent contribution.

## Next tests

- Score Maybe quality with blinded humans
- Run placebo-controlled ablations
- Measure approval preservation on safe controls
- Test whether Therefore addresses the strongest objection

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/protocol/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
