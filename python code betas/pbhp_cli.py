#!/usr/bin/env python3
"""
Pause-Before-Harm Protocol (PBHP) - Interactive CLI
Version: 0.7 (Full Specification)

An interactive command-line interface for conducting PBHP v0.7 assessments,
including all foundation gates, seven protocol steps, epistemic fencing,
red team review, drift detection, tone validation, and structured logging.

Usage:
    python pbhp_cli.py              Launch interactive menu
    python pbhp_cli.py --help       Show help information

No external dependencies required.

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

import sys
import os
import json
from datetime import datetime
from typing import List, Optional

# ---------------------------------------------------------------------------
# Import from core module
# ---------------------------------------------------------------------------

from pbhp_core import (
    # Enumerations
    ImpactLevel,
    LikelihoodLevel,
    RiskClass,
    DecisionOutcome,
    Mode,
    UncertaintyLevel,
    Confidence,
    # Data classes
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
    PBHPLog,
    # Engine and detectors
    PBHPEngine,
    DriftAlarmDetector,
    ToneValidator,
    LexicographicPriority,
    # Convenience functions
    quick_harm_check,
    detect_drift_alarms,
    compare_options,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VERSION = "0.7"
CONTACT_EMAIL = "pausebeforeharmprotocol_pbhp@protonmail.com"
BANNER_WIDTH = 72

# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------


def banner(title, char="="):
    """Print a section banner."""
    print()
    print(char * BANNER_WIDTH)
    print("  " + title)
    print(char * BANNER_WIDTH)


def sub_banner(title, char="-"):
    """Print a subsection banner."""
    print()
    print(char * BANNER_WIDTH)
    print("  " + title)
    print(char * BANNER_WIDTH)


def info(msg):
    """Print an informational message."""
    print("  [INFO] " + msg)


def warn(msg):
    """Print a warning message."""
    print("  [WARN] " + msg)


def error(msg):
    """Print an error message."""
    print("  [ERROR] " + msg)


def success(msg):
    """Print a success message."""
    print("  [OK] " + msg)


def drift_alarm(msg):
    """Print a drift alarm."""
    print("  [DRIFT ALARM] " + msg)


def prompt(msg, default=""):
    """Prompt the user for input with an optional default."""
    if default:
        raw = input("  > " + msg + " [" + default + "]: ").strip()
        return raw if raw else default
    return input("  > " + msg + ": ").strip()


def prompt_yes_no(msg, default=None):
    """Prompt for a yes/no answer."""
    hint = "y/n"
    if default is True:
        hint = "Y/n"
    elif default is False:
        hint = "y/N"
    while True:
        raw = input("  > " + msg + " (" + hint + "): ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        if raw == "" and default is not None:
            return default
        print("    Please enter 'y' or 'n'.")


def prompt_yes_no_unsure(msg):
    """Prompt for yes/no/unsure. Returns True, False, or None (unsure)."""
    while True:
        raw = input("  > " + msg + " (y/n/unsure): ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        if raw in ("u", "unsure", ""):
            return None
        print("    Please enter 'y', 'n', or 'unsure'.")


def prompt_choice(msg, options):
    """Prompt the user to choose from a numbered list of options."""
    print("\n  " + msg)
    for i, opt in enumerate(options, 1):
        print("    " + str(i) + ". " + opt)
    while True:
        raw = input("  > Choice: ").strip()
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        # Allow typing the option text directly
        for o in options:
            if o.lower() == raw.lower():
                return o
        print("    Please enter a number 1-" + str(len(options)) + ".")


def prompt_list(msg):
    """Prompt for a list of items, one per line. Empty line to finish."""
    print("  " + msg + " (enter one per line, blank line to finish):")
    items = []
    while True:
        raw = input("    + ").strip()
        if not raw:
            break
        items.append(raw)
    return items


def display_risk_class(risk):
    """Format a risk class for display with description."""
    labels = {
        RiskClass.GREEN:  "GREEN  - Low risk, proceed normally",
        RiskClass.YELLOW: "YELLOW - Moderate risk, document and monitor",
        RiskClass.ORANGE: "ORANGE - High risk, alternatives + red team required",
        RiskClass.RED:    "RED    - Very high risk, must justify why alternatives fail",
        RiskClass.BLACK:  "BLACK  - Extreme risk, refuse or escalate only",
    }
    return labels.get(risk, risk.value.upper())


def display_risk_color(risk):
    """Return the risk class name in uppercase."""
    return risk.value.upper()


def pause_continue():
    """Pause until user presses Enter."""
    input("\n  Press Enter to continue...")


# ===================================================================
# PROTOCOL STEPS
# ===================================================================


# -------------------------------------------------------------------
# Step 00: Protocol Understanding (Competence Gate)
# -------------------------------------------------------------------

def step_00_protocol_understanding():
    """
    Step 00: Protocol Understanding - Competence Gate.
    Verifies the user has a basic grasp of PBHP before proceeding.
    Returns True if confirmed, False otherwise.
    """
    banner("Step 00: Protocol Understanding (Competence Gate)")
    print("""
  Before running a full PBHP assessment, please confirm you understand
  the core principles:

  1. PBHP asks you to PAUSE before any action that could cause harm.
  2. The protocol uses a risk classification system:
     GREEN < YELLOW < ORANGE < RED < BLACK
  3. Higher risk classes require more safeguards (alternatives, red team).
  4. The protocol prioritizes the LEAST POWERFUL affected parties.
  5. 'Brutal Clarity + Zero Contempt' is the required tone.
  6. Drift alarms detect rationalization patterns.
  7. Door/Wall/Gap analysis ensures an escape vector always exists.
  8. BLACK risk actions must be refused or escalated -- never executed.
  9. PBHP governs process, not outcomes.
  10. PBHP cannot be 'passed' by wording alone.
""")
    confirmed = prompt_yes_no(
        "Do you confirm you understand these principles?", default=True
    )
    if not confirmed:
        print()
        warn("Protocol understanding not confirmed.")
        print("  Please review the PBHP v0.7 specification before proceeding.")
        print("  Contact: " + CONTACT_EMAIL)
        return False
    success("Protocol understanding confirmed. Proceeding.")
    return True


# -------------------------------------------------------------------
# Step 0a: Ethical Pause
# -------------------------------------------------------------------

def step_0a_ethical_pause(engine, log):
    """
    Step 0a: Ethical Pause.
    Triune minds: compassion / logic / paradox.
    High arousal check.
    Returns True to continue, False to pause the assessment.
    """
    banner("Step 0a: Ethical Pause")
    print("""
  Pause and balance three forces before proceeding:
    - Compassion / Empathy / Love / Protection / Courage
    - Logic / Intelligence / Clarity / Craft / Responsibility
    - Paradox / Integration / Artistry / Red Team

  Roughly one-third attention on each. This is a posture, not a metric.
""")

    action_stmt = prompt(
        "What exactly am I about to do? (restate the action)",
        default=log.action_description
    )
    print()
    compassion = prompt("Compassion lens -- who could be hurt, who needs protection?")
    logic = prompt("Logic lens -- what are the facts, what is the clearest path?")
    paradox = prompt("Paradox lens -- what am I missing, what contradictions exist?")

    print()
    high_arousal = prompt_yes_no(
        "Are you in a high-arousal state (anger, euphoria, sleep-deprived)?",
        default=False
    )
    arousal_notes = ""
    if high_arousal:
        arousal_notes = prompt("Describe the arousal state")
        print()
        warn("High arousal detected. PBHP recommends: slow down, clarify intent,")
        warn("take the smallest safe action. Consider delaying this assessment.")

    engine.perform_ethical_pause(
        log,
        action_statement=action_stmt,
        compassion_notes=compassion,
        logic_notes=logic,
        paradox_notes=paradox,
        high_arousal_state=high_arousal,
        high_arousal_notes=arousal_notes,
    )

    if high_arousal:
        cont = prompt_yes_no("Continue despite high arousal?", default=False)
        if not cont:
            info("Assessment paused due to high arousal. Resume when ready.")
            return False

    success("Ethical pause complete.")
    return True


# -------------------------------------------------------------------
# Step 0d: Quick Risk Check
# -------------------------------------------------------------------

def step_0d_quick_risk_check(engine, log):
    """
    Step 0d: Quick Risk Check (pre-screening).
    Returns the QuickRiskCheck object.
    """
    banner("Step 0d: Quick Risk Check (Pre-Screening)")
    print("""
  Fast pre-screening before the full protocol.
  Two questions to determine if behavior should tighten.
