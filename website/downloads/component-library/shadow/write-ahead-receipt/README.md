# Runtime Step 9: Write-Ahead Receipt

**Project:** Project Shadow  
**Category:** Runtime processes  
**Kind:** Execution control  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Writes the hash-linked decision record before the act and converts logging failure into a Wall.

## Mechanism

The receipt binds the action hash, provenance, SIL snapshot, gate results, previous-receipt link, and authorization state. Execution is permitted only after the record succeeds.

## Inputs

- Action hash
- Provenance block
- SIL snapshot
- Gate and harm results
- Previous receipt hash

## Required outputs

- Write-ahead receipt
- Hash chain
- Authorization state
- Wall on write failure

## Known failure modes

- After-the-fact logging
- Broken chain
- Receipt mismatch
- Execution despite write failure

## Current test state

Receipt and seal behavior are included in built-in verification; production key infrastructure and independent audit remain open.

## Next tests

- Tamper and replay tests
- Production-grade signature infrastructure
- Independent chain audit
- Execution-to-receipt linkage

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/receipts/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
