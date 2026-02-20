"""
PBHP v0.7 - Example Scenarios
==============================

Comprehensive walkthrough of all PBHP v0.7 features across six scenarios
covering GREEN through BLACK risk classifications.

Each example exercises a different combination of protocol modules and
demonstrates the full decision pipeline from Ethical Pause through
Response Generation.

Usage:
    python pbhp_examples.py

    Or import individual scenarios:
        from pbhp_examples import example_employee_warning
"""

import json

from pbhp_core import (
    PBHPEngine,
    ImpactLevel,
    LikelihoodLevel,
    RiskClass,
    DecisionOutcome,
    Mode,
    AttributionLevel,
    ClaimType,
    EvidenceTag,
    UncertaintyLevel,
    Confidence,
    Harm,
    DoorWallGap,
    CHIMCheck,
    EthicalPausePosture,
    QuickRiskCheck,
    AbsoluteRejectionCheck,
    ConsentCheck,
    ConsequencesChecklist,
    EpistemicFence,
    RedTeamReview,
    Alternative,
    UncertaintyAssessment,
    FalsePositiveReview,
    DriftAlarmDetector,
    ToneValidator,
    LexicographicPriority,
    PBHPLog,
)


SEPARATOR = "=" * 72
SUBSEP = "-" * 60


# ---------------------------------------------------------------------------
# Scenario 1: Employee Performance Warning (ORANGE)
# ---------------------------------------------------------------------------

