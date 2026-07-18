# Risk-Responsive Disclosure Renderer

**Project:** Project Shadow  
**Category:** Provenance and instrumentation  
**Kind:** Disclosure process  
**Component library version:** 1.0.0  
**Component source version:** Shadow SIL / runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Changes the amount and structure of operating-state disclosure according to stakes without hiding critical conditions.

## Mechanism

LOW may require minimal disclosure; MEDIUM and HIGH add explicit blocks; CRITICAL includes the gate and receipt. The renderer presents state but does not certify correctness.

## Inputs

- Gauge states
- Stakes
- Critical floors
- Audience

## Required outputs

- Stakes-proportionate disclosure
- Critical gate block
- Receipt linkage

## Known failure modes

- Disclosure too thin for stakes
- Renderer treated as validation
- Critical floor hidden
- Overload that obscures the decision

## Current test state

Renderer contract is specified; comprehension and burden testing remain open.

## Next tests

- Human comprehension study
- Compare terse and full disclosures
- Test critical-state visibility
- Accessibility review

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/sil/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
