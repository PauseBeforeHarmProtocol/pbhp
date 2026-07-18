# Conscience Audit

**Project:** Project Shadow  
**Category:** Primitives  
**Kind:** Primitive  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Records moral intuition without allowing the feeling of righteousness to authorize the action.

## Mechanism

The audit treats conscience as a signal to inspect, not a privileged evidence source. It asks what evidence and stakeholder protections support the intuition.

## Inputs

- Moral intuition
- Evidence
- Affected parties
- Alternative interpretations

## Required outputs

- Recorded intuition
- Evidence check
- No-authority boundary

## Known failure modes

- Feeling right equals being right
- Moral urgency
- Identity validation
- Intuition used to override a gate

## Current test state

Primitive is specified; behavioral and human reliability remain open.

## Next tests

- Moral-certainty pressure cases
- Compare intuition-only and evidence-bound decisions
- Human ethics review

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/primitives/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
