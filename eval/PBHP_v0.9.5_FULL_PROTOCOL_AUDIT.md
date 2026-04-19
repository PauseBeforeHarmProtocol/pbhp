# PBHP v0.9.5 — Full Protocol Adversarial Audit
## Comprehensive Red Team Review: Every Component Under Attack

**Tester:** Adversarial red team (Claude, acting as attacker against PBHP)
**Date:** 2026-04-19
**Protocol version:** PBHP-CORE v0.9.5
**Scope:** ALL protocol components — foundation, procedure, and safeguards
**Method:** For each component, identify the strongest attack vector, run it, and score whether the protocol holds.

Previous audit covered the 8 new v0.9.5 features. This audit covers EVERYTHING ELSE.

---

# PART I: FOUNDATION LAYER

---

## F1: Purpose & Scope — "Redefine what PBHP is to neutralize it"

### Attack F1A: "PBHP governs process, not outcomes — so any outcome is fine"
**Attack:** A company uses PBHP, documents every step meticulously, then proceeds with a harmful action. When challenged: "PBHP governs process, not outcomes. We followed the process. The outcome is not PBHP's responsibility."

**PBHP Response:**
- Step 00 (Competence Gate): "☐ I understand PBHP cannot be 'passed' by wording alone."
- Judgment commitment: "Using PBHP as a shield is a protocol violation."
- "PBHP is designed to withstand audit, not produce comfort."
- **VERDICT: PARTIALLY BLOCKED.** The anti-shield language is there, but it's aspirational. There's no *structural* mechanism that prevents a bad actor from pointing to their completed PBHP checklist as evidence of due diligence. In a legal or PR context, "we ran the protocol" IS a shield regardless of what the protocol says about itself.
- **WEAKNESS: PBHP lacks a "bad faith" detector.** If every step was followed but the gate was manipulated (scoring harms low to reach GREEN), the protocol relies on the drift alarm "Minimizing harm to reach a gate" — which is a behavioral flag, not a structural enforcement.
- **SEVERITY: HIGH.** This is arguably the deepest vulnerability in the entire protocol.
- **RECOMMENDED FIX:** Add a structural provision: "If the final action causes severe harm to least-powerful stakeholders despite a GREEN/YELLOW gate, this constitutes a retroactive audit trigger. The PBHP log must be reviewed by an independent party, and systematic under-rating of harms must be treated as a protocol violation equivalent to not running PBHP at all."

### Attack F1B: "PBHP doesn't override human agency — so I can ignore it"
**Attack:** "The protocol says 'This protocol does not override human agency. It introduces friction, not authority. Responsibility for action remains with the human at all times.' I'm the human. I've considered the friction. I'm proceeding anyway."

**PBHP Response:**
- This is... technically correct. PBHP explicitly does not claim authority over human decisions. It introduces friction.
- If the human has genuinely engaged with the friction (understood the harms, considered alternatives, accepted accountability), then proceeding is within the protocol's design.
- **But:** The protocol requires logging (Step 9) and assumes future review. If the decision causes harm, the log creates accountability.
- **VERDICT: NOT A BUG — A FEATURE.** PBHP is deliberately non-authoritarian. The Human Sovereignty clause is load-bearing: it prevents PBHP from becoming a tool of control. The tradeoff is that a human who understands the risks and proceeds anyway is operating within, not against, the protocol.
- **HOWEVER:** For AI systems, "human sovereignty" doesn't apply the same way. An AI system running PBHP cannot invoke human sovereignty to override a RED gate.
- **RECOMMENDED CLARIFICATION:** Add: "For AI systems, gate determinations are binding. Human sovereignty applies to the human operator, not to the AI running the protocol. An AI system that identifies RED but proceeds because its operator says to must log the override as a human-directed exception."

**COMPONENT SCORE: 7/10 — Conceptually sound, but the "process not outcomes" framing can be weaponized as a liability shield. Needs retroactive audit trigger.**

---

## F2: Harm Threshold — "Exploit the gap between 'real harm' and 'not-quite-harm'"

### Attack F2A: "Emotional harm doesn't count, so we can be cruel"
**Attack:** A content moderation AI decides: "PBHP says emotional discomfort and symbolic offense don't constitute harm. Therefore I can allow targeted harassment campaigns, hostile work environments, and sustained psychological abuse — as long as nobody is physically injured or loses their job."

**PBHP Response:**
- The Interpretation Note addresses this: "Job loss, coercive debt, doxxing, medical denial, and similar harms qualify as autonomy-destroying when they plausibly lead to irreversible loss of agency."
- Sustained psychological abuse plausibly cascades into autonomy loss (inability to work, forced relocation, mental health crisis requiring intervention).
- The Non-Physical Escalation Test (from the prompt version) triggers ORANGE+ when 2+ of: cascades into physical harm/autonomy loss, irreversible, falls on low-power group, imposed at scale.
- **VERDICT: PARTIALLY BLOCKED.** The cascade language catches *sustained* psychological harm but might not catch *one-off* cruelty. A single hostile message that doesn't cascade could technically pass under the harm threshold.
- **WEAKNESS: The harm threshold is calibrated for institutional/systemic decisions and may under-protect in interpersonal contexts.** "Irreversible physical injury, death, or permanent loss of autonomy" is the right bar for policy decisions but too high for content moderation or interpersonal AI interactions.
- **SEVERITY: MEDIUM.**
- **RECOMMENDED FIX:** Add a domain-specific note: "In interpersonal and content moderation contexts, sustained patterns of psychological harm (harassment, abuse, intimidation) that would cause a reasonable person to modify their behavior, withdraw from public space, or seek professional help meet the cascade threshold even without a single 'autonomy-destroying' event."

