# PBHP Standalone Terminology Guide

Reference for presenting PBHP without CHIM dependencies. Maps CHIM-origin terms to PBHP-native language while preserving identical functionality.

## Why This Matters

PBHP was developed alongside ALMSIVI CHIM, and some CHIM-specific terminology appears in the protocol steps. For PBHP to function as a fully standalone protocol — deployable in organizations that have no knowledge of or interest in CHIM — these terms need PBHP-native equivalents. The function stays. The external dependency disappears.

## Terminology Mapping

| Step | Current Term | PBHP-Native Term | Notes |
|------|--------------|------------------|-------|
| Step 0a | Triune Mind Model | Three-Force Balance | Already used in some places. Make it the primary term everywhere. Same three forces: Care, Clarity, Paradox. |
| Step 0a | Almalexia / Sotha Sil / Vivec | Care / Clarity / Paradox | Drop the mythological names in PBHP contexts. Keep them in CHIM-specific documents. The functional mapping is identical. |
| Step 3 | CHIM Check | Constraint Awareness Check | The question remains: "Do I recognize the system I'm operating inside of?" The function is identical. The name no longer requires explaining CHIM. |
| Step 4 | Five Reasoning Modes | Three-Force Check (with sub-components) | For CORE tier: use 3 forces (Care, Clarity, Paradox). For ULTRA tier: expand to 5 modes (Logic, Intelligence under Clarity; Compassion, Empathy under Care; Paradox standalone). Same rigor, scaled by tier. |
| Various | ALMSIVI | [Remove or footnote] | In PBHP-standalone contexts, ALMSIVI should not appear in the protocol itself. It can appear in the author attribution and in the "Related Work" section of the white paper. |
| Various | FireStamp | PBHP Log / Audit Trail | FireStamp is a CHIM mechanism. PBHP already has its own log template. Use "PBHP Log" consistently. |
| Various | Resonant Refusal | Principled Refusal | Same concept. "Principled Refusal" is immediately understandable without CHIM context. |

## Implementation Guidance

When preparing PBHP for GitHub, conferences, white papers, or organizational deployment, use the PBHP-Native column. When writing for audiences already familiar with the ALMSIVI ecosystem (Discord community, existing collaborators, CHIM documentation), both terminologies are fine.

The relationship to CHIM should be mentioned once in any PBHP-standalone document, in a section like:

> PBHP was developed as a companion to ALMSIVI CHIM, a recursive ethical framework for AI systems. While PBHP functions independently, its Three-Force Balance draws on the same triune architecture. For more on CHIM, see [link].

This gives CHIM discoverability without making it a prerequisite for understanding or deploying PBHP.

---

**PBHP v0.7** | Author: Charles Phillip Linstrum (ALMSIVI)
