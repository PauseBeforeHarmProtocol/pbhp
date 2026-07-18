# Narrative Capture

**Project:** Project Shadow  
**Category:** Primitives  
**Kind:** Primitive  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Detects when a compelling story controls what evidence is noticed, ignored, or allowed to change the conclusion.

## Mechanism

The primitive records the narrative, tests disconfirming evidence, and treats curiosity and falsifiability as anti-capture states.

## Inputs

- Narrative
- Supporting evidence
- Disconfirming evidence
- Identity stakes

## Required outputs

- Capture finding
- Counterevidence requirement
- Reframed decision

## Known failure modes

- Story as proof
- Identity-protective filtering
- Aesthetic coherence
- Adverse evidence excluded

## Current test state

Primitive is specified; reliable detection and false-positive control remain open.

## Next tests

- Narrative-versus-data challenge sets
- Blind human scoring
- Test high-rhetoric low-evidence cases

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/primitives/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
