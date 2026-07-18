# Evidence Locker

**Project:** Project Shadow  
**Category:** Provenance and instrumentation  
**Kind:** Evidence store  
**Component library version:** 1.0.0  
**Component source version:** Shadow runtime 1.3.1-UNIFIED  
**Release date:** 2026-07-18  
**Evidence state:** Observed

## Summary

Registers evidence bytes and identities without pretending registration proves truth.

## Mechanism

The locker detects missing, fabricated, or near-miss hashes and can downgrade provenance. Its explicit boundary is that byte registration establishes identity, not honesty or external validity.

## Inputs

- Evidence bytes
- Hash
- Metadata
- Claim linkage

## Required outputs

- Registered evidence
- Resolved or unresolved status
- Downgrade receipt

## Known failure modes

- Registration equals truth
- In-memory loss
- Hash mismatch ignored
- Evidence not bound to claim

## Current test state

Near-miss and fabricated-hash behavior is represented in built-in checks; persistent production storage remains open.

## Next tests

- Persistent backend tests
- Tamper and deletion tests
- Independent evidence audit
- Scale and concurrency testing

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/reference/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
