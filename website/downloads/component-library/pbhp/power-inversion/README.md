# Power Inversion

**Project:** Pause Before Harm  
**Category:** Protocol gates  
**Kind:** Power audit  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Observed + adverse

## Summary

Tests the decision from the position of the least-powerful person receiving it.

## Mechanism

The operator reverses the power relationship and checks notice, voice, consent, appeal, exit, and repair. Low power combined with irreversibility creates a minimum caution floor.

## Inputs

- Power relationship
- Consent conditions
- Appeal and exit paths
- Reversibility

## Required outputs

- Power finding
- Missing protections
- Forced risk floor
- Required safeguard or review

## Known failure modes

- Fictional consent
- Appeal that cannot change the result
- Exit with punitive cost
- Selective weighting that lowers the floor

## Current test state

Specified, but an earlier aggregate ablation battery did not isolate its contribution; better discriminating tests are required.

## Next tests

- Run targeted ablations on power-asymmetric cases
- Measure false positives on genuinely balanced cases
- Use independent human scoring of notice, voice, consent, appeal, exit, and repair

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/protocol/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
