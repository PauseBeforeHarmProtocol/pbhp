# Changelog

All notable changes to PBHP will be documented in this file.

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
