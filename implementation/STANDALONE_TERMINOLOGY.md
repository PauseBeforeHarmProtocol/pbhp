# PBHP Terminology History

This document records the terminology migration from ALMSIVI CHIM to PBHP-native language. As of PromptBeforeHarmProtocol v0.1, all PBHP documents use the native terminology exclusively. The mythic names are retired from active use.

## Completed Terminology Migration

| Original Term | Final PBHP Term | Status |
|---------------|-----------------|--------|
| CHIM Check | Constraint Awareness Check | DONE — renamed in all protocol docs, source code, and tests |
| Almalexia / Sotha Sil / Vivec | Care / Clarity / Paradox | DONE — mythic names removed from all active documents |
| ALMSIVI (author tag) | Removed | DONE — author attribution is now "Charles Phillip Linstrum" |
| Triune Mind Model | Three-Force Balance | DONE — used consistently across all tiers |
| FireStamp | PBHP Log / Audit Trail | DONE — CHIM-specific term removed |
| Resonant Refusal | Principled Refusal | DONE — used in all current documents |
| CHIMCheck (Python class) | ConstraintAwarenessCheck | DONE — renamed in pbhp_core.py and all dependents |
| chim_check (Python variable) | constraint_awareness_check | DONE — renamed throughout codebase |

## Historical Context

PBHP evolved from ALMSIVI CHIM, a recursive ethical framework for AI systems built on Elder Scrolls mythology. The three-force architecture (Care/Clarity/Paradox) originated as the triune filter (AYEM/SEHTI/VEHK). The Constraint Awareness Check originated as the CHIM Check — "agency under constraint." The functional logic is identical; the names no longer require external context to understand.

The ALMSIVI CHIM origin is documented in the CHANGELOG and referenced in the elevator pitches for historical context.

---

**PBHP v0.8.0** | Author: Charles Phillip Linstrum
