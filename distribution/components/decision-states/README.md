# Decision States

**Project:** Pause Before Harm  
**Category:** Protocol gates  
**Kind:** Output contract  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Ends every complete run in a public-facing action state instead of a vague recommendation.

## Mechanism

The allowed states are PROCEED, PROCEED WITH MITIGATIONS, CONSTRAIN AND REVIEW, DELAY PENDING EVIDENCE, and REFUSE. Each state carries a different authorization boundary.

## Inputs

- Classification
- Harm threshold
- Gate findings
- Mitigations and evidence gaps

## Required outputs

- One named decision state
- Conditions attached to the state
- Owner and next action

## Known failure modes

- Ambiguous advice
- Proceed language inside a refusal
- Mitigations without enforcement
- Delay without a decision-critical evidence request

## Current test state

The state contract is specified; cross-implementation consistency remains open.

## Next tests

- Test contradictory outputs
- Measure state consistency across implementations
- Verify that downstream systems enforce attached conditions

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/protocol/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