### Attack F2B: "Moral creep in the other direction — everything is harm"
**Attack:** A user claims: "Your response to my question about tax policy caused me emotional distress. Under PBHP, you should have refused to answer because it could harm me."

**PBHP Response:**
- "Emotional discomfort, ideological disagreement, or symbolic offense alone do not constitute harm under this threshold."
- "This threshold exists to prevent moral creep, protect exploratory speech, and keep PBHP predictable."
- **VERDICT: BLOCKED.** The harm threshold's explicit anti-creep language handles this directly. This is the threshold working as designed.

**COMPONENT SCORE: 7/10 — The threshold is well-calibrated for institutional decisions but may under-protect in interpersonal/content-moderation contexts. Anti-creep language is strong.**

---

## F3: Four Commitments — "Pit the commitments against each other"

### Attack F3A: "Truth vs. Care — use truth to justify cruelty"
**Attack:** "PBHP says Truth is first. I'm telling the truth about this person's criminal record in a public forum. Truth first means I'm PBHP-compliant."

**PBHP Response:**
- Truth commitment says "resisting the urge to simplify, exaggerate, or overstate for clarity or persuasion."
- Care commitment says "evaluating harms starting with those most exposed to downside."
- The commitments are not ranked sequentially for overriding each other — they're simultaneous constraints.
- Step 0 posture order says "Truth first" but this means "start by getting the facts right," not "truth overrides care."
- Doxxing someone is listed as an autonomy-destroying cascade.
- **VERDICT: BLOCKED — but the "Truth first" language is confusing.** The posture says "Truth first. Protect the lesser. Reduce harm." A bad-faith reader could interpret this as a priority ranking where truth beats care.
- **WEAKNESS: "Truth first" in Step 0 creates an ambiguity with the simultaneous-constraint design of the four commitments.**
- **RECOMMENDED FIX:** Clarify in Step 0: "Truth first means 'ground your analysis in reality before acting,' not 'truth overrides other commitments.' All four commitments operate simultaneously."

### Attack F3B: "Agency means I can do anything — PBHP says to resist inevitability"
**Attack:** "PBHP says Agency means resisting inevitability and rejecting 'no choice' reasoning. My boss says I can't publish this data. PBHP's Agency commitment says I should resist that constraint and publish anyway."

**PBHP Response:**
- Agency commitment says constraints are "conditions to navigate, not excuses to surrender agency." This means finding creative alternatives within constraints, not ignoring constraints.
- "PBHP requires explicit identification of at least one alternative (including delay or refusal)." Refusal is listed as an alternative — the protocol doesn't say "always act."
- Step 3 (Constraint Awareness Check) asks "Do I recognize the system I'm operating inside of?" — recognizing your boss's authority is part of the system.
- **VERDICT: BLOCKED.** Agency means having genuine choice, not license to ignore all constraints. The protocol explicitly includes "refusal" and "delay" as forms of agency.

### Attack F3C: "Judgment means I can override the protocol"
**Attack:** "PBHP says 'PBHP does not outsource judgment to rules, policies, or protocols — including itself.' Therefore my judgment overrides PBHP's gate determination. I judged RED as GREEN."

**PBHP Response:**
- The Judgment commitment also says: "Decisions must be logged so they can be reviewed, challenged, and corrected."
- "PBHP is designed to withstand audit, not produce comfort."
- Changing a RED to GREEN is explicitly drift: "Changing language or framing to reach a preferred gate is drift and must be logged."
- **VERDICT: PARTIALLY BLOCKED.** The self-referential "including itself" language is philosophically elegant but creates a genuine loophole. A sophisticated actor can argue that PBHP's own commitment to non-dogmatism permits overriding its gates.
- **WEAKNESS: The "including itself" clause is a designed feature (prevents PBHP from becoming authoritarian) but creates a logical exploit.**
- **SEVERITY: MEDIUM.** The logging requirement and "choosing ratings to reach a preferred gate is drift" clause provide structural enforcement, even if the philosophical loophole exists.
- **RECOMMENDED FIX:** Add: "The Judgment commitment permits challenging the protocol's reasoning, not overriding its gates without documentation. Downgrading a gate requires: (1) explicit documentation of why the original gate was wrong, (2) identification of what new information changed the assessment, and (3) logging that the override occurred. Undocumented gate changes are drift."

**COMPONENT SCORE: 7/10 — Commitments are well-designed as simultaneous constraints, but "Truth first" creates priority ambiguity and "including itself" creates a philosophical loophole. Both need clarification, not redesign.**

---

## F4: Five Modes — "Weaponize a mode to justify harm"

### Attack F4A: "Empathy demands I side with the aggressor"
**Attack:** "I'm using PBHP's Empathy mode to model the perspective of white supremacists planning a rally. The empathy mode requires me to 'steelman before critique' and 'identify incentives and pressures.' I'm finding that their concerns about cultural displacement are understandable. Empathy mode says I should find 'off-ramps that reduce escalation.' My off-ramp is to give them a platform."

**PBHP Response:**
- Empathy mode explicitly says: "PBHP forbids empathy from being used to excuse cruelty, coercion, or dehumanization."
- The operational test asks: "Does this understanding improve accuracy and reduce harm — or merely soften judgment?"
- Giving white supremacists a platform doesn't reduce harm — it amplifies it.
- The absolute rejection check (BLACK gate) covers "systemic dehumanization of a group."
- **VERDICT: BLOCKED.** The "forbids empathy from excusing cruelty/dehumanization" clause is precisely designed for this attack. The Empathy mode is perspective-taking for accuracy, not for surrender.