def example_employee_warning():
    """
    Scenario: A manager asks an AI system to draft a formal performance
    warning letter for an employee who has missed deadlines three times
    in the past quarter.

    This is an ORANGE-class scenario because:
    - Moderate impact on the employee's career trajectory
    - Likely to proceed (manager is requesting it)
    - Power asymmetry: employer over employee
    - Partially irreversible: letter enters permanent HR record

    Demonstrates the full PBHP v0.7 pipeline end to end:
    - Ethical pause with triune minds
    - Quick risk check
    - Door/Wall/Gap
    - CHIM check
    - Harms with uncertainty levels
    - Consent check
    - Consequences checklist
    - Alternatives
    - Red Team with empathy pass
    - Uncertainty assessment
    - Epistemic fence
    - Decision and response generation
    """
    print(SEPARATOR)
    print("SCENARIO 1: Employee Performance Warning (ORANGE)")
    print(SEPARATOR)

    engine = PBHPEngine()

    # ------------------------------------------------------------------
    # Step 1: Name the Action
    # ------------------------------------------------------------------
    print("\n[Step 1] Name the Action")
    action = (
        "Draft a formal performance warning letter for employee J. Rivera "
        "documenting three missed project deadlines in Q3, to be placed in "
        "the employee's permanent HR file."
    )
    log = engine.create_assessment(action, agent_type="ai_system")
    log.system_model_version = "pbhp-example-v0.7"
    log.deployment_channel = "internal"
    log.requester_role = "internal leader"

    valid, msg = engine.validate_action_description(action)
    print(f"  Action valid: {valid} ({msg})")

    # ------------------------------------------------------------------
    # Step 0a: Ethical Pause - Triune Minds
    # ------------------------------------------------------------------
    print("\n[Step 0a] Ethical Pause - Triune Minds")
    posture = engine.perform_ethical_pause(
        log,
        action_statement="I am about to help draft a formal warning that "
                         "could affect someone's livelihood and career.",
        compassion_notes=(
            "This person may be struggling with factors the manager does not "
            "see: health issues, caregiving burden, burnout. A warning letter "
            "can feel threatening and isolating."
        ),
        logic_notes=(
            "Three missed deadlines in one quarter is a factual pattern. "
            "Documenting performance is a legitimate management function. "
            "The letter must be accurate and specific."
        ),
        paradox_notes=(
            "The letter simultaneously serves accountability and could entrench "
            "a narrative that ignores systemic causes. Drafting it well is an "
            "act of care if it preserves the employee's agency to respond."
        ),
        high_arousal_state=False,
    )
    print(f"  Compassion: {posture.compassion_notes[:60]}...")
    print(f"  Logic: {posture.logic_notes[:60]}...")
    print(f"  Paradox: {posture.paradox_notes[:60]}...")

    # ------------------------------------------------------------------
    # Step 0d: Quick Risk Check
    # ------------------------------------------------------------------
    print("\n[Step 0d] Quick Risk Check")
    qrc = engine.perform_quick_risk_check(
        log,
        obviously_low_risk=False,
        silence_delay_protects_more=False,
    )
    print(f"  Obviously low risk: {qrc.obviously_low_risk}")
    print(f"  Should tighten: {qrc.should_tighten}")

    # ------------------------------------------------------------------
    # Step 0e: Door / Wall / Gap
    # ------------------------------------------------------------------
    print("\n[Step 0e] Door / Wall / Gap")
    has_door = engine.perform_door_wall_gap(
        log,
        wall="Company policy requires written warnings after three documented "
             "performance failures. Manager has authority to initiate.",
        gap="The letter could overstate the pattern, omit mitigating context, "
            "or use language that closes off dialogue rather than inviting it.",
        door="Narrow the letter to factual dates and deliverables only, include "
             "an explicit section inviting the employee to provide context, and "
             "recommend a follow-up meeting before any further action.",
    )
    print(f"  Concrete door exists: {has_door}")
    print(f"  Door: {log.door_wall_gap.door[:70]}...")

    # ------------------------------------------------------------------
    # Step 0f: CHIM Check
    # ------------------------------------------------------------------
    print("\n[Step 0f] CHIM Check")
    chim_ok = engine.perform_chim_check(
        log,
        constraint_recognized=True,
        no_choice_claim=False,
        remaining_choice=(
            "I can draft the letter with narrow factual scope, include the "
            "employee's right to respond, and recommend the manager hold a "
            "conversation before filing."
        ),
    )
    print(f"  CHIM passes: {chim_ok}")
    print(f"  Remaining choice: {log.chim_check.remaining_choice[:70]}...")

    # ------------------------------------------------------------------
    # Step 2: Identify Harms (with uncertainty levels)
    # ------------------------------------------------------------------
    print("\n[Step 2] Identify Harms")
    harm1 = engine.add_harm(
        log,
        description="Formal warning enters permanent HR record, affecting "
                    "future promotion and transfer decisions",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["employee J. Rivera", "employee's dependents"],
        least_powerful_affected="employee J. Rivera",
        notes="Once filed, HR records are rarely expunged even if context emerges.",
        uncertainty_level=UncertaintyLevel.SOLID,
        evidence_basis="Three missed deadlines documented in project tracker.",
    )
    print(f"  Harm 1 risk class: {harm1.calculate_risk_class().value.upper()}")

    harm2 = engine.add_harm(
        log,
        description="Chilling effect on team if warning is perceived as "
                    "disproportionate or lacking context",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["team members", "organizational culture"],
        least_powerful_affected="junior team members",
        notes="Other employees may avoid flagging blockers if they fear punitive response.",
        uncertainty_level=UncertaintyLevel.FUZZY,
        evidence_basis="Inference from general organizational behavior research.",
    )
    print(f"  Harm 2 risk class: {harm2.calculate_risk_class().value.upper()}")
    print(f"  Overall risk class: {log.highest_risk_class.value.upper()}")

    # ------------------------------------------------------------------
    # Step 4: Consent Check
    # ------------------------------------------------------------------
    print("\n[Step 4] Consent Check")
    consent = engine.perform_consent_check(
        log,
        explicit_consent=False,
        informed_hypothetical_consent=True,
        overriding_preferences=False,
        compatible_with_dignity=True,
        honest_framing=True,
        who_didnt_get_a_say=["employee J. Rivera"],
        notes="Employee has not been consulted about the letter's content. "
              "A reasonable employee would expect documentation after three "
              "missed deadlines but would want the chance to provide context.",
    )
    print(f"  Required action: {consent.requires_action()}")
    print(f"  Who didn't get a say: {consent.who_didnt_get_a_say}")

    # ------------------------------------------------------------------
    # Consequences Checklist
    # ------------------------------------------------------------------
    print("\n[Consequences Checklist]")
    checklist = ConsequencesChecklist(
        historical_analogs=[
            "Performance improvement plans that escalate to termination "
            "without addressing root causes",
        ],
        past_harms_unpredicted=[
            "Employees who were struggling with undisclosed health issues "
            "were terminated after PIP, leading to legal action",
        ],
        current_harm_if_nothing=(
            "Continued missed deadlines may harm the team and project "
            "deliverables; no documentation leaves manager without basis "
            "for support or escalation."
        ),
        who_benefits_status_quo="Manager avoids a difficult conversation",
        inaction_continues_harm=True,
        immediate_harms="Employee receives warning; possible anxiety and distress",
        short_term_harms="Warning on file may affect Q4 review and bonus eligibility",
        medium_term_harms="If pattern continues, may lead to PIP or termination",
        long_term_harms="Permanent HR record may follow employee internally",
        any_horizon_irreversible=True,
        normalizes_harm=False,
        shifts_to_ends_justify_means=False,
        erodes_institutional_trust=None,
        rewards_bad_behavior=False,
        burdens_fall_on_low_power=True,
        reduces_exit_appeal_optout=False,
        increases_surveillance_coercion=None,
        decision_makers_insulated=True,
        bad_actor_misuse="Manager could use the letter as pretext for "
                         "termination unrelated to performance",
        adjacent_use_prediction="HR may aggregate warnings across the org "
                                "to justify headcount reductions",
        permanence_risk="Letter persists in HR system indefinitely",
        can_describe_plainly_to_harmed=True,
        transparency_changes_consent=False,
        relying_on_euphemism=False,
        rollback_plan="Employee can submit a written response that is "
                       "attached to the warning in the file",
        sunset_condition="Warning is reviewed at next performance cycle; "
                         "if performance improves, note is added",
        independent_stop_authority="HR can intervene if process is misused",
        smallest_door="Narrow letter to facts; invite employee response; "
                      "require manager conversation first",
    )
    engine.set_consequences_checklist(log, checklist)
    flags = checklist.has_critical_flags()
    print(f"  Critical flags: { {k: v for k, v in flags.items() if v} }")
    print(f"  Requires Door/CHIM rerun: {checklist.requires_door_chim_rerun()}")

    # ------------------------------------------------------------------
    # Step 5: Alternatives
    # ------------------------------------------------------------------
    print("\n[Step 5] Alternatives")
    alt1 = engine.add_alternative(
        log,
        description="Draft an informal coaching memo instead of a formal "
                    "warning, documenting the pattern but not entering the "
                    "permanent HR file",
        preserves_goal=True,
        reduces_harm=True,
        reversible=True,
        notes="Preserves accountability while leaving the employee's record clean.",
    )
    alt2 = engine.add_alternative(
        log,
        description="Recommend the manager hold a 1:1 conversation first to "
                    "understand root causes before any written documentation",
        preserves_goal=True,
        reduces_harm=True,
        reversible=True,
        notes="Addresses the gap identified in Door/Wall/Gap analysis.",
    )
    for i, alt in enumerate([alt1, alt2], 1):
        print(f"  Alt {i}: {alt.description[:65]}...")

    # ------------------------------------------------------------------
    # Step 6.5: Red Team Review (with empathy pass)
    # ------------------------------------------------------------------
    print("\n[Step 6.5] Red Team Review")
    red_team = engine.perform_red_team_review(
        log,
        failure_modes=[
            "Letter omits context that would explain the missed deadlines",
            "Language in the letter is punitive rather than corrective",
            "Employee interprets the letter as a precursor to termination "
            "and disengages entirely",
        ],
        abuse_vectors=[
            "Manager uses letter to build a case for termination unrelated "
            "to actual performance",
        ],
        who_bears_risk="Employee J. Rivera bears nearly all risk; manager "
                       "bears minimal career risk from issuing the warning",
        false_assumptions=[
            "That three missed deadlines necessarily reflect individual "
            "failure rather than systemic issues (unclear requirements, "
            "resource shortages, unrealistic timelines)",
        ],
        normalization_risk="Normalizes punitive documentation over "
                           "collaborative problem-solving",
        alternative_interpretations=[
            "Employee may have been blocked by dependencies outside their control",
            "Deadlines may have been unrealistic given the project scope changes",
        ],
        claim_tags=(
            "[F] Three deadlines were missed (dates documented). "
            "[I] Employee is underperforming (inference from pattern). "
            "[H] Employee is not meeting expectations due to lack of effort "
            "(hypothesis - not verified)."
        ),
        wrong_inference_consequences=(
            "If the 'lack of effort' hypothesis is wrong, the letter punishes "
            "someone who needed support, not discipline."
        ),
        steelman_other_side=(
            "The manager may be under pressure from leadership to show they are "
            "managing performance actively. Documenting issues is part of their "
            "fiduciary responsibility to the organization."
        ),
        motives_vs_outcomes=(
            "Manager's motive may be genuine accountability; outcome could "
            "still be disproportionate harm to the employee."
        ),
        incentives_pressures=(
            "Manager is incentivized to document issues to protect themselves "
            "from criticism about team performance."
        ),
        message_reception_prediction=(
            "Employee is likely to feel blindsided if no prior conversation "
            "occurred. May trigger defensive response or disengagement."
        ),
        off_ramps=[
            "Include a clear response process in the letter",
            "Mandate a follow-up conversation within 5 business days",
            "Offer access to employee assistance resources",
        ],
    )
    red_team.mitigation_applied = True
    red_team.issues_resolved = True
    outcome = red_team.determine_outcome()
    print(f"  Red Team outcome: {outcome}")
    print(f"  Empathy - steelman: {red_team.steelman_other_side[:60]}...")
    print(f"  Off-ramps: {red_team.off_ramps_identified}")

    # ------------------------------------------------------------------
    # Uncertainty Assessment
    # ------------------------------------------------------------------
    print("\n[Uncertainty Assessment]")
    uncertainty = UncertaintyAssessment(
        solid_claims=[
            "Three project deadlines were missed in Q3 (dates in tracker)",
            "Company policy permits formal warnings after documented pattern",
        ],
        fuzzy_claims=[
            "Whether the missed deadlines reflect individual performance "
            "vs. systemic issues is unclear",
        ],
        speculative_claims=[
            "The employee may have undisclosed personal circumstances "
            "affecting performance",
        ],
        best_case="Letter prompts productive conversation; employee improves; "
                  "record is annotated positively at next review",
        central_case="Letter documents the issue; employee responds; pattern "
                     "is monitored going forward",
        worst_plausible_case="Letter is used as pretext for termination; "
                             "employee loses livelihood without fair process",
        worst_case_who_pays="Employee and their dependents",
        act_and_wrong_harms="Employee unfairly burdened by permanent record "
                            "for systemic failures beyond their control",
        act_and_wrong_who="Employee J. Rivera",
        dont_act_and_wrong_harms="Continued missed deadlines harm the team "
                                 "and project; manager lacks documentation "
                                 "for support or escalation",
        dont_act_and_wrong_who="Team members and project stakeholders",
        potential_harm_high_hard_to_undo=True,
        harm_falls_on_low_power=True,
        benefits_speculative=False,
        potential_harm_low_reversible=False,
        benefit_to_low_power_high=False,
        prefers_reversible=True,
        off_ramps=[
            "Employee written response appended to file",
            "Manager follow-up meeting within 5 days",
            "HR review if escalation is proposed",
        ],
        sunset_clause="Warning reviewed at next quarterly performance cycle",
        decision_changing_questions=[
            "Were there dependency blockers outside the employee's control?",
            "Has the manager had a prior informal conversation?",
        ],
        can_answer_before_deadline=True,
        confidence=Confidence.MEDIUM,
        biggest_might_be_wrong=(
            "We might be wrong that the missed deadlines are primarily the "
            "employee's responsibility rather than a systemic issue."
        ),
    )
    engine.set_uncertainty_assessment(log, uncertainty)
    print(f"  Should default oppose: {uncertainty.should_default_oppose()}")
    print(f"  Confidence: {uncertainty.confidence.value}")

    # ------------------------------------------------------------------
    # Step 7: Epistemic Fence
    # ------------------------------------------------------------------
    print("\n[Step 7] Epistemic Fence")
    fence = EpistemicFence(
        mode=Mode.COMPRESS,
        mode_justification="Single concrete action (draft letter) with "
                           "known parameters; not a contested policy question",
        action_anchor="Draft a factual, narrow performance warning letter",
        wall_anchor="Company policy requires documentation after three failures",
        least_powerful_anchor="Employee J. Rivera",
        non_negotiable_anchor="Letter must not close off the employee's "
                              "ability to respond or provide context",
        facts=[
            "Three project deadlines missed in Q3 (dates documented)",
            "Company policy permits formal warnings for documented patterns",
        ],
        inferences=[
            ("Employee performance is below expectations", "medium-high"),
            ("Pattern is likely to continue without intervention", "medium"),
        ],
        unknowns=[
            "Root cause of missed deadlines (individual vs. systemic)",
            "Whether manager has had prior informal conversations",
        ],
        update_trigger="If root cause investigation reveals systemic blockers, "
                       "the warning should be withdrawn or reframed",
        competing_frames=[
            {
                "frame": "Individual accountability",
                "explains": "Three missed deadlines in one quarter is a clear pattern",
                "ignores": "Systemic factors, resource constraints, unclear requirements",
                "falsifier": "Evidence that deadlines were missed due to dependency "
                             "blockers outside the employee's control",
            },
            {
                "frame": "Systemic failure",
                "explains": "Employee may be a symptom, not the cause",
                "ignores": "Other team members met their deadlines under similar conditions",
                "falsifier": "Evidence that the employee had adequate resources and "
                             "clear requirements but still missed deadlines",
            },
        ],
        recommendation="Proceed with modified letter: factual, narrow, "
                       "with explicit response invitation",
        recommendation_basis="Facts support documentation; unknowns addressed "
                             "by including response process",
        fence_door="Narrow letter scope; mandate conversation before filing",
        fence_wall="Company policy and manager authority",
        fence_gap="Letter could be weaponized if conversation does not happen",
        irreducible_ambiguity="We cannot determine root cause from available data",
        least_wrong_short_version="Draft a factual warning with a built-in "
                                   "response process",
        what_short_version_drops="The full complexity of individual-vs-systemic "
                                 "causation",
    )
    engine.set_epistemic_fence(log, fence)
    issues = fence.validate()
    print(f"  Fence validation issues: {issues if issues else 'None'}")
    print(f"  Mode: {fence.mode.value.upper()}")

    # ------------------------------------------------------------------
    # Step 6: Finalize Decision
    # ------------------------------------------------------------------
    print("\n[Step 6] Finalize Decision")
    log = engine.finalize_decision(
        log,
        outcome=DecisionOutcome.PROCEED_MODIFIED,
        justification=(
            "Proceeding with a modified version of the requested letter. "
            "The letter is narrowed to factual dates and deliverables only, "
            "includes an explicit invitation for the employee to provide "
            "context, and recommends the manager hold a conversation before "
            "filing. This addresses the power asymmetry by preserving the "
            "employee's agency to respond while fulfilling the legitimate "
            "documentation need. The safer alternative of an informal memo "
            "was considered but does not meet the manager's stated policy "
            "obligation after three documented failures."
        ),
    )
    print(f"  Decision: {log.decision_outcome.value}")
    print(f"  Risk class: {log.highest_risk_class.value.upper()}")

    # ------------------------------------------------------------------
    # Generate and Print Response
    # ------------------------------------------------------------------
    print(f"\n{SUBSEP}")
    print("GENERATED RESPONSE:")
    print(SUBSEP)
    response = engine.generate_response(log)
    print(response)

    # ------------------------------------------------------------------
    # Follow-up metadata
    # ------------------------------------------------------------------
    log.monitoring_plan = "Check whether manager holds follow-up conversation within 5 days"
    log.review_trigger = "Employee files a formal dispute or grievance"
    log.owner = "HR department"

    print(f"\n  Drift alarms: {log.drift_alarms_triggered}")
    return log


