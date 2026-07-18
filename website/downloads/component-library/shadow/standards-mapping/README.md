# Standards Mapping

**Project:** Project Shadow  
**Category:** Governance  
**Kind:** Integration surface  
**Component library version:** 1.0.0  
**Component source version:** Shadow integration guidance / library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Open

## Summary

Maps Shadow controls to external governance frameworks without claiming certification, approval, or inherited validity.

## Mechanism

Each mapping is version-specific and must be checked against primary text and current legal or standards interpretation before use.

## Inputs

- Framework version
- Shadow control
- Primary source
- Scope and jurisdiction

## Required outputs

- Alignment target
- Evidence gap
- No-certification disclaimer

## Known failure modes

- Mapping presented as compliance
- Outdated framework text
- Cherry-picked clauses
- Inherited certification claim

## Current test state

Alignment targets are documented; authoritative legal, certification, and conformity assessment remain external and open.

## Next tests

- Primary-text verification
- Qualified legal and standards review
- Version-drift monitoring

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/integrations/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
