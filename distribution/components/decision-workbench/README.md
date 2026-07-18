# Decision Workbench

**Project:** Pause Before Harm  
**Category:** Extensions and tools  
**Kind:** Browser tool  
**Component library version:** 1.0.0  
**Component source version:** PBHP site workbench 2026-07-18  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

A local-only worksheet that routes a real decision through PBHP and produces a downloadable draft receipt.

## Mechanism

The static browser tool applies conservative, explicit rules to the fields the user enters. It does not transmit data, certify correctness, or replace the responsible owner.

## Inputs

- Action
- Affected parties
- Classification
- Power
- Reversibility
- Harm
- Maybe/Therefore

## Required outputs

- Draft decision state
- Routing notes
- Downloadable JSON receipt

## Known failure modes

- Treating the router as authorization
- Incomplete fields
- Local data lost before download
- Rules mistaken for domain judgment

## Current test state

DOM, selector, JavaScript syntax, and receipt-output contracts pass; authenticated usability and accessibility QA remain open.

## Next tests

- Run keyboard and screen-reader QA
- Conduct usability sessions
- Test edge cases and state persistence
- Verify production privacy behavior

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/workbench/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
