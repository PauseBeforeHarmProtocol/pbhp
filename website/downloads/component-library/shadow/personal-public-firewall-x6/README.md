# X-6 Personal / Public Firewall

**Project:** Project Shadow  
**Category:** Governance  
**Kind:** Publication control  
**Component library version:** 1.0.0  
**Component source version:** Shadow governance X-6  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Prevents private recovery material, personal context, and identity-dependent content from shipping merely because it appeared in a working session.

## Mechanism

Public release is allowlisted, scanned, checksummed, and limited to material necessary for explanation, reproduction, testing, or critique.

## Inputs

- Candidate files
- Publication purpose
- Privacy markers
- Allowlist

## Required outputs

- Included public artifact
- Excluded private material
- Boundary scan report

## Known failure modes

- Session dump
- Credential leak
- Opaque chat-file dependency
- Personal material included without necessity

## Current test state

Automated public-boundary scans pass for the release; professional security and privacy review remain open.

## Next tests

- Independent privacy review
- Secret-scanner expansion
- Manual artifact-by-artifact publication review

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/governance/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
