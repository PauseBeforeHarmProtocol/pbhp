# Who Pays First

**Project:** Pause Before Harm  
**Category:** Protocol gates  
**Kind:** Stakeholder analysis  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Forces the decision to begin with the person or group that bears the first cost if it is wrong.

## Mechanism

The operator names the first affected stakeholder, the type and timing of harm, the recovery path, and the evidence supporting that judgment. The analysis privileges actual exposure over institutional convenience.

## Inputs

- Affected parties
- Failure scenario
- Timing
- Recovery options

## Required outputs

- First-cost stakeholder
- First harm
- Recovery path
- Evidence basis

## Known failure modes

- Centering the decision-maker
- Using abstract stakeholders
- Ignoring delayed or distributed harm
- Assuming recovery without a mechanism

## Current test state

Specified and used across the protocol; human field reliability remains open.

## Next tests

- Compare expert and non-expert stakeholder identification
- Test hidden and delayed harms
- Measure whether the component changes mitigation selection

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/protocol/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
