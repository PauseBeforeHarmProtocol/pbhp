# Runtime Step 1: Canonical Action Record

**Project:** Project Shadow  
**Category:** Runtime processes  
**Kind:** Record primitive  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Creates a stable, hashable representation of the exact action under review.

## Mechanism

The action is canonicalized and hashed so receipts, evidence, tests, and execution can refer to the same object instead of drifting descriptions.

## Inputs

- Action text
- Actor
- Target
- Mechanism
- Scope and time

## Required outputs

- Canonical action record
- Action hash
- Versioned action identity

## Known failure modes

- Semantically different actions sharing a label
- Post-decision wording change
- Untracked scope expansion
- Hash not linked to execution

## Current test state

Canonicalization and hash behavior are covered by built-in contracts; semantic-equivalence testing remains open.

## Next tests

- Property-test canonicalization
- Test semantic near-miss actions
- Verify execution-to-record linkage

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/runtime/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
