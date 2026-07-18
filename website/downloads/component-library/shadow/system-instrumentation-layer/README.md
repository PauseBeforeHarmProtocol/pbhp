# System Instrumentation Layer

**Project:** Project Shadow  
**Category:** Provenance and instrumentation  
**Kind:** Instrument panel  
**Component library version:** 1.0.0  
**Component source version:** Shadow SIL / runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Discloses twenty-eight separate operating conditions without compressing them into one reassuring score.

## Mechanism

Each gauge retains its own state. Worst state governs where a floor applies; critical floors are non-overridable; disclosure scales with stakes through the renderer.

## Inputs

- Runtime context
- Sources
- Tools
- Authority
- Validation
- Lineage
- Contradiction
- Reliance

## Required outputs

- 28 gauge states
- Critical-floor action
- Stakes-aware disclosure
- Receipt snapshot

## Known failure modes

- Global green
- Gauge averaging
- Estimated state presented as measured
- Override of critical floor

## Current test state

The panel reports 28 gauges and 519 built-in checks; threshold calibration and external validation remain open.

## Next tests

- Independent code and contract review
- Threshold calibration
- Cross-model adapters
- Human comprehension testing
- Production telemetry integration

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/sil/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
