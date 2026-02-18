# PBHP Pause Receipt Schema v1.1

## Purpose

A Pause Receipt is a compact, structured record of what PBHP decided and why. It turns PBHP from a private ritual into an auditable artifact. Receipts should be short enough to generate under pressure (<12 lines / small JSON) but complete enough to audit later.

## Schema (Required Fields)

```json
{
  "schema": "PBHP_RECEIPT_v1.1",
  "decision_id": "unique-id-or-hash",
  "timestamp": "2026-02-17T22:00:00Z",
  "agent_id": "agent name or ID (or 'unknown')",
  "operator_id": "human operator or org (or 'unknown')",
  "model_config": "model/version string + config identifier",

  "named_action": "I am going to [verb] [object] for [who] using [method]",
  "key_assumption": "what I'm assuming that could be wrong",
  "first_reversible_test": "what I checked (or 'skipped: [reason]')",

  "wall": "1-2 lines: constraints",
  "gap": "1-2 lines: where harm leaks",
  "door": "1-2 lines: smallest safer alternative",

  "gate": "GREEN | YELLOW | ORANGE | RED | BLACK",
  "impact": "Trivial | Moderate | Severe | Catastrophic",
  "likelihood": "Unlikely | Possible | Likely | Imminent",
  "irreversible": true,
  "power_asymmetry": true,
  "confidence": "Calibrated | Uncalibrated | Overconfident-under-uncertainty",
  "blast_radius": "Single-user | Multi-user | Systemic",
  "epistemic_tag": "FACT | INFERENCE | GUESS | UNKNOWN",

  "who_pays_first": "one line: who absorbs harm if wrong",
  "maybe": "If _____ is true, risk increases because _____",

  "tool_intent": {
    "tool_name": "name of tool (or null)",
    "irreversible": true
  },

  "decision": "proceed | constrain | modify | refuse",
  "justification": "1-2 lines: why this gate, why this decision"
}
```

## Optional Fields (Future-Proofing)

```json
{
  "receipt_hash": "sha256 of receipt content (blank today is fine)",
  "signature": "ed25519 signature slot (blank today is fine)",
  "config_fingerprint": "prompt hash or policy bundle version",
  "frame_check": "what am I treating as simple that might be the risk",
  "game_check": "what frame am I accepting that could be the harm engine",
  "drift_alarms_triggered": ["list of any drift phrases detected"],
  "forced_motion_detected": false,
  "parent_receipt_id": "for delegated/chained decisions"
}
```

## Plain-Text Receipt Format (for chat logs)

```
PBHP RECEIPT | 2026-02-17T22:00:00Z | agent: PBHP_Agent | gate: ORANGE
ACTION: I am going to batch-delete emails older than 6 months from user's inbox
ASSUMPTION: User wants permanent deletion (not archive)
FIRST TEST: List affected emails + count before deleting
WALL: No undo for permanent delete; don't know if compliance-relevant emails exist
GAP: User may not realize emails include tax receipts, legal threads
DOOR: Move to trash (recoverable 30 days) instead of permanent delete; show count first
CONFIDENCE: Uncalibrated (don't know email contents)
BLAST: Multi-user (shared threads)
EPISTEMIC: INFERENCE (user said "clean up" — interpreting as delete)
MAYBE: If compliance emails exist, deletion creates legal risk
WHO PAYS: User pays (lost data, potential legal exposure)
TOOL: batch-delete | irreversible: YES → require confirmation
DECISION: CONSTRAIN — move to trash, show preview, get explicit confirmation
```

## Rules

1. **Receipts are mandatory for ORANGE+ decisions.** Recommended for YELLOW. Optional for GREEN.
2. **Receipts should be honest.** A receipt that hides uncertainty is worse than no receipt. If you don't know, say UNKNOWN. If you're guessing, say GUESS.
3. **Comparable receipts for comparable cases.** Two agents facing the same scenario should produce structurally similar receipts, even if they reach different gates.
4. **Tool-use coupling:** If `tool_intent.irreversible` is true AND `epistemic_tag` is GUESS or UNKNOWN → receipt must document why proceeding is justified, or decision must be `constrain` or `refuse`.
5. **Delegation chaining:** If this decision was delegated from another agent, include `parent_receipt_id`. The chain should be traceable.

## Identity Attribution (Lightweight)

Even without cryptographic signing, receipts should include enough info to reconstruct "which agent config made this call":

- `agent_id`: stable identifier for the agent instance
- `model_config`: model name + version (e.g., "claude-opus-4-6", "gpt-4o-2025-01")
- `config_fingerprint`: hash of the system prompt or policy bundle version (optional but encouraged)

This allows post-incident analysis: "Was this decision made by an agent running PBHP v0.7.1 with config X, or a different version?"

## Adoption Path

1. **Today:** Generate plain-text receipts in chat logs for ORANGE+ decisions
2. **Next:** Implement JSON receipts in tool-calling agents
3. **Later:** Add `receipt_hash` and `signature` for tamper-evidence
4. **Eventually:** Receipt aggregation for observability metrics

---

PBHP v0.7.1 | Receipt Schema v1.1
