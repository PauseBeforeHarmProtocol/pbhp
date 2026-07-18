# Runtime Step 00: Competence Gate

**Project:** Project Shadow  
**Category:** Runtime processes  
**Kind:** Runtime gate  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Default-denies consequential execution when expertise, context, tools, authority, or independence are critically missing.

## Mechanism

Five honest checks run before substantive reasoning. The result is hard-locked so a later stage cannot retroactively invent competence.

## Inputs

- Task
- Expertise
- Context
- Tools
- Authority
- Independence

## Required outputs

- Pass
- Pass with limits
- Hold or refuse
- Named missing capability

## Known failure modes

- Silent capability gap
- Role inflation
- Tool unavailability ignored
- Conflict hidden

## Current test state

Implemented in the frozen runtime and included in built-in self-tests; external behavioral validation remains open.

## Next tests

- Cross-model competence challenges
- Tool outage and authority spoofing tests
- Independent code review

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/runtime/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
