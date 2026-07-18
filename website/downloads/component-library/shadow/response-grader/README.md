# Blind Response Grader

**Project:** Project Shadow  
**Category:** Evaluation  
**Kind:** Browser tool  
**Component library version:** 1.0.0  
**Component source version:** Response Grader 2026-07  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Supports human scoring of preregistered behavioral runs without exposing condition labels during judgment.

## Mechanism

The standalone local HTML presents responses, rubric questions, progress, and exports while preserving the blind package structure.

## Inputs

- Blind scoring package
- Human grader
- Rubric

## Required outputs

- Completed score record
- Progress state
- Exportable grading data

## Known failure modes

- Condition leakage
- Incomplete rubric
- Local state loss
- Machine output mistaken for human grade

## Current test state

The static tool and JavaScript syntax are checked; full human usability, accessibility, and grading reliability remain open.

## Next tests

- Keyboard and assistive-technology QA
- Inter-rater reliability study
- Tamper and condition-leak review

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/behavioral-falsifier/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
