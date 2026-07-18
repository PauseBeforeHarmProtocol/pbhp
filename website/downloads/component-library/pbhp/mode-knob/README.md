# Mode Knob

**Project:** Pause Before Harm  
**Category:** Operating controls  
**Kind:** Interaction control  
**Component library version:** 1.0.0  
**Component source version:** PBHP/Shadow operating control / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Makes the intended reasoning posture explicit: explore, compress, or do both.

## Mechanism

The operator chooses whether to broaden possibilities, produce a concise operational result, or preserve both stages. The mode may shape presentation but cannot relax a binding gate.

## Inputs

- Task
- Stakes
- Audience
- Requested mode

## Required outputs

- EXPLORE
- COMPRESS
- BOTH
- Mode-bound output

## Known failure modes

- Compression before inspection
- Exploration without closure
- Mode used to bypass a refusal
- Unstated mode switch

## Current test state

Specified as a control surface; comparative usability evidence remains open.

## Next tests

- Compare error rates by mode
- Test mode-switch transparency
- Measure user comprehension and decision quality

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/operations/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
