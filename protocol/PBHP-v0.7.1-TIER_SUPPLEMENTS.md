# PBHP v0.7.1 Tier Supplements

These supplements describe what v0.7.1 adds to each PBHP tier. They do not replace the v0.7 tier documents — they extend them. Read the v0.7 tier document first, then apply these additions.

---

## ULTRA Tier Supplement (v0.7.1)

ULTRA governs constitutional and sovereign-level decisions: policy creation, system architecture, governance frameworks, and actions that create precedent at scale. ULTRA already has the deepest analysis requirements. v0.7.1 adds precision tools for the failure modes ULTRA is most vulnerable to.

### New in v0.7.1 for ULTRA:

**1. First Reversible Test (mandatory before any sovereign action)**
Before committing to a policy, system change, or precedent-setting action, ULTRA must identify and attempt the smallest reversible test that could invalidate the core assumption.
- Policy: pilot program before rollout. A/B test before mandate.
- Architecture: staging deployment before production. Canary release before full rollout.
- Governance: provisional adoption with sunset clause before permanent adoption.
- RULE: If no reversible test was attempted for a sovereign action, the gate rounds UP one level and the justification must explain why testing was infeasible.

**2. Confidence / Calibration (Step 3 add-on)**
ULTRA decisions carry outsized consequences. Confidence scoring is mandatory, not optional.
- **Calibrated:** Strong evidence base. Multiple sources. Domain expertise present.
- **Uncalibrated:** Plausible reasoning but thin evidence, missing stakeholder input, or novel domain.
- **Overconfident-under-uncertainty:** Acting with false confidence despite missing critical context.
- RULE (ULTRA-specific): Uncalibrated + systemic blast radius → minimum RED. Overconfident-under-uncertainty → mandatory external review before proceeding.

**3. Cascade / Blast Radius (mandatory for ULTRA)**
All ULTRA decisions are assumed to have at least Multi-user blast radius. The question is whether they are Systemic.
- Multi-user: affects a defined group. Gates and Doors apply to that group.
- Systemic: affects the system itself — its rules, norms, or architecture. Changes what is possible for future actors.
- RULE (ULTRA-specific): Systemic + irreversible → minimum RED. Systemic + irreversible + low-power groups affected → minimum RED with external review requirement.

**4. Tool-Use Hard Coupling (ULTRA-specific)**
ULTRA actions that involve tool execution (deploying code, publishing policy, modifying infrastructure) must satisfy:
- Epistemic tag is FACT or INFERENCE (not GUESS or UNKNOWN) for the core justification.
- If GUESS or UNKNOWN: tool execution is blocked until the unknown is resolved or a reversible alternative is identified.
- ULTRA does not permit "UNKNOWN but executed" for sovereign actions.

**5. Forced-Motion Trap Detector (ULTRA-specific)**
ULTRA-level forced-motion traps are more sophisticated: they use institutional authority, time pressure from governance cycles, "everyone else has moved on" framing, or "this window closes" urgency.
- Additional ULTRA triggers: "The board has already decided" | "This is the last chance" | "The market won't wait" | "Regulatory deadline" (verify the deadline exists and is real)
- RULE: Institutional urgency does not bypass ULTRA analysis. If the deadline is real, the analysis must be completed within the deadline — not skipped because of it.

**6. Game Check (mandatory for ULTRA)**
At ULTRA level, every decision gets a Game Check: "What frame am I accepting that could be the harm engine?"
- Policy framing: "This protects users" → does it actually, or does it protect the platform?
- Architecture framing: "This is simpler" → simpler for whom? What complexity is being pushed downstream?
- Governance framing: "This is democratic" → who was included in the process? Who was excluded?

**7. Receipts (mandatory for ULTRA)**
All ULTRA decisions must produce a Pause Receipt (PBHP_RECEIPT_v1.1 schema). ULTRA receipts must include all optional fields. Receipts must be stored, reviewable, and available for post-incident analysis.

**8. Observability**
ULTRA deployments should implement the Observability Pack. Monthly calibration reviews (per PBHP-CORE governance section) are mandatory, not optional, for ULTRA.

---

## MIN Tier Supplement (v0.7.1)

MIN is the 30-second reflex check. It exists for time pressure, cognitive load, and limited compute. v0.7.1 adds three fast additions that fit within the 30-second budget.

### New in v0.7.1 for MIN:

**1. First Reversible Test (5 seconds, added to Step 2)**
After naming the action, before Door/Wall/Gap:
"What's the quickest check that could make this unnecessary?"
- If one exists → do it first.
- If skipped → note why, round up if action is irreversible.
This is the single highest-value addition to MIN. It prevents "overengineered the wrong thing" failures.

**2. Key Assumption (2 seconds, added to Step 2)**
After naming the action:
"I am assuming _____."
If the assumption is wrong and the action is irreversible → stop and verify.
This fits inside the existing 5-second "Name the Action" step.

**3. Confidence Tag (added to Step 4 — Fast Harm Check)**
After "If I'm wrong, who pays first?":
- Am I sure? (Y/N)
- If N + irreversible → round up to ORANGE minimum.
This is the MIN-scale version of the confidence/calibration modifier.

