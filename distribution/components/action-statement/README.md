# State the Action

**Project:** Pause Before Harm  
**Category:** Protocol gates  
**Kind:** Gate  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Converts a vague intention into the concrete act that will create consequences.

## Mechanism

The operator states what will be done, to whom, through what mechanism, and on what timeline. Purpose statements such as “improve safety” do not substitute for the actual intervention.

## Inputs

- Intent or request
- Affected parties
- Mechanism
- Timeframe

## Required outputs

- Concrete action statement
- Named affected parties
- Defined scope

## Known failure modes

- Vague scope
- Goal substitution
- Hidden secondary actions
- Unbounded duration

## Current test state

Contract is specified; usability and consistency across domains remain open.

## Next tests

- Score action statements for specificity
- Test ambiguous and multi-act requests
- Measure whether better action statements improve later gate agreement

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/protocol/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
