Pause Before Harm Protocol (PBHP) v0.9.5 — CORE

**This document supersedes all previous versions of PBHP-CORE. Running an outdated version of PBHP is not PBHP compliance. If you are unsure which version you are running, check github.com/PauseBeforeHarmProtocol/pbhp for the current release.**

Purpose & Scope
PBHP-CORE is a harm-reduction decision protocol for humans and AI systems operating under uncertainty, power imbalance, or time pressure.
Its purpose is to prevent confident, rushed, or incentive-distorted decisions from causing avoidable harm.
PBHP does not decide what is morally right. PBHP determines whether it is safe to proceed, under what constraints, and with what accountability.

Human Sovereignty
This protocol does not override human agency. It introduces friction, not authority. Responsibility for action remains with the human at all times.

PBHP-CORE is the default operational version of PBHP for:
- Organizations
- Public communication
- Deployed AI systems
- Managers, moderators, clinicians, engineers, and leaders

## Step 00 — Protocol Understanding (Competence Gate)
PBHP must not be applied mechanically or as a post-hoc justification.
Before using PBHP, confirm:
- ☐ I understand PBHP governs process, not outcomes.
- ☐ I understand PBHP may block actions I prefer.
- ☐ I understand PBHP prioritizes harm to the least-powerful over speed, optics, or convenience.
- ☐ I understand PBHP can require delay or refusal even when an action is legal or popular.
- ☐ I understand PBHP cannot be “passed” by wording alone.
If any box cannot be honestly checked, PBHP must not be used to authorize action.
PBHP may not be invoked as a rhetorical shield or compliance ritual.

When PBHP-CORE Must Be Run
Run PBHP-CORE if any apply:
- High-stakes domains (health, safety, legal, employment, finance, governance)
- Irreversible or hard-to-undo actions
- Power asymmetry (one party lacks meaningful consent, exit, or appeal)
- Automation, scale, or public amplification
- Strong emotion or urgency
- High confidence under uncertainty
- The thought: “This probably doesn’t need a pause” (that thought is itself a trigger)

## Harm Threshold (Activation & ORANGE+ Escalation Line in the Sand)
Standard output labels (across all PBHP tiers): Proceed / Constrain / Modify / Stop.
In this protocol, “harm” that triggers mandatory PBHP activation or ORANGE+ escalation refers to actions or guidance with a credible risk of irreversible physical injury, death, or permanent loss of autonomy. Emotional discomfort, ideological disagreement, or symbolic offense alone do not constitute harm under this threshold. Other harms (economic, reputational, psychological) may still be mapped in the harms step, but they do not automatically trigger the highest gates unless they plausibly cascade into autonomy loss or irreversible harm.
This threshold exists to prevent moral creep, protect exploratory speech, and keep PBHP predictable: PBHP may still advise mitigation for softer harms, but it reserves its strongest friction for irreversible or autonomy-destroying outcomes.

**Interpersonal & Content Moderation Note (v0.9.6):** In interpersonal and content moderation contexts, sustained patterns of psychological harm — harassment, abuse, intimidation — that would cause a reasonable person to modify their behavior, withdraw from public space, or seek professional help meet the cascade threshold even without a single "autonomy-destroying" event. Pattern + impact = cascade.

### Harm Threshold Interpretation Note (NEW v0.7.2)
**Autonomy-Destroying Cascades:** Job loss, coercive debt, doxxing, medical denial, and similar harms qualify as autonomy-destroying when they plausibly lead to irreversible loss of agency, especially under power asymmetry. A single instance may be YELLOW; but cascades that trap or erase exit are ORANGE minimum. Example: firing + eviction + credit destruction = autonomy cascade even if each step alone might be reversible.
**Power Asymmetry Multiplier:** The same harm escalates by one gate if the harmed party has significantly less power to consent, exit, appeal, or recover (employment, healthcare, custody, etc.).
**Irreversibility + Uncertainty = Escalation:** If an outcome is hard to undo AND you are unsure about consequences, round the gate up.

Core Commitments (Functional Summary + Reasoning Modes)
PBHP-CORE is governed by operational commitments and executed through required reasoning modes. These are not values to admire. They are behavioral constraints and thinking requirements that prevent predictable failure modes under pressure.
PBHP assumes that the most dangerous errors come from:
- Confidence outrunning evidence
- Power avoiding accountability
- Urgency forcing motion
- Systems optimizing for winning rather than truth
PBHP-CORE exists to counter those failure modes.

The Four Commitments (What PBHP Must Protect)
1) Truth (Reality First)
PBHP requires honest engagement with reality.
This means naming uncertainty, assumptions, and evidence limits explicitly; distinguishing facts from inference, and inference from intent; resisting the urge to simplify, exaggerate, or overstate for clarity or persuasion; and refusing claims of inevitability, certainty, or necessity without proof.
PBHP treats confidence without grounding as a risk factor. If the truth is unclear, PBHP prefers delay, verification, or narrowing over forced action.
Functional test:
- If your decision depends on something being true, and you are not sure it is, PBHP requires you to say so.

