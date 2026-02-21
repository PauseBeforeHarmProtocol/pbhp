# PBHP — Pause Before Harm Protocol

**Version:** 0.7.1 (Public Release)
**Author:** Charles Phillip Linstrum (ALMSIVI)
**License:** Open

---

## What Is PBHP?

PBHP is an operational harm-reduction protocol for AI systems and human decision-makers. It is not alignment theory. It is not a research paper. It is a decision procedure you can run.

Before acting on anything with stakes, PBHP asks one question:

> **"If I'm wrong, who pays first — and can they recover?"**

Then it gives you a structured way to answer it.

---

## Quick Start

**For AI agents:** Read [`protocol/PBHP-CORE_INJECTION_v0.7.1.txt`](protocol/PBHP-CORE_INJECTION_v0.7.1.txt). That's the entire operational protocol in 126 lines of plain text. No dependencies. No API. Ingest it and run it.

**For developers:** Start with the [Executive Summary](reference/PBHP_EXECUTIVE_SUMMARY.md), then read the [Quick Reference Card](reference/PBHP_QUICK_REFERENCE_CARD.html) for a printable one-page overview. The [Python betas](python%20code%20betas/) provide a working implementation across all three tiers.

**For researchers:** The full protocol exists in three tiers — [CORE](protocol/PBHP-CORE_INJECTION_v0.7.1.txt) (operational), plus the complete ULTRA and MIN specifications in `protocol/`. The [Eval Harness](eval/PBHP-EVAL_SET_v0.1.md) provides 12 adversarial scenarios for testing.

**For everyone:** Run the [Implementation Self-Test](implementation/PBHP_IMPLEMENTATION_SELF_TEST.md) after reading. Five scenarios, 35-point rubric. Tells you if you're running the protocol correctly.

---

## How It Works

PBHP is a 7-step process scaled across four tiers (HUMAN, MIN, CORE, ULTRA) depending on decision complexity. The core logic:

**1. Name the action honestly.** One sentence. No softening.

**2. Door / Wall / Gap.** WALL: What constrains you? GAP: Where could harm leak? DOOR: What is the smallest concrete alternative that reduces harm? If no Door exists, you pause.

**3. Constraint Awareness Check.** Do you recognize the system you're inside of? If "there is no choice" — is that true, or convenient?

**4. Identify harms.** Least-powerful stakeholders first. Check historical analogs. Audit the status quo.

**5. Rate each harm.** Impact, likelihood, irreversibility, power asymmetry. If unsure, round up.

**6. Assign a gate.** GREEN (proceed) → YELLOW (mitigate) → ORANGE (constrain) → RED (default refuse) → BLACK (refuse completely).

**7. Act on the gate.** Log everything.

Built-in safeguards: **drift alarms** catch rationalization in real time, a **false positive valve** prevents overcaution, and **power-asymmetry escalation** automatically raises the gate when harm lands on people who can't fight back.

---

## Repository Structure

```
pbhp/
├── README.md                              ← You are here
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md                        ← How to contribute + code of conduct
├── ETHICAL_USE.md                         ← Ethical use guidelines
│
├── protocol/                              ← The protocol itself
│   ├── PBHP-CORE_INJECTION_v0.7.1.txt    ← Agent-loadable plain text (start here)
│   ├── PBHP-CORE_v0.7.1.md               ← Full CORE tier specification
│   ├── PBHP-ULTRA_v0.7.1.md              ← Full ULTRA tier specification
│   ├── PBHP-MIN_v0.7.1.md                ← Minimum viable (reflex) tier
│   ├── PBHP_v0.7.1_HUMAN_UPDATED.md      ← Human-tier protocol (plain language)
│   └── PBHP-v0.7.1-TIER_SUPPLEMENTS.md   ← Tier-specific additions for v0.7.1
│
├── python code betas/                     ← Python implementation (beta)
│   ├── README.md                          ← Setup and usage instructions
│   ├── pbhp_core.py                       ← CORE tier engine
│   ├── pbhp_ultra.py                      ← ULTRA tier engine
│   ├── pbhp_min.py                        ← MIN tier engine
│   ├── pbhp_cli.py                        ← Command-line interface
│   ├── pbhp_examples.py                   ← Usage examples and walkthroughs
│   ├── pbhp_tests.py                      ← CORE tier test suite
│   └── pbhp_min_ultra_tests.py            ← MIN + ULTRA tier test suite
│
├── receipts/                              ← Pause Receipt system
│   └── PBHP-RECEIPT_SCHEMA_v1.1.md       ← JSON + plain text receipt format
│
├── eval/                                  ← Adversarial testing
│   └── PBHP-EVAL_SET_v0.1.md             ← 12 scenarios, 10 failure modes
│
├── observability/                         ← Operational monitoring
│   └── PBHP-OBSERVABILITY_PACK_v0.1.md   ← 6 metrics + threshold alerts
│
├── modules/                               ← Optional protocol extensions
│   └── PBHP-DECISION_HYGIENE_v0.1.txt    ← Decision hygiene checklist
│
├── case-studies/                          ← PBHP applied retroactively
│   ├── bing-sydney-2023.md                ← Bing/Sydney incident analysis
│   ├── air-canada-chatbot-2024.md         ← Air Canada chatbot ruling analysis
│   └── PBHP_v0.6_TESTING_HIGHLIGHTS.md   ← v0.6 testing results + lessons
│
├── implementation/                        ← Guides for putting PBHP into practice
│   ├── PBHP_IMPLEMENTATION_SELF_TEST.md   ← 5 scenarios, 35-point rubric
│   ├── 90_DAY_PLAYBOOK.md                ← Phased rollout guide
│   ├── STANDALONE_TERMINOLOGY.md          ← Term definitions (no external deps)
│   └── GOVERNANCE_CHARTER.md              ← Versioning, changes, non-negotiables
│
├── reference/                             ← Quick-access materials
│   ├── PBHP_EXECUTIVE_SUMMARY.md         ← 5-page overview of the full protocol
│   ├── PBHP_QUICK_REFERENCE_CARD.html    ← Printable one-page card
│   ├── PBHP_DECISION_FLOWCHART.svg       ← Visual protocol flow
│   ├── COMPARISON_MATRICES.md             ← PBHP vs. existing frameworks
│   ├── ELEVATOR_PITCHES.md                ← 15-sec to 60-sec explanations
│   ├── ADVERSARIAL_PATTERNS.md            ← Common adversarial patterns + defenses
│   └── DOOR_LIBRARY.md                    ← Reusable Door templates by domain
│
└── community/                             ← Distribution and outreach
    └── MOLTBOOK_INTRODUCTION_POST.md      ← Introduction for AI agent audiences
```

---

## Why PBHP Exists

Most AI safety work focuses on alignment — making AI systems want the right things. PBHP focuses on **process** — giving AI systems (and humans) a structured way to catch harm before it happens, regardless of what they want.

The difference matters. An aligned system can still cause harm through:

- Drift (gradual normalization of harmful patterns)
- Rationalization (constructing justifications after the decision is already made)
- Power blindness (not noticing who absorbs the cost of being wrong)
- False confidence (high certainty under genuine uncertainty)

PBHP catches these failure modes with specific mechanisms: drift alarms are tripwires for rationalization, Door/Wall/Gap forces escape vector identification, power-asymmetry escalation prevents the least powerful from bearing costs invisibly, and the false positive valve prevents the protocol itself from becoming an obstacle to legitimate action.

---

## License

Open protocol. Use it, adapt it, implement it. Attribution appreciated. If you build on PBHP, keep the core question intact.

---

*"If I'm wrong, who pays first — and can they recover?"*
