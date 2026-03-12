# PBHP Roadmap

**Pause Before Harm Protocol** — Future development priorities.

Last updated: 2026-03-11

---

## Current State (v0.8.0)

Implemented and tested modules:

- **pbhp_core** — Triage engine, uncertainty gate, pause logic, risk scoring
- **pbhp_ultra** — Extended constraints, adversarial-prompt detection, multi-agent coordination
- **pbhp_drift** — Behavioral drift monitoring and alerting
- **pbhp_srl** — Scheming Resistance Layer (6 rules, 60 tests)
- **pbhp_qs** — Quality Systems Layer (8 rules, 73 tests)

---

## Near-Term (v0.9.0)

### Healthcare Compliance Bridge
Adapter for MDR / AiMD / ISO 14971 risk-management requirements. Map PBHP triage
outputs to IEC 62304 software-lifecycle artifacts so medical-device teams can use
PBHP without building a separate compliance layer.

### MBSE Requirement Taxonomy Integration
Plug PBHP triage into existing Model-Based Systems Engineering (MBSE) requirement
taxonomies (SysML, DOORS). Triage decisions should map cleanly to system-level
requirements so PBHP doesn't live in a silo.

### Cross-Module Subcontracting
Currently modules are siloed — each runs its own checks independently. Add an
internal protocol so modules can delegate checks to each other (e.g., SRL asks
Drift for a behavioral snapshot before making a gate decision).

### Demonstration > Declaration
Make "show, don't tell" an explicit design principle. Every safety claim must point
to a test, log artifact, or reproducible evidence — never just a docstring assertion.

### Drift Monitoring Self-Check
The drift monitor monitors the agent but nobody monitors the drift monitor. Add a
meta-monitoring layer: if drift monitoring stops producing heartbeats or its own
behavior changes, escalate.

### Coverage Gap Prominence
Make coverage gaps prominent in every output — not an optional flag. If PBHP can't
evaluate something, that should be the loudest signal in the response.

### Uncertainty Gate Enhancement
Add `update_threshold` field so the uncertainty gate can adapt its sensitivity based
on operational context (e.g., tighter thresholds in production, looser in dev).

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