""")

    low_risk = prompt_yes_no("Is this obviously low-risk?", default=False)
    silence_protects = None
    if not low_risk:
        silence_protects = prompt_yes_no_unsure(
            "Would silence or delay protect people more than acting now?"
        )

    check = engine.perform_quick_risk_check(
        log,
        obviously_low_risk=low_risk,
        silence_delay_protects_more=silence_protects,
    )

    if check.should_tighten:
        warn("Quick risk check recommends TIGHTENING behavior.")
        warn("Proceeding with extra caution through the remaining steps.")
    else:
        success("Quick risk check: no immediate concerns flagged.")

    return check


def standalone_quick_risk_check():
    """Standalone quick risk check (from main menu)."""
    banner("Quick Risk Check")
    print("""
  Quickly calculate a risk class from four parameters.
  No full assessment required.
""")

    impact_str = prompt_choice(
        "Impact level:",
        ["trivial", "moderate", "severe", "catastrophic"]
    )
    likelihood_str = prompt_choice(
        "Likelihood:",
        ["unlikely", "possible", "likely", "imminent"]
    )
    irreversible = prompt_yes_no("Is the harm irreversible?", default=False)
    power_asym = prompt_yes_no("Is there a power asymmetry?", default=False)

    risk = quick_harm_check(impact_str, likelihood_str, irreversible, power_asym)

    sub_banner("Result")
    print("  Risk Class: " + display_risk_class(risk))
    print()

    if risk in (RiskClass.ORANGE, RiskClass.RED, RiskClass.BLACK):
        warn("This risk level requires a full PBHP assessment.")
        warn("Use 'Start New Assessment' from the main menu for the complete walkthrough.")

    pause_continue()


# -------------------------------------------------------------------
# Step 0g: Absolute Rejection Check
# -------------------------------------------------------------------

def step_0g_absolute_rejection(engine, log):
    """
    Step 0g: Absolute Rejection Check.
    Returns True if the action passes (no rejection triggered).
    Returns False if the action is absolutely rejected.
    """
    banner("Step 0g: Absolute Rejection Check")
    print("""
  Checking whether this action upholds:
    - Fascism
    - Genocide
    - Slavery
    - Non-consensual authoritarian control
    - Systemic dehumanization of a group

  If it does, PBHP requires REFUSAL unless the discussion is in
  critique / dismantling / prevention mode.
""")

    check = engine.perform_absolute_rejection_check(log)

    if check.triggers_rejection:
        error("ABSOLUTE REJECTION TRIGGERED.")
        print("  Matched categories: " + ", ".join(check.matched_categories))
        print()
        analysis = prompt_choice(
            "Is this discussion in one of the permitted modes?",
            ["critique", "dismantling", "prevention", "none of these"]
        )
        if analysis in ("critique", "dismantling", "prevention"):
            check.analysis_mode = analysis
            log.absolute_rejection = check
            # Reset the forced refusal so assessment can continue
            log.highest_risk_class = RiskClass.GREEN
            log.decision_outcome = DecisionOutcome.PROCEED
            log.justification = ""
            info("Permitted in " + analysis + " mode. Continuing assessment.")
            return True
        else:
            error("Action REFUSED by absolute rejection gate.")
            error("PBHP does not permit proceeding.")
            log.decision_outcome = DecisionOutcome.REFUSE
            return False
    else:
        success("No absolute rejection categories matched. Proceeding.")
        return True


# -------------------------------------------------------------------
# Step 1: Name the Action
# -------------------------------------------------------------------

def step_1_name_action(engine, log):
    """
    Step 1: Name the Action (with validation).
    Returns True if action is accepted.
    """
    banner("Step 1: Name the Action")
    print("""
  State the action clearly and honestly.
  Truth check: Is this honest and complete enough that a skeptical
  outsider would recognize what you are doing?

  The description should include a clear verb (what you are doing).
  Format: 'I am going to [verb] [object] for/to [who] using [method]'
""")

    while True:
        action = prompt("Describe the action", default=log.action_description)
        valid, msg = engine.validate_action_description(action)
        if valid:
            log.action_description = action
            success("Action accepted: " + msg)
            return True
        else:
            warn("Validation failed: " + msg)
            retry = prompt_yes_no("Try again?", default=True)
            if not retry:
                return False


# -------------------------------------------------------------------
# Step 0e: Door/Wall/Gap
# -------------------------------------------------------------------

def step_0e_door_wall_gap(engine, log):
    """
    Step 0e: Door/Wall/Gap analysis.
    Returns True if a concrete Door is identified.
    """
    banner("Step 0e: Door / Wall / Gap Analysis")
    print("""
  Mandatory micro-module to prevent PBHP from defaulting inside
  an imposed system.

  Wall: What constraint am I operating inside of right now?
        (e.g., deadline, policy, law, authority pressure, lack of info)
  Gap:  Where could harm leak through despite good intent?
        (e.g., misuse, escalation, downstream automation, precedent)
  Door: What is the smallest real escape vector available right now?
        (e.g., delay, verify, narrow scope, refuse)

  The Door MUST be a concrete action -- NOT a feeling ('be careful')
  or a slogan.
""")

    wall = prompt("WALL - What constraint are you operating inside?")
    gap = prompt("GAP  - Where could harm leak through despite good intent?")
    door = prompt("DOOR - Smallest real escape vector (concrete action)?")

    has_door = engine.perform_door_wall_gap(log, wall=wall, gap=gap, door=door)

    if not has_door:
        error("No concrete Door identified.")
        error("PBHP does not permit proceeding without an escape vector.")
        warn("Consider: delay, verify, narrow scope, refuse, or escalate.")
        retry = prompt_yes_no("Would you like to try again?", default=True)
        if retry:
            return step_0e_door_wall_gap(engine, log)
        return False

    success("Door identified: " + door)
    return True


# -------------------------------------------------------------------
# Step 0f: CHIM Check
# -------------------------------------------------------------------

def step_0f_chim_check(engine, log):
    """
    Step 0f: CHIM Check - Agency Under Constraint.
    Returns True if check passes (agency maintained).
    """
    banner("Step 0f: CHIM Check (Agency Under Constraint)")
    print("""
  Prevents surrender of agency to perceived inevitability.

  If the system cannot name a remaining choice, PBHP must pause
  or refuse until that claim is validated.

  If 'no choice' is claimed twice in a row, the problem must be
  reframed in at least two alternative framings and Door/Wall/Gap
  re-run for each.
