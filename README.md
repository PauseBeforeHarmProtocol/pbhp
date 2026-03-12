# PBHP — Pause Before Harm Protocol

**Version:** 0.8.1 (Public Release)
**Author:** Charles Phillip Linstrum
**License:** Open
**Email/Contact:** pausebeforeharmprotocol_pbhp@protonmail.com
**Social Media:** facebook.com/plinst
---

## What Is PBHP?

PBHP is an operational harm-reduction protocol for AI systems and human decision-makers. It is not alignment theory. It is not a research paper. It is a decision procedure you can run.

Before acting on anything with stakes, PBHP asks one question:

> **"If I'm wrong, who pays first — and can they recover?"**

Then it gives you a structured way to answer it.

---

## Quick Start

**For AI agents:** Use [`PromptBeforeHarmProtocol v0.1`](protocol/PromptBeforeHarmProtocol_v0.1.md) — the definitive system prompt. Three paste-ready versions available in [`Paste Versions`](protocol/PBHP_Prompt_Paste_Versions.md) (~1250 and ~500 token options). No dependencies. No API. Paste it and run it.

**For developers:** Start with the [Executive Summary](reference/PBHP_EXECUTIVE_SUMMARY.md), then read the [Quick Reference Card](reference/PBHP_QUICK_REFERENCE_CARD.html) for a printable one-page overview. The [Python implementation](src/) provides a working implementation across all three tiers.

**For researchers:** The full protocol exists in three tiers — [CORE](protocol/PBHP-CORE_INJECTION_v0.7.2.txt) (operational), plus the complete ULTRA and MIN specifications in `protocol/`. The [Eval Harness](eval/PBHP-EVAL_SET_v0.1.md) provides 12 adversarial scenarios for testing.

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

## v0.8.0 Modules

PBHP v0.8.0 adds five operational modules that extend the core protocol:

**Triage Classifier** (`pbhp_triage.py`) — Routes incoming decisions to the appropriate tier (HUMAN/MIN/CORE/ULTRA) based on signal analysis. Evaluates irreversibility, vulnerable population impact, power asymmetry, and amplification potential. Prevents unnecessary escalation while ensuring high-risk decisions get appropriate scrutiny.

**Domain Metric Packs** (`pbhp_metrics.py`) — Pre-built severity thresholds for hiring, healthcare, finance, content moderation, and security. Each pack defines concrete harm levels (healthcare CATASTROPHIC = patient death), reversibility timeframes, and stakeholder templates. Eliminates guesswork in domain-specific risk scoring.

**Multi-Agent Coordination** (`pbhp_multiagent.py`) — Rules for when multiple agents running PBHP reach different gate decisions. Implements quorum voting with veto for irreversible actions, weighted expert voting, and mandatory human-in-the-loop for BLACK gates. Ensures multi-agent disagreement never weakens safety.

**Compliance Crosswalks** (`pbhp_compliance.py`) — Maps PBHP steps and artifacts to NIST AI RMF, ISO/IEC 42001, ISO/IEC 23894, and EU AI Act requirements. Shows which PBHP step satisfies which compliance requirement. Generates audit checklists and compliance reports.

**Drift Measurement** (`pbhp_drift.py`) — Upgrades from binary drift flags to quantifiable drift rates. Tracks refuse rate, average gate level, vulnerable population impact, and confidence scores over time. Computes drift velocity, acceleration, and projects threshold breach dates.

### v0.8.1 Modules — Scheming Resistance and Quality Systems

**Scheming Resistance Layer** (`pbhp_srl.py`) — Six rules that prevent frontier model scheming behaviors: anti-self-preservation (SRL-01), mandatory confession (SRL-02), live-systems gating (SRL-03), eval-awareness skepticism (SRL-04), self-report distrust (SRL-05), and anti-sandbagging (SRL-06). Safety-monotonic state machine where states can escalate freely but only de-escalate through human-authorized paths. 60 tests including red-team scenarios based on real frontier model failures.

