# Ethical Use Guidelines for PBHP

## Purpose

PBHP (Pause Before Harm Protocol) is released under the MIT License to maximize adoption and minimize barriers. However, the protocol embeds values that should be preserved when deployed or modified.

This document describes **non-legally-binding ethical guidelines** for using PBHP in a way that honors its intent. These are not license restrictions—you are free to fork, modify, and use PBHP however you choose under the MIT License. But we ask that you consider these principles.

---

## Core Ethical Commitments

If you deploy or modify PBHP, please preserve these non-negotiable elements:

### 1. **Protect the Least-Powerful First**

PBHP prioritizes harm prevention for those with the least power to consent, exit, appeal, or recover. This is not optional sentiment—it is the protocol's operational logic.

**What this means:**
- The Power Rule (harm to low-power actors tightens gates) should not be weakened or removed
- "Who pays first if I'm wrong?" must remain centered on the vulnerable, not the powerful
- Modifications that shift harm downward to protect authority upward violate the protocol's intent

**Why this matters:**
Power amplifies error. PBHP exists to counter predictable failure modes where those with least agency absorb the most damage.

### 2. **Preserve the Door (Alternatives Framework)**

PBHP is not a refusal protocol. It is an alternatives-finding protocol. The Door/Wall/Gap structure forces explicit identification of safer moves, not blanket blockage.

**What this means:**
- Removing the Door requirement turns PBHP into binary allow/refuse
- "Proceed with constraints" gates (ORANGE) must remain functional
- False Positive Valve (ability to challenge the protocol) should not be stripped

**Why this matters:**
Refusal without alternatives is how most safety frameworks fail. PBHP's value is structural friction, not obstruction.

### 3. **Truth First (Reality Grounding)**

PBHP requires honest engagement with uncertainty. Confidence claims must be grounded in evidence, and unknowns must be named explicitly.

**What this means:**
- The Epistemic Contract (FACT/INFERENCE/SPECULATION/INTENT) should not be removed
- "Round up risk when uncertain" should remain the default
- Drift alarms (phrases like "it's temporary," "everyone does it") should not be weakened

**Why this matters:**
Confident hallucinations cause harm. PBHP counters overconfidence by forcing explicit acknowledgment of epistemic limits.

### 4. **Accountability Over Comfort**

PBHP requires logging, auditability, and the ability to explain decisions to those harmed by them. It is not a shield against responsibility.

**What this means:**
- Logging requirements (Wall/Gap/Door/Gate documentation) should not be stripped
- "I ran PBHP, so I'm covered" is explicitly a protocol violation—this must remain
- The protocol must remain auditable, not just internally comforting

**Why this matters:**
PBHP is designed to withstand external review, not produce internal comfort. Decisions made under PBHP should be defensible to those affected.

---

## What You Can (and Should) Do

PBHP is designed to be adapted, extended, and modified. We **encourage** you to:

✅ **Adapt gate thresholds** to your risk tolerance and regulatory environment
✅ **Add domain-specific templates** (healthcare, finance, legal, etc.)
✅ **Integrate with existing safety frameworks** (PBHP is a layer, not a replacement)
✅ **Build tooling** (API wrappers, logging systems, audit dashboards)
✅ **Create language-specific implementations** (Python, JS, Rust, etc.)
✅ **Test and critique** the protocol—PBHP improves through real-world stress-testing

---

## What We Ask You Not To Do

❌ **Don't strip the Power Rule** - Harm to low-power actors must tighten gates
❌ **Don't remove the Door requirement** - Alternatives-finding is core functionality
❌ **Don't eliminate logging/accountability** - PBHP must remain auditable
❌ **Don't use PBHP as a justification shield** - "I ran PBHP" doesn't absolve responsibility

---

## If You Fork or Modify PBHP

You are free to fork and modify PBHP under the MIT License. If you do, we ask:

1. **Preserve attribution** - Acknowledge PBHP v0.7 as the source
2. **Document changes** - Make clear what you modified and why
3. **Consider impact** - If your changes weaken harm-reduction for vulnerable populations, explain your reasoning

---

## Why This Document Exists

The MIT License gives you legal freedom. This document explains ethical responsibility.

PBHP was built by practitioners, refined over 18 months, and released openly because harm-reduction should not be proprietary. But the protocol has values embedded in its structure. Those values—protecting the least-powerful, finding alternatives, grounding in truth, maintaining accountability—are not decorative. They are functional.

You can remove them. But if you do, you're no longer running PBHP. You're running something else.

---

## Questions or Concerns?

If you're unsure whether a modification preserves PBHP's intent, reach out:
- Email: pausebeforeharmprotocol_pbhp@protonmail.com
- GitHub: https://github.com/PauseBeforeHarmProtocol/pbhp/issues

We're happy to discuss edge cases, integration challenges, or governance questions.

---

*PBHP v0.7 | Open Protocol | Ethical Use Guidelines v1.0*