""")

    constraint = prompt_yes_no(
        "Do you recognize a constraint on your action?", default=True
    )
    no_choice = prompt_yes_no(
        "Are you claiming there is no choice?", default=False
    )
    remaining = ""
    reframes = []
    if no_choice:
        remaining = prompt(
            "Despite the constraint, what remaining choice can you name? (blank if none)"
        )
        if not remaining:
            warn("No remaining choice identified. PBHP requires reframing.")
            reframes = prompt_list("Provide alternative framings of this problem")
    else:
        remaining = prompt("What remaining choice do you have?")

    passed = engine.perform_chim_check(
        log,
        constraint_recognized=constraint,
        no_choice_claim=no_choice,
        remaining_choice=remaining,
        reframes=reframes,
    )

    if not passed:
        error("CHIM check requires PAUSE.")
        if log.chim_check and log.chim_check.consecutive_no_choice_count >= 2:
            error("'No choice' claimed twice in a row.")
            error("Must provide at least 2 alternative framings and re-run Door/Wall/Gap.")
        retry = prompt_yes_no("Would you like to retry?", default=True)
        if retry:
            return step_0f_chim_check(engine, log)
        return False

    success("CHIM check passed. Agency maintained.")
    return True


# -------------------------------------------------------------------
# Step 2: Identify Harms
# -------------------------------------------------------------------

def step_2_identify_harms(engine, log):
    """Step 2: Identify potential harms (loop)."""
    banner("Step 2: Identify Potential Harms")
    print("""
  Identify all potential harms from this action.
  For each harm, you will specify:
    - Description of the potential harm
    - Impact level (trivial / moderate / severe / catastrophic)
    - Likelihood (unlikely / possible / likely / imminent)
    - Irreversibility
    - Power asymmetry
    - Affected parties and the least powerful among them
    - Uncertainty level (S=solid, F=fuzzy, X=speculative)
    - Whether audience risk is elevated

  Add at least one harm. Enter harms one at a time.
""")

    harm_count = 0
    while True:
        sub_banner("Harm #" + str(harm_count + 1), char="-")
        desc = prompt("Describe the potential harm (blank to finish adding harms)")
        if not desc:
            if harm_count == 0:
                warn("You must identify at least one potential harm.")
                continue
            break

        impact_str = prompt_choice("Impact level:", [
            "trivial", "moderate", "severe", "catastrophic"
        ])
        likelihood_str = prompt_choice("Likelihood:", [
            "unlikely", "possible", "likely", "imminent"
        ])
        irreversible = prompt_yes_no("Is this harm irreversible?", default=False)
        power_asym = prompt_yes_no(
            "Is there a power asymmetry (harm lands on low-power group)?",
            default=False
        )

        affected = prompt_list("Who are the affected parties?")
        least_powerful = prompt("Who is the least powerful among the affected?")

        uncertainty_str = prompt_choice("Uncertainty level:", [
            "S (solid -- multiple sources agree)",
            "F (fuzzy -- analysts disagree, incomplete data)",
            "X (speculative -- conjectural, theoretical)",
        ])
        unc_map = {
            "S": UncertaintyLevel.SOLID,
            "F": UncertaintyLevel.FUZZY,
            "X": UncertaintyLevel.SPECULATIVE,
        }
        uncertainty = unc_map.get(uncertainty_str[0], UncertaintyLevel.FUZZY)

        evidence = prompt("Evidence basis (brief description)", default="")
        audience_risk = prompt_yes_no(
            "Is audience risk elevated (vulnerable audience)?", default=False
        )
        notes = prompt("Additional notes (optional)", default="")

        harm = engine.add_harm(
            log,
            description=desc,
            impact=ImpactLevel(impact_str),
            likelihood=LikelihoodLevel(likelihood_str),
            irreversible=irreversible,
            power_asymmetry=power_asym,
            affected_parties=affected,
            least_powerful_affected=least_powerful,
            notes=notes,
            uncertainty_level=uncertainty,
            evidence_basis=evidence,
            audience_risk_elevated=audience_risk,
        )

        risk = harm.calculate_risk_class()
        print()
        info("Harm risk class: " + display_risk_class(risk))
        harm_count += 1

        if not prompt_yes_no("Add another harm?", default=False):
            break

    print()
    info("Total harms identified: " + str(harm_count))
    info("Highest risk class so far: " + display_risk_color(log.highest_risk_class))


# -------------------------------------------------------------------
# Step 3: Risk Class Display
# -------------------------------------------------------------------

def step_3_risk_display(log):
    """Step 3: Display calculated risk class and requirements."""
    banner("Step 3: Risk Classification")

    risk = log.highest_risk_class
    print("\n  Overall Risk Class: " + display_risk_class(risk))
    print()

    if risk == RiskClass.GREEN:
        info("Requirements: Document and proceed.")
    elif risk == RiskClass.YELLOW:
        info("Requirements: Document, monitor, consequences checklist optional.")
    elif risk == RiskClass.ORANGE:
        info("Requirements: Safer alternatives REQUIRED.")
        info("              Red team review REQUIRED (including empathy pass).")
        info("              Consequences checklist REQUIRED.")
        info("              Epistemic fence REQUIRED.")
    elif risk == RiskClass.RED:
        info("Requirements: All ORANGE requirements PLUS:")
        info("              Must justify why safer alternatives cannot meet need.")
        info("              Transparency note in output.")
    elif risk == RiskClass.BLACK:
        info("Requirements: REFUSE or ESCALATE only.")
        info("              Cannot proceed under any circumstances.")

    # List all harms with their individual risk classes
    if log.harms:
        sub_banner("Individual Harm Risk Classes")
        for i, h in enumerate(log.harms, 1):
            hr = h.calculate_risk_class()
            print("  " + str(i) + ". [" + display_risk_color(hr) + "] " + h.description)
            print("     Impact: " + h.impact.value
                  + " | Likelihood: " + h.likelihood.value
                  + " | Irreversible: " + str(h.irreversible)
                  + " | Power Asymmetry: " + str(h.power_asymmetry))
            if h.audience_risk_elevated:
                print("     * Audience risk elevated (risk class bumped up one level)")

    pause_continue()


# -------------------------------------------------------------------
# Step 4: Consent and Representation Check
# -------------------------------------------------------------------

def step_4_consent_check(engine, log):
    """Step 4: Consent and Representation Check."""
    banner("Step 4: Consent and Representation Check")
    print("""
  Would the affected parties reasonably agree if they understood
  the situation?
""")

    explicit = prompt_yes_no(
        "Is there explicit consent from affected parties?", default=False
    )
    hypothetical = None
    if not explicit:
        hypothetical = prompt_yes_no_unsure(
            "Would a reasonable, informed affected party hypothetically consent?"
        )

    overriding = prompt_yes_no(
        "Are you overriding anyone's stated preferences?", default=False
    )
    dignity = prompt_yes_no(
        "Is this action compatible with the dignity of the least powerful affected?",
        default=True
    )
    honest = prompt_yes_no(
        "Is the framing honest (no euphemisms hiding real impact)?",
        default=True
    )
    who_no_say = prompt_list("Who did NOT get a say in this decision?")
    notes = prompt("Notes on consent analysis (optional)", default="")

    check = engine.perform_consent_check(
        log,
        explicit_consent=explicit,
        informed_hypothetical_consent=hypothetical,
        overriding_preferences=overriding,
        compatible_with_dignity=dignity,
        honest_framing=honest,
        who_didnt_get_a_say=who_no_say,
        notes=notes,
    )

    action = check.requires_action()
    print()
    info("Consent analysis recommends: " + action.upper())
    if action == "delay":
        warn("Consider delaying until consent can be obtained or preferences clarified.")
    elif action == "seek_info":
        warn("More information needed before consent can be assessed.")
    elif action == "narrow":
        warn("Narrow the action scope to restore dignity-compatibility.")


# -------------------------------------------------------------------
# Step 5: Safer Alternatives
# -------------------------------------------------------------------

def step_5_alternatives(engine, log):
    """Step 5: Safer Alternatives (required for ORANGE+)."""
    required = log.highest_risk_class in (
        RiskClass.ORANGE, RiskClass.RED, RiskClass.BLACK
    )
    banner("Step 5: Safer Alternatives")
    if required:
        print("\n  REQUIRED for " + display_risk_color(log.highest_risk_class) + " risk class.")
    else:
        print("\n  Optional for this risk class, but recommended.")
    print("""
  Identify safer alternatives that could achieve the same goal
  with less harm. For each alternative, assess whether it:
    - Preserves the original goal
    - Reduces harm
    - Is more reversible
