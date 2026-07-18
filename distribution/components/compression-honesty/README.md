# Compression Honesty

**Project:** Pause Before Harm  
**Category:** Operating controls  
**Kind:** Communication control  
**Component library version:** 1.0.0  
**Component source version:** PBHP/Shadow operating control / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Prevents a shortened answer from silently dropping decision-critical caveats, blockers, or adverse evidence.

## Mechanism

Every compressed representation keeps a no-drops list or explicitly names what has been omitted. A short version cannot reverse the governing decision state.

## Inputs

- Full analysis
- Audience
- Length constraint
- Decision-critical items

## Required outputs

- Compressed output
- No-drops list
- Omissions disclosure

## Known failure modes

- Caveat stripping
- Refusal softened into advice
- Adverse evidence omitted
- Summary treated as source

## Current test state

Specified; controlled evaluation of information loss remains open.

## Next tests

- Build compression fidelity tests
- Score preservation of blockers and evidence states
- Test extreme length constraints

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/operations/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
