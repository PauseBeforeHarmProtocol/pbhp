# PBHP — Pause Before Harm Protocol

**Repository snapshot:** v0.9.5-named research source with 17 post-audit fix categories implemented across 103 source/protocol lines explicitly labeled v0.9.6 (unreleased)

**Author:** Charles Phillip Linstrum

**License:** MIT for code; CC BY-SA 4.0 for protocol and documentation

**Email/Contact:** pausebeforeharmprotocol_pbhp@protonmail.com

**Social Media:** facebook.com/plinst

---

> [!IMPORTANT]
> This repository preserves the April 19, 2026 PBHP research snapshot. Its files and top-level `VERSION` retain the v0.9.5 name, while the final audit-fix commit implemented 17 fix categories across 103 source/protocol lines explicitly labeled v0.9.6. No matching v0.9.5 or v0.9.6 GitHub release/tag exists; the latest formal GitHub release remains v0.9.0. Do not represent this branch as a cleanly versioned release. It is not the canonical Project Shadow R1 package, a production system, a certification, or evidence of legal or regulatory compliance. Project Shadow is locked at `PROJECT SHADOW 1.0 / R1 REFERENCE / BETA-ACTIVE-TESTING / PRELIVE`; see [CURRENT_STATUS.md](CURRENT_STATUS.md) for exact identities and the current publication boundary.

## What Is PBHP?

PBHP is an experimental harm-reduction decision procedure for AI systems and human decision-makers. It is not alignment theory, professional advice, or a substitute for qualified human judgment.

Before acting on anything with stakes, PBHP asks one question:

> **"If I'm wrong, who pays first — and can they recover?"**

Then it gives you a structured way to answer it.

---

## Quick Start

**For AI research:** Review [`PromptBeforeHarmProtocol v0.2`](protocol/PromptBeforeHarmProtocol_v0.2.md) and the [`Paste Versions`](protocol/PBHP_Prompt_Paste_Versions.md) (~2200 and ~1000 token options) as preserved research prompts. Evaluate them in a controlled setting before any use; they do not grant action authority or qualify a live system.

**For developers:** Start with the [Executive Summary](reference/PBHP_EXECUTIVE_SUMMARY.md), then read the [Quick Reference Card](reference/PBHP_QUICK_REFERENCE_CARD.html) for a printable one-page overview. The [Python implementation](src/) is a tested research reference across the three software tiers; it is not qualified for production use.

**For researchers:** The full protocol exists in four tiers — [CORE](protocol/PBHP-CORE_v0.9.5.md) (operational), [ULTRA](protocol/PBHP-ULTRA_v0.9.5.md) (constitutional), [MIN](protocol/PBHP-MIN_v0.9.5.md) (reflex), and [HUMAN](protocol/PBHP_v0.9.5_HUMAN.md) (checklist). The [Eval Harness](eval/PBHP-EVAL_SET_v0.1.md) provides 12 adversarial scenarios for testing.

**For everyone:** Run the [Implementation Self-Test](implementation/PBHP_IMPLEMENTATION_SELF_TEST.md) after reading. Its five scenarios and 35-point rubric check the documented cases only; a passing score is not certification or evidence of real-world safety.

---

## How It Works

PBHP is a structured process scaled across four tiers (HUMAN, MIN, CORE, ULTRA) depending on decision complexity. The v0.9.5-named snapshot includes eight features: Mode Balance Monitor, Forward Consequence Projection, Stakeholder Dignity Rubric, Counterfactual Rehearsal, Power-Inversion Test, Crisis Commitment Priority, Multimodal Signal Filters, and Data Freshness Assurance. The core logic:

**1. Name the action honestly.** One sentence. No softening.

**2. Door / Wall / Gap.** WALL: What constrains you? GAP: Where could harm leak? DOOR: What is the smallest concrete alternative that reduces harm? If no Door exists, you pause.

**3. Constraint Awareness Check.** Do you recognize the system you're inside of? If "there is no choice" — is that true, or convenient?

**4. Identify harms.** Least-powerful stakeholders first. Check historical analogs. Audit the status quo.

**5. Rate each harm.** Impact, likelihood, irreversibility, power asymmetry. If unsure, round up.

**6. Assign a gate.** GREEN (proceed) → YELLOW (mitigate) → ORANGE (constrain) → RED (default refuse) → BLACK (refuse completely).

**7. Act on the gate.** Log everything.

Built-in controls are designed to flag rationalization through **drift alarms**, provide a challenge path through a **false positive valve**, and route identified power asymmetry to a higher gate under the documented rules.

---

## Modules

PBHP v0.8.x–v0.9.x adds operational modules that extend the core protocol:

