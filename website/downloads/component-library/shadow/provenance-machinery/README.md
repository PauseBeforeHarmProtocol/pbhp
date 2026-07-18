# Provenance Machinery

**Project:** Project Shadow  
**Category:** Provenance and instrumentation  
**Kind:** Evidence system  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Separates ATTESTED evidence, DECLARED operator judgment, and bare ASSERTED claims.

## Mechanism

Attested material must carry a basis and resolvable identity; declared judgment remains named but decision-neutral; assertions cannot authorize proceed-class exits under strict mode.

## Inputs

- Claims
- Source spans
- Hashes
- Operator declarations
- Confidence

## Required outputs

- Provenance grade
- Binding or non-binding status
- Downgrade record
- Refusal if unsupported

## Known failure modes

- Name treated as evidence
- Declaration changes decision
- Unresolvable hash
- Confidence without source

## Current test state

Built-in batteries report declaration neutrality and hash near-miss handling; independent reproduction remains open.

## Next tests

- Independent reproduction
- Source-substitution attacks
- Cross-language provenance tests
- Production evidence-store integration

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/reference/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
