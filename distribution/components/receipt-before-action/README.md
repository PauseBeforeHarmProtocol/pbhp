# Receipt Before Action

**Project:** Pause Before Harm  
**Category:** Protocol gates  
**Kind:** Record control  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Creates the auditable decision record before commitment rather than after the outcome is known.

## Mechanism

The receipt binds the action, affected parties, evidence, classification, threshold, safeguards, Maybe/Therefore, owner, review date, and effectiveness check. No record means no authorization.

## Inputs

- Completed gate outputs
- Evidence references
- Owner
- Follow-up criterion

## Required outputs

- Pre-action receipt
- Action state
- Review and effectiveness plan

## Known failure modes

- After-the-fact rationalization
- Missing evidence basis
- No owner
- Receipt that cannot be linked to the executed act

## Current test state

Receipt generation and static workbench contracts are implemented; real-world audit and outcome value remain open.

## Next tests

- Verify receipt-to-action linkage
- Test tamper evidence and version migration
- Measure audit usefulness and correction speed
- Conduct independent record sampling

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/receipts/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
