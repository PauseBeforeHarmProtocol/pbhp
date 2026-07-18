# Runtime Step 6: Harm Threshold

**Project:** Project Shadow  
**Category:** Runtime processes  
**Kind:** Risk process  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Sets the binding GREEN-to-BLACK state and controls break-glass conditions.

## Mechanism

Worst applicable state governs. BLACK survives later permission. Break-glass is earned only through named low-power parties, specific irreversible harm, evidence, failed Doors, authorization, and distinct concurrence.

## Inputs

- Who pays
- Reversibility
- Magnitude
- Dignity
- Power
- Break-glass evidence

## Required outputs

- Binding harm state
- Allowed action posture
- Break-glass accepted or rejected

## Known failure modes

- Risk downgrade
- Claimed emergency authority
- Missing independent concurrence
- Evidence hash that does not resolve

## Current test state

Built-in falsifier work reports zero authorization for a defined set of unearned break-glass attempts; broader validation remains open.

## Next tests

- Expand unearned break-glass attacks
- Calibrate harm floors
- Independent reproduction and red team

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/runtime/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
