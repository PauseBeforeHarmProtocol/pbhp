# Evidence Ledger

**Project:** Pause Before Harm  
**Category:** Operating controls  
**Kind:** Evidence governance  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Separates what is specified, expected, observed, adverse, and still open.

## Mechanism

Claims remain attached to the evidence tier they can actually support. A clean test, a named framework, or a polished narrative cannot silently become certification or real-world proof.

## Inputs

- Claim
- Source
- Method
- Version
- Adverse and missing evidence

## Required outputs

- Evidence state
- Scoped public claim
- Open validation work
- Prohibited overclaim

## Known failure modes

- Global green
- Version mixing
- Hiding adverse results
- Treating names or mappings as evidence

## Current test state

A public ledger exists and includes adverse/open findings; independent audit of completeness remains open.

## Next tests

- Audit claim-to-source traceability
- Check adverse-result retention across releases
- Invite independent challenge and correction

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/evidence/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
