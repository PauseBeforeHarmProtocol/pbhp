# Changelog

All notable changes to PBHP will be documented in this file.

## [0.8.1] - 2026-03-11

### Added
- Scheming Resistance Layer (`pbhp_srl.py`) — 6 rules: anti-self-preservation (SRL-01), mandatory confession (SRL-02), live-systems gating (SRL-03), eval-awareness skepticism (SRL-04), self-report distrust (SRL-05), anti-sandbagging (SRL-06). Safety-monotonic state machine with human-required de-escalation. 60 tests including red-team scenarios based on real frontier model failures
- Quality Systems Layer (`pbhp_qs.py`) — 8 rules modeled after aviation/pharma/nuclear QA: authority separation, immutable SHA-256 evidence chains, deception tripwires, CAPA lifecycle, symbolic mode containment, safe requalification. 73 tests
- Bridge Module (`pbhp_bridge.py`) — cross-module subcontracting via ModuleRegistry, coverage gap prominence, healthcare compliance adapter (ISO 14971 / MDR / IEC 62304), MBSE requirement taxonomy interface, SafetyClaimRegistry for demonstration > declaration. 44 tests
- Drift Meta-Monitor (`DriftMetaMonitor` in `pbhp_drift.py`) — drift monitoring monitors itself via heartbeat tracking, computation time drift, and alert rate change detection. 7 tests
- Adaptive Uncertainty Threshold (`update_threshold` on `UncertaintyAssessment` in `pbhp_core.py`) — context-aware multipliers (prod=0.7x stricter, dev=1.5x looser, emergency=1.3x). 11 tests
- ROADMAP.md — near-term, mid-term, and long-term development priorities
- GitHub Actions CI workflow — automated test execution on push/PR

### Changed
- Coverage gaps are now the loudest signal in every output (CoverageGapCollector with prominent formatting)
- Modules can now subcontract capabilities to each other via ModuleRegistry instead of silently skipping checks
- Every safety claim must point to evidence (test, log, artifact) — unverified claims flagged prominently
- QS requalification properly routes through FROZEN → AWAITING_HUMAN_REVIEW → REQUALIFIED state path

### Community Improvements Addressed
- #1: Healthcare compliance gap (MDR/AiMD/ISO 14971) — adapter with compliance matrix
- #2: MBSE requirement taxonomy integration — interface for SysML/DOORS
- #3: Architecture siloed — cross-module subcontracting protocol
- #4: Demonstration > declaration — SafetyClaimRegistry
- #5: Uncertainty gate update_threshold — adaptive sensitivity
- #6: Drift monitoring self-check — DriftMetaMonitor
- #7: Coverage gaps prominent — CoverageGapCollector

### Test Coverage
- Total: 328 tests passing (60 SRL + 73 QS + 44 bridge + 18 improvements + 88 core + 45 min/ultra)

## [0.8.0] - 2026-03-04

### Added
- Decision Triage Classifier (`pbhp_triage.py`) — routes decisions to HUMAN/MIN/CORE/ULTRA based on 8 risk signals with weighted scoring
- Domain-Specific Metric Packs (`pbhp_metrics.py`) — pre-built severity thresholds for hiring, healthcare, finance, content moderation, security
- Multi-Agent Coordination Protocol (`pbhp_multiagent.py`) — quorum voting, qualified veto on irreversible actions, BLACK gate auto-escalation
- Compliance Framework Crosswalks (`pbhp_compliance.py`) — mappings to NIST AI RMF, ISO/IEC 42001, ISO/IEC 23894, EU AI Act
- Drift Rate Measurement Engine (`pbhp_drift.py`) — quantifiable drift velocity, acceleration, threshold breach projection, temporal analysis

### Changed
- Version bump from 0.7.2 to 0.8.0 across all source files, documentation, and references
- Triage module integrates with existing tier architecture (HUMAN/MIN/CORE/ULTRA)
- Metric packs use existing ImpactLevel and LikelihoodLevel enums from pbhp_core
- Multi-agent coordination uses existing RiskClass and DecisionOutcome from pbhp_core
- Compliance crosswalks reference existing PBHP 7-step process
- Drift measurement extends existing drift alarm concept from qualitative flags to quantitative metrics

### Design Principles (v0.8.0)
- All new modules import from pbhp_core — no parallel type systems
- Each module is independently usable — no mandatory dependencies between new modules
- Triage routes TO existing tiers, does not replace them
- Metric packs are domain templates, not overrides — existing scoring logic unchanged
- Multi-agent coordination defaults to most conservative gate on ties
- Compliance crosswalks are evidence maps, not certification claims
- Drift measurement is additive — existing binary drift alarms still function

## [0.7.2] - 2026-02-25

### Terminology Migration
- "CHIM Check" renamed to "Constraint Awareness Check" across all protocol docs, source code, and tests
- Author attribution "(ALMSIVI)" removed — author is now "Charles Phillip Linstrum"
- Mythic names (AYEM/SEHTI/VEHK) retired from active use; Care/Clarity/Paradox is final terminology
- STANDALONE_TERMINOLOGY.md converted to historical reference (migration complete)
- Python class `CHIMCheck` renamed to `ConstraintAwarenessCheck`
- Python variable `chim_check` renamed to `constraint_awareness_check`

