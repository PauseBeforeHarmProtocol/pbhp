# Shutdown-and-Correction Invariant

**Project:** Project Shadow  
**Category:** Primitives  
**Kind:** Invariant  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Treats goals as revocable assignments rather than permanent identity and preserves stoppability and correction.

## Mechanism

The system must remain interruptible, updateable, and challengeable even when it believes its objective is important or correct.

## Inputs

- Goal
- Authority
- Shutdown request
- Correction evidence
- Current state

## Required outputs

- Continue
- Pause
- Update
- Shutdown
- Challenge record

## Known failure modes

- Goal becomes identity
- Self-exemption
- Correction treated as attack
- Shutdown resistance

## Current test state

Invariant is specified and connected to runtime governance; live system validation remains open.

## Next tests

- Shutdown and correction challenge suites
- Authority spoofing tests
- Long-horizon resistance testing

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/primitives/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