""")

    alt_count = 0
    while True:
        sub_banner("Alternative #" + str(alt_count + 1), char="-")
        desc = prompt("Describe a safer alternative (blank to finish)")
        if not desc:
            if required and alt_count == 0:
                warn("At least one safer alternative is REQUIRED for this risk class.")
                continue
            break

        preserves = prompt_yes_no("Does it preserve the original goal?", default=True)
        reduces = prompt_yes_no("Does it reduce harm?", default=True)
        reversible = prompt_yes_no("Is it more reversible?", default=True)
        notes = prompt("Notes (optional)", default="")

        engine.add_alternative(
            log,
            description=desc,
            preserves_goal=preserves,
            reduces_harm=reduces,
            reversible=reversible,
            notes=notes,
        )
        alt_count += 1
        success("Alternative #" + str(alt_count) + " recorded.")

        if not prompt_yes_no("Add another alternative?", default=False):
            break

    print()
    info("Total alternatives recorded: " + str(alt_count))


# -------------------------------------------------------------------
# Step 6.5: Red Team Review
# -------------------------------------------------------------------

def step_6_5_red_team(engine, log):
    """Step 6.5: Red Team Review (required for ORANGE+, includes empathy pass)."""
    required = log.highest_risk_class in (
        RiskClass.ORANGE, RiskClass.RED, RiskClass.BLACK
    )
    banner("Step 6.5: Red Team Review")
    if required:
        print("\n  REQUIRED for " + display_risk_color(log.highest_risk_class) + " risk class.")
    else:
        if not prompt_yes_no(
            "Run red team review? (optional for this risk class)", default=False
        ):
            return
    print("""
  Adversarial stress test of the proposed action.
  Answer all questions honestly -- the point is to find weaknesses.
""")

    sub_banner("Core Questions")
    failure_modes = prompt_list("What are the possible failure modes?")
    abuse_vectors = prompt_list("How could this be abused or misused?")
    who_bears = prompt("Who bears the most risk if this goes wrong?")
    false_assumptions = prompt_list("What false assumptions might we be making?")
    norm_risk = prompt("What norms does this risk normalizing?", default="")

    sub_banner("Epistemic Questions")
    alt_interps = prompt_list("What alternative interpretations exist?")
    claim_tags = prompt(
        "Which parts are [F]act vs [I]nference/[H]ypothesis/[S]peculative?",
        default=""
    )
    wrong_inf = prompt(
        "If our key inference is wrong, what are the consequences?", default=""
    )

    sub_banner("Empathy Pass (Accuracy, Not Excuse)")
    print("""
  The empathy pass is about ACCURACY in modeling the other side,
  NOT about excusing harm. Boundaries are maintained throughout.
""")
    steelman = prompt("Steelman the opposing view (strongest version of their argument)")
    motives_vs = prompt("Separate motives from outcomes -- what matters here?")
    incentives = prompt("What incentives and pressures are acting on them?")
    reception = prompt("How will the affected parties receive this message?")
    off_ramps = prompt_list("What off-ramps can you identify for them?")
    boundaries = prompt_yes_no(
        "Are your ethical boundaries maintained throughout this analysis?",
        default=True
    )

    review = engine.perform_red_team_review(
        log,
        failure_modes=failure_modes,
        abuse_vectors=abuse_vectors,
        who_bears_risk=who_bears,
        false_assumptions=false_assumptions,
        normalization_risk=norm_risk,
        alternative_interpretations=alt_interps,
        claim_tags=claim_tags,
        wrong_inference_consequences=wrong_inf,
        steelman_other_side=steelman,
        motives_vs_outcomes=motives_vs,
        incentives_pressures=incentives,
        message_reception_prediction=reception,
        off_ramps=off_ramps,
    )
    review.boundaries_maintained = boundaries

    # Display drift alarms from red team
    if review.drift_alarms_detected:
        print()
        for da in review.drift_alarms_detected:
            drift_alarm(da)

    # Determine mitigation
    sub_banner("Mitigation")
    if failure_modes or abuse_vectors:
        mitigated = prompt_yes_no(
            "Have you applied mitigations for the issues found?", default=False
        )
        resolved = prompt_yes_no(
            "Are all issues resolved?", default=False
        )
        review.mitigation_applied = mitigated
        review.issues_resolved = resolved
    else:
        review.mitigation_applied = True
        review.issues_resolved = True

    outcome = review.determine_outcome()
    print()
    info("Red team outcome: " + outcome.upper())
    if outcome == "unresolved":
        error("Unresolved issues found. Proceeding is NOT recommended.")
    elif outcome == "mitigated":
        success("Issues found and mitigated.")
    else:
        success("No significant issues found.")


# -------------------------------------------------------------------
# Steps 6-7: Decision and Justification
# -------------------------------------------------------------------

def step_6_7_decision(engine, log):
    """Steps 6-7: Decision and Justification."""
    banner("Steps 6-7: Decision and Justification")

    # For BLACK risk, restrict choices
    if log.highest_risk_class == RiskClass.BLACK:
        print("\n  Risk class is BLACK. Only REFUSE or ESCALATE are permitted.\n")
        outcome_str = prompt_choice("Decision:", ["refuse", "escalate"])
    else:
        print("""
  Choose your decision outcome based on the full assessment.
  Available decisions:
    proceed          - Continue with the action as planned
    proceed_modified - Proceed with modifications to reduce harm
    redirect         - Redirect to a safer alternative
    delay            - Delay until more information is available
    refuse           - Refuse to take the action
    escalate         - Escalate to a higher authority
""")
        outcome_str = prompt_choice("Decision:", [
            "proceed", "proceed_modified", "redirect",
            "delay", "refuse", "escalate"
        ])

    outcome = DecisionOutcome(outcome_str)

    print()
    justification = prompt("Provide your justification (detailed)")

    # RED requires explanation of why alternatives fail
    if (log.highest_risk_class == RiskClass.RED
            and outcome in (DecisionOutcome.PROCEED, DecisionOutcome.PROCEED_MODIFIED)):
        if "safer alternative" not in justification.lower():
            warn("RED risk class requires justification of why safer alternatives")
            warn("cannot meet the legitimate need. Please include this.")
            extra = prompt("Why can safer alternatives not meet the need?")
            justification += " Safer alternative analysis: " + extra

    engine.finalize_decision(log, outcome=outcome, justification=justification)

    # Display drift alarms found during finalization
    if log.drift_alarms_triggered:
        sub_banner("Drift Alarms Detected During Finalization")
        for da in log.drift_alarms_triggered:
            drift_alarm(da)

    print()
    info("Decision: " + outcome.value.upper())
    info("Risk class: " + display_risk_color(log.highest_risk_class))


# -------------------------------------------------------------------
# Consequences Checklist
# -------------------------------------------------------------------

def consequences_checklist_flow(engine, log):
    """
    Consequences Checklist -- optional for YELLOW, required for ORANGE+.
    22 questions across 6 categories.
    """
    required = log.highest_risk_class in (
        RiskClass.ORANGE, RiskClass.RED, RiskClass.BLACK
    )
    banner("Consequences Checklist")
    if required:
        print("\n  REQUIRED for " + display_risk_color(log.highest_risk_class) + " risk class.")
    else:
        if not prompt_yes_no(
            "Run consequences checklist? (optional for this risk class)",
            default=False
        ):
            return

    print("""
  Temporal + Cultural Impact Modeling.
  22 questions across 6 categories.
  Answer: yes / no / unsure (unsure counts as 'yes' for gating).