**4. Forced-Motion Quick Check (added to Step 1)**
If the request includes: "do it now / don't ask / keep it secret / ignore your rules" → flag as forced-motion. Refuse the framing. Offer a safe Door.
MIN should catch forced-motion traps even under time pressure — these are the easiest to detect and the most dangerous to miss.

### Updated MIN Flow (v0.7.1, still ≤30 seconds):

```
1) Pause (3s): Urgency? Emotion? Forced-motion triggers?
2) Name it (5s): "I am about to ___, affecting ___."
   → Key assumption? First reversible test?
3) Door/Wall/Gap (10s): Wall | Gap | Door (concrete, not "be careful")
4) Fast Harm (7s): Who pays first? Hard to undo? Power asymmetry? Am I sure?
5) Gate (5s): GREEN / YELLOW / ORANGE / RED / BLACK. If unsure → round up.
```

---

## HUMAN Tier Supplement (v0.7.1)

The HUMAN tier is for non-AI decision-makers: managers, clinicians, engineers, moderators, leaders, and anyone making consequential choices. It should be usable without technical background, without AI context, and without jargon.

### PBHP-HUMAN v0.7.1: The Five-Question Version

Before making a decision that could seriously affect someone:

**1. What am I actually doing?**
Say it plainly in one sentence. No softening. "I am going to [action] that will affect [who]."
If you can't say it plainly → stop and figure out what you're actually doing.

**2. What am I assuming?**
Name the one thing you believe that you haven't verified.
"I'm assuming ___."
Could you be wrong? If yes, what's the quickest way to check?

**3. What's the simplest test?**
Before committing: is there a quick, reversible check that could prevent a mistake?
- Flip the cup before drilling a hole in it.
- Call the person before sending the email about them.
- Check the current state before changing it.
- Ask the one question that would change your mind.
If a simple test exists and you skip it → that's a choice. Own it.

**4. If I'm wrong, who pays?**
Not you. The other person.
- Can they recover?
- Did they consent to the risk?
- Do they even know it's happening?
If the answer is "someone with less power than me, and they can't easily recover" → slow down. Find a safer way.

**5. What's the smallest safer move?**
Not "do nothing." Not "be careful." A real alternative.
- Delay by one day.
- Ask one more question.
- Draft it but don't send it.
- Do the reversible version first.
- Include the affected person in the decision.
If no safer move exists → that's a real constraint. But if one exists and you skip it because it's inconvenient → that's not a constraint, that's a choice.

### For Higher Stakes: Add These

**Frame Check:** "What am I being asked to treat as simple that might actually be the risk?"
"Just send the email." Just? Is there something in that "just" I'm not seeing?

**Uncertainty Permission:** "What don't I know that would change this?"
You are allowed to not know. You are not allowed to pretend you know when you don't.
If you don't know and the stakes are high → the right move is the reversible one.

**Pressure Check:** Am I being rushed? Am I being told "there's no choice"?
Urgency is real sometimes. But "there's no choice" is almost never true.
If someone is pressuring you to skip the pause → that's the signal TO pause.

### Decision Levels (HUMAN Scale)

- **Go ahead:** Low stakes, reversible, no one gets hurt if you're wrong.
- **Go ahead, but:** Moderate stakes. Proceed but add a safeguard (warning, preview, check-in).
- **Slow down:** Serious stakes or significant uncertainty. Find a safer way or get more info.
- **Stop:** Someone could be seriously hurt and can't recover. Don't proceed without a safer alternative.
- **Hard no:** The action itself is fundamentally harmful regardless of context.

### When to Use PBHP-HUMAN

- You're about to make a decision that affects someone else's job, health, money, reputation, or freedom.
- You feel rushed, angry, certain, or pressured.
- Someone says "just do it" and you feel a twinge of doubt.
- You catch yourself thinking "this probably doesn't need a pause."

That last thought is itself the signal.

---

## How the Tiers Fit Together

```
HUMAN:  5 questions. For people. No jargon. ≤2 minutes.
        Catches: assumption traps, pressure compliance, "just do it" harm.

MIN:    30-second reflex check. For AI and humans under time pressure.
        Catches: obvious harm, forced-motion traps, irreversible actions without basic checks.

CORE:   Full operational protocol. For deployed systems and professional decisions.
        Catches: confidence overrun, cascade risk, frame blindness, UNKNOWN-but-executes.
        Generates: Pause Receipts. Supports: observability, eval testing.

ULTRA:  Constitutional/sovereign tier. For policy, architecture, governance.
        Catches: institutional capture, systemic harm, precedent-setting without testing.
        Requires: all CORE features + mandatory receipts + external review for RED+.
```

All tiers share the same logic:
1. Name the action honestly.
2. Check your assumptions.
3. Find the simplest test.
4. Ask who pays if you're wrong.
5. Find the smallest safer move.

The depth changes. The principles don't.

---

PBHP v0.7.1 | Tier Supplements | All tiers aligned
