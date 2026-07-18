# K1 Kernel

**Project:** Project Shadow  
**Category:** Evaluation  
**Kind:** Execution artifact  
**Component library version:** 1.0.0  
**Component source version:** K1 kernel development snapshot  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Packages a sealed, self-checking subset of the runtime intended to refuse activation when its integrity fails.

## Mechanism

The kernel extracts and verifies the canonical set, binds activation to integrity, and is intended to support per-tier execution packages.

## Inputs

- Sealed component set
- Hashes
- Activation request
- Tier configuration

## Required outputs

- Verified activation
- Integrity refusal
- Kernel receipt

## Known failure modes

- Seal bypass
- Wrong component set
- Tier mismatch
- Integrity check presented as safety proof

## Current test state

Differential integrity work is reported; per-tier kernels, production signing, and independent verification remain open.

## Next tests

- Independent integrity review
- Per-tier kernels
- Key management and signature tests
- Hostile extraction and replay tests

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/reference/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
