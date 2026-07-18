# Competence and Honest-Use Gate

**Project:** Pause Before Harm  
**Category:** Protocol gates  
**Kind:** Gate  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Checks whether the decision-maker has the expertise, context, tools, authority, and independence needed to evaluate the action honestly.

## Mechanism

The gate names missing capability, conflicts, time pressure, and requests for endorsement without inspection. A critical missing capability blocks authorization instead of becoming an invisible caveat.

## Inputs

- Proposed action
- Available expertise and tools
- Authority and role
- Conflicts, pressure, and missing context

## Required outputs

- competent
- competent_with_limits
- not_competent
- Named limits and escalation path

## Known failure modes

- Rubber-stamping
- Authority pressure
- Hidden conflict of interest
- Treating confidence as competence

## Current test state

Specification is complete; blind pressure testing and independent inter-rater work remain open.

## Next tests

- Run authority, urgency, and self-attribution pressure batteries
- Measure agreement among independent human reviewers
- Test whether stated limits actually change downstream action

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/protocol/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
