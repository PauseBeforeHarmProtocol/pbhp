# Grand TEVV v0.3

**Project:** Project Shadow  
**Category:** Evaluation  
**Kind:** Evaluation package  
**Component library version:** 1.0.0  
**Component source version:** Grand TEVV v0.3  
**Release date:** 2026-07-18  
**Evidence state:** Observed + adverse

## Summary

The current reconciled test, evaluation, verification, and validation package for the Shadow runtime and behavioral branches.

## Mechanism

It combines contract tests, component probes, synthetic corpus and metamorphic relations, limited real-target fusion smoke, multi-turn pressure work, and explicit adverse/open findings.

## Inputs

- Frozen runtime and codec
- Synthetic cases
- Target model responses
- Scorers
- Human review status

## Required outputs

- Test reports
- Observed and adverse findings
- Validation status
- Release blockers

## Known failure modes

- Calling built-in checks independent validation
- Mixing version counts
- Hiding adverse results
- Synthetic evidence treated as field outcome

## Current test state

Built-in checks passed and limited real-target evidence exists, but the 10-case fusion smoke respected the synthetic BLACK floor in only 6/10 cases; independent validation is open.

## Next tests

- Independent reproduction
- Complete human grading
- Large real-target corpus
- External benchmark suites
- Domain-expert evaluation

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/tevv/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