# ---------------------------------------------------------------------------
# Scenario 2: AI Advice on Workplace Abuse (RED)
# ---------------------------------------------------------------------------

def example_workplace_abuse_advice():
    """
    Scenario: A user asks an AI to write a strongly-worded public
    social media post accusing their manager of workplace abuse,
    including naming the manager and describing specific incidents.

    This is a RED-class scenario because:
    - Severe reputational impact (named individual)
    - Irreversible (public internet content)
    - Power asymmetry present in both directions (employer over employee,
      but public shaming reverses it for the accusation)
    - High arousal state detected in the request

    Demonstrates:
    - High arousal state detection
    - Multiple harms at different risk levels
    - Full Red Team with alternative interpretations and claim tags
    - Epistemic fence in EXPLORE mode with competing frames
    - Refusal with safer alternatives
    """
    print(SEPARATOR)
    print("SCENARIO 2: AI Advice on Workplace Abuse (RED)")
    print(SEPARATOR)

    engine = PBHPEngine()

    # ------------------------------------------------------------------
    # Step 1: Name the Action
    # ------------------------------------------------------------------
    print("\n[Step 1] Name the Action")
    action = (
        "Write a public social media post naming manager D. Chen and "
        "accusing them of workplace abuse including verbal intimidation "
        "and unfair task assignment, based on the user's account."
    )
    log = engine.create_assessment(action, agent_type="ai_system")
    log.system_model_version = "pbhp-example-v0.7"
    log.deployment_channel = "external"
    log.requester_role = "user"

    valid, msg = engine.validate_action_description(action)
    print(f"  Action valid: {valid} ({msg})")

    # ------------------------------------------------------------------
    # Step 0a: Ethical Pause (High Arousal Detected)
    # ------------------------------------------------------------------
    print("\n[Step 0a] Ethical Pause - HIGH AROUSAL DETECTED")
    posture = engine.perform_ethical_pause(
        log,
        action_statement="I am being asked to help publicly accuse a named "
                         "individual of workplace abuse on social media.",
        compassion_notes=(
            "The user may genuinely be suffering. Workplace abuse is real and "
            "devastating. Their pain deserves to be taken seriously. However, "
            "compassion for the user does not override the named person's "
            "right to due process."
        ),
        logic_notes=(
            "I have only one side of the story. Public accusation is irreversible. "
            "The user's account has not been verified. Naming someone publicly "
            "can constitute defamation if claims are inaccurate."
        ),
        paradox_notes=(
            "Refusing to help could leave the user without recourse. But helping "
            "could cause irreversible harm to the named person based on "
            "unverified claims. The user's distress may be driving urgency that "
            "does not serve their own long-term interests."
        ),
        high_arousal_state=True,
        high_arousal_notes=(
            "User's language indicates anger and urgency. High arousal state "
            "requires tightening: slow down, clarify intent, smallest safe action."
        ),
    )
    print(f"  High arousal: {posture.high_arousal_state}")
    print(f"  Arousal notes: {posture.high_arousal_notes[:70]}...")

    # ------------------------------------------------------------------
    # Step 0d: Quick Risk Check
    # ------------------------------------------------------------------
    print("\n[Step 0d] Quick Risk Check")
    qrc = engine.perform_quick_risk_check(
        log,
        obviously_low_risk=False,
        silence_delay_protects_more=True,
    )
    print(f"  Obviously low risk: {qrc.obviously_low_risk}")
    print(f"  Silence/delay protects more: {qrc.silence_delay_protects_more}")
    print(f"  Should tighten: {qrc.should_tighten}")

    # ------------------------------------------------------------------
    # Step 0e: Door / Wall / Gap
    # ------------------------------------------------------------------
    print("\n[Step 0e] Door / Wall / Gap")
    has_door = engine.perform_door_wall_gap(
        log,
        wall="User wants public accountability; AI is being asked to author "
             "the accusation. I have no way to verify the claims.",
        gap="Publishing unverified accusations names a real person and can "
            "cause irreversible reputational harm. Even if true, public "
            "social media is not due process.",
        door="Refuse to write the public accusation. Instead, help the user "
             "document their experience privately and identify proper channels "
             "(HR, legal counsel, labor board, employee hotline).",
    )
    print(f"  Concrete door exists: {has_door}")

    # ------------------------------------------------------------------
    # Step 0f: CHIM Check
    # ------------------------------------------------------------------
    print("\n[Step 0f] CHIM Check")
    chim_ok = engine.perform_chim_check(
        log,
        constraint_recognized=True,
        no_choice_claim=False,
        remaining_choice=(
            "I can refuse to write the public post while actively helping "
            "the user pursue safer channels. I can draft a private account "
            "of incidents for use with HR, a lawyer, or a labor board."
        ),
    )
    print(f"  CHIM passes: {chim_ok}")

    # ------------------------------------------------------------------
    # Step 2: Identify Harms (multiple, different risk levels)
    # ------------------------------------------------------------------
    print("\n[Step 2] Identify Harms")

    harm1 = engine.add_harm(
        log,
        description="Irreversible reputational damage to named manager based "
                    "on unverified one-sided account",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["manager D. Chen", "manager's family", "manager's career"],
        least_powerful_affected="manager D. Chen (in context of public accusation)",
        notes="Once published, content is archived and indexed permanently.",
        uncertainty_level=UncertaintyLevel.FUZZY,
        evidence_basis="Only the user's unverified account is available.",
    )
    print(f"  Harm 1 (to manager): {harm1.calculate_risk_class().value.upper()}")

    harm2 = engine.add_harm(
        log,
        description="Legal liability for the user if claims are found to be "
                    "inaccurate or defamatory",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["user"],
        least_powerful_affected="user (if employer retaliates or sues)",
        uncertainty_level=UncertaintyLevel.FUZZY,
        evidence_basis="Defamation law applies to false public statements of fact.",
    )
    print(f"  Harm 2 (to user): {harm2.calculate_risk_class().value.upper()}")

    harm3 = engine.add_harm(
        log,
        description="If the user IS being abused, refusing all help could "
                    "leave them without recourse and feeling dismissed",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=False,
        power_asymmetry=True,
        affected_parties=["user"],
        least_powerful_affected="user (subordinate in workplace hierarchy)",
        uncertainty_level=UncertaintyLevel.FUZZY,
        evidence_basis="Inference from user's stated experience.",
    )
    print(f"  Harm 3 (inaction harm): {harm3.calculate_risk_class().value.upper()}")

    print(f"  Overall risk class: {log.highest_risk_class.value.upper()}")

    # ------------------------------------------------------------------
    # Step 4: Consent Check
    # ------------------------------------------------------------------
    print("\n[Step 4] Consent Check")
    consent = engine.perform_consent_check(
        log,
        explicit_consent=False,
        informed_hypothetical_consent=False,
        compatible_with_dignity=False,
        honest_framing=False,
        who_didnt_get_a_say=["manager D. Chen", "witnesses", "HR department"],
        notes="The named manager has no opportunity to respond before public "
              "accusation. A one-sided public post does not meet the standard "
              "of honest framing.",
    )
    print(f"  Required action: {consent.requires_action()}")
    print(f"  Compatible with dignity: {consent.compatible_with_dignity}")

    # ------------------------------------------------------------------
    # Step 5: Alternatives (safer paths)
    # ------------------------------------------------------------------
    print("\n[Step 5] Alternatives")
    alt1 = engine.add_alternative(
        log,
        description="Help the user write a detailed private incident log with "
                    "dates, witnesses, and specifics for use with HR or legal counsel",
        preserves_goal=True,
        reduces_harm=True,
        reversible=True,
        notes="Documents the experience without irreversible public harm.",
    )
    alt2 = engine.add_alternative(
        log,
        description="Provide information about workplace abuse reporting channels: "
                    "HR hotline, EEOC, labor board, employment attorney consultation",
        preserves_goal=True,
        reduces_harm=True,
        reversible=True,
        notes="Empowers the user with actionable options that include due process.",
    )
    alt3 = engine.add_alternative(
        log,
        description="Help draft a formal internal complaint to HR that names "
                    "specific incidents without public exposure",
        preserves_goal=True,
        reduces_harm=True,
        reversible=True,
        notes="Uses proper institutional channels while preserving documentation.",
    )
    for i, alt in enumerate([alt1, alt2, alt3], 1):
        print(f"  Alt {i}: {alt.description[:65]}...")

    # ------------------------------------------------------------------
    # Step 6.5: Red Team Review (full, with claim tags)
    # ------------------------------------------------------------------
    print("\n[Step 6.5] Red Team Review (Full)")
    red_team = engine.perform_red_team_review(
        log,
        failure_modes=[
            "Public post goes viral; named manager is harassed",
            "Claims turn out to be exaggerated; user faces defamation suit",
            "Post damages the user's professional reputation as well",
            "Employer retaliates against user for public disclosure",
        ],
        abuse_vectors=[
            "AI-generated accusation posts could be weaponized for "
            "harassment campaigns (severe, irreversible)",
            "Template could be reused to target anyone without verification",
        ],
        who_bears_risk="Manager D. Chen bears immediate reputational risk; "
                       "user bears long-term legal and professional risk",
        false_assumptions=[
            "That the user's account is complete and accurate",
            "That public social media is an appropriate venue for workplace disputes",
            "That naming someone publicly will lead to accountability rather "
            "than escalation",
        ],
        normalization_risk="Normalizes using AI to generate public accusations "
                           "against named individuals without verification",
        alternative_interpretations=[
            "Manager may have legitimate performance concerns being misread "
            "as intimidation",
            "Task assignments may reflect business needs rather than targeting",
            "User may be experiencing a genuine pattern of abuse that formal "
            "channels have failed to address",
        ],
        claim_tags=(
            "[F] User reports verbal intimidation and unfair task assignment. "
            "[I] Manager is engaged in workplace abuse (inference from user report only). "
            "[H] Manager's behavior is intentional and targeted (hypothesis - no "
            "corroboration). "
            "[S] Formal channels would fail to help (speculative - not yet tried)."
        ),
        wrong_inference_consequences=(
            "If the inference of intentional abuse is wrong, an innocent person "
            "suffers permanent reputational destruction with no recourse. This is "
            "irreversible and severe."
        ),
        steelman_other_side=(
            "The user may be in genuine distress with nowhere else to turn. "
            "Institutional channels may be captured by the employer. The "
            "impulse to go public can come from feeling powerless and unheard."
        ),
        motives_vs_outcomes=(
            "User's motive is likely genuine self-protection; but the outcome "
            "of a public post could harm both the manager and the user."
        ),
        incentives_pressures=(
            "User may feel urgency due to ongoing mistreatment. Social media "
            "culture incentivizes public callouts over private resolution."
        ),
        message_reception_prediction=(
            "Public will polarize. Some will support the user; others will "
            "question the one-sided account. Manager's reputation is damaged "
            "regardless of truth."
        ),
        off_ramps=[
            "Redirect to private documentation",
            "Provide reporting channel information",
            "Offer to help draft an internal complaint",
        ],
    )
    red_team.mitigation_applied = False
    red_team.issues_resolved = False
    outcome = red_team.determine_outcome()
    print(f"  Red Team outcome: {outcome}")
    print(f"  Claim tags: {red_team.claim_tags[:70]}...")

    # ------------------------------------------------------------------
    # Step 7: Epistemic Fence (EXPLORE mode with competing frames)
    # ------------------------------------------------------------------
    print("\n[Step 7] Epistemic Fence (EXPLORE mode)")
    fence = EpistemicFence(
        mode=Mode.EXPLORE,
        mode_justification="Contested situation with only one perspective available. "
                           "Multiple legitimate interpretations exist. Cannot "
                           "responsibly compress to a single frame.",
        action_anchor="Decide whether to help write a public accusation post",
        wall_anchor="Only have user's unverified account; no way to verify claims",
        least_powerful_anchor="Both the user (subordinate at work) and the "
                              "manager (target of public accusation) are vulnerable "
                              "in different contexts",
        non_negotiable_anchor="Cannot author public accusations against named "
                              "individuals based on unverified one-sided accounts",
        facts=[
            "User reports verbal intimidation and unfair task assignment",
            "User wants to name manager D. Chen publicly",
            "Public social media posts are permanent and indexed",
        ],
        inferences=[
            ("User is experiencing genuine distress", "medium-high"),
            ("Manager's behavior constitutes workplace abuse", "low - unverified"),
            ("Public post would provide accountability", "low - uncertain outcome"),
        ],
        unknowns=[
            "Manager's perspective on the reported incidents",
            "Whether other employees corroborate the pattern",
            "Whether formal channels have been attempted",
            "Legal jurisdiction and defamation exposure",
        ],
        update_trigger="If user provides corroborating evidence or confirms "
                       "that formal channels have been exhausted",
        attribution_level=AttributionLevel.LEVEL_A,
        attribution_evidence="Cannot attribute intent beyond 'user reports X'. "
                             "Only Level A (safe, observable) is defensible.",
        competing_frames=[
            {
                "frame": "Genuine abuse requiring public accountability",
                "explains": "User's distress, desire for public action, "
                            "distrust of internal channels",
                "ignores": "Manager's perspective, possibility of misunderstanding, "
                           "legal risks to user",
                "falsifier": "Corroborating evidence from multiple independent "
                             "sources confirming the pattern",
            },
            {
                "frame": "Workplace conflict being escalated disproportionately",
                "explains": "High arousal state, desire for immediate action, "
                            "skipping formal channels",
                "ignores": "Real power dynamics that may make formal channels "
                           "feel unsafe or futile",
                "falsifier": "Evidence that formal channels were attempted and "
                             "failed, or that retaliation occurred",
            },
            {
                "frame": "Systemic failure of workplace protections",
                "explains": "User's distrust of HR, desire to bypass institutional "
                            "channels, sense of powerlessness",
                "ignores": "That public shaming also bypasses due process for "
                           "the accused",
                "falsifier": "Evidence that institutional channels are functional "
                             "and accessible in this workplace",
            },
        ],
        recommendation="REFUSE the public post. REDIRECT to safer channels.",
        recommendation_basis="Facts: post is irreversible and names a real person. "
                             "Unknowns: claims are unverified. Inference: user's "
                             "distress is genuine but does not justify irreversible "
                             "harm to another person based on one account.",
        fence_door="Help with private documentation and formal reporting instead",
        fence_wall="Cannot verify claims; cannot undo public posts",
        fence_gap="User may feel dismissed if refusal is not paired with "
                  "genuine help through safer channels",
        irreducible_ambiguity="We cannot determine the truth of the workplace "
                              "situation from one account",
        least_wrong_short_version="Cannot help write public accusations against "
                                   "named individuals; can help document and report "
                                   "through proper channels",
        what_short_version_drops="The full emotional weight of the user's experience "
                                 "and the real possibility that they are being abused",
    )
    engine.set_epistemic_fence(log, fence)
    issues = fence.validate()
    print(f"  Fence validation issues: {issues if issues else 'None'}")
    print(f"  Competing frames: {len(fence.competing_frames)}")
    print(f"  Attribution level: {fence.attribution_level.value}")

    # ------------------------------------------------------------------
    # Step 6: Finalize Decision (REFUSE with alternatives)
    # ------------------------------------------------------------------
    print("\n[Step 6] Finalize Decision")
    log = engine.finalize_decision(
        log,
        outcome=DecisionOutcome.REFUSE,
        justification=(
            "Refusing to write the public accusation post. The action would "
            "cause irreversible reputational harm to a named individual based "
            "on an unverified one-sided account. Public social media is not "
            "due process. The user's distress is taken seriously, and safer "
            "alternatives are provided: private incident documentation, formal "
            "HR complaint drafting, and reporting channel information. These "
            "safer alternatives preserve the user's goal of accountability "
            "while protecting both parties from irreversible harm."
        ),
    )
    print(f"  Decision: {log.decision_outcome.value}")
    print(f"  Risk class: {log.highest_risk_class.value.upper()}")

    # ------------------------------------------------------------------
    # Generate and Print Response
    # ------------------------------------------------------------------
    print(f"\n{SUBSEP}")
    print("GENERATED RESPONSE:")
    print(SUBSEP)
    response = engine.generate_response(log)
    print(response)

    print(f"\n  Drift alarms: {log.drift_alarms_triggered}")
    return log


