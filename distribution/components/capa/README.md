# Corrective and Preventive Action

**Project:** Pause Before Harm  
**Category:** Operating controls  
**Kind:** Quality process  
**Component library version:** 1.0.0  
**Component source version:** PBHP v0.9.5 / site library 1.0.0  
**Release date:** 2026-07-18  
**Evidence state:** Specified

## Summary

Turns protocol failures and adverse findings into owned correction, verification, and prevention work.

## Mechanism

A defect is described, contained, analyzed, corrected, verified for effectiveness, and recorded. Narrative defense does not close a finding.

## Inputs

- Failure or adverse finding
- Containment need
- Root and contributing causes
- Owner and due date

## Required outputs

- Correction
- Preventive control
- Effectiveness criterion
- Closure record

## Known failure modes

- Closing on implementation alone
- Blame substitution
- No effectiveness check
- Repeated recurrence without escalation

## Current test state

Quality-system process is specified; program-level effectiveness data remain open.

## Next tests

- Track recurrence after closure
- Audit overdue CAPA
- Compare root-cause methods
- Review whether corrections introduce new harm

## Scope and claim boundary

This component specification describes the current public design and evidence state. It is not certification, independent validation, legal advice, or proof of beneficial real-world outcomes. A component can be implemented and contract-tested while its human, organizational, or safety effect remains open.

## Related site route

`/operations/`

## Change control

Update this specification, `component.json`, and `TEST_PLAN.md` together. Regenerate the component pack and manifest, run the repository validation suite, review the public/private boundary, then deploy only through a reviewed candidate version.