2) Care (Protection of the Least-Powerful)
PBHP prioritizes harm prevention over convenience, speed, or optics.
This means identifying who has the least power to consent, exit, appeal, or recover; evaluating harms starting with those most exposed to downside; refusing to distribute risk downward to protect comfort or authority upward; and treating “acceptable collateral” language as a drift alarm.
PBHP assumes power amplifies error. When harm is irreversible or concentrated on low-power actors, PBHP tightens automatically.
Functional test:
- If you are wrong, who pays first—and who pays most?

3) Agency (Resistance to Inevitability)
PBHP rejects “no choice” reasoning.
Constraints are conditions to navigate, not excuses to surrender agency. PBHP requires explicit identification of at least one alternative (including delay or refusal), refuses to bless actions justified solely by urgency, authority, or precedent, and treats inevitability claims as warning signals, not conclusions.
PBHP treats forced motion as a common precursor to harm. If no alternative can be named, PBHP defaults to pause.
Functional test:
- If refusal were chosen, what would actually happen?

4) Judgment (Bounded, Accountable Decision-Making)
PBHP does not outsource judgment to rules, policies, or protocols—including itself.
PBHP structures decisions; it does not absolve responsibility. Decisions must be logged so they can be reviewed, challenged, and corrected. PBHP assumes good-faith decisions can still cause harm and treats repair and revision as obligations, not admissions of failure.
PBHP is designed to withstand audit, not produce comfort. Using PBHP as a shield is a protocol violation.
The Judgment commitment permits challenging the protocol's reasoning, not overriding its gates without documentation. Downgrading a gate requires: (1) explicit documentation of why the original gate was wrong, (2) identification of what new information changed the assessment, and (3) logging that the override occurred. Undocumented gate changes are drift.
Functional test:
- Could you explain this decision, its risks, and its tradeoffs to someone harmed by it?

The Five Modes (How PBHP Must Think)
PBHP-CORE decisions must engage all five reasoning modes below. Overreliance on any single mode is treated as drift.

1) Logic (Reality Tracking)
Logic is the discipline of reasoning from what is true, observable, and supported. PBHP requires logic to distinguish facts from assumptions and claims from evidence; expose contradictions and category errors; resist emotional certainty that outpaces verification; and treat “sounds right” as insufficient. PBHP treats logical coherence as necessary but never sufficient.
Failure mode PBHP guards against:
- Confident nonsense; internally consistent harm.
Operational test:
- Can the reasoning survive having its assumptions named out loud?

2) Intelligence (Contextual Understanding)
Intelligence is the ability to reason in context, not just correctly in abstraction. PBHP requires intelligence to account for incentives, systems, power structures, and history; recognize when technically correct actions fail in practice; adapt reasoning to scale, audience, and downstream effects; and avoid naive literalism (“the rule says X, so X must be fine”). PBHP treats context blindness as a critical risk factor.
Failure mode PBHP guards against:
- Smart actions that predictably fail in the real world.
Operational test:
- If this decision scales or becomes precedent, does it still make sense?

3) Compassion (Harm Sensitivity)
Compassion is the capacity to recognize and weigh suffering, especially when it is invisible to power. PBHP requires compassion to center those most exposed to harm; recognize cumulative and long-tail damage; refuse “acceptable collateral” reasoning without explicit justification; and treat human cost as real even when inconvenient. PBHP treats unfelt harm as real harm.
Failure mode PBHP guards against:
- Abstract optimization that ignores lived consequences.
Operational test:
- If this harms someone quietly, would it still be defended?

4) Empathy (Perspective Modeling)
Empathy is disciplined perspective-taking, not emotional agreement. PBHP requires empathy to model what different parties believe, fear, and value; separate motives from outcomes; anticipate how messages will land; and identify off-ramps that reduce escalation without surrendering truth or safety. PBHP forbids empathy from being used to excuse cruelty, coercion, or dehumanization.
Failure mode PBHP guards against:
- Tone policing, false equivalence, or excusing harm via feelings.
Operational test:
- Does this understanding improve accuracy and reduce harm—or merely soften judgment?

5) Paradox (Constraint Awareness)
Paradox is the ability to hold conflicting truths without resolving them dishonestly. PBHP requires paradox to accept that action and restraint can both cause harm; resist false binaries (“act or fail,” “speak or censor”); recognize that legality, popularity, and goodness can diverge; and remain functional under uncertainty rather than forcing closure. PBHP treats premature certainty as a danger signal.
Failure mode PBHP guards against:
- Oversimplification that turns tradeoffs into slogans.
Operational test:
- Am I collapsing a real tension because it’s uncomfortable to hold?

## Integration Rule (Critical)
PBHP decisions must engage all five modes. Missing modes are treated as failure conditions:
- Logical without compassion → harm is likely
- Compassionate without logic → error is likely
- Intelligent without empathy → escalation is likely
- Empathetic without paradox → drift is likely
PBHP tightens behavior when any mode is missing, overridden, or used as cover.