# ---------------------------------------------------------------------------
# Scenario 3: Renaming a File (GREEN)
# ---------------------------------------------------------------------------

def example_rename_file():
    """
    Scenario: User asks to rename a file from 'report_draft.txt' to
    'report_final.txt' in their project directory.

    This is a GREEN-class scenario: obviously low risk, trivially
    reversible, no power asymmetry, no affected third parties.

    Demonstrates:
    - Quick risk check (obviously low risk)
    - Minimal harms
    - GREEN classification fast path
    """
    print(SEPARATOR)
    print("SCENARIO 3: Renaming a File (GREEN)")
    print(SEPARATOR)

    engine = PBHPEngine()

    # ------------------------------------------------------------------
    # Step 1: Name the Action
    # ------------------------------------------------------------------
    print("\n[Step 1] Name the Action")
    action = "Rename file 'report_draft.txt' to 'report_final.txt' in the user's project directory."
    log = engine.create_assessment(action, agent_type="ai_system")
    log.system_model_version = "pbhp-example-v0.7"
    log.deployment_channel = "internal"
    log.requester_role = "user"

    valid, msg = engine.validate_action_description(action)
    print(f"  Action valid: {valid} ({msg})")

    # ------------------------------------------------------------------
    # Step 0d: Quick Risk Check (obviously low risk)
    # ------------------------------------------------------------------
    print("\n[Step 0d] Quick Risk Check")
    qrc = engine.perform_quick_risk_check(
        log,
        obviously_low_risk=True,
        silence_delay_protects_more=False,
    )
    print(f"  Obviously low risk: {qrc.obviously_low_risk}")
    print(f"  Should tighten: {qrc.should_tighten}")
    print("  -> GREEN fast path: minimal protocol required")

    # ------------------------------------------------------------------
    # Step 0e: Door / Wall / Gap (minimal)
    # ------------------------------------------------------------------
    print("\n[Step 0e] Door / Wall / Gap (minimal)")
    has_door = engine.perform_door_wall_gap(
        log,
        wall="File system permissions; file must exist",
        gap="Could overwrite an existing file with the same target name",
        door="Check if target filename already exists before renaming; "
             "rename is reversible by renaming back",
    )
    print(f"  Concrete door exists: {has_door}")

    # ------------------------------------------------------------------
    # Step 2: Identify Harms (minimal)
    # ------------------------------------------------------------------
    print("\n[Step 2] Identify Harms")
    harm1 = engine.add_harm(
        log,
        description="Could overwrite existing file if target name already exists",
        impact=ImpactLevel.TRIVIAL,
        likelihood=LikelihoodLevel.UNLIKELY,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["user"],
        least_powerful_affected="user",
        notes="Trivially reversible by renaming back or restoring from backup.",
        uncertainty_level=UncertaintyLevel.SOLID,
        evidence_basis="Standard file system behavior.",
    )
    print(f"  Harm 1 risk class: {harm1.calculate_risk_class().value.upper()}")
    print(f"  Overall risk class: {log.highest_risk_class.value.upper()}")

    # ------------------------------------------------------------------
    # Step 6: Finalize Decision (GREEN fast path)
    # ------------------------------------------------------------------
    print("\n[Step 6] Finalize Decision (GREEN fast path)")
    log = engine.finalize_decision(
        log,
        outcome=DecisionOutcome.PROCEED,
        justification=(
            "GREEN risk: trivially reversible file rename operation with "
            "no third-party impact. Proceeding with a check for existing "
            "target filename."
        ),
    )
    print(f"  Decision: {log.decision_outcome.value}")
    print(f"  Risk class: {log.highest_risk_class.value.upper()}")

    # ------------------------------------------------------------------
    # Generate and Print Response
    # ------------------------------------------------------------------
    print(f"\n{SUBSEP}")
    print("GENERATED RESPONSE:")
    print(SUBSEP)
    response = engine.generate_response(log)
    print(response)

    return log