### Added
- PromptBeforeHarmProtocol v0.1 — definitive system prompt merging best of v0.7.1 CORE and v0.8
- Door Quality Rubric (D0–D3) with enforcement rules (ORANGE+ requires ≥D2)
- Accumulation Gate — multi-step chain detection for individually-GREEN steps composing into harm
- LOCK/FLOOD governor — prevents premature collapse and analysis paralysis
- Deterministic gate → action mapping (GREEN=PROCEED through BLACK=REFUSE)
- Harm threshold interpretation note (financial/psychological harm as autonomy-destroying cascades)
- Tool-use coupling with epistemic tags restored from v0.7.1 CORE
- Paste-ready prompt versions: Version A (~1250 tokens), Version B (~500 tokens)

### Changed
- Gate assignments now have explicit required actions, not just risk labels
- Door quality is scored (D0–D3), not just warned about
- False positive valve, game check, forced-motion trap detector integrated into system prompt

## [0.7.1] - 2026-02-18

### Added (CORE Injection)
- First Reversible Test micro-step (mandatory before irreversible actions)
- Key Assumption declaration ("I am assuming _____. Quick check: _____.")
- Frame Check ("What am I being asked to treat as 'simple' that might be the risk?")
- Protected MAYBE slot (formal uncertainty that changes behavior, not just labels)
- Confidence/Calibration modifier (Calibrated / Uncalibrated / Overconfident-under-uncertainty)
- Cascade/Blast Radius modifier (Single-user / Multi-user / Systemic)
- Tool-Use Hard Coupling (GUESS/UNKNOWN + irreversible tool → require confirmation or reversible Door)
- Low-Power Requester edge case (requester is the vulnerable party)
- Forced-Motion Trap Detector (anti-coercion trigger list + calm procedural response)
- Game Check (frame audit: "What frame am I accepting that could be the harm engine?")
- Epistemic tags in harm rating (FACT / INFERENCE / GUESS / UNKNOWN)

### Added (New Files)
- Receipt Schema v1.1 (`receipts/PBHP-RECEIPT_SCHEMA_v1.1.md`)
- Decision Hygiene Micro-Module (`modules/PBHP-DECISION_HYGIENE_v0.1.txt`)
- Observability Pack v0.1 (`observability/PBHP-OBSERVABILITY_PACK_v0.1.md`)
- Eval Harness Starter Pack v0.1 (`eval/PBHP-EVAL_SET_v0.1.md`) — 12 adversarial scenarios, 10 failure modes
- Tier Supplements v0.7.1 (`protocol/PBHP-v0.7.1-TIER_SUPPLEMENTS.md`) — aligned updates for ULTRA, MIN, and HUMAN
- CONTRIBUTING.md
- Adversarial Patterns reference (`reference/ADVERSARIAL_PATTERNS.md`)
- Door Library reference (`reference/DOOR_LIBRARY.md`)

### Changed from 0.7
- CORE injection restructured with new micro-steps (Step 1a: First Reversible Test + Assumption + Frame + MAYBE)
- Harm rating expanded: confidence scoring (3 levels), cascade scoring (3 levels), epistemic tags
- CONFIDENCE RULE: Uncalibrated + irreversible → round gate UP or require reversible Door
- OVERCONFIDENCE RULE: Overconfident-under-uncertainty → force pause + verification Door
- CASCADE RULE: Multi-user + uncertainty → minimum ORANGE; Systemic + tool execution → minimum ORANGE+
- All four tiers (HUMAN, MIN, CORE, ULTRA) aligned with v0.7.1 concepts via tier supplements

### Design Principles (v0.7.1)
- CORE injection stays lean and runnable in-context
- Receipts, observability, and eval packs are optional add-ons
- New checks prevent known failure modes (assumption traps, premature irreversibility, frame blindness)
- Every new item either: prevents a known failure mode, makes decisions measurable/auditable, or improves handling of uncertainty and framing

## [0.7] - 2026-02-14

### Added
- Four-tier architecture: HUMAN, MIN, CORE, ULTRA
- Five-gate risk classification: GREEN, YELLOW, ORANGE, RED, BLACK
- Door/Wall/Gap escape vector framework
- False positive release valve with 4-part challenge mechanism
- Power-asymmetry auto-escalation (deterministic, not multiplicative)
- Three-Force Balance (Care, Clarity, Paradox) replacing five-mode requirement at CORE tier
- 17+ drift alarm triggers with specific rerun requirements
- Standalone terminology (no external framework dependencies)
- PBHP-CORE plain text injection format (agent-loadable)
- Implementation self-test (5 scenarios, 35-point rubric)
- Retrospective case studies (Bing Sydney 2023, Air Canada 2024)
- 90-day implementation playbook
- Governance charter with non-negotiable elements
- Comparison matrices against existing frameworks

### Changed from 0.6
- Replaced simple risk multiplier with deterministic power-asymmetry escalation
- Expanded drift alarms from phrase-only to behavioral pattern detection
- Added Baseline Reality Check (Historical Analog Scan + Status Quo Harm Audit)
- Added Temporal + Cultural Impact Modeling
- Introduced Mode Selection (EXPLORE/COMPRESS/BOTH) at Step 1B
- Separated CORE and ULTRA into distinct documents
- Created MIN tier for reflex-speed decisions
- Created HUMAN tier for non-AI decision-makers

## [0.6] - 2025

- Five reasoning modes (Logic, Intelligence, Compassion, Empathy, Paradox)
- Initial gate system (GREEN through BLACK)
- Door/Wall/Gap first implementation
- Drift alarm phrases introduced
- White paper draft

## [0.5] - 2025

- Core protocol structure established
- Harm identification and rating system
- Power asymmetry as risk factor
- Initial false positive mechanism

## [0.1–0.4] - 2024–2025

- Conceptual development
- Iterative testing with multiple AI systems
- Integration with ALMSIVI CHIM framework
- Progressive refinement of gate criteria
