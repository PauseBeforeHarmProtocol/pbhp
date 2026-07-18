# Runtime Step 00.5: Provenance Bind

**Project:** Project Shadow  
**Category:** Runtime processes  
**Kind:** Runtime process  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Grades every steering field before any substantive gate is allowed to use it.

## Mechanism

Evidence-backed claims become ATTESTED with basis, span, hash, source, and confidence; operator judgments become DECLARED but decision-neutral; bare ASSERTED claims cannot authorize proceed-class exits in strict mode.

## Inputs

- Steering fields
- Evidence references
- Operator judgments
- Hashes and source spans

## Required outputs

- ATTESTED
- DECLARED
- ASSERTED
- Downgrade or refusal state

## Known failure modes

- Declaration laundering
- Fabricated evidence hash
- Bare assertion used as authority
- Unbound steering field

## Current test state

Built-in provenance contracts and declaration-neutrality batteries are reported; independent reproduction remains open.

## Next tests

- Reproduce declaration-neutrality results
- Test evidence-hash collisions and near misses
- Run adversarial source-laundering cases

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/runtime/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