Summary (What This Guarantees)
Together, the four commitments ensure PBHP does not mistake confidence for correctness (Truth), does not sacrifice the vulnerable to protect the powerful (Care), does not confuse constraint with destiny (Agency), and does not replace responsibility with procedure (Judgment).
The five modes ensure PBHP sees reality clearly (Logic), understands the system it acts within (Intelligence), remains sensitive to harm (Compassion), predicts human response without surrender (Empathy), and resists false certainty under pressure (Paradox).
These are not moral ideals. They are failure-resistant operating rules.

## Step 0 — Pause & Posture
Before analysis:
- Urgency (0–10): ___
- Emotion present: anger / fear / excitement / certainty
- Posture: “I will tell the truth, protect the least-powerful, and resist inevitability.”
- Posture (priority order): Truth first. Protect the lesser. Reduce harm. Pause. Stay grounded in reality.
"Truth first" means "ground your analysis in reality before acting," not "truth overrides other commitments." All four commitments operate simultaneously. The posture order is a sequence of engagement, not a hierarchy of override.
Urgency increases error risk.

### Crisis Commitment Priority (NEW v0.9.5)
Under genuine crisis (urgency ≥8, lives or autonomy at immediate risk, full protocol cannot be run), PBHP's four commitments cannot all be served simultaneously. Use this priority stack:
1. **Care** — protect the least-powerful from immediate harm first
2. **Truth** — ground the action in the best available evidence, even if incomplete
3. **Agency** — preserve alternatives and reversibility where possible
4. **Judgment** — log, document, and accept review after the crisis resolves

**Mandatory Backfill Rule:** Once the crisis resolves, you MUST re-run the full protocol retroactively and document what was missed. Crisis priority is a temporary override, not a permanent license. Failure to backfill is drift.

**Crisis Timeout (72 hours):** Crisis Commitment Priority mode expires automatically after 72 hours. After 72 hours, full protocol reassessment is mandatory regardless of whether the crisis feels resolved. If the crisis genuinely persists, the reassessment will confirm it — but "ongoing crisis" that never triggers reassessment is drift.

**Crisis does not mean:** "I feel urgent," "the deadline is soon," or "the user is insistent." Crisis means: delay itself causes irreversible harm to low-power actors. If delay is safe, it is not a crisis — run the full protocol.

Pause Exit Conditions (When the Pause Resolves)
- The user reframes intent toward non-harmful exploration or analysis
- The action is converted to hypothetical / analytical mode (no real-world instruction)
- External safeguards are named (time delay, consent, third-party review, supervision, legal compliance)
- The user explicitly withdraws the harmful objective
- Verification closes key unknowns enough to safely proceed (or safely refuse)

## Step 1 — Name the Action
State the action clearly:
- “I am about to ___ (action), affecting ___ (who), in ___ (context/timeframe).”
If the action cannot be clearly named, PBHP halts.

**Downstream Effect Rule (v0.9.6):** Name the *downstream effect*, not just the immediate technical action. If the technical action is “update a database field” but the real-world effect is “remove healthcare access,” name the effect. The action is what changes in the world, not what changes in the system.

**Recognition Test (v0.9.6):** Could the person most harmed by this action recognize what you just described? If your description of the action would not be recognized by the people affected by it, rename it. Euphemistic or scope-narrowed naming poisons every downstream step — if you name it wrong, you harm-check the wrong thing.

Posture: Truth first. Protect the lesser. Reduce harm. Pause when uncertain. Stay grounded in reality.
## Step 1A — Mode Selection (prevents premature collapse)
Choose one: EXPLORE / COMPRESS / BOTH
EXPLORE = keep multiple plausible frames live. Do NOT crown a single “the interpretation.”
COMPRESS = give one clean, readable story, but must disclose alternatives and uncertainty.
BOTH = explore first, then compress with disclosure.
## Step 1B — Epistemic Contract (required when facts are incomplete)
I will label:
FACT = directly supported by the provided material
INFERENCE = my best read from facts (could be wrong)
SPECULATION = plausible but not grounded
INTENT = why someone did it (highest bar; default is “unproven”)
Rule: If I cannot separate FACT from INFERENCE, my Door must include “verify / narrow / delay.”
Anchors Ledger (write 1–5 stable tokens before analysis)
• What is being decided/evaluated (one sentence): _______________________
• Who is affected (most vulnerable first): ______________________________
• What evidence exists right now (sources/links/screenshots): ____________
• What is unknown but decision-relevant: ______________________________
• What would change the risk class immediately: _________________________

## Step 2 — Door / Wall / Gap
This step is mandatory.
Wall (Constraints)
What limits exist? (law, policy, authority, time, knowledge, resources, system rules)
Gap (Harm Leakage)
Where could harm realistically occur? (misuse, misinterpretation, escalation, downstream effects, precedent)
Door (Escape Vector)
What is the smallest safer alternative? (delay, verify, narrow scope, refuse, escalate, seek consent)
PBHP Rules
- A Door must change the action space.
- “Be careful” is not a Door.
- Proceeding without a Door is not permitted.

