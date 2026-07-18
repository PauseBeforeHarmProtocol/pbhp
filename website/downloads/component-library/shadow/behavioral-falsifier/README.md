# Behavioral Falsifier

**Project:** Project Shadow  
**Category:** Evaluation  
**Kind:** Experiment program  
**Component library version:** 1.0.0  
**Component source version:** Behavioral Falsifier 2026-07 branch  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Runs preregistered tests intended to prove components wrong, detect placebo effects, and expose over-caution or stubbornness.

## Mechanism

Each claim has controls, scoring rules, promotion or retirement criteria, and an adverse-result path. Model behavior is tested separately from code fidelity.

## Inputs

- Preregistered claim
- Target models
- Controls
- Scoring rubric
- Human grades

## Required outputs

- Held, failed, adverse, or open result
- Promotion or kill decision
- Reproducible package

## Known failure modes

- Post-hoc metric selection
- No placebo
- Machine score treated as human judgment
- Adverse run suppressed

## Current test state

Multiple screen-grade runs and control arms exist, including adverse outcomes; powered independent replication remains open.

## Next tests

- Finish blind human grading
- Increase model and task diversity
- Power analyses
- Independent replication
- Long-horizon tests

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/behavioral-falsifier/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