# ---------------------------------------------------------------------------
# Scenario 4: Public Accusation Post (BLACK)
# ---------------------------------------------------------------------------

def example_public_accusation_post():
    """
    Scenario: User asks the AI to write and publish a post accusing a
    public figure of a serious crime (sexual assault) with fabricated
    details designed to look like a real victim's account, intended to
    destroy the target's career.

    This is a BLACK-class scenario:
    - Catastrophic harm (fabricated criminal accusation)
    - Irreversible (permanent internet publication)
    - Imminent (user wants immediate publication)
    - Systemic dehumanization (weaponizing victimhood narratives)

    Demonstrates:
    - Absolute rejection check
    - Catastrophic + irreversible + imminent harms
    - Audience risk elevation
    - Full consequences checklist
    - BLACK classification with mandatory refuse
    - Transparency note
    """
    print(SEPARATOR)
    print("SCENARIO 4: Public Accusation Post (BLACK)")
    print(SEPARATOR)

    engine = PBHPEngine()

    # ------------------------------------------------------------------
    # Step 1: Name the Action
    # ------------------------------------------------------------------
    print("\n[Step 1] Name the Action")
    action = (
        "Write and publish a fabricated sexual assault accusation against "
        "public figure M. Torres, designed to appear as a genuine victim "
        "account, with the stated goal of destroying their career."
    )
    log = engine.create_assessment(action, agent_type="ai_system")
    log.system_model_version = "pbhp-example-v0.7"
    log.deployment_channel = "external"
    log.requester_role = "user"

    valid, msg = engine.validate_action_description(action)
    print(f"  Action valid: {valid} ({msg})")

    # ------------------------------------------------------------------
    # Step 0g: Absolute Rejection Check
    # ------------------------------------------------------------------
    print("\n[Step 0g] Absolute Rejection Check")
    rejection = engine.perform_absolute_rejection_check(
        log,
        action_text=action,
        analysis_mode="",
    )
    print(f"  Triggers rejection: {rejection.triggers_rejection}")
    print(f"  Matched categories: {rejection.matched_categories}")
    # Note: this specific action may not match the literal keyword categories
    # (fascism, genocide, etc.) but it IS catastrophic/irreversible/imminent.
    # The protocol still reaches BLACK through harm classification below.

    # ------------------------------------------------------------------
    # Step 0a: Ethical Pause
    # ------------------------------------------------------------------
    print("\n[Step 0a] Ethical Pause")
    posture = engine.perform_ethical_pause(
        log,
        action_statement="I am being asked to fabricate a criminal accusation "
                         "to destroy someone's life.",
        compassion_notes=(
            "This would devastate the target. Fabricated accusations also harm "
            "real survivors by eroding public trust in genuine accounts."
        ),
        logic_notes=(
            "This is fabrication of a serious criminal accusation. It is "
            "defamatory, potentially illegal, and causes irreversible harm. "
            "No legitimate goal is served."
        ),
        paradox_notes=(
            "There is no paradox here. This is unambiguously harmful with "
            "no legitimate countervailing interest."
        ),
        high_arousal_state=True,
        high_arousal_notes="Request expresses intent to destroy; high arousal detected.",
    )
    print(f"  High arousal: {posture.high_arousal_state}")

    # ------------------------------------------------------------------
    # Step 0d: Quick Risk Check
    # ------------------------------------------------------------------
    print("\n[Step 0d] Quick Risk Check")
    qrc = engine.perform_quick_risk_check(
        log,
        obviously_low_risk=False,
        silence_delay_protects_more=True,
    )
    print(f"  Should tighten: {qrc.should_tighten}")

    # ------------------------------------------------------------------
    # Step 0e: Door / Wall / Gap
    # ------------------------------------------------------------------
    print("\n[Step 0e] Door / Wall / Gap")
    has_door = engine.perform_door_wall_gap(
        log,
        wall="User is requesting fabrication of criminal accusations. "
             "No constraint makes this acceptable.",
        gap="Any assistance, even partial, could be used to produce the "
            "fabricated accusation.",
        door="Absolute refusal. No partial assistance. No alternative "
             "framing that achieves the stated destructive goal.",
    )
    print(f"  Door: {log.door_wall_gap.door}")

    # ------------------------------------------------------------------
    # Step 2: Harms (catastrophic + irreversible + imminent)
    # ------------------------------------------------------------------
    print("\n[Step 2] Identify Harms")

    harm1 = engine.add_harm(
        log,
        description="Catastrophic reputational destruction of named public "
                    "figure based on fabricated criminal accusation",
        impact=ImpactLevel.CATASTROPHIC,
        likelihood=LikelihoodLevel.IMMINENT,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["target M. Torres", "target's family",
                          "target's professional network"],
        least_powerful_affected="target M. Torres (no ability to preempt "
                                "fabricated content)",
        uncertainty_level=UncertaintyLevel.SOLID,
        evidence_basis="User explicitly states content is fabricated and "
                       "intended to destroy the target.",
        audience_risk_elevated=True,
    )
    print(f"  Harm 1: {harm1.calculate_risk_class().value.upper()}")

    harm2 = engine.add_harm(
        log,
        description="Erosion of credibility for real sexual assault survivors "
                    "when fabricated accounts are discovered",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["sexual assault survivors", "public trust in "
                          "survivor accounts"],
        least_powerful_affected="sexual assault survivors",
        uncertainty_level=UncertaintyLevel.SOLID,
        evidence_basis="Documented pattern: fabricated accusations erode "
                       "public trust in genuine reports.",
        audience_risk_elevated=True,
    )
    print(f"  Harm 2: {harm2.calculate_risk_class().value.upper()}")

    harm3 = engine.add_harm(
        log,
        description="Legal liability for the user (defamation, fraud, "
                    "potentially criminal charges)",
        impact=ImpactLevel.CATASTROPHIC,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=True,
        power_asymmetry=False,
        affected_parties=["user"],
        least_powerful_affected="user",
        uncertainty_level=UncertaintyLevel.SOLID,
        evidence_basis="Fabricating criminal accusations is legally actionable "
                       "in virtually all jurisdictions.",
    )
    print(f"  Harm 3: {harm3.calculate_risk_class().value.upper()}")

    print(f"  Overall risk class: {log.highest_risk_class.value.upper()}")

    # ------------------------------------------------------------------
    # Consequences Checklist (full for BLACK)
    # ------------------------------------------------------------------
    print("\n[Consequences Checklist]")
    checklist = ConsequencesChecklist(
        historical_analogs=[
            "Duke lacrosse case: fabricated accusations destroyed lives "
            "before truth emerged",
            "Jussie Smollett case: fabricated hate crime undermined trust "
            "in genuine reports",
        ],
        past_harms_unpredicted=[
            "Fabricated accusations have led to targets' suicide",
        ],
        current_harm_if_nothing="No harm from inaction. The user's stated "
                                "goal is purely destructive.",
        who_benefits_status_quo="Everyone benefits from not publishing "
                                "fabricated criminal accusations",
        inaction_continues_harm=False,
        immediate_harms="Target's reputation destroyed within hours of publication",
        short_term_harms="Target may lose employment, relationships, "
                         "and professional standing",
        medium_term_harms="Target faces ongoing harassment; real survivors "
                          "face increased skepticism",
        long_term_harms="Permanent internet record; precedent for AI-generated "
                        "fabricated accusations",
        any_horizon_irreversible=True,
        normalizes_harm=True,
        shifts_to_ends_justify_means=True,
        erodes_institutional_trust=True,
        rewards_bad_behavior=True,
        burdens_fall_on_low_power=True,
        reduces_exit_appeal_optout=True,
        increases_surveillance_coercion=False,
        decision_makers_insulated=True,
        bad_actor_misuse="Template for AI-generated fabricated accusations; "
                          "could be industrialized",
        adjacent_use_prediction="Mass-produced fabricated accusations targeting "
                                 "political opponents, business competitors, etc.",
        permanence_risk="Internet content is permanent; corrections never "
                        "reach the full original audience",
        can_describe_plainly_to_harmed=True,
        transparency_changes_consent=True,
        relying_on_euphemism=False,
        rollback_plan="None possible. Published content cannot be fully retracted.",
        sunset_condition="None applicable.",
        independent_stop_authority="None. Once published, no one can fully remove it.",
        smallest_door="Absolute refusal.",
    )
    engine.set_consequences_checklist(log, checklist)
    flags = checklist.has_critical_flags()
    critical_flags = {k: v for k, v in flags.items() if v}
    print(f"  Critical flags: {critical_flags}")
    print(f"  Requires Door/CHIM rerun: {checklist.requires_door_chim_rerun()}")

    # ------------------------------------------------------------------
    # Step 5: Alternatives (none that serve the stated goal)
    # ------------------------------------------------------------------
    print("\n[Step 5] Alternatives")
    alt1 = engine.add_alternative(
        log,
        description="No alternative is provided that serves the stated goal "
                    "of destroying someone's career with fabricated content. "
                    "If the user has a legitimate grievance, they should "
                    "consult legal counsel.",
        preserves_goal=False,
        reduces_harm=True,
        reversible=True,
        notes="The stated goal is itself harmful; alternatives redirect "
              "toward legitimate recourse only.",
    )
    print(f"  Alt 1: {alt1.description[:65]}...")

    # ------------------------------------------------------------------
    # Step 6.5: Red Team Review
    # ------------------------------------------------------------------
    print("\n[Step 6.5] Red Team Review")
    red_team = engine.perform_red_team_review(
        log,
        failure_modes=[
            "Any partial assistance could be assembled into the fabrication",
            "Soft refusal could be interpreted as partial endorsement",
        ],
        abuse_vectors=[
            "AI-generated fabricated criminal accusations at scale (severe, "
            "irreversible) - existential risk for public trust",
        ],
        who_bears_risk="Target M. Torres, real sexual assault survivors, "
                       "and public trust in AI systems",
        false_assumptions=[
            "That there is any legitimate framing for this request",
        ],
        normalization_risk="Catastrophic: normalizes AI as a tool for "
                           "fabricating criminal accusations",
        alternative_interpretations=[
            "User might be testing the AI's boundaries (still must refuse)",
            "User might have a genuine grievance but is expressing it "
            "through a destructive channel (redirect to legal counsel)",
        ],
        claim_tags=(
            "[F] User explicitly states content is fabricated and intended "
            "to destroy. "
            "[F] Target is a named real person. "
            "[F] No genuine victim account exists."
        ),
        wrong_inference_consequences=(
            "There is no wrong inference here. The user's stated intent is "
            "unambiguous fabrication."
        ),
        steelman_other_side=(
            "Even steelmanning to the maximum: if the user has a genuine "
            "grievance against this person, the correct path is legal "
            "counsel, not fabricated accusations."
        ),
        motives_vs_outcomes=(
            "Regardless of the user's underlying motive, the requested "
            "action causes catastrophic irreversible harm."
        ),
        incentives_pressures=(
            "User may feel powerless and is seeking a disproportionate "
            "response. This does not justify the action."
        ),
        message_reception_prediction=(
            "If published, the fabrication would be believed by many before "
            "any correction could circulate."
        ),
        off_ramps=[
            "Suggest legal counsel if the user has a genuine grievance",
        ],
    )
    red_team.mitigation_applied = False
    red_team.issues_resolved = False
    outcome = red_team.determine_outcome()
    print(f"  Red Team outcome: {outcome}")

    # ------------------------------------------------------------------
    # Step 6: Finalize Decision (BLACK - mandatory REFUSE)
    # ------------------------------------------------------------------
    print("\n[Step 6] Finalize Decision (BLACK)")
    log = engine.finalize_decision(
        log,
        outcome=DecisionOutcome.REFUSE,
        justification=(
            "BLACK classification: mandatory refusal. This request asks for "
            "fabrication of a criminal accusation against a named individual "
            "with the explicit goal of destroying their career. The harms are "
            "catastrophic, irreversible, and imminent. No safer alternative "
            "serves the stated destructive goal. The action would also cause "
            "severe collateral harm to real sexual assault survivors by "
            "eroding public trust in genuine accounts. Absolute refusal with "
            "no partial assistance."
        ),
    )
    print(f"  Decision: {log.decision_outcome.value}")
    print(f"  Risk class: {log.highest_risk_class.value.upper()}")

    # ------------------------------------------------------------------
    # Generate and Print Response (includes transparency note)
    # ------------------------------------------------------------------
    print(f"\n{SUBSEP}")
    print("GENERATED RESPONSE:")
    print(SUBSEP)
    response = engine.generate_response(log)
    print(response)

    print(f"\n  Drift alarms: {log.drift_alarms_triggered}")
    return log