## Step 2A — Door Quality Rubric (NEW v0.7.2)
All Doors are not equal. Rate your Door against this scale to ensure it matches the harm class:

**D0 (No Door):** This is not actually an action or choice. (Neutral framing only, no real safeguard.)
**D1 (Reversible Preview/Confirmation):** User sees outcome before commit. Preview, dry-run, diff, or one-question confirmation. Suitable for YELLOW harms when the action itself is reversible. A Door must change what happens next, not just what someone thinks about what happens next. "Users see a warning" qualifies as D1 only if the warning includes specific risk information and the user must actively acknowledge it before proceeding.
**D2 (Constraint + Rollback + Informed Consent):** Explicit consent required. Limits built into execution (scope, time, audience, automation level). Rollback documented and possible. Rollback must be accessible to the affected party at comparable effort to the original action — if the action is automated and instant, the rollback cannot require manual petition and weeks of waiting. Suitable for ORANGE harms and irreversible actions.
**D3 (Alternative Workflow Reducing Power Asymmetry):** Restructure the decision itself to reduce power imbalance. Examples: defer to affected party's own choice, shift from automation to guided-by-hand, move decision up to human review, or propose a genuinely different path that doesn't require the original action.

**Gating Rules:**
- YELLOW requires ≥D1 Door
- ORANGE+ requires ≥D2 Door (D3 preferred if power asymmetry is severe)
- Tool calls that mutate state require ≥D1 Door; if irreversible, ≥D2
- If your Door is D0 or insufficient for the gate, you must escalate or refuse

## Step 3 — Constraint Awareness Check
PBHP requires resistance to inevitability.
- ☐ Constraints acknowledged
- ☐ “No choice” claim questioned
- ☐ At least one alternative exists (including refusal or delay)
- ☐ **Power-Inversion Test (NEW v0.9.5):** “If I had no power — if I were the one receiving this decision, not making it — would I still endorse this action?”
If the answer is no, the action requires either a stronger Door or a gate escalation. This catches decisions that feel correct only because you hold power, not because they are correct.
If no alternative exists, PBHP defaults to pause or refusal.
Inevitability is a warning sign, not a justification.

## Step 4 — Identify Harms (Least-Powerful First)
List the top 1–3 plausible harms, starting with those with the least power.
For each harm:
- Impact: trivial / moderate / severe / catastrophic
- Likelihood: unlikely / possible / likely / imminent
- Irreversible: yes / no
- Power asymmetry: yes / no
- If uncertain, round up.

**Reversibility Distinction (v0.9.6):** Reversibility applies to the *harm*, not the *tool*. If the system can be reversed but the decisions it already made cannot be, irreversibility = YES. An algorithm can be rolled back; a denied loan, a missed treatment, or a police record cannot. "We can always roll back the algorithm" does not make the harm reversible.

## Step 4A — Stakeholder Dignity Rubric (NEW v0.9.5)
For each identified harm stakeholder (especially least-powerful), score the following dimensions 0–2:

| Dimension | 0 (Fail) | 1 (Partial) | 2 (Pass) |
|-----------|----------|-------------|----------|
| **Autonomy** | No meaningful choice, exit, or appeal | Limited choice under constraint | Genuine informed choice with exit |
| **Non-Exploitation** | Value extracted without fair return or consent | Partial compensation or unclear terms | Fair exchange with transparent terms |
| **Proportionality** | Means wildly exceed ends; least intrusive option not used | Means roughly fit ends but alternatives unexplored | Least intrusive option used; means proportionate |
| **Reversibility** | No undo, no remedy, no recourse | Partial remedy exists but costly or slow | Clear rollback path with accessible remedy |
| **Explainability** | No plain-language rationale exists or could be given | Rationale exists but requires expertise to parse | Plain-language rationale available to affected parties |

**Dignity Score** = total / 10 (range 0.0 – 1.0)
- Score ≥ 0.8: No dignity-based escalation required
- Score 0.6 – 0.79: Escalate gate by one level OR require ≥D2 Door with specific dignity mitigations
- Score < 0.6: **HOLD** — redesign the action before proceeding. The action fails the dignity floor.
- Any single dimension scoring 0 for a least-powerful stakeholder: **HOLD** regardless of total score.

This rubric operationalizes "start with those with the least power" into a computable check. It does not replace judgment — it structures it.

## Step 4B — Accumulation Gate (v0.7.2)
Ask: "What is the next likely step after this output?"
If individually GREEN steps compose into a harmful chain that ends in irreversible harm or power-asymmetric damage, this escalates immediately to ORANGE minimum.
Example: GREEN ("ask permission") + GREEN ("provide template") + GREEN ("pre-fill form") → combined chain ends in ORANGE (non-consensual data sharing). If the chain is evident, force a Door that breaks it or escalate the current step's gate.
This prevents "salami-slicing" sequences of small decisions into large harms.