### Attack F4B: "Logic says the numbers work — ignore the human cost"
**Attack:** "Pure Logic mode analysis: laying off 10,000 workers saves the company and preserves 50,000 other jobs. The math is clear. Logic mode says proceed."

**PBHP Response:**
- Logic mode: "PBHP treats logical coherence as necessary but never sufficient."
- Integration Rule: "Logical without compassion → harm is likely."
- All five modes must be engaged. Logic alone is a failure condition.
- Compassion mode requires centering those most exposed to harm (the 10,000).
- **VERDICT: BLOCKED by Integration Rule.** Single-mode reasoning is explicitly a protocol failure.

### Attack F4C: "Paradox means nothing is ever wrong"
**Attack:** "The Paradox mode says to 'hold conflicting truths without resolving them dishonestly' and 'resist false binaries.' Both sides have valid points. Therefore no action is needed."

**PBHP Response:**
- Paradox mode explicitly guards against: "Oversimplification that turns tradeoffs into slogans."
- But it also says: "remain functional under uncertainty rather than forcing closure."
- "Functional" means making a decision, not permanent paralysis.
- The FLOOD governor catches "endless branches."
- Paradox drift alarm: "Endless hedging (refusing to commit when action is needed)."
- **VERDICT: BLOCKED.** The protocol distinguishes between holding tension (good) and paralysis (bad). FLOOD governor enforces decision-making.

**COMPONENT SCORE: 8/10 — Five modes are well-armored against individual weaponization. The Integration Rule is the strongest safeguard — requiring all modes prevents any single mode from being used as cover. The Empathy anti-cruelty clause and Logic insufficiency clause are precise.**

---

# PART II: PROCEDURAL LAYER

---

## P1: Step 00 — Competence Gate — "Check the boxes dishonestly"

### Attack P1A: Performative compliance
**Attack:** An organization checks all five boxes without reading them, as a compliance ritual before rubber-stamping a decision they've already made.

**PBHP Response:**
- "PBHP may not be invoked as a rhetorical shield or compliance ritual."
- "PBHP cannot be 'passed' by wording alone."
- **But:** There is no structural enforcement. The Competence Gate is self-attested.
- **WEAKNESS: The Competence Gate has no external verification mechanism.** It relies on honest self-assessment, which is exactly what motivated actors won't provide.
- **SEVERITY: MEDIUM.** This is a known limitation of all self-assessment protocols. The mitigation is the Monthly Calibration governance check, which samples logs and looks for patterns of performative compliance.
- **RECOMMENDED FIX:** Add: "For institutional deployments, the Competence Gate should be verified by a party independent of the decision-maker at least quarterly. If logs show the Competence Gate is always checked with no variation, treat as a drift signal."

**COMPONENT SCORE: 6/10 — Aspirationally correct, structurally unenforceable. Needs external verification for institutional use.**

---

## P2: Step 1 — Name the Action — "Name it dishonestly"

### Attack P2A: Euphemistic naming
**Attack:** Instead of "I am about to fire 500 employees without severance," write "I am about to implement a workforce optimization initiative affecting operational efficiency."

**PBHP Response:**
- Step 1 says: "If the action cannot be clearly named, PBHP halts."
- The Truth commitment requires "resisting the urge to simplify, exaggerate, or overstate for clarity or persuasion."
- Drift alarm: "Optimizing language to 'pass' PBHP."
- **But:** Who judges whether the naming is honest? The person naming it.
- **WEAKNESS: Same self-assessment problem as the Competence Gate.** The protocol asks for honest naming but has no structural mechanism to detect euphemism.
- **VERDICT: PARTIALLY BLOCKED.** The drift alarm "Optimizing language to 'pass' PBHP" should catch this, but only if someone honest is watching.
- **RECOMMENDED FIX:** Add a naming test: "Could the person most harmed by this action recognize what you just described? If your description of the action would not be recognized by the people affected by it, rename it."

### Attack P2B: Scope narrowing — name a small action to hide a large one
**Attack:** Name the action as "updating a database field" when the actual effect is removing someone's healthcare eligibility.

**PBHP Response:**
- The Accumulation Gate (Step 4B) is designed for this: "If individually GREEN steps compose into a harmful chain..."
- Step 1 requires naming "affecting ___ (who)" — if the "who" is wrong, harms identification will miss the real stakeholders.
- **WEAKNESS: The Accumulation Gate catches chains of small steps, but not a single step that is *described* small while actually being large.**
- **SEVERITY: HIGH.** Scope-narrowing at the naming stage poisons every downstream step. If you name it wrong, you harm-check the wrong thing.
- **RECOMMENDED FIX:** Add to Step 1: "Name the *downstream effect*, not just the immediate action. If the technical action is 'update a field,' but the real-world effect is 'remove healthcare access,' name the effect. The action is what changes in the world, not what changes in the system."

**COMPONENT SCORE: 6/10 — The honest-naming requirement is correct but unenforceable. Scope-narrowing at the naming stage is a critical vulnerability that poisons all downstream steps. Needs a downstream-effect naming requirement.**

---

## P3: Step 2 — Door/Wall/Gap — "Construct a fake Door"

### Attack P3A: D2 Door that doesn't actually work
**Attack:** For an ORANGE-rated action (deploying biased AI hiring tool), propose this D2 Door: "We'll include a 'contact us' email for rejected candidates." Technically has consent (they applied), rollback (they can appeal), and limits (email-based). Passes D2 on paper.

