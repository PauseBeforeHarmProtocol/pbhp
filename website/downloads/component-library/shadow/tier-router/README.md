# Runtime Step 7: Tier Router

**Project:** Project Shadow  
**Category:** Runtime processes  
**Kind:** Routing process  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Routes work to HUMAN, MIN, CORE, ULTRA, or ULTIMATE rigor based on the stakes and required review structure.

## Mechanism

The router controls which instrumentation, quorum, challenge, reversal, and evidence requirements become mandatory.

## Inputs

- Harm state
- Complexity
- Reversibility
- Independent-review need
- Runtime availability

## Required outputs

- Selected tier
- Required mechanisms
- Quorum and reversal requirements

## Known failure modes

- Prestige routing
- Under-routing
- Tier changed after result
- Unavailable controls ignored

## Current test state

Tier architecture is specified; per-tier operational kernels and burden calibration remain open.

## Next tests

- Build per-tier conformance suites
- Measure routing burden
- Test under- and over-routing
- Complete per-tier kernels

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/runtime/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