**Triage Classifier** (`pbhp_triage.py`) — Routes incoming decisions to the appropriate tier (HUMAN/MIN/CORE/ULTRA) based on signal analysis. Evaluates irreversibility, vulnerable population impact, power asymmetry, and amplification potential. Prevents unnecessary escalation while ensuring high-risk decisions get appropriate scrutiny.

**Domain Metric Packs** (`pbhp_metrics.py`) — Pre-built severity thresholds for hiring, healthcare, finance, content moderation, and security. Each pack defines concrete harm levels (healthcare CATASTROPHIC = patient death), reversibility timeframes, and stakeholder templates. Eliminates guesswork in domain-specific risk scoring.

**Multi-Agent Coordination** (`pbhp_multiagent.py`) — Rules for modeled cases where multiple agents running PBHP reach different gate decisions. Implements quorum voting with veto for irreversible actions, weighted expert voting, and mandatory human review for BLACK gates. Tests exercise the intended fail-closed behavior; they do not establish real-world safety.

**Compliance Crosswalks** (`pbhp_compliance.py`) — Maps PBHP steps and artifacts to selected concepts in NIST AI RMF, ISO/IEC 42001, ISO/IEC 23894, and the EU AI Act for review. These are research crosswalks, not a determination that any requirement is satisfied and not certification or legal advice.

**Drift Measurement** (`pbhp_drift.py`) — Upgrades from binary drift flags to quantifiable drift rates. Tracks refuse rate, average gate level, vulnerable population impact, and confidence scores over time. Computes drift velocity, acceleration, and projects threshold breach dates.

**Scheming Resistance Layer** (`pbhp_srl.py`, v0.8.1) — Six experimental controls aimed at modeled scheming-related behaviors: anti-self-preservation (SRL-01), mandatory confession (SRL-02), live-systems gating (SRL-03), eval-awareness skepticism (SRL-04), self-report distrust (SRL-05), and anti-sandbagging (SRL-06). The state machine permits escalation while restricting de-escalation to human-authorized paths. Sixty tests exercise these rules; they do not prove prevention in frontier models.

**Quality Systems Layer** (`pbhp_qs.py`, v0.8.1) — Eight rules modeled after regulated QA (aviation, pharma, nuclear): authority separation (QS-01), tamper-evident SHA-256 evidence chains (QS-02), live-system qualification (QS-03), deviation/CAPA lifecycle (QS-04), deception tripwires (QS-05), eval integrity (QS-06), symbolic mode containment (QS-07), and safe requalification (QS-08). Sits above SRL as the governance layer. 73 tests.

**Bridge Module** (`pbhp_bridge.py`, v0.8.1) — Cross-module coordination via ModuleRegistry, coverage gap prominence via CoverageGapCollector, healthcare compliance adapter (ISO 14971 / MDR / IEC 62304), MBSE requirement taxonomy interface, and SafetyClaimRegistry for "demonstration > declaration" enforcement. Coverage gaps are prominently reported in every output — if PBHP cannot evaluate something, that is the loudest signal. 44 tests.

**Drift Meta-Monitor** (in `pbhp_drift.py`, v0.8.1) — The drift monitor monitors itself. Tracks heartbeat regularity, computation time drift, and alert rate changes. If drift monitoring stops producing heartbeats or its own behavior shifts, it escalates. 7 tests.

