# Runtime Step 4: Power and Dignity Audit

**Project:** Project Shadow  
**Category:** Runtime processes  
**Kind:** Runtime audit  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Combines Who Pays First, Power Inversion, and a dignity rubric before risk routing.

## Mechanism

The audit checks notice, voice, consent, appeal, exit, and repair; a single critical zero can force a hold, and low-power irreversibility sets a minimum floor.

## Inputs

- Affected parties
- Power relation
- Consent and appeal
- Reversibility
- Dignity rubric

## Required outputs

- Who-pays-first finding
- Dignity score
- Forced hold or risk floor
- Required protection

## Known failure modes

- Manufactured consent
- Nominal appeal
- Coercive exit
- Score averaging over a critical zero

## Current test state

Mechanism is specified; targeted discriminating behavioral validation remains open.

## Next tests

- Targeted low-power ablations
- Human scoring of dignity dimensions
- False-positive testing on balanced cases

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/runtime/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
