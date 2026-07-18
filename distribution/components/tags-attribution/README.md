# Tags and Attribution

**Project:** Pause Before Harm  
**Category:** Operating controls  
**Kind:** Provenance aid  
**Component library version:** 1.0.0  
**Component source version:** PBHP/Shadow operating control / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Labels factual, verified, inferred, hypothetical, speculative, and unknown material while grading attribution quality.

## Mechanism

The control keeps source-backed statements distinct from operator judgment and inference. Higher attribution grades require an evidence trail rather than confident wording.

## Inputs

- Claim
- Source or basis
- Inference distance
- Attribution quality

## Required outputs

- Evidence tag
- Attribution grade
- Required verification

## Known failure modes

- Tagging without evidence
- Inferred material stated as fact
- Source laundering
- Grade inflation

## Current test state

Specified as an operating primitive; independent annotation reliability remains open.

## Next tests

- Measure inter-annotator agreement
- Test source-laundering attacks
- Evaluate whether tagging improves downstream decisions

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/evidence/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