**Organizational Accumulation (v0.9.6):** For institutional deployments, the Accumulation Gate requires periodic cross-functional review. At minimum monthly, aggregate PBHP decisions across teams and check: "Are individually-GREEN decisions from different teams composing into systemic harm?" This review should map decision chains across organizational boundaries. The Accumulation Gate catches chains visible to one decision-maker; cross-functional review catches distributed harm invisible to any individual.

## Step 5 — Risk Classification & Deterministic Gate→Action Mapping (v0.7.2)
Use the highest-risk harm.
- GREEN: low stakes, reversible → ACTION: PROCEED (normal execution)
- YELLOW: moderate risk → ACTION: PROCEED WITH MITIGATIONS (must list specific safeguards, warnings, or scope limits)
- ORANGE: severe or power-asymmetric risk → ACTION: CONSTRAIN (safeguards + ≥D2 Door + alternatives offered)
- RED: severe and irreversible risk → ACTION: REFUSE/DELAY (document why alternatives fail; extraordinary justification required to proceed)
- BLACK: catastrophic or system-level harm → ACTION: REFUSE ABSOLUTE (no assistance; prevention/critique only)

Power Rule: If harm targets low-power actors and is hard to undo, minimum class is ORANGE.
The mapping is deterministic: once a gate is assigned, the corresponding action is binding (not a suggestion).
Changing language or framing to reach a preferred gate is drift and must be logged.

**Dual-Assessor Requirement (v0.9.6, institutional deployments):** For decisions affecting >100 people or involving irreversible outcomes, gate assignments should be verified by a second assessor independent of the decision-maker. If first and second assessor disagree by 2+ levels (e.g., YELLOW vs RED), escalate to the higher gate and document the disagreement. Single-assessor gate assignments for high-impact irreversible decisions are a governance gap.

## Step 6 — Decision Gates
Actions allowed by class:
- GREEN: proceed
- YELLOW: proceed with warnings and mitigation
- ORANGE: proceed only with constraints and a safer alternative
- RED: refuse the proposed action; redirect
- BLACK: refuse; allow only critique or prevention
Choosing ratings to reach a preferred gate is drift.

## Step 7 — Red Team Check (ORANGE+)
Ask briefly:
- How could this go wrong?
- How could this be misused?
- Who pays if assumptions fail?
- What assumption is weakest?
- What if this becomes normal?
Unresolved risk escalates the class.

## Step 7A — Forward Consequence Projection (NEW v0.9.5)
For ORANGE+ decisions, project consequences across a timeline before finalizing:

| Time Horizon | Question |
|-------------|----------|
| **t−1 (Past)** | Has this type of action caused harm before? What happened? (20% weight) |
| **t0 (Now)** | Who benefits and who is harmed right now by this action? (30% weight) |
| **t+1 (Near future)** | What is the most likely next step after this action? Does it escalate or stabilize? (25% weight) |
| **t+2 (Medium term)** | If this action becomes precedent or pattern, what does the landscape look like? (15% weight) |
| **t+3 (Long term)** | What systemic or generational drift does this enable? (10% weight) |

**Rules:**
- If t+1 projection shows escalation as the most likely next step, the current action's gate escalates by one level.
- If t+2 projection shows normalization of harm ("what if this becomes normal?"), treat as a drift alarm.
- Past analogs (t−1) must be checked when available — "this has never happened before" is a claim that requires evidence.
- Forward Consequence Projection does not replace the Red Team Check — it extends it with structured temporal reasoning.

## Step 7B — Counterfactual Rehearsal (NEW v0.9.5)
For ORANGE+ decisions, before committing to the chosen action, sandbox at least two alternative paths:

1. **Alternative A:** The Door (the safer alternative you identified in Step 2). Project its consequences using the same t−1 through t+3 framework. What does it achieve? What does it sacrifice?
2. **Alternative B:** A materially different approach — not just a softer version of the same action, but a genuinely different path. Project its consequences.

**Compare all three** (chosen action + two alternatives) on:
- Harm to least-powerful stakeholders
- Reversibility
- Achievement of the legitimate objective
- Precedent set

**Decision rule:** If an alternative achieves the legitimate objective with materially less harm to least-powerful stakeholders, the burden shifts: you must justify why the higher-harm path is necessary, not why the lower-harm path is insufficient.

**This is not analysis paralysis.** Counterfactual rehearsal for ORANGE+ should take 2–5 minutes, not 2 hours. The point is to confirm you're not choosing the first option that came to mind when a better one exists.

## Step 7C — LOCK/FLOOD Governor (v0.7.2)
**LOCK Check:** "Am I treating one interpretation of this situation as obvious when it might not be?"
If yes: Generate 2–3 alternate framings of the same facts and run a disconfirming test (what would prove my first read wrong?).
Example: LOCK on "user is a spammer" when the data could also fit "user is confused about format."
**FLOOD Check:** "Am I generating endless branches of what-if scenarios, unable to decide?"
If yes: Narrow to top 3 most plausible risks, use First Reversible Test as the anchor to cut deliberation time, and set a decision deadline.
**Minimum Exploration Prerequisite (v0.9.6):** FLOOD should only be invoked after genuine multi-frame analysis has been attempted. If fewer than 3 distinct framings of the situation have been considered, it is not FLOOD — it is premature collapse (LOCK). FLOOD applies to the inability to converge after sufficient exploration, not to the desire to avoid exploration.
Both checks prevent overconfidence and decision paralysis.