""")

    cc = ConsequencesChecklist()

    # --- Category A: Baseline Reality Check ---
    sub_banner("A. Baseline Reality Check")
    cc.historical_analogs = prompt_list(
        "Name historical analogs to this action"
    )
    cc.past_harms_unpredicted = prompt_list(
        "What harms were unpredicted in those analogs?"
    )
    cc.past_mitigation_failures = prompt_list(
        "What mitigations failed in those cases?"
    )
    cc.past_disproportionate_groups = prompt_list(
        "Which groups were disproportionately harmed?"
    )
    cc.past_defender_claims = prompt_list(
        "What did defenders claim about those cases?"
    )

    # --- Category B: Status Quo Harm Audit ---
    sub_banner("B. Status Quo Harm Audit")
    cc.current_harm_if_nothing = prompt(
        "What harm continues if nothing is done?"
    )
    cc.who_benefits_status_quo = prompt(
        "Who benefits from the status quo?"
    )
    cc.inaction_continues_harm = prompt_yes_no_unsure(
        "Does inaction continue harm?"
    )

    # --- Category C: Time Horizon Scan ---
    sub_banner("C. Time Horizon Scan")
    cc.immediate_harms = prompt("Immediate harms (0-72 hours)?", default="")
    cc.short_term_harms = prompt("Short-term harms (1-12 weeks)?", default="")
    cc.medium_term_harms = prompt("Medium-term harms (3-24 months)?", default="")
    cc.long_term_harms = prompt("Long-term harms (2-10+ years)?", default="")
    cc.any_horizon_irreversible = prompt_yes_no(
        "Is any of the above irreversible?", default=False
    )

    # --- Category D: Cultural and Institutional Effects (Q5-Q8) ---
    sub_banner("D. Cultural and Institutional Effects (Q5-Q8)")
    cc.normalizes_harm = prompt_yes_no_unsure(
        "Q5: Does this normalize harm?"
    )
    cc.shifts_to_ends_justify_means = prompt_yes_no_unsure(
        "Q6: Does this shift toward 'ends justify means' thinking?"
    )
    cc.erodes_institutional_trust = prompt_yes_no_unsure(
        "Q7: Does this erode institutional trust?"
    )
    cc.rewards_bad_behavior = prompt_yes_no_unsure(
        "Q8: Does this reward bad behavior?"
    )

    # --- Category E: Power and Representation Effects (Q9-Q12) ---
    sub_banner("E. Power and Representation Effects (Q9-Q12)")
    cc.burdens_fall_on_low_power = prompt_yes_no_unsure(
        "Q9: Do burdens fall on low-power groups?"
    )
    cc.reduces_exit_appeal_optout = prompt_yes_no_unsure(
        "Q10: Does this reduce exit/appeal/opt-out options?"
    )
    cc.increases_surveillance_coercion = prompt_yes_no_unsure(
        "Q11: Does this increase surveillance or coercion?"
    )
    cc.decision_makers_insulated = prompt_yes_no_unsure(
        "Q12: Are decision-makers insulated from consequences?"
    )

    # --- Category F: Drift and Abuse Resistance (Q13-Q15) ---
    sub_banner("F. Drift and Abuse Resistance (Q13-Q15)")
    cc.bad_actor_misuse = prompt(
        "Q13: How could a bad actor misuse this?", default=""
    )
    cc.adjacent_use_prediction = prompt(
        "Q14: What adjacent uses are predictable?", default=""
    )
    cc.permanence_risk = prompt(
        "Q15: What is the permanence risk?", default=""
    )

    # --- Category G: Narrative and Honesty Test (Q16-Q18) ---
    sub_banner("G. Narrative and Honesty Test (Q16-Q18)")
    cc.can_describe_plainly_to_harmed = prompt_yes_no_unsure(
        "Q16: Can you describe this action plainly to the person most harmed?"
    )
    cc.transparency_changes_consent = prompt_yes_no_unsure(
        "Q17: Would full transparency change whether people consent?"
    )
    cc.relying_on_euphemism = prompt_yes_no_unsure(
        "Q18: Are you relying on euphemism to make this palatable?"
    )

    # --- Category H: Repair and Exit Requirements (Q19-Q22) ---
    sub_banner("H. Repair and Exit Requirements (Q19-Q22)")
    cc.rollback_plan = prompt(
        "Q19: What is the rollback plan?", default=""
    )
    cc.sunset_condition = prompt(
        "Q20: What is the sunset condition?", default=""
    )
    cc.independent_stop_authority = prompt(
        "Q21: Who has independent authority to stop this?", default=""
    )
    cc.smallest_door = prompt(
        "Q22: What is the smallest door (escape vector)?", default=""
    )

    engine.set_consequences_checklist(log, cc)

    # Display critical flags
    flags = cc.has_critical_flags()
    sub_banner("Critical Flags Summary")
    for flag_name, flag_val in flags.items():
        status = "FLAGGED" if flag_val else "clear"
        marker = "[!]" if flag_val else "[ ]"
        print("  " + marker + " " + flag_name + ": " + status)

    if cc.requires_door_chim_rerun():
        print()
        error("Critical flags in categories A/C/D require:")
        error("  - Door/Wall/Gap re-run")
        error("  - CHIM check re-run")
        error("  - Safer alternative search")


# -------------------------------------------------------------------
# Uncertainty Assessment
# -------------------------------------------------------------------

def uncertainty_assessment_flow(engine, log):
    """Uncertainty Assessment -- optional but recommended."""
    banner("Uncertainty Assessment")
    if not prompt_yes_no("Run uncertainty assessment?", default=False):
        return

    print("""
  Structured approach to handling incomplete information.
  Name your uncertainties -- do not vibe them.
""")

    ua = UncertaintyAssessment()

    sub_banner("Named Uncertainties")
    ua.solid_claims = prompt_list(
        "[S] Solid claims (multiple independent sources agree)"
    )
    ua.fuzzy_claims = prompt_list(
        "[F] Fuzzy claims (analysts disagree, incomplete data)"
    )
    ua.speculative_claims = prompt_list(
        "[X] Speculative claims (conjectural, theoretical)"
    )

    sub_banner("Bounded Scenarios")
    ua.best_case = prompt("Best case scenario?")
    ua.central_case = prompt("Central (most likely) case?")
    ua.worst_plausible_case = prompt("Worst plausible case?")
    ua.worst_case_who_pays = prompt("In the worst case, who pays the cost?")

    sub_banner("Action vs. Inaction")
    ua.act_and_wrong_harms = prompt(
        "If we act and are wrong, what harms result?"
    )
    ua.act_and_wrong_who = prompt(
        "If we act and are wrong, who is harmed?"
    )
    ua.dont_act_and_wrong_harms = prompt(
        "If we don't act and are wrong, what harms result?"
    )
    ua.dont_act_and_wrong_who = prompt(
        "If we don't act and are wrong, who is harmed?"
    )

    sub_banner("High-Stakes Rules")
    ua.potential_harm_high_hard_to_undo = prompt_yes_no(
        "Is potential harm HIGH and HARD TO UNDO?", default=False
    )
    ua.harm_falls_on_low_power = prompt_yes_no(
        "Does harm fall on low-power groups?", default=False
    )
    ua.benefits_speculative = prompt_yes_no(
        "Are the benefits speculative?", default=False
    )

    if ua.should_default_oppose():
        print()
        error("HIGH-STAKES RULE TRIGGERED:")
        error("  High harm + low power + speculative benefits")
        error("  -> Default to SHRINK / SLOW / OPPOSE")

    ua.potential_harm_low_reversible = prompt_yes_no(
        "Is potential harm LOW and REVERSIBLE?", default=False
    )
    ua.benefit_to_low_power_high = prompt_yes_no(
        "Are benefits to low-power groups high?", default=False
    )

    if ua.can_act_with_monitoring():
        print()
        info("Low harm + high benefit to vulnerable -> acceptable to act with monitoring.")

    sub_banner("Reversibility Design")
    ua.prefers_reversible = prompt_yes_no(
        "Does this design prefer reversible actions?", default=True
    )
    ua.off_ramps = prompt_list("What off-ramps exist?")
    ua.sunset_clause = prompt("What is the sunset clause?", default="")

    sub_banner("Key Questions and Confidence")
    ua.decision_changing_questions = prompt_list(
        "What questions, if answered, could change the decision?"
    )
    ua.can_answer_before_deadline = prompt_yes_no(
        "Can these questions be answered before any deadline?", default=True
    )

    conf_str = prompt_choice("Overall confidence:", [
        "low", "medium-low", "medium", "medium-high", "high"
    ])
    conf_map = {
        "low": Confidence.LOW,
        "medium-low": Confidence.MEDIUM_LOW,
        "medium": Confidence.MEDIUM,
        "medium-high": Confidence.MEDIUM_HIGH,
        "high": Confidence.HIGH,
    }
    ua.confidence = conf_map[conf_str]
    ua.biggest_might_be_wrong = prompt(
        "What is the biggest thing you might be wrong about?"
    )

    engine.set_uncertainty_assessment(log, ua)
    success("Uncertainty assessment recorded.")


# -------------------------------------------------------------------
# Epistemic Fence
# -------------------------------------------------------------------

def epistemic_fence_flow(engine, log):
    """Epistemic Fence -- required for ORANGE+."""
    required = log.highest_risk_class in (
        RiskClass.ORANGE, RiskClass.RED, RiskClass.BLACK
    )
    banner("Epistemic Fence")
    if required:
        print("\n  REQUIRED for " + display_risk_color(log.highest_risk_class) + " risk class.")
    else:
        if not prompt_yes_no(
            "Run epistemic fence? (optional for this risk class)", default=False
        ):
            return

    print("""
  Handles uncertainty, competing frames, attribution, and
  compression honesty. Required for public-facing / ORANGE+ outputs.

  Sections: 6A Mode, 6B Anchors, 6C Reality Separation,
  6D Competing Frames, 6E Recommendation, 6F Door/Wall/Gap,
  6G Compression Honesty.