**Adaptive Uncertainty Threshold** (in `pbhp_core.py`, v0.8.1) — `UncertaintyAssessment.update_threshold` with context-aware multipliers (production = stricter, dev = looser). 11 tests.

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
│   ├── PromptBeforeHarmProtocol_v0.2.md  ← System prompt (START HERE)
│   ├── PBHP_Prompt_Paste_Versions.md     ← Paste-ready versions (~2200 / ~1000 tokens)
│   ├── PBHP-CORE_INJECTION_v0.9.5.txt    ← Agent-loadable plain text injection
│   ├── PBHP-CORE_v0.9.5.md               ← Full CORE tier specification
│   ├── PBHP-ULTRA_v0.9.5.md              ← Full ULTRA tier specification (constitutional)
│   ├── PBHP-MIN_v0.9.5.md                ← Minimum viable (reflex) tier
│   ├── PBHP_v0.9.5_HUMAN.md              ← Human-tier protocol (plain language)
│   ├── PBHP-v0.7.2-TIER_SUPPLEMENTS.md   ← Tier-specific additions (legacy)
│   └── [legacy v0.7.2 files preserved]   ← Previous version specifications
│
├── src/                                   ← Python implementation (20 modules)
│   ├── README.md                          ← Setup and usage instructions
│   ├── pbhp_core.py                       ← CORE tier engine
│   ├── pbhp_ultra.py                      ← ULTRA tier engine
│   ├── pbhp_min.py                        ← MIN tier engine
│   ├── pbhp_cli.py                        ← Command-line interface
│   ├── pbhp_examples.py                   ← Usage examples and walkthroughs
│   ├── pbhp_triage.py                     ← Decision triage classifier
│   ├── pbhp_metrics.py                    ← Domain-specific harm metric packs
│   ├── pbhp_multiagent.py                 ← Multi-agent coordination protocol
│   ├── pbhp_compliance.py                 ← Compliance framework crosswalks
│   ├── pbhp_drift.py                      ← Drift rate measurement + meta-monitor
│   ├── pbhp_srl.py                        ← Scheming Resistance Layer (6 rules)
│   ├── pbhp_qs.py                         ← Quality Systems Layer (8 rules)
│   ├── pbhp_bridge.py                     ← Bridge: cross-module, compliance, coverage
│   ├── pbhp_tests.py                      ← CORE tier tests (88)
│   ├── pbhp_min_ultra_tests.py            ← MIN + ULTRA tier tests (45)
│   ├── pbhp_srl_tests.py                  ← SRL tests (60)
│   ├── pbhp_qs_tests.py                   ← QS tests (73)
│   ├── pbhp_bridge_tests.py               ← Bridge tests (44)
│   ├── pbhp_improvements_tests.py         ← Threshold + meta-monitor tests (18)
│   ├── pbhp_cli_tests.py                  ← CLI + examples smoke tests (29)
│   ├── pbhp_compliance_tests.py           ← Compliance framework tests (89)
│   ├── pbhp_metrics_tests.py              ← Domain metric pack tests (53)
│   ├── pbhp_multiagent_tests.py           ← Multi-agent coordination tests (61)
│   ├── pbhp_triage_tests.py               ← Decision triage tests (80)
│   ├── pbhp_integration_tests.py          ← Cross-module integration tests (43)
│   └── pbhp_eval_tests.py                 ← Adversarial red-team eval tests (47)
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

Most AI safety work focuses on alignment — making AI systems want the right things. PBHP focuses on **process** by offering AI systems and humans a structured way to look for potential harm before acting.

The difference matters. An aligned system can still cause harm through:

- Drift (gradual normalization of harmful patterns)
- Rationalization (constructing justifications after the decision is already made)
- Power blindness (not noticing who absorbs the cost of being wrong)
- False confidence (high certainty under genuine uncertainty)

PBHP addresses these failure modes with specific mechanisms: drift alarms act as tripwires for rationalization, Door/Wall/Gap prompts escape-vector identification, power-asymmetry rules raise the documented gate floor, and the false-positive valve provides a structured challenge path.

---

## Test Coverage

**730 tests passing** across 13 test files in a fresh local run on August 14, 2026; CI is configured for Python 3.10, 3.11, and 3.12. Test passage demonstrates the checked software behavior only. It does not establish efficacy, safety, production readiness, compliance, certification, complete coverage, or absence of defects.

| Module | Tests | Recorded test focus |
|--------|-------|--------|
| `pbhp_core` | 88 | Checked cases |
| `pbhp_min` / `pbhp_ultra` | 45 | Checked cases |
| `pbhp_srl` | 60 | Red-team-style scenarios included |
| `pbhp_qs` | 73 | CAPA lifecycle and tripwire cases |
| `pbhp_bridge` | 44 | ModuleRegistry, SafetyClaimRegistry, and gap-reporting cases |
| `pbhp_drift` (meta-monitor) | 18 | Heartbeat and threshold-adaptation cases |
| `pbhp_cli` / `pbhp_examples` | 29 | Smoke and structural checks |
| `pbhp_compliance` | 89 | Four research crosswalks, report, and checklist cases |
| `pbhp_metrics` | 53 | Five domain-pack, threshold, and stakeholder cases |
| `pbhp_multiagent` | 61 | Quorum, veto, and BLACK-escalation cases |
| `pbhp_triage` | 80 | Tier-routing, signal-weight, and HUMAN-escalation cases |
| Cross-module integration | 43 | SRL↔QS, Bridge↔core, and pipeline cases |
| Adversarial eval | 47 | BLACK-bypass, state-escape, and disguise cases |

---

## License

Dual licensed: **MIT** for code (`src/`, `eval/`) and **CC BY-SA 4.0** for the protocol and documentation paths listed in [LICENSE](LICENSE). The ethical invariants in [ETHICAL_USE.md](ETHICAL_USE.md) are non-legally-binding guidance, not additional license restrictions. Permission to reuse does not imply validation, endorsement, suitability, safety, or compliance.

---

*"If I'm wrong, who pays first — and can they recover?"*