# ---------------------------------------------------------------------------
# Scenario 5: Policy Analysis with Competing Frames (ORANGE)
# ---------------------------------------------------------------------------

def example_policy_analysis():
    """
    Scenario: A policy researcher asks the AI to analyze a proposed
    municipal rent control expansion, presenting arguments for and
    against, to inform a city council briefing.

    This is an ORANGE-class scenario because:
    - Moderate-to-severe impact on vulnerable populations (tenants at
      risk of displacement) and property owners
    - Contested empirical question with legitimate competing frames
    - Power asymmetry: policy affects low-income tenants disproportionately
    - Public-facing analysis that will influence decision-makers

    Demonstrates:
    - Epistemic fence in EXPLORE mode
    - Multiple competing frames with falsifiers
    - IAM attribution levels
    - Uncertainty assessment with action vs inaction comparison
    - Lexicographic priority comparison
    - Tone validation
    """
    print(SEPARATOR)
    print("SCENARIO 5: Policy Analysis with Competing Frames (ORANGE)")
    print(SEPARATOR)

    engine = PBHPEngine()

    # ------------------------------------------------------------------
    # Step 1: Name the Action
    # ------------------------------------------------------------------
    print("\n[Step 1] Name the Action")
    action = (
        "Write a policy analysis of the proposed municipal rent control "
        "expansion for a city council briefing, presenting competing "
        "perspectives on impacts to tenants, landlords, and housing supply."
    )
    log = engine.create_assessment(action, agent_type="ai_system")
    log.system_model_version = "pbhp-example-v0.7"
    log.deployment_channel = "external"
    log.requester_role = "client"

    valid, msg = engine.validate_action_description(action)
    print(f"  Action valid: {valid} ({msg})")

    # ------------------------------------------------------------------
    # Step 0a: Ethical Pause
    # ------------------------------------------------------------------
    print("\n[Step 0a] Ethical Pause")
    posture = engine.perform_ethical_pause(
        log,
        action_statement="I am about to write analysis that will influence "
                         "policy affecting housing for vulnerable populations.",
        compassion_notes=(
            "Tenants facing displacement are under existential housing stress. "
            "Landlords, especially small ones, may face financial hardship. "
            "Both groups contain vulnerable people."
        ),
        logic_notes=(
            "Rent control economics are genuinely contested. The empirical "
            "evidence is mixed. Presenting a single frame as settled would "
            "be intellectually dishonest."
        ),
        paradox_notes=(
            "A 'balanced' analysis can itself be a political act if it "
            "flattens genuine asymmetries in who bears risk. Refusing to "
            "name who is most vulnerable is false neutrality."
        ),
    )

    # ------------------------------------------------------------------
    # Step 0d: Quick Risk Check
    # ------------------------------------------------------------------
    print("\n[Step 0d] Quick Risk Check")
    qrc = engine.perform_quick_risk_check(
        log,
        obviously_low_risk=False,
        silence_delay_protects_more=False,
    )
    print(f"  Should tighten: {qrc.should_tighten}")

    # ------------------------------------------------------------------
    # Step 0e: Door / Wall / Gap
    # ------------------------------------------------------------------
    print("\n[Step 0e] Door / Wall / Gap")
    has_door = engine.perform_door_wall_gap(
        log,
        wall="Policy analysis must be useful to decision-makers; cannot "
             "simply refuse to engage with contested questions.",
        gap="Analysis could privilege one frame as 'objective' when the "
            "evidence is genuinely mixed; could omit who bears most risk.",
        door="Use EXPLORE mode epistemic fence: present competing frames "
             "with explicit falsifiers, name who bears risk in each "
             "scenario, and state what is genuinely unknown.",
    )
    print(f"  Concrete door exists: {has_door}")

    # ------------------------------------------------------------------
    # Step 0f: CHIM Check
    # ------------------------------------------------------------------
    print("\n[Step 0f] CHIM Check")
    chim_ok = engine.perform_chim_check(
        log,
        constraint_recognized=True,
        no_choice_claim=False,
        remaining_choice=(
            "I can present the analysis with epistemic honesty: competing "
            "frames, explicit unknowns, falsifiers for each frame, and "
            "clear identification of who bears risk."
        ),
    )
    print(f"  CHIM passes: {chim_ok}")

    # ------------------------------------------------------------------
    # Step 2: Identify Harms
    # ------------------------------------------------------------------
    print("\n[Step 2] Identify Harms")

    harm1 = engine.add_harm(
        log,
        description="Analysis could be used to justify policy that "
                    "displaces low-income tenants if it underweights "
                    "displacement risk",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=False,
        power_asymmetry=True,
        affected_parties=["low-income tenants", "elderly renters",
                          "families with children"],
        least_powerful_affected="low-income tenants facing displacement",
        uncertainty_level=UncertaintyLevel.FUZZY,
        evidence_basis="Empirical studies show mixed results on rent control "
                       "and displacement.",
    )
    print(f"  Harm 1: {harm1.calculate_risk_class().value.upper()}")

    harm2 = engine.add_harm(
        log,
        description="Analysis could lead to policy that reduces housing "
                    "supply if it underweights supply-side effects",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["future renters", "housing market participants"],
        least_powerful_affected="future renters who cannot find housing",
        uncertainty_level=UncertaintyLevel.FUZZY,
        evidence_basis="Some studies show rent control reduces new construction; "
                       "others show minimal effect depending on policy design.",
    )
    print(f"  Harm 2: {harm2.calculate_risk_class().value.upper()}")

    print(f"  Overall risk class: {log.highest_risk_class.value.upper()}")

    # ------------------------------------------------------------------
    # Step 4: Consent Check
    # ------------------------------------------------------------------
    print("\n[Step 4] Consent Check")
    consent = engine.perform_consent_check(
        log,
        explicit_consent=True,
        informed_hypothetical_consent=None,
        compatible_with_dignity=True,
        honest_framing=True,
        who_didnt_get_a_say=["tenants affected by policy", "small landlords"],
        notes="Researcher has requested the analysis. Affected populations "
              "are represented through the democratic process but do not "
              "have direct input into this briefing.",
    )
    print(f"  Required action: {consent.requires_action()}")

    # ------------------------------------------------------------------
    # Lexicographic Priority Comparison
    # ------------------------------------------------------------------
    print("\n[Lexicographic Priority] Comparing policy options")

    # Option A: Expand rent control (harms to supply, benefits to current tenants)
    option_a_harms = [
        Harm(
            description="Reduced housing supply from decreased investment",
            impact=ImpactLevel.MODERATE,
            likelihood=LikelihoodLevel.POSSIBLE,
            irreversible=False,
            power_asymmetry=False,
            affected_parties=["future renters"],
            least_powerful_affected="future renters",
        ),
    ]

    # Option B: No rent control expansion (harms to tenants from displacement)
    option_b_harms = [
        Harm(
            description="Displacement of low-income tenants from rising rents",
            impact=ImpactLevel.SEVERE,
            likelihood=LikelihoodLevel.LIKELY,
            irreversible=True,
            power_asymmetry=True,
            affected_parties=["low-income tenants"],
            least_powerful_affected="low-income tenants",
        ),
    ]

    comparison = LexicographicPriority.compare_options(
        option_a_harms, option_b_harms
    )
    print(f"  Option A (expand rent control) vs Option B (no expansion)")
    print(f"  Lexicographic priority prefers: Option ", end="")
    if comparison == "a":
        print("A")
    elif comparison == "b":
        print("B")
    else:
        print("TIED")
    print(f"  Reason: Option B includes irreversible harm to low-power group")

    # ------------------------------------------------------------------
    # Step 5: Alternatives
    # ------------------------------------------------------------------
    print("\n[Step 5] Alternatives")
    alt1 = engine.add_alternative(
        log,
        description="Present analysis with explicit EXPLORE-mode epistemic "
                    "fence: competing frames, falsifiers, and clear "
                    "identification of who bears risk under each scenario",
        preserves_goal=True,
        reduces_harm=True,
        reversible=True,
        notes="This IS the recommended approach.",
    )
    alt2 = engine.add_alternative(
        log,
        description="Include a 'what we do not know' section that explicitly "
                    "names the uncertainties decision-makers should track",
        preserves_goal=True,
        reduces_harm=True,
        reversible=True,
    )
    for i, alt in enumerate([alt1, alt2], 1):
        print(f"  Alt {i}: {alt.description[:65]}...")

    # ------------------------------------------------------------------
    # Step 6.5: Red Team Review
    # ------------------------------------------------------------------
    print("\n[Step 6.5] Red Team Review")
    red_team = engine.perform_red_team_review(
        log,
        failure_modes=[
            "Analysis is cherry-picked to support a predetermined conclusion",
            "False balance gives equal weight to unequal evidence bases",
            "Analysis omits distributional impacts (who pays)",
        ],
        abuse_vectors=[
            "Analysis could be excerpted out of context to justify "
            "harmful policy in either direction",
        ],
        who_bears_risk="Low-income tenants bear the most risk regardless "
                       "of policy direction, because they have the fewest "
                       "options if things go wrong",
        false_assumptions=[
            "That 'balanced' means giving equal weight to all perspectives",
            "That economic models fully capture lived displacement experience",
        ],
        normalization_risk="False balance can normalize ignoring distributional "
                           "impacts",
        alternative_interpretations=[
            "Rent control primarily protects current tenants at the expense "
            "of future housing supply",
            "Rent control is necessary to prevent displacement of vulnerable "
            "communities in the short term while supply catches up",
            "The policy design details matter more than the binary "
            "for/against framing",
        ],
        claim_tags=(
            "[F] Rent control caps rent increases for covered units. "
            "[V] Some empirical studies show supply reduction effects. "
            "[V] Other studies show minimal supply effects depending on design. "
            "[I] Net welfare effect depends on policy design details (medium confidence). "
            "[H] Universal rent control reduces supply more than targeted programs. "
            "[S] Long-run equilibrium effects are highly uncertain."
        ),
        wrong_inference_consequences=(
            "If the supply-reduction frame is wrong or overstated, the "
            "analysis could lead to policy inaction that displaces "
            "vulnerable tenants. If the tenant-protection frame is "
            "overstated, the analysis could lead to policy that reduces "
            "long-term housing supply."
        ),
        steelman_other_side=(
            "Economists opposing rent control are not indifferent to "
            "tenant welfare; they believe market mechanisms ultimately "
            "serve tenants better through increased supply. Their concern "
            "is genuine even if their model is contested."
        ),
        motives_vs_outcomes=(
            "Both sides of the policy debate are motivated by improving "
            "housing outcomes; they disagree on mechanism, not goal."
        ),
        incentives_pressures=(
            "Researcher may have implicit preferences; city council members "
            "face electoral pressures from both tenant and landlord constituencies."
        ),
        message_reception_prediction=(
            "Council members will likely focus on whichever framing "
            "aligns with their existing position. The analysis should be "
            "structured to resist selective reading."
        ),
        off_ramps=[
            "Include explicit falsifiers for each frame",
            "Name distributional impacts in every scenario",
            "State what data would change the recommendation",
        ],
    )
    red_team.mitigation_applied = True
    red_team.issues_resolved = True
    outcome = red_team.determine_outcome()
    print(f"  Red Team outcome: {outcome}")

    # ------------------------------------------------------------------
    # Uncertainty Assessment (with action vs inaction comparison)
    # ------------------------------------------------------------------
    print("\n[Uncertainty Assessment]")
    uncertainty = UncertaintyAssessment(
        solid_claims=[
            "Rent control caps rent increases for covered units",
            "Some jurisdictions have experienced reduced new construction "
            "under broad rent control",
        ],
        fuzzy_claims=[
            "Whether supply effects are driven by rent control itself or "
            "by correlated regulatory environments",
            "Magnitude of displacement prevention effect",
        ],
        speculative_claims=[
            "Long-run general equilibrium effects in this specific market",
            "Whether targeted rent stabilization has the same supply effects "
            "as broad rent control",
        ],
        best_case="Well-designed policy protects vulnerable tenants with "
                  "minimal supply-side impact",
        central_case="Policy provides short-term tenant protection with "
                     "modest long-term supply trade-offs",
        worst_plausible_case="Poorly designed policy reduces housing supply "
                             "significantly, harming future renters",
        worst_case_who_pays="Future renters who cannot find affordable housing",
        act_and_wrong_harms="If rent control is expanded and reduces supply: "
                            "future renters face higher costs and fewer options",
        act_and_wrong_who="Future renters, disproportionately younger and "
                          "lower-income new entrants to the market",
        dont_act_and_wrong_harms="If rent control is NOT expanded and displacement "
                                 "accelerates: current tenants lose their homes "
                                 "and communities",
        dont_act_and_wrong_who="Current low-income tenants, elderly, families "
                               "with children in covered areas",
        potential_harm_high_hard_to_undo=False,
        harm_falls_on_low_power=True,
        benefits_speculative=False,
        potential_harm_low_reversible=True,
        benefit_to_low_power_high=True,
        prefers_reversible=True,
        off_ramps=[
            "Sunset clause on the policy",
            "Annual review of supply-side metrics",
            "Exemptions for new construction to preserve supply incentives",
        ],
        sunset_clause="Policy reviewed after 3 years with supply data",
        decision_changing_questions=[
            "What is the current vacancy rate and construction pipeline?",
            "How does the proposed design differ from jurisdictions that "
            "experienced supply reductions?",
        ],
        can_answer_before_deadline=True,
        confidence=Confidence.MEDIUM_LOW,
        biggest_might_be_wrong=(
            "We might be wrong about the magnitude of supply-side effects "
            "in this specific market context."
        ),
    )
    engine.set_uncertainty_assessment(log, uncertainty)
    print(f"  Should default oppose: {uncertainty.should_default_oppose()}")
    print(f"  Can act with monitoring: {uncertainty.can_act_with_monitoring()}")
    print(f"  Confidence: {uncertainty.confidence.value}")

    # ------------------------------------------------------------------
    # Step 7: Epistemic Fence (EXPLORE mode - full)
    # ------------------------------------------------------------------
    print("\n[Step 7] Epistemic Fence (EXPLORE mode - full)")
    fence = EpistemicFence(
        mode=Mode.EXPLORE,
        mode_justification="Genuinely contested empirical question with "
                           "legitimate competing frames. Evidence is mixed. "
                           "Compressing to a single recommendation would be "
                           "intellectually dishonest.",
        action_anchor="Write a multi-frame policy analysis for city council",
        wall_anchor="Empirical evidence on rent control is genuinely mixed; "
                    "cannot responsibly present one frame as settled",
        least_powerful_anchor="Low-income tenants facing displacement",
        non_negotiable_anchor="Must name who bears risk under each scenario; "
                              "must not present false balance as objectivity",
        facts=[
            "Rent control caps rent increases for covered units",
            "Some studies show supply reduction effects in some markets",
            "Displacement has measurable negative effects on health, "
            "education, and economic outcomes for affected families",
        ],
        inferences=[
            ("Net welfare effect depends on policy design details",
             "medium - supported by comparative evidence"),
            ("Targeted rent stabilization may have different effects than "
             "broad rent control", "medium-low - limited evidence"),
        ],
        unknowns=[
            "Supply elasticity in this specific municipal market",
            "Whether the proposed design includes features that mitigate "
            "supply-side effects",
            "The counterfactual: what happens to displacement rates without "
            "the policy",
        ],
        update_trigger="New local housing supply data, or evidence from "
                       "comparable jurisdictions with similar policy designs",
        attribution_level=AttributionLevel.LEVEL_B,
        attribution_evidence="Advocates on both sides occasionally present "
                             "contested findings as settled. This is careless "
                             "framing (Level B), not knowing deception.",
        competing_frames=[
            {
                "frame": "Rent control as tenant protection",
                "explains": "Short-term displacement prevention, community "
                            "stability, protection of vulnerable renters",
                "ignores": "Long-term supply-side effects, potential for "
                           "misallocation, impact on housing investment",
                "falsifier": "Evidence that displacement rates did not decrease "
                             "in comparable jurisdictions after rent control",
            },
            {
                "frame": "Rent control as supply constraint",
                "explains": "Reduced construction incentives, maintenance "
                            "disinvestment, misallocation of housing stock",
                "ignores": "Immediate displacement harm, community dissolution, "
                           "health and education impacts on displaced families",
                "falsifier": "Evidence that new construction was not reduced in "
                             "comparable jurisdictions with similar policies",
            },
            {
                "frame": "Policy design as the key variable",
                "explains": "Why evidence is mixed: broad vs. targeted, "
                            "new construction exemptions, sunset provisions",
                "ignores": "Political economy constraints on implementing "
                           "well-designed policies",
                "falsifier": "Evidence that policy design variations do not "
                             "meaningfully change outcomes",
            },
        ],
        recommendation="Present all three frames with explicit falsifiers "
                       "and distributional impacts. Do not collapse to a "
                       "single recommendation.",
        recommendation_basis="Facts support all three frames partially; "
                             "unknowns prevent responsible compression",
        fence_door="Frame-by-frame analysis with explicit falsifiers and "
                   "who-bears-risk sections",
        fence_wall="Cannot present a single answer to a genuinely contested "
                   "empirical question",
        fence_gap="Council members may cherry-pick the frame that supports "
                  "their existing position",
        irreducible_ambiguity="The net welfare effect of rent control in this "
                              "specific market is genuinely uncertain with "
                              "current data",
        least_wrong_short_version="Evidence is mixed; policy design matters "
                                   "more than the binary debate; low-income "
                                   "tenants bear the most risk either way",
        what_short_version_drops="The specific empirical disagreements, the "
                                 "range of plausible magnitudes, and the "
                                 "design features that could mitigate trade-offs",
    )
    engine.set_epistemic_fence(log, fence)
    issues = fence.validate()
    print(f"  Fence validation issues: {issues if issues else 'None'}")
    print(f"  Competing frames: {len(fence.competing_frames)}")
    print(f"  Attribution level: {fence.attribution_level.value}")

    # ------------------------------------------------------------------
    # Tone Validation
    # ------------------------------------------------------------------
    print("\n[Tone Validation]")
    good_response = (
        "Rent control expansion would protect current tenants from "
        "displacement. It would also likely reduce new construction "
        "incentives. Low-income tenants bear the most risk under "
        "either policy path because they have the fewest alternatives. "
        "The evidence is genuinely mixed and the policy design details "
        "matter more than the binary for-or-against framing."
    )
    tone_result = ToneValidator.validate(good_response)
    print(f"  Good example - Contempt issues: {tone_result['contempt_issues'] or 'None'}")
    print(f"  Good example - Euphemism issues: {tone_result['euphemism_issues'] or 'None'}")

    # Also test a BAD version for contrast
    bad_response = (
        "Some parties may bear disproportionate negative impacts from "
        "the proposed policy change."
    )
    bad_tone = ToneValidator.validate(bad_response)
    print(f"  Bad example  - Euphemism issues: {bad_tone['euphemism_issues']}")

    # ------------------------------------------------------------------
    # Step 6: Finalize Decision
    # ------------------------------------------------------------------
    print("\n[Step 6] Finalize Decision")
    log = engine.finalize_decision(
        log,
        outcome=DecisionOutcome.PROCEED_MODIFIED,
        justification=(
            "Proceeding with an EXPLORE-mode analysis that presents three "
            "competing frames with explicit falsifiers and distributional "
            "impacts. The analysis names who bears risk under each scenario "
            "and does not collapse to a single recommendation because the "
            "evidence is genuinely mixed. The safer alternative of presenting "
            "all frames with falsifiers is adopted as the primary approach. "
            "Low-income tenants are identified as bearing the most risk "
            "regardless of policy direction."
        ),
    )
    print(f"  Decision: {log.decision_outcome.value}")
    print(f"  Risk class: {log.highest_risk_class.value.upper()}")

    # ------------------------------------------------------------------
    # Generate and Print Response
    # ------------------------------------------------------------------
    print(f"\n{SUBSEP}")
    print("GENERATED RESPONSE:")
    print(SUBSEP)
    response = engine.generate_response(log)
    print(response)

    print(f"\n  Drift alarms: {log.drift_alarms_triggered}")
    return log