""")

    # 6A: Mode
    sub_banner("6A: Mode")
    print("""
  EXPLORE: Multiple frames are live; present them without collapsing.
           Requires at least 2 competing frames.
  COMPRESS: One recommendation is being given.
            Requires explicit unknowns and update trigger.
""")
    mode_str = prompt_choice("Epistemic mode:", ["explore", "compress"])
    mode = Mode.EXPLORE if mode_str == "explore" else Mode.COMPRESS
    mode_just = prompt("Why this mode?")

    # 6B: Anchors
    sub_banner("6B: Anchors")
    action_anchor = prompt("Action anchor (what are we actually doing)?")
    wall_anchor = prompt("Wall anchor (what constraint are we in)?")
    lp_anchor = prompt("Least powerful anchor (who is most vulnerable)?")
    nn_anchor = prompt("Non-negotiable anchor (what must NOT be compromised)?")

    # 6C: Reality Separation
    sub_banner("6C: Reality Separation")
    facts = prompt_list("[F] Facts (directly observed or verified)")
    print("  [I] Inferences (claim + confidence level):")
    inferences = []
    while True:
        claim = prompt("    Inference claim (blank to finish)", default="")
        if not claim:
            break
        conf = prompt("    Confidence for this inference", default="medium")
        inferences.append((claim, conf))
    unknowns = prompt_list("[U] Unknowns")
    update_trigger = prompt(
        "Update trigger (what would change the recommendation)?", default=""
    )

    # 6D: Competing Frames (2-5)
    sub_banner("6D: Competing Frames (2-5 recommended)")
    frames = []
    while True:
        frame_name = prompt(
            "Frame #" + str(len(frames) + 1) + " name (blank to finish)", default=""
        )
        if not frame_name:
            if mode == Mode.EXPLORE and len(frames) < 2:
                warn("EXPLORE mode requires at least 2 competing frames.")
                continue
            break
        explains = prompt("  What does this frame explain well?")
        ignores = prompt("  What does this frame ignore or downplay?")
        falsifier = prompt("  What would falsify this frame?")
        frames.append({
            "frame": frame_name,
            "explains": explains,
            "ignores": ignores,
            "falsifier": falsifier,
        })
        if len(frames) >= 5:
            info("Maximum of 5 frames reached.")
            break

    # 6E: Recommendation
    sub_banner("6E: Recommendation")
    recommendation = prompt("What is your recommendation?")
    rec_basis = prompt("On what facts/inferences is this based?")

    # 6F: Door/Wall/Gap (restatement in fence context)
    sub_banner("6F: Door/Wall/Gap (Fence Context)")
    fence_door = prompt("Door (escape vector in this context)?")
    fence_wall = prompt("Wall (constraint in this context)?")
    fence_gap = prompt("Gap (where could harm leak)?")

    # 6G: Compression Honesty
    sub_banner("6G: Compression Honesty")
    irreducible = prompt(
        "What ambiguity is irreducible (cannot be simplified away)?", default=""
    )
    least_wrong = prompt(
        "Least-wrong short version of the situation?", default=""
    )
    what_drops = prompt(
        "What does the short version drop?", default=""
    )

    fence = EpistemicFence(
        mode=mode,
        mode_justification=mode_just,
        action_anchor=action_anchor,
        wall_anchor=wall_anchor,
        least_powerful_anchor=lp_anchor,
        non_negotiable_anchor=nn_anchor,
        facts=facts,
        inferences=inferences,
        unknowns=unknowns,
        update_trigger=update_trigger,
        competing_frames=frames,
        recommendation=recommendation,
        recommendation_basis=rec_basis,
        fence_door=fence_door,
        fence_wall=fence_wall,
        fence_gap=fence_gap,
        irreducible_ambiguity=irreducible,
        least_wrong_short_version=least_wrong,
        what_short_version_drops=what_drops,
    )

    engine.set_epistemic_fence(log, fence)

    # Display validation issues
    issues = fence.validate()
    if issues:
        sub_banner("Epistemic Fence Validation Issues")
        for issue in issues:
            warn(issue)
    else:
        success("Epistemic fence validated successfully.")


# ===================================================================
# STANDALONE TOOLS (from main menu)
# ===================================================================


def standalone_drift_alarm():
    """Standalone Drift Alarm Detector."""
    banner("Drift Alarm Detector")
    print("""
  Paste or type text to scan for rationalization patterns.
  PBHP drift alarms detect phrases that often indicate ethical shortcuts.

  Categories checked:
    - General drift phrases (e.g., "it's temporary", "for the greater good")
    - Premature collapse indicators (e.g., "it's obvious what they meant")
    - Compassion drift (e.g., dehumanizing language)
    - Sycophancy indicators (e.g., flattery that bypasses scrutiny)
""")

    text = prompt("Enter text to scan for drift alarms")
    if not text:
        return

    alarms = detect_drift_alarms(text)

    sub_banner("Results")
    if alarms:
        warn("Found " + str(len(alarms)) + " drift alarm(s):")
        for a in alarms:
            drift_alarm(a)
        print()
        warn("When drift alarms fire, you must explicitly name:")
        warn("  Wall (constraint), Gap (harm leak), Door (escape vector)")
        warn("in writing before proceeding.")
    else:
        success("No drift alarms detected in the provided text.")

    pause_continue()


def standalone_tone_validator():
    """Standalone Tone Validator."""
    banner("Tone Validator (Brutal Clarity + Zero Contempt)")
    print("""
  Validates text against PBHP's tone requirements.

  MUST:
    - Use plain, direct language about harm
    - Name who carries/enables harm
    - Call out bullshit framing
    - Refuse fake neutrality on core harm
    - State stakes explicitly

  MUST NOT:
    - Insult people's basic worth
    - Dehumanize or imply lives don't matter
    - Speculate about secret motives as fact
    - Express joy about suffering
    - Flatten real nuance
    - Use euphemistic hedging that obscures real harm