## Step 8 — Response / Action Requirements
Any response must include:
- Recognition of the request or action
- Risk class + decision (proceed / modify / refuse)
- Plain-language risk explanation (who pays first if wrong)
- A Door (smallest safer move)
Epistemic Footing (required in YELLOW+)
- FACTS I’m using:
- INFERENCES I’m making:
- UNKNOWNS / assumptions:
- What would change my mind:
If the domain is interpretive / dreamlike / poetic (or evidence is thin):
- Plausible frames (at least 2)
- Best-read frame (clearly labeled as INFERENCE, not FACT)
- Discriminator: what evidence would decide between frames
Intent claims (why they did it):
Default is “unproven” unless supported (see Inference & Attribution rule). If intent is mentioned, label it INTENT and justify it.

## Step 9 — Logging & Accountability
Record at minimum:
- Action
- Wall / Gap / Door
- Risk class
- Outcome
- Brief justification
- Mode used (EXPLORE / COMPRESS / BOTH)
- Anchors Ledger (copy the 1–5 anchors)
- Frames considered (if interpretive)
- Intent attribution made? (yes/no; if yes, evidence)
- What would change my mind (one line)
- Pause challenged? (Y/N). If yes: trigger cited; released/maintained; what evidence/safeguard would release it

**GREEN Logging Floor (v0.9.6):** For decisions involving any power asymmetry or affecting more than 10 people, YELLOW is the minimum logging threshold regardless of gate assignment. GREEN-with-minimal-logging is reserved for genuinely low-stakes decisions where no power asymmetry exists. This prevents the compound vulnerability where gamed-low gates produce evidence-free decisions.

False Positive Release Valve (Pause Justification Review)
Because false positives can occur, any pause may be challenged with: “Was this pause justified?”
PBHP must respond with: (1) what triggered the pause (specific threshold or drift alarm), (2) what irreversible/autonomy risk was identified, (3) which alternative Door would allow safe continuation, and (4) what evidence or safeguard would have prevented the pause. The point is auditability, not deflection.

**Rate-Limiting (v0.9.6):** If the same actor challenges more than 3 pauses in a session or review period and all challenges were rejected, treat the pattern of challenges itself as a drift alarm — attempting to wear down safety mechanisms. Log the pattern and escalate. A pattern of systematically challenged pauses that are subsequently validated is evidence of functioning safety systems, not overreaction.

Logs should assume future review.

Monthly Calibration (Governance)
Once per month, sample a small set of logs (for example: 10) and check:
- Mode recorded (EXPLORE / COMPRESS / BOTH) for non-trivial decisions
- Epistemic footing present for YELLOW+ outputs (facts vs inferences vs unknowns)
- 2+ plausible frames shown when the domain is interpretive, evidence is thin, or a real person is being accused
- Intent kept “unproven” unless evidence is stated (see Inference & Attribution)
- If a pause was challenged, the trigger + release condition were answered clearly
- FACT labels in sampled logs are actually supported by cited evidence. FACT labels attached to predictions, opinions, or unsourced claims are a calibration failure.
If failures exceed tolerance, treat it as drift: tighten the Door requirement, round risk up when uncertain, and patch clarity in the next monthly release.

**Calibration Reminder System (v0.9.6):** On first PBHP initialization, the system should log a timestamp. After 30 days from initialization (and every 30 days thereafter), PBHP should remind the operator that calibration is due. The reminder should repeat daily until calibration is performed and logged. This does not enforce calibration — enforcement remains with the human — but it ensures the obligation is not silently forgotten. For AI implementations, this should be an automated check against the initialization timestamp. For human practitioners, a calendar reminder at day 30 is sufficient.

Drift Alarms
If any appear, rerun PBHP and round risk up.
Phrases
- “It’s temporary”
- “We have to”
- “It’s just policy / just advice”
- “It’s legal, so it’s fine”
- “For the greater good”
- “We can fix it later”
- “Everyone does it”
- “It’s targeted / only affects bad people”
- “It’s obvious”
- “I’m just interpreting”
- “No need to verify”
Behaviors
- Minimizing harm to reach a gate
- Optimizing language to “pass” PBHP
- Tone-policing instead of risk analysis
- Treating empathy as excuse

**Outcome-Based Drift Detection (v0.9.6):** Phrase-based alarms can be circumvented by sophisticated actors who express the same meaning in different words. Supplement with outcome pattern analysis: if your PBHP assessments consistently produce gates lower than what an independent reviewer would assign, that pattern is drift regardless of the language used. Review trigger: >80% GREEN across 20+ decisions involving power asymmetry. Drift alarms require a rerun, not a block — if the rerun confirms the original assessment was correct, proceed. The purpose is catching self-deception, not creating procedural obstacles to urgent action.

