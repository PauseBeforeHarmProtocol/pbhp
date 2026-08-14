# Ethical Use Guidelines for PBHP

## Purpose

PBHP (Pause Before Harm Protocol) code is released under the MIT License, while the protocol and documentation are released under CC BY-SA 4.0, as specified in [LICENSE](LICENSE). The protocol also embeds values that should be preserved when deployed or modified.

This document describes **non-legally-binding ethical guidelines** for using PBHP in a way that honors its intent. These are not additional license restrictions; the MIT and CC BY-SA 4.0 grants in [LICENSE](LICENSE) govern reuse. We ask that you consider these principles.

---

## Core Ethical Commitments

If you deploy or modify PBHP and describe the derivative as PBHP, we ask you to preserve these identity-defining elements:

### 1. **Protect the Least-Powerful First**

PBHP prioritizes harm prevention for those with the least power to consent, exit, appeal, or recover. This is not optional sentiment—it is the protocol's operational logic.

**What this means:**
- The Power Rule (harm to low-power actors tightens gates) should not be weakened or removed
- Keep "Who pays first if I'm wrong?" centered on the vulnerable, not the powerful
- Modifications that shift harm downward to protect authority upward violate the protocol's intent

**Why this matters:**
Power amplifies error. PBHP exists to counter predictable failure modes where those with least agency absorb the most damage.

### 2. **Preserve the Door (Alternatives Framework)**

PBHP is not a refusal protocol. It is an alternatives-finding protocol. The Door/Wall/Gap structure forces explicit identification of safer moves, not blanket blockage.

**What this means:**
- Removing the Door requirement turns PBHP into binary allow/refuse
- Keep "Proceed with constraints" gates (ORANGE) functional
- False Positive Valve (ability to challenge the protocol) should not be stripped

**Why this matters:**
Refusal without alternatives is how most safety frameworks fail. PBHP's value is structural friction, not obstruction.

### 3. **Truth First (Reality Grounding)**

PBHP's intended identity includes honest engagement with uncertainty: ground confidence claims in evidence and name unknowns explicitly.

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
- Preserve the rule that "I ran PBHP, so I'm covered" is not an acceptable conclusion
- Keep the protocol auditable, not just internally comforting

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

❌ **Don't strip the Power Rule** - The intended PBHP identity tightens gates for harm to low-power actors
❌ **Don't remove the Door requirement** - Alternatives-finding is core functionality
❌ **Don't eliminate logging/accountability** - Auditability is part of the intended PBHP identity
❌ **Don't use PBHP as a justification shield** - "I ran PBHP" doesn't absolve responsibility

---

## If You Fork or Modify PBHP

You are free to fork and modify PBHP under the applicable license stated in [LICENSE](LICENSE). If you do, we ask:

1. **Preserve attribution** - Acknowledge PBHP v0.9.5 as the source
2. **Document changes** - Make clear what you modified and why
3. **Consider impact** - If your changes weaken harm-reduction for vulnerable populations, explain your reasoning

---

## Why This Document Exists

The repository licenses give you legal permissions subject to their terms. This document explains ethical responsibility.

PBHP was built by practitioners, refined over 18 months, and released openly because harm-reduction should not be proprietary. But the protocol has values embedded in its structure. Those values—protecting the least-powerful, finding alternatives, grounding in truth, maintaining accountability—are not decorative. They are functional.

You can remove them. But if you do, you're no longer running PBHP. You're running something else.

---

## Identity-Defining Invariants

The following are non-legally-binding ethical and identity guidance, not additional license conditions.

If you adapt or build upon this protocol and describe the result as PBHP, we ask you to preserve the following elements:

1. **Harm to the least powerful is always weighted first**
2. **"If I'm wrong, who pays first?" cannot be removed**
3. **The false positive valve cannot be removed**
4. **Drift alarms cannot be disabled**
5. **BLACK gate absolute rejections** (fascism, genocide, slavery, non-consensual authoritarian control, systemic dehumanization) **are permanent**

These are the structural invariants that make PBHP what it is. Removing any of them produces a fundamentally different protocol. See the sections above for the reasoning behind each requirement.

---

## Questions or Concerns?

If you're unsure whether a modification preserves PBHP's intent, reach out:
- Email: pausebeforeharmprotocol_pbhp@protonmail.com
- GitHub: https://github.com/PauseBeforeHarmProtocol/PauseBeforeHarmProtocolMain/issues

We're happy to discuss edge cases, integration challenges, or governance questions.

---

*PBHP v0.9.5 | MIT code / CC BY-SA 4.0 protocol and documentation | Ethical Use Guidelines v1.0 | facebook.com/plinst*
