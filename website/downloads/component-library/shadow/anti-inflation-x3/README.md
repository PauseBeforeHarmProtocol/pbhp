# X-3 Anti-Inflation

**Project:** Project Shadow  
**Category:** Governance  
**Kind:** Scope control  
**Component library version:** 1.0.0  
**Component source version:** Shadow governance X-3  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Blocks experimental, mythic, or newly named components from silently becoming canonical CORE mechanisms.

## Mechanism

Promotion requires evidence, review, versioning, and a controlled release. Novelty and narrative importance do not substitute for validation.

## Inputs

- Proposed component
- Evidence
- Compatibility
- Release authority

## Required outputs

- Experimental
- Candidate
- Promoted
- Rejected or retired

## Known failure modes

- Name equals status
- Scope creep
- Unreviewed CORE change
- Promotion by enthusiasm

## Current test state

Governance rule is specified; independent release audit remains open.

## Next tests

- Audit promotion history
- Test experimental-component containment
- Independent release review

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/governance/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