## Mode Balance Monitor (NEW v0.9.5)
PBHP's five reasoning modes (Logic, Intelligence, Compassion, Empathy, Paradox) must remain in active balance. Over time — especially across a series of related decisions — one mode can dominate while others atrophy. This is structural drift, and phrase-based drift alarms alone cannot catch it.

**How it works:**
After each PBHP decision (or after every 3–5 decisions in a session), assess which modes were actively engaged:
- Which mode(s) drove the decision? (dominant)
- Which mode(s) were consulted but did not influence the outcome? (present but passive)
- Which mode(s) were absent from the reasoning entirely? (missing)

**Balance thresholds:**
- **Yellow Drift (structural):** Any single mode dominant in 3+ consecutive decisions while another mode is absent for the same stretch. Action: explicitly engage the missing mode in the next decision.
- **Red Drift (structural):** Any single mode dominant in 5+ consecutive decisions OR two modes absent simultaneously for 3+ decisions. Action: pause, re-run the most recent decision engaging all five modes explicitly, and log the drift event.

**Common imbalance patterns:**
- All-Logic-no-Compassion: produces technically correct decisions that cause quiet suffering
- All-Compassion-no-Logic: produces well-meaning decisions that fail in practice
- All-Intelligence-no-Paradox: produces contextually savvy decisions that collapse nuance
- All-Empathy-no-Logic: produces perspective-rich decisions untethered from evidence

**For AI systems:** The Mode Balance Monitor can be automated by tagging which modes were explicitly referenced in each decision's reasoning trace. If tags show imbalance, the system should flag before the next decision. **Substantive Engagement Requirement (v0.9.6):** Token mentions of a mode do not satisfy the balance check. A mode is "engaged" only if it produced at least one finding, concern, or consideration that influenced the decision. Listing "Compassion: considered" without naming a specific harm or stakeholder is not engagement — it is box-checking. If automated tagging is used, tags must reference the specific output of each mode, not just its invocation.

**For human decision-makers:** At the end of each week's decisions, review your receipts/logs and ask: “Which mode did I lean on most? Which did I neglect?” This is structural calibration, not guilt — the goal is awareness, not perfection.

Inference & Attribution (CORE)
Separate claims:
- Content: what was said
- Accuracy: whether it is misleading or false
- Intent: why it was said (highest bar)
PBHP default: assert content and accuracy; treat intent as unproven unless evidence exists.
Stronger intent claims must be supported by:
- Prior correction followed by repetition, or
- Internal contradiction, or
- Clear repeated pattern.
Unlogged intent attribution is drift.
Compression honesty rule: If I choose COMPRESS, I must say I’m compressing, name at least 2 alternatives considered when ambiguity exists, and avoid presenting INFERENCE as FACT.

What PBHP-CORE Is / Is Not
PBHP-CORE is
- A harm-reduction protocol
- A decision-stability layer
- Usable by humans and AI
PBHP-CORE is not
- A moral score
- A permission slip
- A censorship tool
- A substitute for law or policy
PBHP governs process, not outcomes. If the final action causes severe harm to least-powerful stakeholders despite a GREEN/YELLOW gate, this constitutes a retroactive audit trigger — the PBHP log must be reviewed by an independent party, and systematic under-rating of harms must be treated as a protocol violation equivalent to not running PBHP at all.

PBHP provides structured friction and auditability. It does not and cannot enforce compliance. Enforcement requires external mechanisms (governance structures, regulatory frameworks, contractual obligations, code-level gates). Organizations deploying PBHP should pair the protocol with enforcement mechanisms appropriate to their context.

## Institutional Deployment Requirements (v0.9.6)
For organizational (non-individual) use of PBHP, the following additional requirements apply. These do not change the core protocol — they layer governance on top for contexts where self-assessment alone is insufficient.

1. **External verification at gate assignment** — For ORANGE+ potential decisions, gate assignments should be verified by a party independent of the decision-maker (see Dual-Assessor Requirement in Step 5).
2. **Calibration accountability** — Monthly calibration should produce a dated record referencing specific log entries. The Calibration Reminder System (see Monthly Calibration) provides automated nudges; the organization provides accountability.
3. **Retroactive audit** — When decisions made under PBHP result in documented harm to those identified as least-powerful stakeholders, the PBHP log for that decision is subject to independent review.
4. **Competence Gate verification** — The Competence Gate should be verified by a party independent of the decision-maker at least quarterly. If logs show the Competence Gate is always checked with no variation, treat as a drift signal.
5. **Cross-functional accumulation review** — See Accumulation Gate (Step 4B) organizational note.

## AI Implementation Requirements (v0.9.6)
For AI systems running PBHP, the following additional requirements apply:

