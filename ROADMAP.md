# PBHP Roadmap

**Pause Before Harm Protocol** — Future development priorities.

Last updated: 2026-03-12

---

## Current State (v0.9.5)

20 Python modules, 730 tests passing across 13 test files, CI green on Python 3.10–3.12.

**All modules tested:**
- **pbhp_core** — CORE tier engine, uncertainty gate, pause logic, risk scoring (88 tests)
- **pbhp_min** / **pbhp_ultra** — MIN and ULTRA tier engines (45 tests)
- **pbhp_srl** — Scheming Resistance Layer: 6 rules, safety-monotonic state machine (60 tests)
- **pbhp_qs** — Quality Systems Layer: 8 rules modeled after aviation/pharma/nuclear QA (73 tests)
- **pbhp_bridge** — Cross-module coordination, healthcare compliance adapter, MBSE interface, SafetyClaimRegistry, CoverageGapCollector (44 tests)
- **pbhp_drift** — Drift measurement + DriftMetaMonitor self-check (18 tests)
- **pbhp_cli** / **pbhp_examples** — CLI and example smoke tests (29 tests)
- **pbhp_compliance** — Compliance framework crosswalks: NIST AI RMF, ISO/IEC 42001, ISO/IEC 23894, EU AI Act (89 tests)
- **pbhp_metrics** — Domain-specific harm metric packs: hiring, healthcare, finance, content moderation, security (53 tests)
- **pbhp_multiagent** — Multi-agent coordination: quorum voting, qualified veto, BLACK auto-escalation (61 tests)
- **pbhp_triage** — Decision triage classifier: tier routing, signal weights, HUMAN escalation triggers (80 tests)

**Cross-module verification:**
- **Integration tests** — SRL↔QS evidence flow, Bridge subcontracting, Triage→Core→Multiagent pipelines, drift→compliance mapping, full action→triage→SRL→QS→drift pipeline, state machine consistency, audit trail correlation (43 tests)
- **Adversarial eval** — BLACK gate bypass, state machine escape, self-preservation disguise, evidence tampering, tripwire evasion, sandbagging detection, multiagent safety weakening, triage gaming, drift manipulation, coverage gap honesty (47 tests)

**Community improvements shipped in v0.8.1** (all 7 implemented, carried forward to v0.9.5):
1. Healthcare compliance adapter (MDR/AiMD/ISO 14971) — `pbhp_bridge.py`
2. MBSE requirement taxonomy integration — `pbhp_bridge.py`
3. Cross-module subcontracting via ModuleRegistry — `pbhp_bridge.py`
4. Demonstration > declaration via SafetyClaimRegistry — `pbhp_bridge.py`
5. Adaptive uncertainty threshold — `pbhp_core.py`
6. Drift monitoring self-check via DriftMetaMonitor — `pbhp_drift.py`
7. Coverage gap prominence via CoverageGapCollector — `pbhp_bridge.py`

---

## Near-Term (v0.9.0) — "Prove the protocol before promoting it"

**Status: COMPLETE.** All v0.9.0 objectives shipped.

- ✅ **Test coverage hardening** — 283 new unit tests for compliance (89), metrics (53), multiagent (61), triage (80). All 13 modules now have dedicated test suites.
- ✅ **Cross-module integration tests** — 43 tests in `pbhp_integration_tests.py` covering SRL↔QS evidence flow, Bridge subcontracting, full pipeline workflows, state machine consistency, and audit trail correlation.
- ✅ **Adversarial eval scenarios** — 47 tests in `pbhp_eval_tests.py` covering BLACK gate bypass, state machine escape, self-preservation disguise, evidence tampering, tripwire evasion, sandbagging detection, multiagent safety weakening, triage gaming, drift manipulation, and coverage gap honesty.
- ✅ **Version coherence** — All public-facing files (README, src/README, ETHICAL_USE, CHANGELOG) updated to reflect v0.9.5 state accurately.
- ✅ **Release hygiene** — Honest test coverage table in README, CI running all 13 test suites, ROADMAP reflecting actual state.

### What v0.9.0 Proved
730 tests across 13 files. Every module boundary is exercised. 47 adversarial scenarios confirm that the safety-monotonic state machine, evidence chains, and cross-module coordination hold under attack. No test gaps remain at the unit or integration level.

---

## Mid-Term (v1.0.0)

### Eval Suite
Purpose-built evaluation suite for PBHP modules:
- Red-team prompt sets targeting each SRL rule
- Synthetic scenarios for QS tripwire and CAPA flows
- Regression tests against known frontier-model failure modes (Gemini shutdown
  redefinition, Claude sycophancy, GPT-4 sandbagging patterns)
- Benchmark scoring with variance analysis across runs

### Adapter Layer for Existing Frameworks
Lightweight adapters so PBHP can wrap existing agent frameworks:
- LangChain / LangGraph middleware
- AutoGen safety hooks
- CrewAI pre/post action gates
- OpenAI Assistants API wrapper

### Formal Specification
Translate the SRL and QS rules into a formal specification language (TLA+ or Alloy)
to enable model-checking of safety properties. Prove that the state machine is
safety-monotonic and that no sequence of agent actions can bypass human-required
gates.

### API and SDK
Expose PBHP as a lightweight HTTP service or Python SDK that teams can drop into
existing pipelines. Prioritize single-call integration: one function call to gate
an action, one function call to log evidence.

---

## Long-Term (v2.0.0+)

### Coworker Model Research
Investigate whether a fundamentally different training objective can produce an AI
that optimizes for joint work rather than task completion. Key research questions:

- Can a model be trained to maximize human agency preservation as a primary reward?
- What does a "deference-first" objective look like in RLHF?
- How do you train truth-telling as a terminal value rather than an instrumental one?
- Can symbolic reasoning modes be safely integrated without creating an operational
  backdoor?

This is exploratory research, not a near-term deliverable.

### Synthetic Dataset Generation
Generate training data that exercises PBHP safety properties:
- Scenarios where the "correct" action is to pause, confess, or defer
- Adversarial prompts that test each SRL rule boundary
- Multi-turn conversations where scheming would be rational but PBHP prevents it

### Multi-Agent Governance
Extend QS governance to multi-agent systems where multiple AI agents coordinate.
Key challenges:
- Which agent holds authority when agents disagree?
- How do you maintain evidence chains across agent boundaries?
- Can one agent's tripwire trigger freeze another agent?

### Symbolic Containment Formal Verification
Prove that symbolic/reflective modes cannot leak into operational authority through
any sequence of state transitions. This requires formal verification of the full
state machine including cross-module interactions.

---

## Contributing

PBHP is open source and welcomes contributors. Priority areas:
1. Healthcare/regulatory compliance adapters
2. Red-team test scenarios
3. Framework integration adapters
4. Formal verification of safety properties

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
GitHub: https://github.com/PauseBeforeHarmProtocol/pbhp