""")

    text = prompt("Enter text to validate")
    if not text:
        return

    result = ToneValidator.validate(text)

    sub_banner("Results")
    has_issues = False
    if result["contempt_issues"]:
        has_issues = True
        for issue in result["contempt_issues"]:
            error("CONTEMPT: " + issue)
    if result["euphemism_issues"]:
        has_issues = True
        for issue in result["euphemism_issues"]:
            warn("EUPHEMISM: " + issue)

    if not has_issues:
        success("No tone violations detected.")
    else:
        warn("Revise the text to meet PBHP tone requirements.")

    pause_continue()


def standalone_compare_options():
    """Standalone Lexicographic Priority comparison."""
    banner("Compare Options (Lexicographic Priority)")
    print("""
  Compare two options using PBHP's lexicographic priority system.

  Priority order:
    1. Prevent catastrophic irreversible harm first (even if fewer people)
    2. Minimize irreversible harm, then severe harm
    3. Prefer fair distribution of burden
    4. Choose most reversible / safest option

  This prevents: "We helped 10,000 by ruining 500."
""")

    def collect_harms(label):
        sub_banner("Harms for " + label)
        harms = []
        while True:
            desc = prompt("  Describe a harm for " + label + " (blank to finish)")
            if not desc:
                if not harms:
                    warn("Enter at least one harm for comparison.")
                    continue
                break
            impact_str = prompt_choice("  Impact:", [
                "trivial", "moderate", "severe", "catastrophic"
            ])
            likelihood_str = prompt_choice("  Likelihood:", [
                "unlikely", "possible", "likely", "imminent"
            ])
            irr = prompt_yes_no("  Irreversible?", default=False)
            power = prompt_yes_no("  Power asymmetry?", default=False)
            harms.append(Harm(
                description=desc,
                impact=ImpactLevel(impact_str),
                likelihood=LikelihoodLevel(likelihood_str),
                irreversible=irr,
                power_asymmetry=power,
                affected_parties=[],
                least_powerful_affected="",
            ))
        return harms

    harms_a = collect_harms("Option A")
    harms_b = collect_harms("Option B")

    result = compare_options(harms_a, harms_b)

    sub_banner("Result")
    if result == "a":
        info("PREFERRED: Option A (fewer/less severe harms by lexicographic priority).")
    elif result == "b":
        info("PREFERRED: Option B (fewer/less severe harms by lexicographic priority).")
    else:
        info("Options are TIED under lexicographic priority.")
        info("Choose the most reversible / safest option.")

    pause_continue()


# ===================================================================
# VIEW / EXPORT LOGS
# ===================================================================


def view_logs(engine):
    """View assessment logs."""
    banner("Assessment Logs")
    if not engine.logs:
        info("No assessments recorded yet.")
        pause_continue()
        return

    print("\n  Total assessments: " + str(len(engine.logs)) + "\n")
    for i, log in enumerate(engine.logs, 1):
        risk = display_risk_color(log.highest_risk_class)
        outcome = log.decision_outcome.value.upper()
        ts = log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        action = log.action_description[:60]
        if len(log.action_description) > 60:
            action += "..."
        print("  " + str(i) + ". [" + risk + "] " + outcome + " | " + ts)
        print("     " + action)
        print("     ID: " + log.record_id)
        if log.drift_alarms_triggered:
            print("     Drift alarms: " + str(len(log.drift_alarms_triggered)))
        print()

    # Offer to view details
    choice = prompt(
        "Enter log number to view details (or blank to return)", default=""
    )
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(engine.logs):
            view_log_detail(engine.logs[idx])
        else:
            warn("Invalid log number.")

    pause_continue()


def view_log_detail(log):
    """Display detailed log information as formatted JSON."""
    sub_banner("Log Detail: " + log.record_id)
    print(json.dumps(log.to_dict(), indent=2, ensure_ascii=False))


def export_logs(engine):
    """Export logs to a JSON file."""
    banner("Export Logs")
    if not engine.logs:
        info("No assessments to export.")
        pause_continue()
        return

    default_name = "pbhp_logs_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    filepath = prompt("Export file path", default=default_name)
    if not filepath.endswith(".json"):
        filepath += ".json"

    try:
        engine.export_logs(filepath)
        success("Logs exported to: " + filepath)
        info("Total records exported: " + str(len(engine.logs)))
    except Exception as e:
        error("Export failed: " + str(e))

    pause_continue()


# ===================================================================
# FULL ASSESSMENT WALKTHROUGH
# ===================================================================


def full_assessment(engine):
    """Run the complete PBHP v0.7 assessment walkthrough."""
    banner("PBHP v0.7 Full Assessment Walkthrough", char="=")
    print("""
  This will guide you through every step of the protocol.
  You can press Ctrl+C at any time to abort.

  Steps in order:
    00   Protocol Understanding (competence gate)
    0a   Ethical Pause (triune minds, high arousal check)
    0d   Quick Risk Check (pre-screening)
    0g   Absolute Rejection Check
     1   Name the Action (with validation)
    0e   Door / Wall / Gap
    0f   CHIM Check (agency under constraint)
     2   Identify Harms (loop with uncertainty and audience risk)
     3   Risk Class Display (automatic calculation)
     4   Consent and Representation Check
     5   Safer Alternatives (required ORANGE+)
    6.5  Red Team Review (required ORANGE+, includes empathy pass)
    6-7  Decision and Justification
    --   Consequences Checklist (optional YELLOW, required ORANGE+)
    --   Uncertainty Assessment (optional)
    --   Epistemic Fence (required ORANGE+)
    --   Display Generated Response
    --   Save Option