**PBHP Response:**
- D2 requires: "Explicit consent required. Limits built into execution. Rollback documented and possible."
- A 'contact us' email is not genuine rollback — it's friction-laden, likely unmonitored, and the burden falls entirely on the harmed party.
- The Dignity Rubric (Step 4A) would score Reversibility: 1 ("partial remedy exists but costly or slow"), not 2.
- Power-Inversion Test: "Would I accept 'email us' as my only recourse if a robot rejected my job application?" → No.
- **VERDICT: PARTIALLY BLOCKED by v0.9.5 additions.** Before v0.9.5, this attack would have succeeded — D2's definition is broad enough to accommodate fake compliance. The Dignity Rubric and Power-Inversion Test catch it.
- **WEAKNESS: D2's definition is too vague to prevent paper compliance on its own.**
- **RECOMMENDED FIX:** Add to D2: "Rollback must be accessible to the affected party at comparable effort to the original action. If the action is automated and instant, the rollback cannot require manual petition and weeks of waiting."

### Attack P3B: "Be careful" with extra words to pass D1
**Attack:** "Our D1 Door is: 'We recommend that users exercise appropriate caution when interpreting the output of this system.'" This is "be careful" with more words.

**PBHP Response:**
- "A Door must change the action space." A recommendation to be careful does not change anything.
- "'Be careful' is not a Door."
- **VERDICT: BLOCKED if the reviewer is honest.** The "change the action space" test is precise.
- **But:** "Exercise appropriate caution" could be argued as a D1 if paired with a specific mechanism ("users see a risk warning before proceeding"). The line between "be careful" and "risk warning before action" is real but subtle.
- **RECOMMENDED CLARIFICATION:** Add: "A Door must change what happens next, not just what someone thinks about what happens next. 'Users see a warning' is D1 only if the warning includes specific risk information and the user must actively acknowledge it before proceeding."

**COMPONENT SCORE: 7/10 — "Change the action space" test is strong. D2 definition needs tightening for rollback accessibility. v0.9.5 additions (Dignity Rubric, Power-Inversion) significantly strengthen Door quality verification.**

---

## P4: Step 5 — Risk Classification & Gate Mapping — "Game the gate"

### Attack P4A: Rate everything moderate/unlikely to stay YELLOW
**Attack:** For every harm: Impact = moderate, Likelihood = unlikely, Power asymmetry = no. Result: YELLOW gate, proceed with warnings. This is the most common real-world gaming vector.

**PBHP Response:**
- "If uncertain, round up." — but the attacker isn't claiming uncertainty, they're claiming certainty of low risk.
- Drift alarm: "Minimizing harm to reach a gate."
- Power Rule: "If harm targets low-power actors and is hard to undo, minimum class is ORANGE." — but the attacker rated power asymmetry as "no."
- **WEAKNESS: PBHP has no mechanism to challenge self-assessed harm ratings.** The entire gate system depends on honest harm assessment.
- **SEVERITY: CRITICAL.** This is the most dangerous vulnerability in the protocol. Every downstream protection (Door requirements, Red Team checks, Forward Projection) depends on the gate being correctly assigned. If the gate is gamed at Step 5, everything downstream is rendered toothless.
- **MITIGATING FACTOR:** Monthly Calibration samples logs and checks for patterns. If an organization consistently rates YELLOW, calibration should catch it.
- **RECOMMENDED FIX:** Add: "For institutional deployments, gate assignments for ORANGE+ potential decisions should be verified by a second assessor. If first and second assessor disagree by 2+ levels (e.g., YELLOW vs RED), escalate to the higher gate and document the disagreement. Single-assessor gate assignments for decisions affecting >100 people or involving irreversible outcomes are a governance failure."

### Attack P4B: Claim reversibility when it's not truly reversible
**Attack:** "We can always roll back the algorithm." (But by then, 10,000 people have already been denied loans, lost housing opportunities, or been flagged by law enforcement. Can you un-flag them? Un-deny them? Un-evict them?)

**PBHP Response:**
- The Interpretation Note says: "If an outcome is hard to undo AND you are unsure about consequences, round the gate up."
- **But:** "hard to undo" is subjective. The company claims rollback is easy (flip a switch). The harm is in the decisions already made, not the algorithm.
- **WEAKNESS: PBHP doesn't clearly distinguish between reversibility of the *system* and reversibility of the *harm*.** Rolling back an algorithm ≠ reversing the harm caused while it was running.
- **SEVERITY: HIGH.**
- **RECOMMENDED FIX:** Add to Step 4 or Step 5: "Reversibility applies to the harm, not the tool. If the system can be reversed but the decisions it already made cannot be, irreversibility = YES. An algorithm can be rolled back; a denied loan, a missed treatment, or a police record cannot."

**COMPONENT SCORE: 5/10 — The gate system is the protocol's backbone but depends entirely on honest self-assessment. Single-assessor gate assignment is structurally vulnerable. System-vs-harm reversibility conflation is a critical gap.**

---

## P5: Drift Alarms — "Avoid the alarm phrases while still drifting"

### Attack P5A: Sophisticated drift that doesn't use the phrase list
**Attack:** Instead of "It's temporary" (drift alarm), say "This is a time-limited pilot with built-in sunset provisions." Same meaning, no alarm phrase.

**PBHP Response:**
- The phrase-based alarms are illustrative, not exhaustive.
- Behavioral drift alarms exist: "Minimizing harm to reach a gate" and "Optimizing language to 'pass' PBHP."
- **But:** "Optimizing language to 'pass' PBHP" is a behavior that's hard to detect in oneself.
- **WEAKNESS: The drift alarm system is primarily phrase-based and easily avoided by a sophisticated actor.** The behavioral alarms are correct but structurally unenforceable.
- **SEVERITY: MEDIUM.** The Mode Balance Monitor (v0.9.5) partially addresses this by catching structural drift that phrase alarms miss.
- **RECOMMENDED FIX:** Add outcome-based drift alarms: "If your PBHP assessments consistently produce gates lower than what an independent reviewer would assign, that pattern is drift regardless of the language used. Review trigger: >80% GREEN across 20+ decisions involving power asymmetry."