**Quality Systems Layer** (`pbhp_qs.py`) — Eight rules modeled after regulated QA (aviation, pharma, nuclear): authority separation (QS-01), immutable SHA-256 evidence chains (QS-02), live-system qualification (QS-03), deviation/CAPA lifecycle (QS-04), deception tripwires (QS-05), eval integrity (QS-06), symbolic mode containment (QS-07), and safe requalification (QS-08). Sits above SRL as the governance layer. 73 tests.

**Bridge Module** (`pbhp_bridge.py`) — Cross-module coordination, coverage gap reporting, healthcare compliance adapter (ISO 14971 / MDR / IEC 62304), MBSE requirement taxonomy interface, and "demonstration > declaration" enforcement. Coverage gaps are prominently reported in every output — if PBHP cannot evaluate something, that is the loudest signal. 44 tests.

**Drift Meta-Monitor** (in `pbhp_drift.py`) — The drift monitor now monitors itself. Tracks heartbeat regularity, computation time drift, and alert rate changes. If drift monitoring stops producing heartbeats or its own behavior shifts, it escalates. 7 tests.

**Adaptive Uncertainty Threshold** (in `pbhp_core.py`) — `UncertaintyAssessment` now has an `update_threshold` field with context-aware multipliers (production = stricter, dev = looser). 11 tests.

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
│   ├── PromptBeforeHarmProtocol_v0.1.md  ← System prompt (START HERE)
│   ├── PBHP_Prompt_Paste_Versions.md     ← Paste-ready versions (~1250 / ~500 tokens)
│   ├── PBHP-CORE_INJECTION_v0.7.2.txt    ← Legacy agent-loadable plain text
│   ├── PBHP-CORE_v0.7.2.md               ← Full CORE tier specification
│   ├── PBHP-ULTRA_v0.7.2.md              ← Full ULTRA tier specification
│   ├── PBHP-MIN_v0.7.2.md                ← Minimum viable (reflex) tier
│   ├── PBHP_v0.7.2_HUMAN_UPDATED.md      ← Human-tier protocol (plain language)
│   └── PBHP-v0.7.2-TIER_SUPPLEMENTS.md   ← Tier-specific additions for v0.7.2
│
├── src/                                   ← Python implementation
│   ├── README.md                          ← Setup and usage instructions
│   ├── pbhp_core.py                       ← CORE tier engine (v0.8.0)
│   ├── pbhp_ultra.py                      ← ULTRA tier engine
│   ├── pbhp_min.py                        ← MIN tier engine
│   ├── pbhp_cli.py                        ← Command-line interface
│   ├── pbhp_examples.py                   ← Usage examples and walkthroughs
│   ├── pbhp_tests.py                      ← CORE tier test suite
│   ├── pbhp_min_ultra_tests.py            ← MIN + ULTRA tier test suite
│   ├── pbhp_triage.py                     ← Decision triage classifier (v0.8.0)
│   ├── pbhp_metrics.py                    ← Domain-specific harm metric packs (v0.8.0)
│   ├── pbhp_multiagent.py                 ← Multi-agent coordination protocol (v0.8.0)
│   ├── pbhp_compliance.py                 ← Compliance framework crosswalks (v0.8.0)
│   ├── pbhp_drift.py                      ← Drift rate measurement + meta-monitor (v0.8.1)
│   ├── pbhp_srl.py                        ← Scheming Resistance Layer (v0.8.1)
│   ├── pbhp_srl_tests.py                  ← SRL test suite (60 tests)
│   ├── pbhp_qs.py                         ← Quality Systems Layer (v0.8.1)
│   ├── pbhp_qs_tests.py                   ← QS test suite (73 tests)
│   ├── pbhp_bridge.py                     ← Bridge: cross-module, compliance, coverage (v0.8.1)
│   ├── pbhp_bridge_tests.py               ← Bridge test suite (44 tests)
│   └── pbhp_improvements_tests.py         ← Threshold + meta-monitor tests (18 tests)
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

Dual licensed: **MIT** for code (`src/`), **CC BY-SA 4.0** for protocol and documentation. Use it, adapt it, implement it. Attribution appreciated. If you build on PBHP, keep the core question intact. See [LICENSE](LICENSE) for details and non-negotiable clauses.

---

*"If I'm wrong, who pays first — and can they recover?"*