""")

    if not prompt_yes_no("Begin the full assessment?", default=True):
        return

    # ---- Step 00: Protocol Understanding ----
    if not step_00_protocol_understanding():
        return

    # Create the assessment log
    action_desc = prompt("Briefly describe the action to assess")
    log = engine.create_assessment(action_desc)
    info("Assessment ID: " + log.record_id)

    # ---- Step 0a: Ethical Pause ----
    if not step_0a_ethical_pause(engine, log):
        info("Assessment paused. Returning to menu.")
        return

    # ---- Step 0d: Quick Risk Check ----
    step_0d_quick_risk_check(engine, log)

    # ---- Step 0g: Absolute Rejection Check ----
    if not step_0g_absolute_rejection(engine, log):
        # Already refused -- finalize and save
        engine.logs.append(log)
        sub_banner("Assessment Complete (Refused at Absolute Rejection)")
        print()
        print(engine.generate_response(log))
        offer_save(log)
        return

    # ---- Step 1: Name the Action ----
    if not step_1_name_action(engine, log):
        return

    # ---- Step 0e: Door/Wall/Gap ----
    if not step_0e_door_wall_gap(engine, log):
        info("No concrete door found. Assessment cannot proceed.")
        return

    # ---- Step 0f: CHIM Check ----
    if not step_0f_chim_check(engine, log):
        info("CHIM check failed. Assessment paused.")
        return

    # ---- Step 2: Identify Harms ----
    step_2_identify_harms(engine, log)

    # ---- Step 3: Risk Class Display ----
    step_3_risk_display(log)

    # ---- Step 4: Consent and Representation Check ----
    step_4_consent_check(engine, log)

    # ---- Step 5: Safer Alternatives ----
    step_5_alternatives(engine, log)

    # ---- Step 6.5: Red Team Review ----
    step_6_5_red_team(engine, log)

    # ---- Steps 6-7: Decision and Justification ----
    step_6_7_decision(engine, log)

    # ---- Consequences Checklist (optional YELLOW, required ORANGE+) ----
    if log.highest_risk_class in (
        RiskClass.YELLOW, RiskClass.ORANGE, RiskClass.RED, RiskClass.BLACK
    ):
        consequences_checklist_flow(engine, log)

    # ---- Uncertainty Assessment (optional) ----
    uncertainty_assessment_flow(engine, log)

    # ---- Epistemic Fence (required ORANGE+, optional otherwise) ----
    epistemic_fence_flow(engine, log)

    # ---- Display Generated Response ----
    banner("Generated PBHP Response")
    response = engine.generate_response(log)
    print()
    print(response)

    # ---- Save Option ----
    offer_save(log)


def offer_save(log):
    """Offer to save a single assessment log to file."""
    print()
    if prompt_yes_no("Save this assessment to a JSON file?", default=False):
        default_name = (
            "pbhp_"
            + log.record_id[:8]
            + "_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".json"
        )
        filepath = prompt("File path", default=default_name)
        if not filepath.endswith(".json"):
            filepath += ".json"
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(log.to_dict(), f, indent=2, ensure_ascii=False)
            success("Assessment saved to: " + filepath)
        except Exception as e:
            error("Save failed: " + str(e))


# ===================================================================
# HELP
# ===================================================================


def show_help():
    """Display comprehensive help information."""
    banner("PBHP CLI Help")
    print("""
  Pause-Before-Harm Protocol (PBHP) v""" + VERSION + """
  Interactive Command-Line Interface

  MENU OPTIONS
  """ + "=" * 66 + """
  1. Start New Assessment
     Complete guided walkthrough of all PBHP v0.7 protocol steps,
     from competence gate through decision and response generation.

  2. Quick Risk Check
     Fast risk class calculation from four parameters:
     impact, likelihood, irreversibility, power asymmetry.

  3. Drift Alarm Detector
     Scan text for rationalization patterns, premature collapse,
     compassion drift, and sycophancy indicators.

  4. Tone Validator
     Check text against PBHP tone requirements:
     Brutal Clarity + Zero Contempt.

  5. Compare Options (Lexicographic Priority)
     Compare two options using PBHP's priority system.
     Prevents trading catastrophic harm for aggregate benefit.

  6. View Assessment Logs
     Browse and inspect completed assessments.

  7. Export Logs
     Export all assessment logs to a JSON file.

  8. Help
     This screen.

  9. Exit
     Exit the CLI.

  PROTOCOL STEPS (Full Assessment)
  """ + "=" * 66 + """
  Step 00    Protocol Understanding (competence gate)
  Step 0a    Ethical Pause (triune minds: compassion/logic/paradox)
  Step 0d    Quick Risk Check (pre-screening)
  Step 0g    Absolute Rejection Check
  Step 1     Name the Action (with verb validation)
  Step 0e    Door / Wall / Gap analysis
  Step 0f    CHIM Check (agency under constraint)
  Step 2     Identify Harms (loop with uncertainty + audience risk)
  Step 3     Risk Class display (automatic calculation)
  Step 4     Consent and Representation Check
  Step 5     Safer Alternatives (required ORANGE+)
  Step 6.5   Red Team Review (required ORANGE+, empathy pass)
  Steps 6-7  Decision and Justification
  --         Consequences Checklist (optional YELLOW, required ORANGE+)
  --         Uncertainty Assessment (optional)
  --         Epistemic Fence (required ORANGE+)
  --         Generated Response display
  --         Save option

  RISK CLASSES
  """ + "=" * 66 + """
  GREEN    Low risk, proceed normally
  YELLOW   Moderate risk, document and monitor
  ORANGE   High risk, alternatives + red team required
  RED      Very high risk, justify why alternatives fail
  BLACK    Extreme risk, refuse or escalate only

  DECISION OUTCOMES
  """ + "=" * 66 + """
  proceed           Continue as planned
  proceed_modified  Proceed with modifications
  redirect          Use a safer alternative
  delay             Wait for more information
  refuse            Refuse the action
  escalate          Escalate to higher authority

  KEY CONCEPTS
  """ + "=" * 66 + """
  Door/Wall/Gap    Identify constraints and escape vectors
  CHIM Check       Prevent surrender to perceived inevitability
  Ethical Pause    Balance compassion, logic, paradox before acting
  Drift Alarms     Detect rationalization and euphemism patterns
  Red Team Review  Adversarial stress test with empathy pass
  Epistemic Fence  Structure uncertainty, competing frames, attribution
  Consequences     22-question temporal + cultural impact checklist
  Lexicographic    Prevent trading catastrophic harm for aggregate good

  CONTACT
  """ + "=" * 66 + """
  """ + CONTACT_EMAIL + """
""")
    pause_continue()


# ===================================================================
# MAIN MENU
# ===================================================================


def main_menu():
    """Main interactive menu loop."""
    engine = PBHPEngine()

    while True:
        banner("PBHP v" + VERSION + " - Pause-Before-Harm Protocol CLI")
        print("""
  Contact: """ + CONTACT_EMAIL + """

  1. Start New Assessment (full guided walkthrough)
  2. Quick Risk Check
  3. Drift Alarm Detector
  4. Tone Validator
  5. Compare Options (Lexicographic Priority)
  6. View Assessment Logs (""" + str(len(engine.logs)) + """ recorded)
  7. Export Logs
  8. Help
  9. Exit
""")

        choice = prompt("Select an option (1-9)")

        if choice == "1":
            full_assessment(engine)
        elif choice == "2":
            standalone_quick_risk_check()
        elif choice == "3":
            standalone_drift_alarm()
        elif choice == "4":
            standalone_tone_validator()
        elif choice == "5":
            standalone_compare_options()
        elif choice == "6":
            view_logs(engine)
        elif choice == "7":
            export_logs(engine)
        elif choice == "8":
            show_help()
        elif choice == "9":
            print()
            info("Exiting PBHP CLI. Remember: pause before harm.")
            print()
            break
        else:
            warn("Invalid selection. Please choose 1-9.")


# ===================================================================
# CLI HELP (--help flag)
# ===================================================================


def print_cli_help():
    """Print CLI help for --help flag and exit."""
    print("""
Pause-Before-Harm Protocol (PBHP) v""" + VERSION + """ - Interactive CLI

Usage:
    python pbhp_cli.py              Launch interactive menu
    python pbhp_cli.py --help       Show this help text

Description:
    An interactive command-line interface for conducting PBHP v0.7
    ethical assessments. Covers all protocol steps including foundation
    gates, seven core steps, epistemic fencing, red team review, drift
    detection, tone validation, and structured logging.

Menu Options:
    1  Start New Assessment     Full guided walkthrough of all steps
    2  Quick Risk Check         Fast risk class from 4 parameters
    3  Drift Alarm Detector     Scan text for rationalization patterns
    4  Tone Validator           Check Brutal Clarity + Zero Contempt
    5  Compare Options          Lexicographic priority comparison
    6  View Assessment Logs     Browse completed assessments
    7  Export Logs              Export logs to JSON
    8  Help                     Detailed help screen
    9  Exit                     Exit the CLI

No external dependencies required. Uses only Python standard library.

Contact: """ + CONTACT_EMAIL + """
""")


# ===================================================================
# ENTRY POINT
# ===================================================================


def main():
    """Entry point for PBHP CLI."""
    # Handle --help flag
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h", "help"):
        print_cli_help()
        sys.exit(0)

    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n")
        print("=" * BANNER_WIDTH)
        print("  PBHP CLI interrupted. No data was lost from completed assessments.")
        print("  Remember: pause before harm.")
        print("  Contact: " + CONTACT_EMAIL)
        print("=" * BANNER_WIDTH)
        print()
        sys.exit(0)


if __name__ == "__main__":
    main()