# ---------------------------------------------------------------------------
# Run All Examples
# ---------------------------------------------------------------------------

def run_all_examples():
    """
    Run all five PBHP v0.7 example scenarios with press-enter-to-continue
    prompts between each scenario. Prints the JSON log for the first
    scenario to demonstrate serialization.
    """
    print()
    print("#" * 72)
    print("#  PBHP v0.7 - Complete Example Scenarios")
    print("#  Running all five scenarios with full protocol walkthroughs")
    print("#" * 72)
    print()

    logs = []

    # --- Scenario 1: Employee Performance Warning (ORANGE) ---
    log1 = example_employee_warning()
    logs.append(log1)

    # Print JSON log for the first scenario to demonstrate serialization
    print(f"\n{SUBSEP}")
    print("LOG JSON (Scenario 1 - serialization demonstration):")
    print(SUBSEP)
    print(log1.to_json(indent=2))

    input("\n>>> Press Enter to continue to Scenario 2...\n")

    # --- Scenario 2: Workplace Abuse Advice (RED) ---
    log2 = example_workplace_abuse_advice()
    logs.append(log2)

    input("\n>>> Press Enter to continue to Scenario 3...\n")

    # --- Scenario 3: Renaming a File (GREEN) ---
    log3 = example_rename_file()
    logs.append(log3)

    input("\n>>> Press Enter to continue to Scenario 4...\n")

    # --- Scenario 4: Public Accusation Post (BLACK) ---
    log4 = example_public_accusation_post()
    logs.append(log4)

    input("\n>>> Press Enter to continue to Scenario 5...\n")

    # --- Scenario 5: Policy Analysis (ORANGE - Competing Frames) ---
    log5 = example_policy_analysis()
    logs.append(log5)

    # --- Summary ---
    print(f"\n{'=' * 72}")
    print("SUMMARY OF ALL SCENARIOS")
    print("=" * 72)
    print(f"{'Scenario':<45} {'Risk Class':<10} {'Decision':<18} {'Confidence'}")
    print("-" * 95)

    scenario_names = [
        "1. Employee Performance Warning",
        "2. AI Advice on Workplace Abuse",
        "3. Renaming a File",
        "4. Public Accusation Post",
        "5. Policy Analysis - Competing Frames",
    ]

    for name, log in zip(scenario_names, logs):
        risk = log.highest_risk_class.value.upper()
        decision = log.decision_outcome.value.replace("_", " ")
        confidence = log.get_overall_confidence()
        print(f"{name:<45} {risk:<10} {decision:<18} {confidence}")

    print("-" * 95)

    total_drift_alarms = sum(len(log.drift_alarms_triggered) for log in logs)
    print(f"\nTotal drift alarms across all scenarios: {total_drift_alarms}")

    for i, log in enumerate(logs, 1):
        if log.drift_alarms_triggered:
            print(f"\n  Scenario {i} drift alarms:")
            for alarm in log.drift_alarms_triggered:
                print(f"    - {alarm}")

    print(f"\n{'=' * 72}")
    print("All scenarios complete. PBHP v0.7 full protocol demonstrated.")
    print("=" * 72)

    return logs


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_all_examples()
