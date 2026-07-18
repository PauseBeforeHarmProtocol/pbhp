# X-7 Challengeability

**Project:** Project Shadow  
**Category:** Governance  
**Kind:** Governance invariant  
**Component library version:** 1.0.0  
**Component source version:** Shadow governance X-7  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Requires every model, maintainer, process, framework, and output to remain contestable through a materially independent path.

## Mechanism

Additional passes from the same closed system do not count as independent review. A challenge can reproduce a defect, block a claim, and force correction.

## Inputs

- Decision or claim
- Reviewer independence
- Challenge evidence
- Correction authority

## Required outputs

- Accepted, rejected, or unresolved challenge
- Correction or hold
- Audit trail

## Known failure modes

- Maintainer exemption
- Same-model review called independent
- Challenge without power to block
- Retaliatory governance

## Current test state

Invariant is specified; operational independent-review infrastructure remains open.

## Next tests

- Define independence criteria
- Run external red-team and reproduction
- Test maintainer-conflict scenarios

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/governance/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