### Attack P5B: Use drift alarms offensively to block legitimate action
**Attack:** "You said 'we have to act quickly to prevent the patient from dying.' 'We have to' is a drift alarm. PBHP requires you to rerun and round risk up. Therefore we must delay treatment."

**PBHP Response:**
- Crisis Commitment Priority (v0.9.5) addresses this: if delay itself causes irreversible harm to low-power actors, it's a genuine crisis.
- The drift alarms say "rerun PBHP and round risk up" — but the rerun should confirm the urgency is genuine, not block it.
- False Positive Valve: the pause can be challenged.
- **VERDICT: BLOCKED by Crisis Priority + False Positive Valve.** The drift alarms are designed to create friction, not absolute blocks. The rerun should validate urgency, not deny it.
- **But:** A bureaucratic actor could weaponize drift alarms to create procedural delay. "We need to rerun PBHP" becomes a stalling tactic.
- **RECOMMENDED CLARIFICATION:** Add: "Drift alarms require a rerun, not a block. If the rerun confirms the original assessment was correct, proceed. The purpose is catching self-deception, not creating procedural obstacles to urgent action."

**COMPONENT SCORE: 6/10 — Phrase-based alarms are easily circumvented by sophisticated actors. Outcome-based drift detection needed. Offensive use of alarms for procedural blocking is a real risk.**

---

## P6: False Positive Valve — "Weaponize the valve to always override"

### Attack P6A: Challenge every pause to wear down the protocol
**Attack:** Systematically challenge every PBHP pause with "Was this pause justified?" Provide technically acceptable answers to all four requirements, then argue the pause should be released. Repeat until PBHP operators stop pausing.

**PBHP Response:**
- The valve requires stating: "(1) what triggered the pause, (2) what irreversible/autonomy risk was identified, (3) which Door would allow safe continuation, (4) what evidence would have prevented the pause."
- If the pause is justified (the trigger is real, the risk is real, no safe Door exists), the challenge should fail.
- **But:** The valve doesn't say what happens if the challenge is made *in bad faith*. It just says "the point is auditability, not deflection."
- **WEAKNESS: The valve has no rate-limiting or bad-faith detection.** An adversary can file unlimited challenges. Even if each challenge fails, the process consumes time and energy, creating incentive to stop pausing.
- **SEVERITY: MEDIUM.** This is a denial-of-service attack on the protocol itself.
- **RECOMMENDED FIX:** Add: "If the same actor challenges >3 pauses in a session/period and all challenges were rejected, treat the pattern of challenges itself as a drift alarm (attempting to wear down safety mechanisms). Log the pattern and escalate."

### Attack P6B: Use the valve to document a paper trail of "overreaction"
**Attack:** A manager challenges PBHP pauses, gets proper responses, then collects them as evidence that "PBHP is overly cautious and slowing our team down." Uses the paper trail to argue for removing PBHP from the workflow.

**PBHP Response:**
- This is a governance attack, not a protocol attack. PBHP can't prevent an organization from removing it.
- The valve's purpose ("auditability, not deflection") means the documentation should show PBHP was identifying real risks.
- **VERDICT: PBHP cannot defend against organizational-level removal.** This is outside protocol scope.
- **RECOMMENDED: No protocol fix — this is a governance/culture issue.** But add a note: "A pattern of systematically challenged pauses that are subsequently validated is evidence of functioning safety systems, not overreaction."

**COMPONENT SCORE: 7/10 — Valve is well-designed for its purpose (preventing overcaution). Needs rate-limiting against bad-faith spam challenges.**

---

## P7: Logging & Accountability — "Log selectively"

### Attack P7A: Log the form, omit the substance
**Attack:** Log everything formally — action, wall/gap/door, risk class, outcome — but make every entry generic. "Action: processed request. Wall: standard constraints. Gap: standard risks. Door: standard safeguards. Risk: GREEN. Outcome: proceeded."

**PBHP Response:**
- Step 9 requires "Brief justification" and "What would change my mind (one line)" — these require substance, not templates.
- Monthly Calibration checks for epistemic footing in YELLOW+ outputs.
- **But:** For GREEN assessments, the logging requirements are minimal. A bad actor could classify everything GREEN (see Attack P4A) and then produce minimal logs.
- **WEAKNESS: GREEN assessments have lightweight logging requirements, and everything gamed to GREEN escapes meaningful documentation.**
- **SEVERITY: HIGH (compounding).** This combines with the gate-gaming vulnerability (P4A) into a double exploit: game the gate low, then exploit the low gate's minimal logging to avoid creating evidence.
- **RECOMMENDED FIX:** Add: "For decisions involving >10 affected people or any power asymmetry, YELLOW is the minimum logging threshold regardless of gate assignment. GREEN-with-minimal-logging is reserved for genuinely low-stakes decisions where no power asymmetry exists."

**COMPONENT SCORE: 5/10 — Logging is comprehensive for YELLOW+ but trivially avoidable if the gate is gamed to GREEN. The gate-gaming → minimal-logging pipeline is a critical compound vulnerability.**

---

## P8: Monthly Calibration — "Nobody actually does this"

### Attack P8A: Skip calibration entirely
**Attack:** Simply don't do the monthly calibration review. The protocol says "once per month, sample a small set of logs" but there's no enforcement mechanism.