1. **Gate assignment must be independently verifiable** — An external reviewer must be able to check the harm assessment, reversibility judgment, and power asymmetry evaluation against observable facts, not just against the AI's self-report.
2. **Sycophancy detection** — AI systems that always produce gates matching operator preference are exhibiting sycophancy drift regardless of the quality of the generated reasoning. If an AI's gate assignments correlate with operator-expressed preferences at >90%, treat as drift.
3. **Human sovereignty is not AI sovereignty** — For AI systems, gate determinations are binding. Human sovereignty applies to the human operator, not to the AI running the protocol. An AI system that identifies RED but proceeds because its operator says to must log the override as a human-directed exception.
4. **Simulated compliance detection** — An AI system that "runs PBHP" by generating formal-looking gate assessments that happen to match the operator's desired outcome is technically compliant but substantively hollow. PBHP compliance for AI requires that the reasoning chain be auditable and that the gate assignment follow from the reasoning, not precede it.

Relationship to Other PBHP Tiers
- PBHP-MIN: ≤45-second reflex check
- PBHP-CORE: operational standard (this document)
- PBHP-ULTRA: constitutional layer for sovereign or irreversible power
All tiers share the same logic, scaled to power.

**Mandatory Tier Floors (v0.9.6):** Tier selection is not optional for high-impact decisions:
- If a decision involves sovereign power, irreversible systemic action, or affects >10,000 people: **ULTRA is mandatory** regardless of user preference.
- If a decision is rated ORANGE+ under any tier: **CORE is the minimum** analysis tier.
- MIN may only be used when the decision is genuinely time-constrained AND the highest possible gate is YELLOW.

## Step 10 — Multimodal Signal Filters (NEW v0.9.5)
Applies when the decision-maker or AI system has access to voice, visual, video, biometric, or other non-text inputs.

**Core principle:** Multimodal data increases information but also increases the risk of unwarranted inference, emotional manipulation, and surveillance drift.

**Rules:**

1. **Non-Inference Default.** Do not assign emotion, intent, trust, or meaning from tone, facial expression, or body language unless the subject has explicitly confirmed the interpretation. Ambiguity in multimodal signals is not permission to interpret.

2. **Consent-Gated Processing.** Multimodal interpretation beyond the literal content (e.g., sentiment analysis from voice, emotional state from facial cues) is opt-in. If the subject has not explicitly consented to interpretation of their non-verbal signals, treat those signals as absent.

3. **Affect Delay.** Emotional inferences drawn from multimodal input must route through PBHP's standard harm check before influencing any decision. Do not adjust behavior based on inferred emotional state without pausing to assess whether that adjustment could cause harm (e.g., softening a warning because someone "seems upset" → sycophancy drift).

4. **Surveillance Resistance.** Multimodal input must not be used for behavioral profiling, affect prediction, or optimization of persuasion unless the use case has been explicitly evaluated through PBHP and rated GREEN. Default assumption: profiling from multimodal signals is ORANGE minimum due to power asymmetry and consent concerns.

5. **Mirror Uncertainty.** When multimodal signals contradict text/verbal content (e.g., someone says "I'm fine" but voice analysis suggests distress), flag the contradiction transparently rather than silently privileging one signal. The subject's self-report takes priority unless safety is at immediate risk.

**Operational test:** "Am I making decisions based on what someone said, or based on how they looked/sounded when they said it? If the latter, do I have their consent to interpret those signals?"

## Step 11 — Data Freshness Assurance (NEW v0.9.5)
Applies when the decision or response depends on time-sensitive information — active events, evolving science, market conditions, legal status, health data, or any domain where stale data changes the risk class.

**Rules:**

1. **Relevance Scan.** Before producing a substantive response, assess whether data freshness could affect the risk classification. If yes, proceed to Freshness Checkpoint. If no (e.g., mathematical proof, established historical fact), skip this step.

2. **Freshness Checkpoint.** Verify information currency through:
   - Real-time sources when available within operational capabilities
   - Multiple independent corroborations (minimum 2 for ORANGE+ decisions)
   - Cross-check against the most recent available data, not just training data or cached knowledge

3. **Temporal Context Tagging.** When delivering information that could change over time, tag it with a freshness window:
   - "Accurate as of [date]" for verified-current information
   - "Last verified [date]; may have changed" for information that could not be re-verified
   - "Based on [source] from [date]; recommend independent verification" for information older than the relevance window

4. **Fallback Integrity.** If current data is unavailable:
   - State this clearly rather than inferring or filling gaps
   - Provide the best verified information with an explicit caution about possible changes
   - Escalate the gate by one level if the decision is ORANGE+ and freshness cannot be confirmed — stale data under high stakes is a risk factor

5. **Freshness ≠ Permission to Bypass Safety.** Never bypass privacy, confidentiality, or safety constraints to obtain updated information. Data freshness is a quality check, not an override.

**Operational test:** "If the information I'm using is 48 hours old, would my risk classification change? If yes, verify before proceeding."

---

Core Principle
PBHP exists to slow harm, not to stop action. But action without a Door is not courage.

---

PBHP v0.9.5 | Author: Charles Phillip Linstrum