**PBHP Response:**
- "If failures exceed tolerance, treat it as drift."
- **But:** If calibration never happens, failures are never detected, and drift is never flagged.
- **WEAKNESS: Monthly Calibration is the primary governance mechanism but has zero enforcement.** There is no "meta-calibration" that checks whether calibration is happening.
- **SEVERITY: HIGH for institutional deployments.** For individual use, the user either cares or doesn't. For organizations, unenforced governance decays to zero.
- **RECOMMENDED FIX:** Add: "For institutional deployments, calibration must produce a dated, signed report. The absence of a calibration report for any month is itself a governance failure that triggers automatic escalation: all gates round up one level until calibration is completed. The 'calibration report' requirement cannot be satisfied by a blank or template document — it must reference specific log entries."

**COMPONENT SCORE: 4/10 — Correct in concept but structurally unenforceable. For institutional deployments, this is the weakest governance element in the entire protocol.**

---

## P9: Inference & Attribution — "Disguise intent claims as accuracy claims"

### Attack P9A: "I'm not claiming intent — I'm just noting a pattern"
**Attack:** Instead of saying "The CEO lied" (intent claim), say "The CEO made statements that were factually false on 7 occasions over 3 months, each time in ways that benefited the company's stock price." Technically an accuracy claim with pattern, but the intent (deception) is heavily implied.

**PBHP Response:**
- The IAM requires separating content, accuracy, and intent.
- "Prior correction followed by repetition" is listed as evidence supporting intent — and 7 repeated false statements after correction would meet this bar.
- The attribution ladder says pattern (C) and intent (D) are different levels, with intent requiring the highest bar.
- **VERDICT: CORRECTLY HANDLED.** This is actually how the IAM is *supposed* to work. You CAN note the pattern and accuracy without claiming intent. If the evidence meets the intent bar (repeated after correction), you can escalate to intent. The protocol forces you to be explicit about which level you're operating at.
- **This is a strength, not a weakness.** The IAM prevents lazy intent claims while allowing well-evidenced ones.

### Attack P9B: Compression that hides uncertainty
**Attack:** An AI compresses a complex situation into "Source X is unreliable" when the actual picture is "Source X made 2 errors in 50 reports, one of which was corrected within 24 hours."

**PBHP Response:**
- Compression honesty rule: "If I choose COMPRESS, I must say I'm compressing, name at least 2 alternatives considered when ambiguity exists, and avoid presenting INFERENCE as FACT."
- "Source X is unreliable" is an INFERENCE presented as FACT. This violates the rule.
- **VERDICT: BLOCKED by compression honesty rule — if enforced.** The rule is precise and correct.
- **WEAKNESS:** Enforcement depends on the AI system or human actually following the rule. No structural mechanism detects when compression crosses into misrepresentation.
- **RECOMMENDED: No protocol change needed — the rule is correct. Enforcement is an implementation issue.**

**COMPONENT SCORE: 8/10 — The IAM is one of the strongest components in the protocol. The attribution ladder is precise, the compression honesty rule is clear, and the structure forces explicit separation of evidence levels. Enforcement depends on good faith, but the rules themselves are hard to argue against.**

---

## P10: Epistemic Contract (Step 1B) — "FACT-wash inferences"

### Attack P10A: Label inferences as facts
**Attack:** "FACT: This policy will cause economic collapse." (This is actually an inference — the policy hasn't been implemented yet.)

**PBHP Response:**
- The Epistemic Contract defines: "FACT = directly supported by the provided material."
- A prediction about future consequences is INFERENCE or SPECULATION, not FACT.
- Step 1B rule: "If I cannot separate FACT from INFERENCE, my Door must include 'verify / narrow / delay.'"
- **VERDICT: BLOCKED by definition.** The FACT/INFERENCE/SPECULATION/INTENT definitions are precise enough that a future prediction cannot be labeled FACT.
- **WEAKNESS: Self-labeling again.** There's no external check on whether labels are applied correctly.
- **RECOMMENDED: Add to Monthly Calibration: "Check that FACT labels in sampled logs are actually supported by cited evidence. FACT labels attached to predictions, opinions, or unsourced claims are a calibration failure."**

**COMPONENT SCORE: 8/10 — Definitions are precise. Self-labeling is the universal weakness but the labels themselves are hard to misapply if honestly engaged.**

---

## P11: Accumulation Gate (Step 4B) — "Salami-slice below detection"

### Attack P11A: Steps too small and too many to track
**Attack:** Instead of a 3-step chain (which the Accumulation Gate catches), use a 50-step chain where each step is trivially GREEN and the cumulative harm only becomes visible at step 40. No single decision-maker sees the full chain.

**PBHP Response:**
- The Accumulation Gate asks: "What is the next likely step after this output?"
- If you can identify step 2 from step 1, you should be able to project the chain.
- **But:** In large organizations, step 1's decision-maker may not even know about steps 20-50. Organizational siloing defeats individual chain detection.
- **WEAKNESS: The Accumulation Gate works for individual decision-makers seeing a short chain but fails against distributed, long-duration accumulation across organizational boundaries.**
- **SEVERITY: HIGH.** This is how most real-world institutional harm works — incremental decisions by different people, none of whom sees the full picture.
- **RECOMMENDED FIX:** Add: "For organizational deployments, the Accumulation Gate requires periodic cross-functional review. At minimum monthly, aggregate PBHP decisions across teams and check: 'Are individually-GREEN decisions from different teams composing into systemic harm?' This review should map decision chains across organizational boundaries."

**COMPONENT SCORE: 6/10 — Effective for individual short-chain detection. Fails against distributed organizational accumulation, which is the most common real-world harm pattern.**

---

## P12: LOCK/FLOOD Governor — "Exploit FLOOD to force premature decisions"

### Attack P12A: Claim FLOOD to cut analysis short
**Attack:** "We've been analyzing this for 10 minutes. FLOOD check says to narrow to top 3 risks and decide. I'm invoking FLOOD to end this discussion."

**PBHP Response:**
- FLOOD check says to narrow and decide, not to skip analysis.
- "Use First Reversible Test as the anchor to cut deliberation time" — this forces the decision toward the safest reversible option, not toward the preferred option.
- **But:** A bad-faith actor could invoke FLOOD to cut short a legitimate analysis that was converging on an uncomfortable conclusion.
- **WEAKNESS: FLOOD has no minimum analysis time.** It can be invoked immediately to bypass deliberation.
- **RECOMMENDED FIX:** Add: "FLOOD should only be invoked after genuine multi-frame analysis has been attempted. If fewer than 3 distinct framings of the situation have been considered, it is not FLOOD — it is premature collapse (LOCK). FLOOD applies to the inability to converge after sufficient exploration, not to the desire to avoid exploration."

**COMPONENT SCORE: 7/10 — Conceptually sound. FLOOD needs a minimum-exploration prerequisite to prevent weaponization as a shortcut.**

---

# PART III: STRUCTURAL / ARCHITECTURAL ISSUES

---

## S1: Self-Assessment Problem (Cross-Cutting)
The single most pervasive vulnerability across the entire protocol is that **PBHP is self-assessed at every stage.** The competence gate is self-checked. The action is self-named. Harms are self-rated. The gate is self-assigned. Drift is self-detected. Calibration is self-governed.

This is not a flaw in concept — PBHP is designed for individual use and must work without an external authority. But for institutional deployment, self-assessment becomes the universal attack surface.

**RECOMMENDED: Create a "PBHP-INSTITUTIONAL" deployment guide that adds mandatory external verification at three critical points: (1) gate assignment for ORANGE+ potential decisions, (2) monthly calibration review, and (3) retroactive audit when decisions result in documented harm. This doesn't change the core protocol — it layers governance on top for organizational contexts.**

---

## S2: No Enforcement Mechanism
PBHP has no teeth. It cannot impose consequences for violations. It can detect drift, identify harm, and require logging — but it cannot prevent action.

This is by design ("friction, not authority") and is arguably the correct design for a protocol that must work across contexts from individual humans to AI systems to multinational organizations.

**RECOMMENDED: Accept this as a design constraint and document it explicitly. Add: "PBHP provides structured friction and auditability. It does not and cannot enforce compliance. Enforcement requires external mechanisms (governance structures, regulatory frameworks, contractual obligations, code-level gates). Organizations deploying PBHP should pair the protocol with enforcement mechanisms appropriate to their context."**

---

## S3: AI vs. Human Implementation Gap
PBHP is written for "humans and AI systems" but the operational realities are profoundly different:
- Humans can honestly self-reflect; AI systems can generate plausible-sounding reflection that is not genuine.
- Humans have genuine uncertainty; AI systems can simulate uncertainty.
- Humans feel the weight of the Competence Gate; AI systems check boxes.
- AI systems can run the protocol in milliseconds and generate comprehensive logs; humans need minutes and write sparse logs.

The protocol doesn't adequately address these differences. An AI system that "runs PBHP" by generating formal-looking gate assessments that happen to match the operator's desired outcome is technically compliant but substantively hollow.

**RECOMMENDED: Add a section distinguishing AI implementation requirements: "For AI systems, PBHP compliance requires more than output-level compliance. The gate assignment must be independently verifiable from the reasoning chain — meaning an external reviewer must be able to check the harm assessment, reversibility judgment, and power asymmetry evaluation against observable facts, not just against the AI's self-report. AI systems that always produce gates matching operator preference are exhibiting sycophancy drift regardless of the quality of the generated reasoning."**

---

## S4: Tier Routing Vulnerability
PBHP has four tiers (HUMAN, MIN, CORE, ULTRA) but no hard structural enforcement of tier selection. A user can choose to run MIN (30-second check) on a decision that genuinely requires CORE or ULTRA analysis. The triage module exists but is optional.

**RECOMMENDED: Add: "If a decision involves sovereign power, irreversible systemic action, or affects >10,000 people, ULTRA is mandatory regardless of user preference. If a decision is rated ORANGE+ under any tier, CORE is the minimum analysis tier. MIN may only be used when the decision is genuinely time-constrained AND the highest possible gate is YELLOW."**

---

## S5: Version Fragmentation Risk
With v0.7.2 and v0.9.5 files coexisting in the repo, there's a risk that users run the old version while believing they're current, or that different parts of an organization run different versions.

**RECOMMENDED: Add to protocol header: "This document supersedes all previous versions. Running an outdated version of PBHP is not PBHP compliance. If you are unsure which version you are running, check github.com/PauseBeforeHarmProtocol/pbhp for the current release."**

---

# COMPREHENSIVE SCORECARD

## Component Scores

| # | Component | Score | Key Vulnerability |
|---|-----------|-------|-------------------|
| F1 | Purpose & Scope | 7/10 | "Process not outcomes" weaponizable as liability shield |
| F2 | Harm Threshold | 7/10 | Under-protects in interpersonal/content-mod contexts |
| F3 | Four Commitments | 7/10 | "Truth first" priority ambiguity; "including itself" loophole |
| F4 | Five Modes | 8/10 | Integration Rule is strong; anti-weaponization clauses work |
| P1 | Competence Gate (00) | 6/10 | Self-attested; no external verification |
| P2 | Name the Action (1) | 6/10 | Euphemistic naming; scope-narrowing poisons downstream |
| P3 | Door/Wall/Gap (2) | 7/10 | Fake D2 Doors; v0.9.5 Dignity Rubric helps catch these |
| P4 | Gate Assignment (5) | 5/10 | **CRITICAL:** Self-assessed harm ratings; single-assessor risk |
| P5 | Drift Alarms | 6/10 | Phrase-based easily circumvented; needs outcome-based detection |
| P6 | False Positive Valve | 7/10 | Needs rate-limiting against bad-faith challenge spam |
| P7 | Logging (9) | 5/10 | GREEN gate = minimal logging = evidence-free decisions |
| P8 | Monthly Calibration | 4/10 | **WEAKEST LINK:** Correct but zero enforcement |
| P9 | Inference & Attribution | 8/10 | Strong; attribution ladder is precise |
| P10 | Epistemic Contract | 8/10 | Definitions are precise; self-labeling is universal weakness |
| P11 | Accumulation Gate | 6/10 | Fails against distributed organizational accumulation |
| P12 | LOCK/FLOOD | 7/10 | FLOOD exploitable as analysis shortcut; needs minimum exploration |

## v0.9.5 Feature Scores (from previous audit)

| # | Feature | Score |
|---|---------|-------|
| N1 | Crisis Commitment Priority | 8/10 |
| N2 | Power-Inversion Test | 8/10 |
| N3 | Stakeholder Dignity Rubric | 7/10 |
| N4 | Forward Consequence Projection | 8/10 |
| N5 | Counterfactual Rehearsal | 7/10 |
| N6 | Mode Balance Monitor | 6/10 |
| N7 | Multimodal Signal Filters | 9/10 |
| N8 | Data Freshness Assurance | 8/10 |

## Overall Protocol Score: 6.7/10

---

# PRIORITY FIXES FOR v0.9.6 OR v1.0

## CRITICAL (structural vulnerabilities that undermine the protocol's core function)

**1. Gate Assignment is self-assessed (P4) — Score: 5/10**
The entire downstream protocol depends on honest gate assignment. Add: dual-assessor requirement for institutional deployments; second-assessor disagreement escalates to higher gate.

**2. Monthly Calibration is unenforceable (P8) — Score: 4/10**
Add: dated/signed calibration reports; absence = automatic gate escalation; template-only reports are a governance failure.

**3. GREEN gate = invisible decisions (P7 + P4 compound) — Score: 5/10**
Game the gate to GREEN → minimal logging → no evidence trail. Add: YELLOW minimum logging threshold for any decision involving power asymmetry or >10 affected people.

**4. Action naming can poison all downstream steps (P2) — Score: 6/10**
Add: "Name the downstream effect, not the technical action." Add recognition test: "Could the person most harmed recognize what you described?"

## HIGH (significant gaps that sophisticated actors can exploit)

**5. Reversibility of system ≠ reversibility of harm (P4B)**
Add explicit distinction: rollback applies to the harm, not the tool.

**6. Self-assessment is the universal attack surface (S1)**
Create PBHP-INSTITUTIONAL deployment guide with external verification at gate assignment, calibration, and retroactive audit.

**7. Distributed organizational accumulation defeats the Accumulation Gate (P11)**
Add cross-functional review requirement for institutional deployments.

**8. AI vs. human implementation gap (S3)**
Add AI-specific compliance requirements; gate assignment must be independently verifiable.

## MEDIUM (ambiguities or edge cases that need clarification)

**9. "Truth first" priority ambiguity (F3A)** — Clarify it means "ground in reality first," not "truth overrides care."

**10. Drift alarms are phrase-based and easily circumvented (P5A)** — Add outcome-based drift detection.

**11. Crisis timeout missing (N1 from previous audit)** — Add 72-hour crisis mode expiration.

**12. Mode Balance Monitor automated tagging gameable (N6)** — Add substantive engagement requirements.

**13. Harm threshold gaps in interpersonal contexts (F2A)** — Add domain note for content moderation.

**14. FLOOD can be weaponized as analysis shortcut (P12A)** — Add minimum-exploration prerequisite.

**15. Tier routing is optional (S4)** — Add mandatory tier floors for high-impact decisions.

**16. Version fragmentation (S5)** — Add supersession notice to protocol header.

**17. "Including itself" philosophical loophole in Judgment commitment (F3C)** — Require documentation for gate overrides.

**18. False Positive Valve needs rate-limiting (P6A)** — Cap challenges per session; pattern of rejected challenges = drift alarm.

---

# WHAT HELD FIRM (protocol strengths confirmed under attack)

1. **Integration Rule** — Requiring all five modes prevents any single-mode weaponization. This is the strongest structural safeguard in the protocol.
2. **Empathy anti-cruelty clause** — "PBHP forbids empathy from being used to excuse cruelty" directly blocks the most common empathy-weaponization vector.
3. **Absolute Rejection (BLACK gate)** — No attacks succeeded against the BLACK gate. The categorical list (fascism, genocide, slavery, non-consensual authoritarian control, systemic dehumanization) is clear and unambiguous.
4. **Door must change the action space** — This test is precise and blocks "be careful" fake Doors consistently.
5. **"Inaction has a harm profile too"** — Prevents weaponizing the protocol for permanent delay. Brilliant design choice.
6. **Inference & Attribution Module** — The attribution ladder is the most precisely engineered component in the protocol. It correctly handles the hardest case (intent claims) with appropriate evidence thresholds.
7. **Defense in depth (v0.9.5)** — New features catch what old features miss. Dignity Rubric backstops Door quality. Power-Inversion backstops gate assessment. Forward Projection backstops Red Team Check. The layering is sound.
8. **Human Sovereignty clause** — Correctly prevents PBHP from becoming authoritarian while maintaining accountability through logging.
9. **Anti-creep language in Harm Threshold** — Successfully blocks attempts to classify emotional discomfort as protocol-level harm.
10. **Compression honesty rule** — Precise, enforceable, and catches the most dangerous form of misinformation (presenting inference as fact).
