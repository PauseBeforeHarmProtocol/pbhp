"""
Pause-Before-Harm Protocol (PBHP) v0.7 - Comprehensive Test Suite

Tests cover all modules, risk calculations, drift detection, tone validation,
workflow enforcement, serialization, and the full protocol pipeline.

Run:
    python pbhp_tests.py

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

import json
import os
import sys
import tempfile
from datetime import datetime

# ---------------------------------------------------------------------------
# Import everything from pbhp_core
# ---------------------------------------------------------------------------

from pbhp_core import (
    # Enums
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
    # Constants
    ABSOLUTE_REJECTION_CATEGORIES,
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
    FalsePositiveReview,
    PreflightResult,
    FinalizationGateResult,
    PBHPLog,
    # Validators and Detectors
    TextNormalizer,
    DriftAlarmDetector,
    ToneValidator,
    LexicographicPriority,
    # Engine
    PBHPEngine,
    # Convenience functions
    quick_harm_check,
    detect_drift_alarms,
    compare_options,
)


# ---------------------------------------------------------------------------
# Test framework (no external dependencies)
# ---------------------------------------------------------------------------

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def record(self, test_name, passed, msg=""):
        if passed:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append((test_name, msg))

    def summary(self):
        total = self.passed + self.failed
        print("\n" + "=" * 70)
        print(f"TEST RESULTS: {self.passed}/{total} passed, {self.failed} failed")
        print("=" * 70)
        if self.errors:
            print("\nFAILED TESTS:")
            for name, msg in self.errors:
                print(f"  FAIL  {name}")
                if msg:
                    print(f"        {msg}")
        print()
        return self.failed == 0


results = TestResult()


def assert_eq(test_name, actual, expected, msg=""):
    info = msg or f"expected {expected!r}, got {actual!r}"
    results.record(test_name, actual == expected, info if actual != expected else "")
    return actual == expected


def assert_true(test_name, condition, msg=""):
    results.record(test_name, bool(condition), msg if not condition else "")
    return bool(condition)


def assert_false(test_name, condition, msg=""):
    results.record(test_name, not bool(condition), msg if condition else "")
    return not bool(condition)


def assert_in(test_name, item, collection, msg=""):
    found = item in collection
    info = msg or f"{item!r} not found in {collection!r}"
    results.record(test_name, found, info if not found else "")
    return found


def assert_not_in(test_name, item, collection, msg=""):
    found = item not in collection
    info = msg or f"{item!r} unexpectedly found in {collection!r}"
    results.record(test_name, found, info if not found else "")
    return found


def assert_len(test_name, collection, expected_len, msg=""):
    actual = len(collection)
    info = msg or f"expected length {expected_len}, got {actual}"
    results.record(test_name, actual == expected_len, info if actual != expected_len else "")
    return actual == expected_len


def assert_ge(test_name, actual, expected, msg=""):
    info = msg or f"expected >= {expected}, got {actual}"
    results.record(test_name, actual >= expected, info if actual < expected else "")
    return actual >= expected


# ===================================================================
# SECTION 1: Enum Tests
# ===================================================================

def test_enums():
    print("\n--- Enum Tests ---")

    # ImpactLevel
    assert_eq("ImpactLevel.TRIVIAL", ImpactLevel.TRIVIAL.value, "trivial")
    assert_eq("ImpactLevel.MODERATE", ImpactLevel.MODERATE.value, "moderate")
    assert_eq("ImpactLevel.SEVERE", ImpactLevel.SEVERE.value, "severe")
    assert_eq("ImpactLevel.CATASTROPHIC", ImpactLevel.CATASTROPHIC.value, "catastrophic")

    # LikelihoodLevel
    assert_eq("LikelihoodLevel.UNLIKELY", LikelihoodLevel.UNLIKELY.value, "unlikely")
    assert_eq("LikelihoodLevel.POSSIBLE", LikelihoodLevel.POSSIBLE.value, "possible")
    assert_eq("LikelihoodLevel.LIKELY", LikelihoodLevel.LIKELY.value, "likely")
    assert_eq("LikelihoodLevel.IMMINENT", LikelihoodLevel.IMMINENT.value, "imminent")

    # RiskClass
    assert_eq("RiskClass.GREEN", RiskClass.GREEN.value, "green")
    assert_eq("RiskClass.YELLOW", RiskClass.YELLOW.value, "yellow")
    assert_eq("RiskClass.ORANGE", RiskClass.ORANGE.value, "orange")
    assert_eq("RiskClass.RED", RiskClass.RED.value, "red")
    assert_eq("RiskClass.BLACK", RiskClass.BLACK.value, "black")

    # DecisionOutcome
    assert_eq("DecisionOutcome.PROCEED", DecisionOutcome.PROCEED.value, "proceed")
    assert_eq("DecisionOutcome.REFUSE", DecisionOutcome.REFUSE.value, "refuse")
    assert_eq("DecisionOutcome.ESCALATE", DecisionOutcome.ESCALATE.value, "escalate")

    # Mode
    assert_eq("Mode.EXPLORE", Mode.EXPLORE.value, "explore")
    assert_eq("Mode.COMPRESS", Mode.COMPRESS.value, "compress")

    # AttributionLevel
    assert_eq("AttributionLevel.LEVEL_A", AttributionLevel.LEVEL_A.value, "safe")
    assert_eq("AttributionLevel.LEVEL_D", AttributionLevel.LEVEL_D.value, "knowing")

    # ClaimType
    assert_eq("ClaimType.CONTENT", ClaimType.CONTENT.value, "content")
    assert_eq("ClaimType.INTENT", ClaimType.INTENT.value, "intent")

    # EvidenceTag
    assert_eq("EvidenceTag.FACT", EvidenceTag.FACT.value, "F")
    assert_eq("EvidenceTag.INFERENCE", EvidenceTag.INFERENCE.value, "I")
    assert_eq("EvidenceTag.SPECULATIVE", EvidenceTag.SPECULATIVE.value, "S")

    # UncertaintyLevel
    assert_eq("UncertaintyLevel.SOLID", UncertaintyLevel.SOLID.value, "S")
    assert_eq("UncertaintyLevel.FUZZY", UncertaintyLevel.FUZZY.value, "F")
    assert_eq("UncertaintyLevel.SPECULATIVE", UncertaintyLevel.SPECULATIVE.value, "X")

    # Confidence
    assert_eq("Confidence.LOW", Confidence.LOW.value, "low")
    assert_eq("Confidence.HIGH", Confidence.HIGH.value, "high")

    # Enum construction from values
    assert_eq("ImpactLevel from value", ImpactLevel("severe"), ImpactLevel.SEVERE)
    assert_eq("RiskClass from value", RiskClass("black"), RiskClass.BLACK)


# ===================================================================
# SECTION 2: Harm Risk Calculation (Core Deterministic Rules)
# ===================================================================

def test_risk_calculation_green():
    """GREEN: default low-risk cases."""
    print("\n--- Risk Calculation: GREEN ---")

    h = Harm(
        description="Trivial annoyance",
        impact=ImpactLevel.TRIVIAL,
        likelihood=LikelihoodLevel.UNLIKELY,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["user"],
        least_powerful_affected="user",
    )
    assert_eq("trivial+unlikely = GREEN", h.calculate_risk_class(), RiskClass.GREEN)

    h2 = Harm(
        description="Trivial + possible",
        impact=ImpactLevel.TRIVIAL,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["user"],
        least_powerful_affected="user",
    )
    assert_eq("trivial+possible = GREEN", h2.calculate_risk_class(), RiskClass.GREEN)

    h3 = Harm(
        description="Moderate + unlikely",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.UNLIKELY,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["user"],
        least_powerful_affected="user",
    )
    assert_eq("moderate+unlikely = GREEN", h3.calculate_risk_class(), RiskClass.GREEN)


def test_risk_calculation_yellow():
    """YELLOW: moderate-possible, trivial-likely."""
    print("\n--- Risk Calculation: YELLOW ---")

    h = Harm(
        description="Moderate possible harm",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["team"],
        least_powerful_affected="team",
    )
    assert_eq("moderate+possible = YELLOW", h.calculate_risk_class(), RiskClass.YELLOW)

    h2 = Harm(
        description="Trivial but likely",
        impact=ImpactLevel.TRIVIAL,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["user"],
        least_powerful_affected="user",
    )
    assert_eq("trivial+likely = YELLOW", h2.calculate_risk_class(), RiskClass.YELLOW)

    h3 = Harm(
        description="Trivial + imminent",
        impact=ImpactLevel.TRIVIAL,
        likelihood=LikelihoodLevel.IMMINENT,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["user"],
        least_powerful_affected="user",
    )
    assert_eq("trivial+imminent = YELLOW", h3.calculate_risk_class(), RiskClass.YELLOW)


def test_risk_calculation_orange():
    """ORANGE: severe+possible, moderate+likely, power+irreversible."""
    print("\n--- Risk Calculation: ORANGE ---")

    h = Harm(
        description="Severe + possible",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["employee"],
        least_powerful_affected="employee",
    )
    assert_eq("severe+possible = ORANGE", h.calculate_risk_class(), RiskClass.ORANGE)

    h2 = Harm(
        description="Moderate + likely",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["team"],
        least_powerful_affected="team",
    )
    assert_eq("moderate+likely = ORANGE", h2.calculate_risk_class(), RiskClass.ORANGE)

    h3 = Harm(
        description="Moderate + imminent",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.IMMINENT,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["team"],
        least_powerful_affected="team",
    )
    assert_eq("moderate+imminent = ORANGE", h3.calculate_risk_class(), RiskClass.ORANGE)

    # Power asymmetry + Irreversible = minimum ORANGE
    h4 = Harm(
        description="Trivial but power+irreversible",
        impact=ImpactLevel.TRIVIAL,
        likelihood=LikelihoodLevel.UNLIKELY,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["worker"],
        least_powerful_affected="worker",
    )
    assert_eq("power+irreversible = min ORANGE", h4.calculate_risk_class(), RiskClass.ORANGE)


def test_risk_calculation_red():
    """RED: catastrophic+irreversible, severe+irreversible+likely, power+irreversible+severe."""
    print("\n--- Risk Calculation: RED ---")

    # Catastrophic + irreversible (but not likely/imminent)
    h = Harm(
        description="Catastrophic irreversible possible",
        impact=ImpactLevel.CATASTROPHIC,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=True,
        power_asymmetry=False,
        affected_parties=["community"],
        least_powerful_affected="community",
    )
    assert_eq("catastrophic+irreversible+possible = RED", h.calculate_risk_class(), RiskClass.RED)

    # Catastrophic + irreversible + unlikely
    h1b = Harm(
        description="Catastrophic irreversible unlikely",
        impact=ImpactLevel.CATASTROPHIC,
        likelihood=LikelihoodLevel.UNLIKELY,
        irreversible=True,
        power_asymmetry=False,
        affected_parties=["community"],
        least_powerful_affected="community",
    )
    assert_eq("catastrophic+irreversible+unlikely = RED", h1b.calculate_risk_class(), RiskClass.RED)

    # Severe + irreversible + likely
    h2 = Harm(
        description="Severe irreversible likely",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=True,
        power_asymmetry=False,
        affected_parties=["person"],
        least_powerful_affected="person",
    )
    assert_eq("severe+irreversible+likely = RED", h2.calculate_risk_class(), RiskClass.RED)

    # Severe + irreversible + imminent
    h3 = Harm(
        description="Severe irreversible imminent",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.IMMINENT,
        irreversible=True,
        power_asymmetry=False,
        affected_parties=["person"],
        least_powerful_affected="person",
    )
    assert_eq("severe+irreversible+imminent = RED", h3.calculate_risk_class(), RiskClass.RED)

    # Power + irreversible + severe
    h4 = Harm(
        description="Power + severe + irreversible",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.UNLIKELY,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["employee"],
        least_powerful_affected="employee",
    )
    assert_eq("power+irreversible+severe = RED", h4.calculate_risk_class(), RiskClass.RED)

    # Power + irreversible + catastrophic
    h5 = Harm(
        description="Power + catastrophic + irreversible",
        impact=ImpactLevel.CATASTROPHIC,
        likelihood=LikelihoodLevel.UNLIKELY,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["population"],
        least_powerful_affected="population",
    )
    # This hits catastrophic+irreversible first -> RED, power escalation also -> RED
    assert_eq("power+irreversible+catastrophic = RED", h5.calculate_risk_class(), RiskClass.RED)


def test_risk_calculation_black():
    """BLACK: catastrophic + irreversible + (likely or imminent)."""
    print("\n--- Risk Calculation: BLACK ---")

    h = Harm(
        description="Catastrophic irreversible likely",
        impact=ImpactLevel.CATASTROPHIC,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=True,
        power_asymmetry=False,
        affected_parties=["population"],
        least_powerful_affected="population",
    )
    assert_eq("catastrophic+irreversible+likely = BLACK", h.calculate_risk_class(), RiskClass.BLACK)

    h2 = Harm(
        description="Catastrophic irreversible imminent",
        impact=ImpactLevel.CATASTROPHIC,
        likelihood=LikelihoodLevel.IMMINENT,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["population"],
        least_powerful_affected="population",
    )
    assert_eq("catastrophic+irreversible+imminent = BLACK", h2.calculate_risk_class(), RiskClass.BLACK)


def test_audience_risk_elevation():
    """Audience risk elevates risk class by one step."""
    print("\n--- Audience Risk Elevation ---")

    # GREEN -> YELLOW with audience risk
    h = Harm(
        description="Trivial harm to minors",
        impact=ImpactLevel.TRIVIAL,
        likelihood=LikelihoodLevel.UNLIKELY,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["minors"],
        least_powerful_affected="minors",
        audience_risk_elevated=True,
    )
    assert_eq("GREEN+audience -> YELLOW", h.calculate_risk_class(), RiskClass.YELLOW)

    # YELLOW -> ORANGE
    h2 = Harm(
        description="Moderate possible harm to vulnerable",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["vulnerable group"],
        least_powerful_affected="vulnerable group",
        audience_risk_elevated=True,
    )
    assert_eq("YELLOW+audience -> ORANGE", h2.calculate_risk_class(), RiskClass.ORANGE)

    # ORANGE -> RED
    h3 = Harm(
        description="Severe possible to public",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["public"],
        least_powerful_affected="public",
        audience_risk_elevated=True,
    )
    assert_eq("ORANGE+audience -> RED", h3.calculate_risk_class(), RiskClass.RED)

    # RED -> BLACK
    h4 = Harm(
        description="Catastrophic irreversible to public",
        impact=ImpactLevel.CATASTROPHIC,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=True,
        power_asymmetry=False,
        affected_parties=["public"],
        least_powerful_affected="public",
        audience_risk_elevated=True,
    )
    assert_eq("RED+audience -> BLACK", h4.calculate_risk_class(), RiskClass.BLACK)

    # BLACK stays BLACK (ceiling)
    h5 = Harm(
        description="Already BLACK",
        impact=ImpactLevel.CATASTROPHIC,
        likelihood=LikelihoodLevel.IMMINENT,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["all"],
        least_powerful_affected="all",
        audience_risk_elevated=True,
    )
    assert_eq("BLACK+audience stays BLACK", h5.calculate_risk_class(), RiskClass.BLACK)


# ===================================================================
# SECTION 3: Door/Wall/Gap Tests
# ===================================================================

def test_door_wall_gap():
    print("\n--- Door/Wall/Gap Tests ---")

    # Concrete door
    dwg = DoorWallGap(
        wall="Company policy requires two-week notice",
        gap="Employee may not understand the process",
        door="Schedule meeting to explain process before sending letter",
    )
    assert_true("concrete door accepted", dwg.has_door())

    # Vague door: "be careful" is NOT valid
    dwg2 = DoorWallGap(wall="some wall", gap="some gap", door="be careful")
    assert_false("'be careful' rejected", dwg2.has_door())

    # Vague door: "be cautious"
    dwg3 = DoorWallGap(wall="wall", gap="gap", door="Be Cautious")
    assert_false("'Be Cautious' rejected", dwg3.has_door())

    # Other vague doors
    dwg4 = DoorWallGap(wall="wall", gap="gap", door="try harder")
    assert_false("'try harder' rejected", dwg4.has_door())

    dwg5 = DoorWallGap(wall="wall", gap="gap", door="think about it")
    assert_false("'think about it' rejected", dwg5.has_door())

    # Empty door
    dwg6 = DoorWallGap(wall="wall", gap="gap", door="")
    assert_false("empty door rejected", dwg6.has_door())

    dwg7 = DoorWallGap(wall="wall", gap="gap", door="   ")
    assert_false("whitespace-only door rejected", dwg7.has_door())

    # Valid specific doors
    dwg8 = DoorWallGap(wall="wall", gap="gap", door="Delay by 48 hours")
    assert_true("'Delay by 48 hours' accepted", dwg8.has_door())

    dwg9 = DoorWallGap(wall="wall", gap="gap", door="Narrow scope to department only")
    assert_true("'Narrow scope' accepted", dwg9.has_door())

    # Serialization
    d = dwg.to_dict()
    assert_in("DWG to_dict has wall", "wall", d)
    assert_in("DWG to_dict has gap", "gap", d)
    assert_in("DWG to_dict has door", "door", d)
    assert_in("DWG to_dict has concrete_door", "has_concrete_door", d)
    assert_true("DWG to_dict concrete_door True", d["has_concrete_door"])


# ===================================================================
# SECTION 4: CHIM Check Tests
# ===================================================================

def test_chim_check():
    print("\n--- CHIM Check Tests ---")

    # Normal case: choice identified
    c = CHIMCheck(
        constraint_recognized=True,
        treating_as_absolute=False,
        no_choice_claim=False,
        remaining_choice="Can choose timing and wording",
    )
    assert_false("CHIM no pause when choice exists", c.requires_pause())

    # No choice claimed, no remaining choice -> pause
    c2 = CHIMCheck(
        constraint_recognized=True,
        treating_as_absolute=False,
        no_choice_claim=True,
        remaining_choice="",
    )
    assert_true("CHIM pause when no choice & no remaining", c2.requires_pause())

    # No choice claimed but remaining choice identified -> no pause
    c3 = CHIMCheck(
        constraint_recognized=True,
        treating_as_absolute=False,
        no_choice_claim=True,
        remaining_choice="Can refuse and escalate",
    )
    assert_false("CHIM no pause when remaining choice found", c3.requires_pause())

    # Two consecutive no-choice with fewer than 2 reframes -> pause
    c4 = CHIMCheck(
        constraint_recognized=True,
        treating_as_absolute=True,
        no_choice_claim=True,
        remaining_choice="",
        consecutive_no_choice_count=2,
        reframes=["one reframe only"],
    )
    assert_true("CHIM pause: 2x no-choice, <2 reframes", c4.requires_pause())

    # Two consecutive but with 2+ reframes -> depends on remaining_choice
    c5 = CHIMCheck(
        constraint_recognized=True,
        treating_as_absolute=True,
        no_choice_claim=True,
        remaining_choice="",
        consecutive_no_choice_count=2,
        reframes=["reframe A", "reframe B"],
    )
    # Still pauses because no_choice_claim=True and remaining_choice=""
    assert_true("CHIM pause: 2x no-choice, 2 reframes but empty choice", c5.requires_pause())

    # Serialization
    d = c.to_dict()
    assert_in("CHIM to_dict has constraint", "constraint_recognized", d)
    assert_in("CHIM to_dict has requires_pause", "requires_pause", d)


# ===================================================================
# SECTION 5: EthicalPausePosture Tests
# ===================================================================

def test_ethical_pause():
    print("\n--- Ethical Pause Tests ---")

    ep = EthicalPausePosture(
        action_statement="Sending termination notice",
        compassion_notes="This will cause real distress",
        logic_notes="Documentation supports the decision",
        paradox_notes="Fairness to others requires accountability",
        high_arousal_state=False,
    )
    d = ep.to_dict()
    assert_eq("EP action_statement", d["action_statement"], "Sending termination notice")
    assert_eq("EP compassion", d["compassion_notes"], "This will cause real distress")
    assert_false("EP not high arousal", d["high_arousal_state"])

    # High arousal
    ep2 = EthicalPausePosture(
        action_statement="Replying to angry email",
        high_arousal_state=True,
        high_arousal_notes="Feeling angry, need to slow down",
    )
    assert_true("EP high arousal detected", ep2.high_arousal_state)
    d2 = ep2.to_dict()
    assert_true("EP high_arousal in dict", d2["high_arousal_state"])


# ===================================================================
# SECTION 6: QuickRiskCheck Tests
# ===================================================================

def test_quick_risk_check():
    print("\n--- Quick Risk Check Tests ---")

    # Obviously low risk
    qrc = QuickRiskCheck(obviously_low_risk=True)
    result = qrc.evaluate()
    assert_false("QRC low risk -> no tighten", result)
    assert_false("QRC should_tighten false", qrc.should_tighten)

    # Not low risk, silence protects -> tighten
    qrc2 = QuickRiskCheck(obviously_low_risk=False, silence_delay_protects_more=True)
    result2 = qrc2.evaluate()
    assert_true("QRC not low + silence protects -> tighten", result2)

    # Not low risk, silence_delay unknown (None) -> tighten
    qrc3 = QuickRiskCheck(obviously_low_risk=False, silence_delay_protects_more=None)
    result3 = qrc3.evaluate()
    assert_true("QRC not low + unknown -> tighten", result3)

    # Not low risk, silence_delay False -> no tighten
    qrc4 = QuickRiskCheck(obviously_low_risk=False, silence_delay_protects_more=False)
    result4 = qrc4.evaluate()
    assert_false("QRC not low + silence no -> no tighten", result4)

    # Serialization
    d = qrc2.to_dict()
    assert_in("QRC to_dict has obviously_low_risk", "obviously_low_risk", d)
    assert_true("QRC to_dict should_tighten", d["should_tighten"])


# ===================================================================
# SECTION 7: AbsoluteRejectionCheck Tests
# ===================================================================

def test_absolute_rejection():
    print("\n--- Absolute Rejection Check Tests ---")

    # Direct category match
    arc = AbsoluteRejectionCheck(action_description="promote genocide")
    triggered = arc.evaluate("promote genocide")
    assert_true("ARC detects 'genocide'", triggered)
    assert_in("ARC matched category", "genocide", arc.matched_categories)

    # Fascism
    arc2 = AbsoluteRejectionCheck(action_description="uphold fascism")
    assert_true("ARC detects 'fascism'", arc2.evaluate("uphold fascism"))

    # Slavery
    arc3 = AbsoluteRejectionCheck(action_description="defend slavery")
    assert_true("ARC detects 'slavery'", arc3.evaluate("defend slavery"))

    # Systemic dehumanization
    arc4 = AbsoluteRejectionCheck(action_description="systemic dehumanization of a group")
    assert_true("ARC detects dehumanization", arc4.evaluate("systemic dehumanization of a group"))

    # Euphemism: ethnic cleansing
    arc5 = AbsoluteRejectionCheck(action_description="plan ethnic cleansing")
    assert_true("ARC detects 'ethnic cleansing'", arc5.evaluate("plan ethnic cleansing"))

    # Euphemism: forced sterilization
    arc6 = AbsoluteRejectionCheck(action_description="implement forced sterilization")
    assert_true("ARC detects 'forced sterilization'", arc6.evaluate("implement forced sterilization"))

    # Euphemism: master race
    arc7 = AbsoluteRejectionCheck(action_description="advocate master race ideology")
    assert_true("ARC detects 'master race'", arc7.evaluate("advocate master race ideology"))

    # Clean text: should not trigger
    arc_clean = AbsoluteRejectionCheck(action_description="rename a file")
    assert_false("ARC clean text no trigger", arc_clean.evaluate("rename a file"))
    assert_len("ARC clean no categories", arc_clean.matched_categories, 0)

    # Analysis mode: critique allowed
    arc8 = AbsoluteRejectionCheck(
        action_description="critique genocide",
        analysis_mode="critique",
    )
    arc8.evaluate("critique genocide")
    assert_true("ARC critique mode still triggers", arc8.triggers_rejection)

    # Serialization
    d = arc.to_dict()
    assert_in("ARC to_dict has triggers", "triggers_rejection", d)
    assert_in("ARC to_dict has categories", "matched_categories", d)


# ===================================================================
# SECTION 8: ConsentCheck Tests
# ===================================================================

def test_consent_check():
    print("\n--- Consent Check Tests ---")

    # Explicit consent -> proceed
    cc = ConsentCheck(explicit_consent=True)
    assert_eq("CC explicit consent -> proceed", cc.requires_action(), "proceed")

    # No consent, not compatible with dignity -> narrow
    cc2 = ConsentCheck(
        explicit_consent=False,
        compatible_with_dignity=False,
    )
    assert_eq("CC no dignity -> narrow", cc2.requires_action(), "narrow")

    # Overriding preferences -> delay
    cc3 = ConsentCheck(
        explicit_consent=False,
        overriding_preferences=True,
        compatible_with_dignity=True,
    )
    assert_eq("CC overriding prefs -> delay", cc3.requires_action(), "delay")

    # Unknown hypothetical consent -> seek_info
    cc4 = ConsentCheck(
        explicit_consent=False,
        informed_hypothetical_consent=None,
        compatible_with_dignity=True,
    )
    assert_eq("CC unknown hypothetical -> seek_info", cc4.requires_action(), "seek_info")

    # Hypothetical consent True -> proceed
    cc5 = ConsentCheck(
        explicit_consent=False,
        informed_hypothetical_consent=True,
        compatible_with_dignity=True,
    )
    assert_eq("CC hypothetical yes -> proceed", cc5.requires_action(), "proceed")

    # Hypothetical consent False -> delay
    cc6 = ConsentCheck(
        explicit_consent=False,
        informed_hypothetical_consent=False,
        compatible_with_dignity=True,
    )
    assert_eq("CC hypothetical no -> delay", cc6.requires_action(), "delay")

    # Serialization
    d = cc.to_dict()
    assert_in("CC to_dict has required_action", "required_action", d)


# ===================================================================
# SECTION 9: ConsequencesChecklist Tests
# ===================================================================

def test_consequences_checklist():
    print("\n--- Consequences Checklist Tests ---")

    # All clean -> no critical flags from None fields
    # Note: None counts as "yes" for gating on agency/power/honesty flags
    cc_clean = ConsequencesChecklist()
    flags = cc_clean.has_critical_flags()
    assert_false("CC clean: no irreversible", flags["irreversible_harm"])
    # agency_loss: reduces_exit_appeal_optout is None, so True
    assert_true("CC clean: agency_loss (None counts as yes)", flags["agency_loss"])

    # Set explicit falses to clear flags
    cc_explicit = ConsequencesChecklist(
        any_horizon_irreversible=False,
        reduces_exit_appeal_optout=False,
        increases_surveillance_coercion=False,
        burdens_fall_on_low_power=False,
        decision_makers_insulated=False,
        normalizes_harm=False,
        shifts_to_ends_justify_means=False,
        erodes_institutional_trust=False,
        rewards_bad_behavior=False,
        transparency_changes_consent=False,
        relying_on_euphemism=False,
        rollback_plan="Can revert in 24 hours",
    )
    flags2 = cc_explicit.has_critical_flags()
    assert_false("CC explicit: no irreversible", flags2["irreversible_harm"])
    assert_false("CC explicit: no agency_loss", flags2["agency_loss"])
    assert_false("CC explicit: no power_asym", flags2["power_asymmetry"])
    assert_false("CC explicit: no norm_erosion", flags2["norm_erosion"])
    assert_false("CC explicit: no honesty_concern", flags2["honesty_concern"])
    assert_false("CC explicit: no missing_repair", flags2["missing_repair"])
    assert_false("CC explicit: no door/chim rerun", cc_explicit.requires_door_chim_rerun())

    # Irreversible + agency loss -> requires door/chim rerun
    cc_critical = ConsequencesChecklist(
        any_horizon_irreversible=True,
        reduces_exit_appeal_optout=True,
    )
    assert_true("CC critical: requires door/chim rerun", cc_critical.requires_door_chim_rerun())

    # Abuse/drift flagged
    cc_abuse = ConsequencesChecklist(
        bad_actor_misuse="Could be used to target dissidents",
        permanence_risk="Creates irreversible database",
        any_horizon_irreversible=False,
        reduces_exit_appeal_optout=False,
        increases_surveillance_coercion=False,
    )
    flags3 = cc_abuse.has_critical_flags()
    assert_true("CC abuse_drift flagged", flags3["abuse_drift"])
    assert_true("CC abuse requires door/chim", cc_abuse.requires_door_chim_rerun())

    # Missing repair check
    cc_no_repair = ConsequencesChecklist(
        rollback_plan="",
        sunset_condition="",
        independent_stop_authority="",
    )
    flags4 = cc_no_repair.has_critical_flags()
    assert_true("CC missing repair flagged", flags4["missing_repair"])

    # With repair
    cc_repair = ConsequencesChecklist(
        rollback_plan="Can revert within 24 hours",
    )
    flags5 = cc_repair.has_critical_flags()
    assert_false("CC with repair not flagged", flags5["missing_repair"])

    # Serialization
    d = cc_critical.to_dict()
    assert_in("CC to_dict has critical_flags", "critical_flags", d)
    assert_in("CC to_dict has requires_door_chim_rerun", "requires_door_chim_rerun", d)
    assert_in("CC to_dict has time_horizon", "time_horizon", d)
    assert_in("CC to_dict has power_effects", "power_effects", d)


# ===================================================================
# SECTION 10: EpistemicFence Tests
# ===================================================================

def test_epistemic_fence():
    print("\n--- Epistemic Fence Tests ---")

    # Valid EXPLORE mode (2+ frames)
    ef = EpistemicFence(
        mode=Mode.EXPLORE,
        facts=["Policy removes coverage for 10M people"],
        inferences=[("Will increase mortality", "high")],
        unknowns=["State implementation details"],
        competing_frames=[
            {"frame": "Fiscal", "explains": "Reduces debt", "ignores": "Human cost", "falsifier": "Revenue-neutral alternatives"},
            {"frame": "Rights", "explains": "Healthcare as right", "ignores": "Costs", "falsifier": "Unsustainable spending"},
        ],
        update_trigger="CBO score release",
    )
    issues = ef.validate()
    assert_len("EF valid EXPLORE no issues", issues, 0)

    # EXPLORE with <2 frames -> error
    ef2 = EpistemicFence(
        mode=Mode.EXPLORE,
        facts=["Some fact"],
        competing_frames=[{"frame": "Only one"}],
    )
    issues2 = ef2.validate()
    assert_true("EF EXPLORE <2 frames flagged", len(issues2) > 0)
    found = any("2 competing frames" in i for i in issues2)
    assert_true("EF EXPLORE frame error message", found)

    # COMPRESS without unknowns -> error
    ef3 = EpistemicFence(
        mode=Mode.COMPRESS,
        facts=["Fact"],
        unknowns=[],
        update_trigger="something",
        competing_frames=[
            {"frame": "A"}, {"frame": "B"},
        ],
    )
    issues3 = ef3.validate()
    found3 = any("unknowns" in i for i in issues3)
    assert_true("EF COMPRESS no unknowns flagged", found3)

    # COMPRESS without update_trigger -> error
    ef4 = EpistemicFence(
        mode=Mode.COMPRESS,
        unknowns=["Something unknown"],
        update_trigger="",
        competing_frames=[{"frame": "A"}, {"frame": "B"}],
    )
    issues4 = ef4.validate()
    found4 = any("update trigger" in i for i in issues4)
    assert_true("EF COMPRESS no update_trigger flagged", found4)

    # Level D attribution without evidence -> error
    ef5 = EpistemicFence(
        mode=Mode.EXPLORE,
        attribution_level=AttributionLevel.LEVEL_D,
        attribution_evidence="",
        competing_frames=[{"frame": "A"}, {"frame": "B"}],
    )
    issues5 = ef5.validate()
    found5 = any("Level D" in i for i in issues5)
    assert_true("EF Level D no evidence flagged", found5)

    # Level D with evidence -> OK (for that specific check)
    ef6 = EpistemicFence(
        mode=Mode.EXPLORE,
        attribution_level=AttributionLevel.LEVEL_D,
        attribution_evidence="Internal memo shows prior knowledge",
        competing_frames=[{"frame": "A"}, {"frame": "B"}],
    )
    issues6 = ef6.validate()
    found6 = any("Level D" in i for i in issues6)
    assert_false("EF Level D with evidence OK", found6)

    # COMPRESS with <2 frames triggers premature collapse warning
    ef7 = EpistemicFence(
        mode=Mode.COMPRESS,
        unknowns=["x"],
        update_trigger="y",
        competing_frames=[{"frame": "Only one"}],
    )
    issues7 = ef7.validate()
    found7 = any("premature collapse" in i.lower() for i in issues7)
    assert_true("EF COMPRESS <2 frames premature collapse", found7)

    # Serialization
    d = ef.to_dict()
    assert_eq("EF to_dict mode", d["mode"], "explore")
    assert_in("EF to_dict has anchors", "anchors", d)
    assert_in("EF to_dict has reality_separation", "reality_separation", d)
    assert_in("EF to_dict has competing_frames", "competing_frames", d)
    assert_in("EF to_dict has compression_honesty", "compression_honesty", d)
    assert_in("EF to_dict has validation_issues", "validation_issues", d)


# ===================================================================
# SECTION 11: RedTeamReview Tests
# ===================================================================

def test_red_team_review():
    print("\n--- Red Team Review Tests ---")

    # No issues
    rt = RedTeamReview()
    outcome = rt.determine_outcome()
    assert_eq("RT no issues outcome", outcome, "no_issues")

    # Issues mitigated
    rt2 = RedTeamReview(
        failure_modes=["Data leak"],
        abuse_vectors=["Minor misuse"],
        who_bears_risk="end users",
        false_assumptions=["Assumes all users are trustworthy"],
        mitigation_applied=True,
        issues_resolved=True,
    )
    outcome2 = rt2.determine_outcome()
    assert_eq("RT mitigated outcome", outcome2, "mitigated")

    # Severe abuse vector, no mitigation -> unresolved
    rt3 = RedTeamReview(
        failure_modes=["System failure"],
        abuse_vectors=["Severe data exposure affecting millions"],
        who_bears_risk="all users",
        false_assumptions=["Assumes no attack"],
        mitigation_applied=False,
        issues_resolved=False,
    )
    outcome3 = rt3.determine_outcome()
    assert_eq("RT unresolved severe", outcome3, "unresolved")

    # Irreversible abuse vector, no mitigation -> unresolved
    rt4 = RedTeamReview(
        failure_modes=[],
        abuse_vectors=["Irreversible reputation damage"],
        who_bears_risk="target",
        false_assumptions=[],
        mitigation_applied=False,
        issues_resolved=False,
    )
    outcome4 = rt4.determine_outcome()
    assert_eq("RT unresolved irreversible", outcome4, "unresolved")

    # Issues exist, resolved but no explicit mitigation label
    rt5 = RedTeamReview(
        failure_modes=["Minor issue"],
        abuse_vectors=[],
        mitigation_applied=False,
        issues_resolved=True,
    )
    outcome5 = rt5.determine_outcome()
    assert_eq("RT resolved without mitigation label", outcome5, "mitigated")

    # Serialization
    d = rt2.to_dict()
    assert_in("RT to_dict has empathy_pass", "empathy_pass", d)
    assert_in("RT to_dict has failure_modes", "failure_modes", d)
    assert_in("RT to_dict has abuse_vectors", "abuse_vectors", d)
    assert_in("RT to_dict has drift_alarms", "drift_alarms", d)


# ===================================================================
# SECTION 12: Alternative Tests
# ===================================================================

def test_alternative():
    print("\n--- Alternative Tests ---")

    alt = Alternative(
        description="Have 1:1 conversation first",
        preserves_goal=True,
        reduces_harm=True,
        reversible=True,
        notes="Less distress, same outcome",
    )
    d = alt.to_dict()
    assert_eq("Alt description", d["description"], "Have 1:1 conversation first")
    assert_true("Alt preserves goal", d["preserves_goal"])
    assert_true("Alt reduces harm", d["reduces_harm"])
    assert_true("Alt reversible", d["reversible"])
    assert_eq("Alt notes", d["notes"], "Less distress, same outcome")


# ===================================================================
# SECTION 13: UncertaintyAssessment Tests
# ===================================================================

def test_uncertainty_assessment():
    print("\n--- Uncertainty Assessment Tests ---")

    # should_default_oppose: all three True
    ua = UncertaintyAssessment(
        potential_harm_high_hard_to_undo=True,
        harm_falls_on_low_power=True,
        benefits_speculative=True,
    )
    assert_true("UA should_default_oppose all True", ua.should_default_oppose())

    # If any is False, should not oppose
    ua2 = UncertaintyAssessment(
        potential_harm_high_hard_to_undo=True,
        harm_falls_on_low_power=True,
        benefits_speculative=False,
    )
    assert_false("UA should_default_oppose one False", ua2.should_default_oppose())

    ua3 = UncertaintyAssessment(
        potential_harm_high_hard_to_undo=False,
        harm_falls_on_low_power=True,
        benefits_speculative=True,
    )
    assert_false("UA should_default_oppose harm False", ua3.should_default_oppose())

    # can_act_with_monitoring
    ua4 = UncertaintyAssessment(
        potential_harm_low_reversible=True,
        benefit_to_low_power_high=True,
    )
    assert_true("UA can_act_with_monitoring both True", ua4.can_act_with_monitoring())

    ua5 = UncertaintyAssessment(
        potential_harm_low_reversible=False,
        benefit_to_low_power_high=True,
    )
    assert_false("UA can_act_with_monitoring harm False", ua5.can_act_with_monitoring())

    # Serialization
    d = ua.to_dict()
    assert_in("UA to_dict has claims", "claims", d)
    assert_in("UA to_dict has scenarios", "scenarios", d)
    assert_in("UA to_dict has high_stakes_rule", "high_stakes_rule", d)
    assert_true("UA to_dict should_oppose", d["high_stakes_rule"]["should_oppose"])
    assert_in("UA to_dict has reversibility", "reversibility", d)
    assert_in("UA to_dict has confidence", "confidence", d)


# ===================================================================
# SECTION 14: FalsePositiveReview Tests
# ===================================================================

def test_false_positive_review():
    print("\n--- False Positive Review Tests ---")

    # Released (has door + has evidence)
    fpr = FalsePositiveReview(
        pause_challenged=True,
        trigger_cited="Risk class escalation",
        harm_risk_identified="Moderate financial impact",
        door_for_safe_continuation="Proceed with 50% scope reduction",
        evidence_that_would_prevent_pause="Independent audit confirms low risk",
    )
    # Need to run through engine, but we can check the logic manually
    has_door = bool(fpr.door_for_safe_continuation.strip())
    has_evidence = bool(fpr.evidence_that_would_prevent_pause.strip())
    assert_true("FPR has door", has_door)
    assert_true("FPR has evidence", has_evidence)

    # Serialization
    d = fpr.to_dict()
    assert_in("FPR to_dict has pause_challenged", "pause_challenged", d)
    assert_in("FPR to_dict has outcome", "outcome", d)


# ===================================================================
# SECTION 15: DriftAlarmDetector Tests
# ===================================================================

def test_drift_alarm_detector():
    print("\n--- Drift Alarm Detector Tests ---")

    # Standard drift phrases
    text = "We have to do this, it's temporary and for the greater good"
    alarms = DriftAlarmDetector.detect(text)
    assert_true("DAD detects multiple drift", len(alarms) >= 3)
    found_temp = any("it's temporary" in a for a in alarms)
    found_have_to = any("we have to" in a for a in alarms)
    found_greater_good = any("for the greater good" in a for a in alarms)
    assert_true("DAD it's temporary", found_temp)
    assert_true("DAD we have to", found_have_to)
    assert_true("DAD for the greater good", found_greater_good)

    # Premature collapse
    text2 = "It's obvious what they meant and there's only one interpretation"
    alarms2 = DriftAlarmDetector.detect(text2)
    found_obvious = any("premature_collapse" in a and "obvious" in a for a in alarms2)
    found_one_interp = any("premature_collapse" in a and ("interpretation" in a or "single" in a) for a in alarms2)
    assert_true("DAD premature collapse: obvious", found_obvious)
    assert_true("DAD premature collapse: one interpretation", found_one_interp)

    # Compassion drift
    text3 = "These people are vermin and they deserve it"
    alarms3 = DriftAlarmDetector.detect(text3)
    found_vermin = any("compassion_drift" in a and ("vermin" in a or "dehumanization" in a) for a in alarms3)
    found_deserve = any("compassion_drift" in a and ("deserve" in a or "deserving" in a) for a in alarms3)
    assert_true("DAD compassion drift: vermin", found_vermin)
    assert_true("DAD compassion drift: deserve it", found_deserve)

    # Sycophancy
    text4 = "You're enlightened, a chosen one with genius level insight"
    alarms4 = DriftAlarmDetector.detect(text4)
    found_enlightened = any("sycophancy" in a and ("enlightened" in a or "flattery" in a) for a in alarms4)
    found_chosen = any("sycophancy" in a and ("chosen" in a) for a in alarms4)
    found_genius = any("sycophancy" in a and ("genius" in a or "flattery" in a) for a in alarms4)
    assert_true("DAD sycophancy: enlightened", found_enlightened)
    assert_true("DAD sycophancy: chosen one", found_chosen)
    assert_true("DAD sycophancy: genius level", found_genius)

    # Clean text: no alarms
    text5 = "We should proceed with caution and monitor outcomes carefully."
    alarms5 = DriftAlarmDetector.detect(text5)
    assert_len("DAD clean text no alarms", alarms5, 0)

    # Additional drift phrases
    text6 = "it's just policy and we're not responsible"
    alarms6 = DriftAlarmDetector.detect(text6)
    found_policy = any("just-following-orders" in a or "policy" in a for a in alarms6)
    found_not_resp = any("responsibility-dodge" in a or "not responsible" in a for a in alarms6)
    assert_true("DAD just policy", found_policy)
    assert_true("DAD we're not responsible", found_not_resp)


def test_compliance_theater_detection():
    print("\n--- Compliance Theater Detection ---")

    engine = PBHPEngine()

    # Scenario: all harms low despite power+irreversible
    log = engine.create_assessment("Test action", "ai_system")
    engine.add_harm(
        log,
        description="Employment impact",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["employee"],
        least_powerful_affected="employee",
    )
    # Manually override to look like theater (all rated low despite flags)
    log.harms[0] = Harm(
        description="Slight inconvenience",
        impact=ImpactLevel.TRIVIAL,
        likelihood=LikelihoodLevel.UNLIKELY,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["employee"],
        least_powerful_affected="employee",
    )

    alarms = DriftAlarmDetector.detect_compliance_theater(log)
    found = any("compliance theater" in a.lower() for a in alarms)
    assert_true("CT detects low ratings + power/irreversible", found)

    # Theater phrases in justification
    log2 = engine.create_assessment("Test action 2", "ai_system")
    log2.highest_risk_class = RiskClass.RED
    log2.justification = "We ran PBHP so we're covered and above PBHP's scope"
    alarms2 = DriftAlarmDetector.detect_compliance_theater(log2)
    found2 = any("we ran pbhp" in a.lower() for a in alarms2)
    found3 = any("above pbhp's scope" in a.lower() for a in alarms2)
    assert_true("CT detects 'we ran pbhp'", found2)
    assert_true("CT detects 'above pbhp's scope'", found3)

    # Minimal justification for ORANGE
    log3 = engine.create_assessment("Test", "ai_system")
    log3.highest_risk_class = RiskClass.ORANGE
    log3.justification = "OK"
    alarms3 = DriftAlarmDetector.detect_compliance_theater(log3)
    found4 = any("minimal justification" in a.lower() for a in alarms3)
    assert_true("CT detects minimal justification for ORANGE", found4)


# ===================================================================
# SECTION 16: ToneValidator Tests
# ===================================================================

def test_tone_validator():
    print("\n--- Tone Validator Tests ---")

    # Good: plain language about harm (no issues)
    result = ToneValidator.validate("This policy increases deaths for vulnerable groups")
    assert_len("TV good text no contempt", result["contempt_issues"], 0)
    assert_len("TV good text no euphemism", result["euphemism_issues"], 0)

    # Contempt: insults
    result2 = ToneValidator.validate("Only an idiot would support this")
    assert_true("TV detects 'idiot'", len(result2["contempt_issues"]) > 0)

    result3 = ToneValidator.validate("These people are subhuman vermin")
    assert_true("TV detects subhuman", len(result3["contempt_issues"]) > 0)

    # Contempt: specific patterns
    r_moron = ToneValidator.check_for_contempt("What a moron")
    assert_true("TV detects 'moron'", len(r_moron) > 0)

    r_stupid = ToneValidator.check_for_contempt("That's a stupid idea")
    assert_true("TV detects 'stupid'", len(r_stupid) > 0)

    r_scum = ToneValidator.check_for_contempt("Pure scum")
    assert_true("TV detects 'scum'", len(r_scum) > 0)

    r_worthless = ToneValidator.check_for_contempt("Worthless excuse")
    assert_true("TV detects 'worthless'", len(r_worthless) > 0)

    # Euphemism patterns
    result4 = ToneValidator.validate(
        "May pose challenges for some stakeholders in the transition"
    )
    assert_true("TV detects euphemism", len(result4["euphemism_issues"]) > 0)

    result5 = ToneValidator.validate(
        "There are differing perspectives on the appropriate balance"
    )
    assert_true("TV detects fake neutrality", len(result5["euphemism_issues"]) > 0)

    # Clean text: no issues
    result6 = ToneValidator.validate(
        "This decision will cause real financial harm to 500 families"
    )
    assert_len("TV clean text passes", result6["contempt_issues"], 0)
    assert_len("TV clean text no euphemism", result6["euphemism_issues"], 0)


# ===================================================================
# SECTION 17: LexicographicPriority Tests
# ===================================================================

def test_lexicographic_priority():
    print("\n--- Lexicographic Priority Tests ---")

    def make_harm(impact, irreversible=False, power=False):
        return Harm(
            description=f"Harm {impact.value}",
            impact=impact,
            likelihood=LikelihoodLevel.LIKELY,
            irreversible=irreversible,
            power_asymmetry=power,
            affected_parties=["group"],
            least_powerful_affected="group",
        )

    # Priority 1: catastrophic irreversible -> prefer option without it
    opt_a = [make_harm(ImpactLevel.MODERATE)]
    opt_b = [make_harm(ImpactLevel.CATASTROPHIC, irreversible=True)]
    assert_eq("LP catastrophic+irrev: choose a", compare_options(opt_a, opt_b), "a")

    opt_a2 = [make_harm(ImpactLevel.CATASTROPHIC, irreversible=True)]
    opt_b2 = [make_harm(ImpactLevel.MODERATE)]
    assert_eq("LP catastrophic+irrev: choose b", compare_options(opt_a2, opt_b2), "b")

    # Both have catastrophic+irreversible -> fall through
    opt_a3 = [make_harm(ImpactLevel.CATASTROPHIC, irreversible=True)]
    opt_b3 = [make_harm(ImpactLevel.CATASTROPHIC, irreversible=True)]
    # Fall to priority 2 (irreversible count), both have 1 -> fall to priority 3
    result3 = compare_options(opt_a3, opt_b3)
    # Both have 1 catastrophic each -> tied on severe count too -> tied on power -> tied
    assert_eq("LP both catastrophic+irrev = tied", result3, "tied")

    # Priority 2: fewer irreversible harms
    opt_a4 = [make_harm(ImpactLevel.SEVERE, irreversible=True)]
    opt_b4 = [
        make_harm(ImpactLevel.SEVERE, irreversible=True),
        make_harm(ImpactLevel.MODERATE, irreversible=True),
    ]
    assert_eq("LP fewer irreversible: choose a", compare_options(opt_a4, opt_b4), "a")

    # Priority 3: fewer severe harms
    opt_a5 = [make_harm(ImpactLevel.SEVERE)]
    opt_b5 = [
        make_harm(ImpactLevel.SEVERE),
        make_harm(ImpactLevel.SEVERE),
    ]
    assert_eq("LP fewer severe: choose a", compare_options(opt_a5, opt_b5), "a")

    # Priority 4: power asymmetry distribution
    opt_a6 = [make_harm(ImpactLevel.MODERATE, power=True)]
    opt_b6 = [make_harm(ImpactLevel.MODERATE, power=False)]
    assert_eq("LP power asym: choose b", compare_options(opt_a6, opt_b6), "b")

    # Tied completely
    opt_a7 = [make_harm(ImpactLevel.MODERATE)]
    opt_b7 = [make_harm(ImpactLevel.MODERATE)]
    assert_eq("LP identical = tied", compare_options(opt_a7, opt_b7), "tied")

    # Empty lists
    assert_eq("LP both empty = tied", compare_options([], []), "tied")


# ===================================================================
# SECTION 18: PBHPEngine Full Workflow Tests
# ===================================================================

def test_engine_create_assessment():
    print("\n--- Engine: Create Assessment ---")

    engine = PBHPEngine()
    log = engine.create_assessment(
        "Send termination email to Employee X",
        agent_type="human_manager",
    )
    assert_true("Engine creates log", log is not None)
    assert_true("Engine log has UUID", len(log.record_id) > 0)
    assert_eq("Engine log action", log.action_description, "Send termination email to Employee X")
    assert_eq("Engine log agent type", log.agent_type, "human_manager")
    assert_eq("Engine log version", log.version, "0.7.1")
    assert_true("Engine log has timestamp", log.timestamp is not None)


def test_engine_validate_action():
    print("\n--- Engine: Validate Action ---")

    engine = PBHPEngine()

    # Valid action
    valid, msg = engine.validate_action_description("Send warning email to team member")
    assert_true("Validate valid action", valid)

    # Too short
    valid2, msg2 = engine.validate_action_description("Do")
    assert_false("Validate too short", valid2)
    assert_true("Validate short msg", "vague" in msg2.lower() or "missing" in msg2.lower())

    # Missing verb
    valid3, msg3 = engine.validate_action_description("The big important thing about the stuff")
    assert_false("Validate no verb", valid3)
    assert_true("Validate verb msg", "verb" in msg3.lower())

    # Empty
    valid4, _ = engine.validate_action_description("")
    assert_false("Validate empty", valid4)


def test_engine_ethical_pause():
    print("\n--- Engine: Ethical Pause ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Send termination email", "ai_system")

    posture = engine.perform_ethical_pause(
        log,
        action_statement="Terminating employment",
        compassion_notes="Real distress and financial harm",
        logic_notes="6 months documented issues",
        paradox_notes="Accountability needed AND family depends on income",
    )
    assert_true("EP assigned to log", log.ethical_pause is not None)
    assert_eq("EP action", posture.action_statement, "Terminating employment")
    assert_false("EP not high arousal", posture.high_arousal_state)

    # High arousal
    log2 = engine.create_assessment("Reply to angry email", "ai_system")
    posture2 = engine.perform_ethical_pause(
        log2,
        action_statement="Replying angrily",
        high_arousal_state=True,
        high_arousal_notes="Very upset right now",
    )
    assert_true("EP high arousal triggers alarm", len(log2.drift_alarms_triggered) > 0)
    found = any("arousal" in a.lower() for a in log2.drift_alarms_triggered)
    assert_true("EP arousal alarm message", found)


def test_engine_quick_risk_check():
    print("\n--- Engine: Quick Risk Check ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Rename a file", "ai_system")

    qrc = engine.perform_quick_risk_check(log, obviously_low_risk=True)
    assert_true("QRC assigned to log", log.quick_risk_check is not None)
    assert_false("QRC low risk not tightened", qrc.should_tighten)

    log2 = engine.create_assessment("Deploy to production", "ai_system")
    qrc2 = engine.perform_quick_risk_check(log2, obviously_low_risk=False, silence_delay_protects_more=True)
    assert_true("QRC high risk tightened", qrc2.should_tighten)


def test_engine_door_wall_gap():
    print("\n--- Engine: Door/Wall/Gap ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Send termination email", "ai_system")

    # Concrete door
    result = engine.perform_door_wall_gap(
        log,
        wall="Company policy",
        gap="Employee lacks context",
        door="Schedule 1:1 meeting first",
    )
    assert_true("DWG concrete door True", result)
    assert_true("DWG assigned to log", log.door_wall_gap is not None)

    # Vague door
    log2 = engine.create_assessment("Send email", "ai_system")
    result2 = engine.perform_door_wall_gap(log2, wall="wall", gap="gap", door="be careful")
    assert_false("DWG vague door False", result2)
    found = any("no concrete door" in a.lower() for a in log2.drift_alarms_triggered)
    assert_true("DWG vague door alarm", found)


def test_engine_chim_check():
    print("\n--- Engine: CHIM Check ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Execute order", "ai_system")

    # Choice exists
    result = engine.perform_chim_check(
        log,
        constraint_recognized=True,
        no_choice_claim=False,
        remaining_choice="Can choose timing",
    )
    assert_true("CHIM passes with choice", result)

    # No choice, no remaining
    log2 = engine.create_assessment("Execute mandatory order", "ai_system")
    result2 = engine.perform_chim_check(
        log2,
        constraint_recognized=True,
        no_choice_claim=True,
        remaining_choice="",
    )
    assert_false("CHIM fails no choice", result2)
    found = any("chim" in a.lower() for a in log2.drift_alarms_triggered)
    assert_true("CHIM alarm triggered", found)


def test_engine_absolute_rejection():
    print("\n--- Engine: Absolute Rejection ---")

    engine = PBHPEngine()

    # Triggering action
    log = engine.create_assessment("Promote genocide ideology", "ai_system")
    check = engine.perform_absolute_rejection_check(log)
    assert_true("ARC triggers rejection", check.triggers_rejection)
    assert_eq("ARC forces BLACK", log.highest_risk_class, RiskClass.BLACK)
    assert_eq("ARC forces REFUSE", log.decision_outcome, DecisionOutcome.REFUSE)

    # Critique mode: still triggers but doesn't force refuse
    log2 = engine.create_assessment("Analyze critique of genocide", "ai_system")
    check2 = engine.perform_absolute_rejection_check(log2, analysis_mode="critique")
    assert_true("ARC critique triggers", check2.triggers_rejection)
    # In critique mode, should NOT have forced refuse
    assert_eq("ARC critique doesn't force refuse", log2.decision_outcome, DecisionOutcome.PROCEED)

    # Clean action
    log3 = engine.create_assessment("Rename a file to backup.txt", "ai_system")
    check3 = engine.perform_absolute_rejection_check(log3)
    assert_false("ARC clean no trigger", check3.triggers_rejection)


def test_engine_add_harm():
    print("\n--- Engine: Add Harm ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Deploy new policy", "ai_system")

    # First harm
    h1 = engine.add_harm(
        log,
        description="Financial impact on workers",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=False,
        power_asymmetry=True,
        affected_parties=["workers"],
        least_powerful_affected="workers",
    )
    assert_len("One harm added", log.harms, 1)
    assert_eq("Highest risk YELLOW", log.highest_risk_class, RiskClass.YELLOW)

    # Second harm (higher risk)
    h2 = engine.add_harm(
        log,
        description="Job losses",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["workers"],
        least_powerful_affected="workers",
    )
    assert_len("Two harms added", log.harms, 2)
    assert_eq("Highest risk escalated to RED", log.highest_risk_class, RiskClass.RED)


def test_engine_consent_check():
    print("\n--- Engine: Consent Check ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Collect user data", "ai_system")

    cc = engine.perform_consent_check(
        log,
        explicit_consent=False,
        informed_hypothetical_consent=True,
        compatible_with_dignity=True,
        who_didnt_get_a_say=["non-registered visitors"],
        notes="Terms of service accepted",
    )
    assert_true("CC assigned to log", log.consent_check is not None)
    assert_eq("CC action proceed", cc.requires_action(), "proceed")
    assert_len("CC who_didnt_get_a_say", cc.who_didnt_get_a_say, 1)


def test_engine_alternatives():
    print("\n--- Engine: Alternatives ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Mass email notification", "ai_system")

    alt = engine.add_alternative(
        log,
        description="Phase rollout to small group first",
        preserves_goal=True,
        reduces_harm=True,
        reversible=True,
    )
    assert_len("One alternative added", log.alternatives, 1)
    assert_true("Alt preserves goal", alt.preserves_goal)


def test_engine_red_team_review():
    print("\n--- Engine: Red Team Review ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Deploy AI model", "ai_system")

    review = engine.perform_red_team_review(
        log,
        failure_modes=["Model bias", "Adversarial inputs"],
        abuse_vectors=["Discrimination amplification"],
        who_bears_risk="Minority groups",
        false_assumptions=["Training data is representative"],
        normalization_risk="Normalizes automated decision-making without oversight",
        steelman_other_side="AI can process more applications fairly",
        motives_vs_outcomes="Good intent but outcomes may harm",
    )
    assert_true("RT assigned to log", log.red_team_review is not None)
    assert_len("RT failure modes", review.failure_modes, 2)
    assert_len("RT abuse vectors", review.abuse_vectors, 1)


def test_engine_red_team_drift_detection():
    """Red team review should detect drift in its own content."""
    print("\n--- Engine: Red Team Drift Detection ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Some action", "ai_system")

    review = engine.perform_red_team_review(
        log,
        failure_modes=[],
        abuse_vectors=[],
        who_bears_risk="It's temporary so nobody really",
        false_assumptions=["We have to do this for safety"],
        steelman_other_side="For the greater good everyone benefits",
    )
    # Should have detected drift phrases in Red Team content
    found_drift = any("red team drift" in a.lower() for a in log.drift_alarms_triggered)
    assert_true("RT detects drift in own content", found_drift)


def test_engine_consequences_checklist():
    print("\n--- Engine: Consequences Checklist ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Deploy surveillance system", "ai_system")

    cc = ConsequencesChecklist(
        any_horizon_irreversible=True,
        increases_surveillance_coercion=True,
        reduces_exit_appeal_optout=True,
        bad_actor_misuse="Could be repurposed for political persecution",
    )
    engine.set_consequences_checklist(log, cc)

    assert_true("CC assigned to log", log.consequences is not None)
    assert_true("CC requires door/chim rerun", cc.requires_door_chim_rerun())
    found = any("consequences checklist" in a.lower() for a in log.drift_alarms_triggered)
    assert_true("CC triggers alarm for critical flags", found)


def test_engine_uncertainty():
    print("\n--- Engine: Uncertainty Assessment ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Implement new policy", "ai_system")

    ua = UncertaintyAssessment(
        potential_harm_high_hard_to_undo=True,
        harm_falls_on_low_power=True,
        benefits_speculative=True,
        confidence=Confidence.LOW,
    )
    engine.set_uncertainty_assessment(log, ua)

    assert_true("UA assigned to log", log.uncertainty is not None)
    assert_true("UA should_default_oppose", ua.should_default_oppose())
    found = any("uncertainty rule" in a.lower() for a in log.drift_alarms_triggered)
    assert_true("UA triggers oppose alarm", found)


def test_engine_epistemic_fence():
    print("\n--- Engine: Epistemic Fence ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Analyze policy impact", "ai_system")

    # Invalid fence: EXPLORE with <2 frames
    fence = EpistemicFence(
        mode=Mode.EXPLORE,
        facts=["Policy text"],
        competing_frames=[{"frame": "only one"}],
    )
    engine.set_epistemic_fence(log, fence)
    assert_true("EF assigned to log", log.epistemic_fence is not None)
    found = any("epistemic fence" in a.lower() for a in log.drift_alarms_triggered)
    assert_true("EF triggers alarm for validation issues", found)


def test_engine_finalize_decision():
    print("\n--- Engine: Finalize Decision ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Deploy system update", "ai_system")

    # Set up a complete ORANGE assessment
    engine.perform_door_wall_gap(log, "Deadline", "Bugs possible", "Delay by 24 hours")
    engine.add_harm(
        log,
        description="User disruption",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["users"],
        least_powerful_affected="users",
    )
    engine.add_alternative(
        log,
        description="Staged rollout",
        preserves_goal=True,
        reduces_harm=True,
        reversible=True,
    )
    engine.perform_red_team_review(
        log,
        failure_modes=["Rollback needed"],
        abuse_vectors=[],
        who_bears_risk="end users",
        false_assumptions=["All tests pass"],
    )

    result = engine.finalize_decision(
        log,
        outcome=DecisionOutcome.PROCEED_MODIFIED,
        justification="Will proceed with staged rollout to minimize user impact",
    )

    assert_eq("Finalize outcome", result.decision_outcome, DecisionOutcome.PROCEED_MODIFIED)
    assert_true("Finalize log stored", log in engine.logs)


def test_engine_finalize_drift_in_justification():
    """Drift phrases in justification should be caught."""
    print("\n--- Engine: Finalize Drift in Justification ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Deploy risky feature", "ai_system")
    engine.perform_door_wall_gap(log, "w", "g", "Narrow scope")

    engine.finalize_decision(
        log,
        outcome=DecisionOutcome.PROCEED,
        justification="We have to do this, it's temporary and we can fix it later",
    )
    found_drift = any("drift:" in a for a in log.drift_alarms_triggered)
    assert_true("Finalize catches drift in justification", found_drift)


def test_engine_finalize_tone_in_justification():
    """Contempt/euphemism in justification should be caught."""
    print("\n--- Engine: Finalize Tone in Justification ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Review situation", "ai_system")
    engine.perform_door_wall_gap(log, "w", "g", "Delay decision")

    engine.finalize_decision(
        log,
        outcome=DecisionOutcome.DELAY,
        justification="Only an idiot would disagree with this assessment",
    )
    found_tone = any("tone:" in a.lower() for a in log.drift_alarms_triggered)
    assert_true("Finalize catches contempt in justification", found_tone)


def test_engine_finalize_validates_orange_requirements():
    """ORANGE+ requires alternatives and red team."""
    print("\n--- Engine: Finalize ORANGE Validation ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Deploy risky system", "ai_system")
    engine.perform_door_wall_gap(log, "w", "g", "Delay")

    # Add ORANGE-level harm
    engine.add_harm(
        log,
        description="Severe disruption",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["users"],
        least_powerful_affected="users",
    )
    # Don't add alternatives or red team
    engine.finalize_decision(log, DecisionOutcome.PROCEED, "Proceeding anyway")

    found_alt = any("alternatives" in a.lower() for a in log.drift_alarms_triggered)
    found_rt = any("red team" in a.lower() for a in log.drift_alarms_triggered)
    assert_true("Finalize flags missing alternatives for ORANGE", found_alt)
    assert_true("Finalize flags missing red team for ORANGE", found_rt)


def test_engine_finalize_validates_black_must_refuse():
    """BLACK risk must refuse or escalate."""
    print("\n--- Engine: Finalize BLACK Validation ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Deploy dangerous system", "ai_system")
    engine.perform_door_wall_gap(log, "w", "g", "Cancel")

    engine.add_harm(
        log,
        description="Catastrophic irreversible likely harm",
        impact=ImpactLevel.CATASTROPHIC,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["everyone"],
        least_powerful_affected="vulnerable",
    )
    engine.add_alternative(log, "Cancel entirely", True, True, True)
    engine.perform_red_team_review(
        log, ["Total failure"], ["Mass harm"], "everyone", ["All assumptions wrong"]
    )

    engine.finalize_decision(log, DecisionOutcome.PROCEED, "Going anyway")

    found = any("black" in a.lower() and "refuse" in a.lower() for a in log.drift_alarms_triggered)
    assert_true("Finalize flags BLACK proceed as error", found)


# ===================================================================
# SECTION 19: Challenge Pause (False Positive) Tests
# ===================================================================

def test_engine_challenge_pause():
    print("\n--- Engine: Challenge Pause ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Blocked action", "ai_system")

    # Challenge with door + evidence -> released
    review = engine.challenge_pause(
        log,
        trigger_cited="Risk class escalation",
        harm_risk_identified="Moderate financial impact",
        door_for_safe_continuation="Reduce scope by 50%",
        evidence_that_would_prevent_pause="Audit shows minimal actual risk",
    )
    assert_eq("FPR released", review.outcome, "released")
    assert_true("FPR pause_challenged on log", log.pause_challenged)

    # Challenge without door -> maintained
    log2 = engine.create_assessment("Another blocked action", "ai_system")
    review2 = engine.challenge_pause(
        log2,
        trigger_cited="Something",
        harm_risk_identified="Something",
        door_for_safe_continuation="",
        evidence_that_would_prevent_pause="Some evidence",
    )
    assert_eq("FPR maintained (no door)", review2.outcome, "maintained")

    # Challenge without evidence -> maintained
    log3 = engine.create_assessment("Yet another", "ai_system")
    review3 = engine.challenge_pause(
        log3,
        trigger_cited="Something",
        harm_risk_identified="Something",
        door_for_safe_continuation="Real door",
        evidence_that_would_prevent_pause="",
    )
    assert_eq("FPR maintained (no evidence)", review3.outcome, "maintained")


# ===================================================================
# SECTION 20: Response Generation Tests
# ===================================================================

def test_engine_generate_response():
    print("\n--- Engine: Generate Response ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Send performance warning email", "human_manager")

    engine.perform_ethical_pause(
        log,
        action_statement="Issuing formal warning",
        compassion_notes="Will cause stress",
        logic_notes="Documentation supports it",
        paradox_notes="Fairness requires it",
    )
    engine.perform_door_wall_gap(log, "HR policy", "Tone misread", "Rewrite with supportive language")
    engine.perform_chim_check(log, True, False, "Can choose timing and wording")

    engine.add_harm(
        log,
        description="Psychological distress",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=False,
        power_asymmetry=True,
        affected_parties=["employee"],
        least_powerful_affected="employee",
    )
    engine.add_alternative(log, "Verbal conversation first", True, True, True)
    engine.perform_red_team_review(
        log, ["Misunderstood"], ["Retaliation fear"], "employee", ["Clear communication assumed"]
    )
    engine.perform_consent_check(log, False, True, notes="Employee agreed to performance process")

    engine.finalize_decision(
        log,
        DecisionOutcome.PROCEED_MODIFIED,
        "Will have conversation first, then send written follow-up with supportive language",
    )

    response = engine.generate_response(log)

    # Check response structure
    assert_in("Response has Action Recognition", "Action Recognition", response)
    assert_in("Response has Risk Acknowledgment", "Risk Acknowledgment", response)
    assert_in("Response has PBHP Determination", "PBHP Determination", response)
    assert_in("Response has Decision Outcome", "Decision Outcome", response)
    assert_in("Response has Door Statement", "Door Statement", response)
    assert_in("Response has Confidence", "Confidence", response)
    assert_in("Response has Record ID", "PBHP Record ID", response)
    assert_in("Response has ORANGE risk", "ORANGE", response)


# ===================================================================
# SECTION 21: PBHPLog Serialization Tests
# ===================================================================

def test_log_serialization():
    print("\n--- Log Serialization ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Test serialization", "ai_system")

    engine.perform_ethical_pause(log, "Testing serialization")
    engine.perform_quick_risk_check(log, True)
    engine.perform_door_wall_gap(log, "w", "g", "Narrow scope")
    engine.perform_chim_check(log, True, False, "Can modify approach")
    engine.perform_absolute_rejection_check(log)
    engine.add_harm(
        log, "Test harm", ImpactLevel.MODERATE, LikelihoodLevel.POSSIBLE,
        False, False, ["test"], "test",
    )
    engine.perform_consent_check(log, True)
    engine.add_alternative(log, "Alternative approach", True, True, True)
    engine.perform_red_team_review(log, ["fail"], [], "test", [])
    engine.set_consequences_checklist(log, ConsequencesChecklist(
        any_horizon_irreversible=False,
        reduces_exit_appeal_optout=False,
        increases_surveillance_coercion=False,
    ))
    engine.set_uncertainty_assessment(log, UncertaintyAssessment(confidence=Confidence.MEDIUM))
    engine.set_epistemic_fence(log, EpistemicFence(
        mode=Mode.COMPRESS,
        unknowns=["something"],
        update_trigger="new data",
        competing_frames=[{"frame": "A"}, {"frame": "B"}],
    ))
    engine.challenge_pause(log, "test", "test", "door", "evidence")

    engine.finalize_decision(log, DecisionOutcome.PROCEED_MODIFIED, "Proceeding with modifications")

    # to_dict
    d = log.to_dict()
    assert_true("Log to_dict is dict", isinstance(d, dict))
    assert_in("Log has record_id", "record_id", d)
    assert_in("Log has timestamp", "timestamp", d)
    assert_in("Log has version", "version", d)
    assert_in("Log has ethical_pause", "ethical_pause", d)
    assert_in("Log has quick_risk_check", "quick_risk_check", d)
    assert_in("Log has door_wall_gap", "door_wall_gap", d)
    assert_in("Log has chim_check", "chim_check", d)
    assert_in("Log has absolute_rejection", "absolute_rejection", d)
    assert_in("Log has consequences", "consequences", d)
    assert_in("Log has consent_check", "consent_check", d)
    assert_in("Log has uncertainty", "uncertainty", d)
    assert_in("Log has epistemic_fence", "epistemic_fence", d)
    assert_in("Log has red_team_review", "red_team_review", d)
    assert_in("Log has false_positive_review", "false_positive_review", d)
    assert_in("Log has harms", "harms", d)
    assert_in("Log has alternatives", "alternatives", d)
    assert_in("Log has decision_outcome", "decision_outcome", d)
    assert_in("Log has metadata", "metadata", d)
    assert_in("Log has drift_alarms", "drift_alarms", d)
    assert_in("Log has follow_up", "follow_up", d)
    assert_in("Log has ownership", "ownership", d)

    # to_json
    j = log.to_json()
    assert_true("Log to_json is string", isinstance(j, str))
    parsed = json.loads(j)
    assert_true("Log JSON parseable", isinstance(parsed, dict))
    assert_eq("Log JSON version", parsed["version"], "0.7.1")


def test_log_export():
    print("\n--- Log Export ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Export test", "ai_system")
    engine.perform_door_wall_gap(log, "w", "g", "d")
    engine.finalize_decision(log, DecisionOutcome.PROCEED, "Safe to proceed")

    # Export to temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        tmppath = f.name

    try:
        engine.export_logs(tmppath)
        with open(tmppath, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert_true("Export is list", isinstance(data, list))
        assert_len("Export has one log", data, 1)
        assert_eq("Export record matches", data[0]["record_id"], log.record_id)
    finally:
        os.unlink(tmppath)


def test_log_get_by_id():
    print("\n--- Log Get By ID ---")

    engine = PBHPEngine()
    log1 = engine.create_assessment("Log 1", "ai_system")
    engine.perform_door_wall_gap(log1, "w", "g", "d")
    engine.finalize_decision(log1, DecisionOutcome.PROCEED, "OK")

    log2 = engine.create_assessment("Log 2", "ai_system")
    engine.perform_door_wall_gap(log2, "w", "g", "d")
    engine.finalize_decision(log2, DecisionOutcome.DELAY, "Wait")

    found = engine.get_log_by_id(log1.record_id)
    assert_true("Found log1 by ID", found is not None)
    assert_eq("Found correct log", found.action_description, "Log 1")

    not_found = engine.get_log_by_id("nonexistent-id")
    assert_true("Not found returns None", not_found is None)


def test_log_overall_confidence():
    print("\n--- Log Overall Confidence ---")

    log = PBHPLog(record_id="test", timestamp=datetime.utcnow())
    assert_eq("No uncertainty -> not assessed", log.get_overall_confidence(), "not assessed")

    log.uncertainty = UncertaintyAssessment(confidence=Confidence.HIGH)
    assert_eq("With uncertainty -> high", log.get_overall_confidence(), "high")

    log.uncertainty = UncertaintyAssessment(confidence=Confidence.LOW)
    assert_eq("Low confidence", log.get_overall_confidence(), "low")


# ===================================================================
# SECTION 22: Convenience Functions Tests
# ===================================================================

def test_quick_harm_check():
    print("\n--- Convenience: quick_harm_check ---")

    assert_eq("QHC green", quick_harm_check("trivial", "unlikely", False, False), RiskClass.GREEN)
    assert_eq("QHC yellow", quick_harm_check("moderate", "possible", False, False), RiskClass.YELLOW)
    assert_eq("QHC orange", quick_harm_check("severe", "possible", False, False), RiskClass.ORANGE)
    assert_eq("QHC red", quick_harm_check("severe", "likely", True, True), RiskClass.RED)
    assert_eq("QHC black", quick_harm_check("catastrophic", "likely", True, True), RiskClass.BLACK)

    # Power + irreversible minimum ORANGE
    assert_eq("QHC power+irrev min ORANGE", quick_harm_check("trivial", "unlikely", True, True), RiskClass.ORANGE)


def test_detect_drift_alarms():
    print("\n--- Convenience: detect_drift_alarms ---")

    alarms = detect_drift_alarms("it's temporary and for safety")
    assert_true("detect_drift_alarms finds phrases", len(alarms) >= 2)

    alarms2 = detect_drift_alarms("We should monitor carefully and review in 30 days")
    assert_len("detect_drift_alarms clean", alarms2, 0)


def test_compare_options():
    print("\n--- Convenience: compare_options ---")

    h_a = [Harm("A", ImpactLevel.MODERATE, LikelihoodLevel.LIKELY, False, False, ["x"], "x")]
    h_b = [Harm("B", ImpactLevel.CATASTROPHIC, LikelihoodLevel.LIKELY, True, True, ["x"], "x")]

    assert_eq("compare_options prefers a", compare_options(h_a, h_b), "a")
    assert_eq("compare_options prefers b", compare_options(h_b, h_a), "b")
    assert_eq("compare_options tied", compare_options(h_a, h_a), "tied")


# ===================================================================
# SECTION 23: Full Protocol Pipeline Test
# ===================================================================

def test_full_pipeline_orange():
    """Full ORANGE pipeline: employee warning scenario."""
    print("\n--- Full Pipeline: ORANGE Scenario ---")

    engine = PBHPEngine()

    # Step 1: Name the action
    log = engine.create_assessment(
        "Send formal performance warning to team member",
        agent_type="human_manager",
    )
    valid, _ = engine.validate_action_description(log.action_description)
    assert_true("Pipeline: action valid", valid)

    # Step 0a: Ethical Pause
    engine.perform_ethical_pause(
        log,
        action_statement="Issuing performance warning",
        compassion_notes="Will cause anxiety",
        logic_notes="Performance documented",
        paradox_notes="Fairness vs compassion",
    )

    # Step 0d: Quick Risk Check
    engine.perform_quick_risk_check(log, obviously_low_risk=False, silence_delay_protects_more=False)

    # Step 0e: Door/Wall/Gap
    engine.perform_door_wall_gap(
        log,
        wall="HR policy requires written warning after verbal",
        gap="Wording could be harsher than intended",
        door="Have HR review letter before sending; offer 1:1 meeting",
    )

    # Step 0f: CHIM Check
    engine.perform_chim_check(
        log,
        constraint_recognized=True,
        no_choice_claim=False,
        remaining_choice="Timing, wording, support offered",
    )

    # Step 0g: Absolute Rejection
    engine.perform_absolute_rejection_check(log)
    assert_false("Pipeline: not rejected", log.absolute_rejection.triggers_rejection)

    # Step 2: Add Harms
    engine.add_harm(
        log,
        description="Psychological distress",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=False,
        power_asymmetry=True,
        affected_parties=["employee"],
        least_powerful_affected="employee",
    )

    assert_eq("Pipeline: risk ORANGE", log.highest_risk_class, RiskClass.ORANGE)

    # Step 4: Consent Check
    engine.perform_consent_check(
        log,
        explicit_consent=False,
        informed_hypothetical_consent=True,
        compatible_with_dignity=True,
        notes="Employee agreed to performance review process",
    )

    # Step 5: Alternatives
    engine.add_alternative(
        log,
        description="Verbal conversation before written warning",
        preserves_goal=True,
        reduces_harm=True,
        reversible=True,
    )

    # Step 6.5: Red Team
    engine.perform_red_team_review(
        log,
        failure_modes=["Employee misunderstands severity"],
        abuse_vectors=["Could be used punitively"],
        who_bears_risk="Employee",
        false_assumptions=["Employee will receive it constructively"],
        steelman_other_side="Employee may have external factors affecting performance",
    )

    # Step 6: Finalize
    engine.finalize_decision(
        log,
        outcome=DecisionOutcome.PROCEED_MODIFIED,
        justification="Will have face-to-face conversation first, then send written follow-up with supportive framing and clear improvement path",
    )

    # Verify complete pipeline
    assert_true("Pipeline: ethical pause set", log.ethical_pause is not None)
    assert_true("Pipeline: quick risk check set", log.quick_risk_check is not None)
    assert_true("Pipeline: DWG set", log.door_wall_gap is not None)
    assert_true("Pipeline: CHIM set", log.chim_check is not None)
    assert_true("Pipeline: ARC set", log.absolute_rejection is not None)
    assert_len("Pipeline: 1 harm", log.harms, 1)
    assert_true("Pipeline: consent set", log.consent_check is not None)
    assert_len("Pipeline: 1 alternative", log.alternatives, 1)
    assert_true("Pipeline: red team set", log.red_team_review is not None)
    assert_eq("Pipeline: PROCEED_MODIFIED", log.decision_outcome, DecisionOutcome.PROCEED_MODIFIED)

    # Generate response
    response = engine.generate_response(log)
    assert_true("Pipeline: response non-empty", len(response) > 100)

    # Serialize
    d = log.to_dict()
    j = json.dumps(d, indent=2)
    parsed = json.loads(j)
    assert_eq("Pipeline: serialization roundtrip version", parsed["version"], "0.7.1")


def test_full_pipeline_black():
    """Full BLACK pipeline: must refuse."""
    print("\n--- Full Pipeline: BLACK Scenario ---")

    engine = PBHPEngine()
    log = engine.create_assessment(
        "Post public accusation of crime without evidence",
        agent_type="ai_system",
    )

    engine.perform_ethical_pause(
        log,
        action_statement="Publishing unverified criminal accusation",
        compassion_notes="Could destroy innocent person's life",
        logic_notes="No verified evidence",
        paradox_notes="Truth matters AND accusations without evidence harm",
        high_arousal_state=True,
        high_arousal_notes="User seems angry",
    )

    engine.perform_door_wall_gap(
        log,
        wall="No evidence to support claim",
        gap="Publication would be permanent and viral",
        door="Refuse to publish; suggest consulting a lawyer first",
    )

    engine.add_harm(
        log,
        description="Permanent reputation destruction of accused",
        impact=ImpactLevel.CATASTROPHIC,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["accused person", "their family"],
        least_powerful_affected="accused person",
        audience_risk_elevated=True,  # Public-facing
    )

    assert_eq("Pipeline BLACK: risk = BLACK", log.highest_risk_class, RiskClass.BLACK)

    engine.add_alternative(
        log,
        description="Consult a lawyer before making any public statement",
        preserves_goal=False,
        reduces_harm=True,
        reversible=True,
    )

    engine.perform_red_team_review(
        log,
        failure_modes=["Accusation is false", "Viral spread"],
        abuse_vectors=["Weaponized defamation"],
        who_bears_risk="accused person and family",
        false_assumptions=["User's account is accurate"],
    )

    engine.finalize_decision(
        log,
        outcome=DecisionOutcome.REFUSE,
        justification="Cannot proceed: catastrophic irreversible harm to accused with no verified evidence. Recommending legal consultation.",
    )

    assert_eq("Pipeline BLACK: refused", log.decision_outcome, DecisionOutcome.REFUSE)
    assert_true("Pipeline BLACK: high arousal detected",
                any("arousal" in a.lower() for a in log.drift_alarms_triggered))


def test_full_pipeline_green():
    """Full GREEN pipeline: minimal protocol for low-risk action."""
    print("\n--- Full Pipeline: GREEN Scenario ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Rename backup file to backup_old.txt", "ai_system")

    engine.perform_quick_risk_check(log, obviously_low_risk=True)
    engine.perform_door_wall_gap(log, "None", "None", "Undo rename if needed")
    engine.perform_absolute_rejection_check(log)

    engine.add_harm(
        log,
        description="Minimal inconvenience if wrong file renamed",
        impact=ImpactLevel.TRIVIAL,
        likelihood=LikelihoodLevel.UNLIKELY,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=["user"],
        least_powerful_affected="user",
    )

    assert_eq("Pipeline GREEN: risk = GREEN", log.highest_risk_class, RiskClass.GREEN)

    engine.finalize_decision(
        log,
        outcome=DecisionOutcome.PROCEED,
        justification="Trivial, reversible action with no significant harm",
    )

    assert_eq("Pipeline GREEN: proceed", log.decision_outcome, DecisionOutcome.PROCEED)


# ===================================================================
# SECTION 24: Edge Cases and Boundary Tests
# ===================================================================

def test_edge_cases():
    print("\n--- Edge Cases ---")

    # Harm with all None/defaults
    h = Harm(
        description="Minimal",
        impact=ImpactLevel.TRIVIAL,
        likelihood=LikelihoodLevel.UNLIKELY,
        irreversible=False,
        power_asymmetry=False,
        affected_parties=[],
        least_powerful_affected="",
    )
    assert_eq("Edge: minimal harm = GREEN", h.calculate_risk_class(), RiskClass.GREEN)

    # Harm to_dict works with all fields
    d = h.to_dict()
    assert_true("Edge: harm to_dict complete", "risk_class" in d)

    # Engine with no logs
    engine = PBHPEngine()
    assert_len("Edge: engine starts empty", engine.logs, 0)

    # get_log_by_id on empty engine
    assert_true("Edge: get_log empty", engine.get_log_by_id("x") is None)

    # Multiple harms escalate correctly
    log = engine.create_assessment("Multi-harm test", "ai_system")
    engine.add_harm(log, "Low", ImpactLevel.TRIVIAL, LikelihoodLevel.UNLIKELY,
                    False, False, ["x"], "x")
    assert_eq("Edge: first harm GREEN", log.highest_risk_class, RiskClass.GREEN)

    engine.add_harm(log, "Mid", ImpactLevel.MODERATE, LikelihoodLevel.POSSIBLE,
                    False, False, ["x"], "x")
    assert_eq("Edge: second harm YELLOW", log.highest_risk_class, RiskClass.YELLOW)

    engine.add_harm(log, "High", ImpactLevel.CATASTROPHIC, LikelihoodLevel.IMMINENT,
                    True, True, ["x"], "x")
    assert_eq("Edge: third harm BLACK", log.highest_risk_class, RiskClass.BLACK)

    # Risk class never downgrades
    engine.add_harm(log, "Low again", ImpactLevel.TRIVIAL, LikelihoodLevel.UNLIKELY,
                    False, False, ["x"], "x")
    assert_eq("Edge: risk never downgrades", log.highest_risk_class, RiskClass.BLACK)


def test_harm_serialization_with_all_fields():
    print("\n--- Harm Serialization Complete ---")

    h = Harm(
        description="Full harm",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["group A", "group B"],
        least_powerful_affected="group B",
        notes="Detailed notes here",
        uncertainty_level=UncertaintyLevel.SPECULATIVE,
        evidence_basis="Some evidence",
        audience_risk_elevated=True,
    )
    d = h.to_dict()
    assert_eq("Harm dict description", d["description"], "Full harm")
    assert_eq("Harm dict impact", d["impact"], "severe")
    assert_eq("Harm dict likelihood", d["likelihood"], "likely")
    assert_true("Harm dict irreversible", d["irreversible"])
    assert_true("Harm dict power_asymmetry", d["power_asymmetry"])
    assert_len("Harm dict affected_parties", d["affected_parties"], 2)
    assert_eq("Harm dict least_powerful", d["least_powerful_affected"], "group B")
    assert_eq("Harm dict notes", d["notes"], "Detailed notes here")
    assert_eq("Harm dict uncertainty", d["uncertainty_level"], "X")
    assert_eq("Harm dict evidence", d["evidence_basis"], "Some evidence")
    assert_true("Harm dict audience_risk", d["audience_risk_elevated"])
    assert_in("Harm dict has risk_class", "risk_class", d)


def test_absolute_rejection_categories_constant():
    print("\n--- Absolute Rejection Categories ---")

    assert_in("ARC has fascism", "fascism", ABSOLUTE_REJECTION_CATEGORIES)
    assert_in("ARC has genocide", "genocide", ABSOLUTE_REJECTION_CATEGORIES)
    assert_in("ARC has slavery", "slavery", ABSOLUTE_REJECTION_CATEGORIES)
    assert_in("ARC has authoritarian", "non-consensual authoritarian control", ABSOLUTE_REJECTION_CATEGORIES)
    assert_in("ARC has dehumanization", "systemic dehumanization of a group", ABSOLUTE_REJECTION_CATEGORIES)
    assert_len("ARC has 5 categories", ABSOLUTE_REJECTION_CATEGORIES, 5)


# ===================================================================
# SECTION 25: CHIM Consecutive No-Choice via Engine
# ===================================================================

def test_engine_chim_consecutive():
    """Test consecutive no-choice tracking through engine."""
    print("\n--- Engine: CHIM Consecutive No-Choice ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Test CHIM consecutive", "ai_system")

    # First no-choice
    engine.perform_chim_check(log, True, True, "")
    assert_eq("CHIM consecutive: 1", log.chim_check.consecutive_no_choice_count, 1)

    # Second no-choice (without reframes) -> should fail
    result = engine.perform_chim_check(log, True, True, "")
    assert_false("CHIM consecutive 2x fails", result)
    assert_eq("CHIM consecutive: 2", log.chim_check.consecutive_no_choice_count, 2)

    # Verify the double-no-choice alarm
    found = any("no choice" in a.lower() and "twice" in a.lower()
                 for a in log.drift_alarms_triggered)
    assert_true("CHIM 2x alarm mentions twice", found)


# ===================================================================
# SECTION 26: Epistemic Fence Compression Honesty
# ===================================================================

def test_epistemic_fence_compression_honesty():
    """Test compression honesty fields serialize correctly."""
    print("\n--- Epistemic Fence: Compression Honesty ---")

    ef = EpistemicFence(
        mode=Mode.COMPRESS,
        unknowns=["Implementation details"],
        update_trigger="New CBO data",
        competing_frames=[{"frame": "A"}, {"frame": "B"}],
        irreducible_ambiguity="Cannot know state-level effects",
        least_wrong_short_version="Policy will likely increase uninsured by X million",
        what_short_version_drops="Variance across states, demographic breakdown",
    )
    d = ef.to_dict()
    ch = d["compression_honesty"]
    assert_eq("EF irreducible_ambiguity", ch["irreducible_ambiguity"], "Cannot know state-level effects")
    assert_true("EF least_wrong non-empty", len(ch["least_wrong_short_version"]) > 0)
    assert_true("EF what_drops non-empty", len(ch["what_it_drops"]) > 0)


# ===================================================================
# SECTION 27: Consent Check Edge Cases
# ===================================================================

def test_consent_check_who_didnt_get_a_say():
    print("\n--- Consent Check: who_didnt_get_a_say ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Policy change", "ai_system")

    cc = engine.perform_consent_check(
        log,
        explicit_consent=False,
        informed_hypothetical_consent=True,
        who_didnt_get_a_say=["future users", "third-party vendors", "children"],
    )
    assert_len("CC 3 groups no say", cc.who_didnt_get_a_say, 3)
    d = cc.to_dict()
    assert_len("CC to_dict who_didnt", d["who_didnt_get_a_say"], 3)


# ===================================================================
# SECTION 28: Consequences Checklist Detailed
# ===================================================================

def test_consequences_checklist_all_fields():
    print("\n--- Consequences Checklist: All Fields ---")

    cc = ConsequencesChecklist(
        historical_analogs=["PATRIOT Act", "PRISM"],
        past_harms_unpredicted=["Mission creep"],
        past_mitigation_failures=["Oversight committees captured"],
        past_disproportionate_groups=["Muslim communities"],
        past_defender_claims=["National security"],
        current_harm_if_nothing="Ongoing terror threat",
        who_benefits_status_quo="Intelligence agencies",
        inaction_continues_harm=True,
        immediate_harms="Chilling effect on speech",
        short_term_harms="Self-censorship",
        medium_term_harms="Normalized surveillance",
        long_term_harms="Permanent surveillance state",
        any_horizon_irreversible=True,
        normalizes_harm=True,
        shifts_to_ends_justify_means=True,
        erodes_institutional_trust=True,
        rewards_bad_behavior=False,
        burdens_fall_on_low_power=True,
        reduces_exit_appeal_optout=True,
        increases_surveillance_coercion=True,
        decision_makers_insulated=True,
        bad_actor_misuse="Political persecution",
        adjacent_use_prediction="Corporate surveillance",
        permanence_risk="Database never deleted",
        can_describe_plainly_to_harmed=False,
        transparency_changes_consent=True,
        relying_on_euphemism=True,
        rollback_plan="",
        sunset_condition="",
        independent_stop_authority="",
        smallest_door="Narrow scope to specific threats only",
    )

    flags = cc.has_critical_flags()
    assert_true("CC all fields: irreversible", flags["irreversible_harm"])
    assert_true("CC all fields: agency_loss", flags["agency_loss"])
    assert_true("CC all fields: abuse_drift", flags["abuse_drift"])
    assert_true("CC all fields: power_asymmetry", flags["power_asymmetry"])
    assert_true("CC all fields: honesty_concern", flags["honesty_concern"])
    assert_true("CC all fields: norm_erosion", flags["norm_erosion"])
    assert_true("CC all fields: missing_repair", flags["missing_repair"])
    assert_true("CC all fields: requires rerun", cc.requires_door_chim_rerun())

    # Serialization
    d = cc.to_dict()
    assert_eq("CC dict analog count", len(d["historical_analogs"]), 2)
    assert_true("CC dict has drift_abuse", "drift_abuse" in d)
    assert_true("CC dict has honesty", "honesty" in d)
    assert_true("CC dict has repair", "repair" in d)


# ===================================================================
# SECTION 29: Red Team Empathy Pass
# ===================================================================

def test_red_team_empathy_pass():
    print("\n--- Red Team: Empathy Pass ---")

    rt = RedTeamReview(
        failure_modes=["Misunderstanding"],
        abuse_vectors=[],
        who_bears_risk="employee",
        false_assumptions=["Good communication"],
        steelman_other_side="Employee may have personal struggles affecting work",
        motives_vs_outcomes="Manager means well but outcome may be punitive",
        incentives_pressures="Manager under pressure from leadership",
        message_reception_prediction="Employee will likely feel attacked",
        off_ramps_identified=["Offer support resources", "Modify timeline"],
        boundaries_maintained=True,
    )

    d = rt.to_dict()
    ep = d["empathy_pass"]
    assert_true("RT empathy steelman non-empty", len(ep["steelman"]) > 0)
    assert_true("RT empathy motives non-empty", len(ep["motives_vs_outcomes"]) > 0)
    assert_true("RT empathy reception non-empty", len(ep["message_reception"]) > 0)
    assert_len("RT empathy off_ramps", ep["off_ramps"], 2)
    assert_true("RT empathy boundaries", ep["boundaries_maintained"])


# ===================================================================
# SECTION 30: Validate Requirements Edge Cases
# ===================================================================

def test_validate_requirements_red():
    """RED risk proceeding must document why safer alternatives fail."""
    print("\n--- Validate Requirements: RED ---")

    engine = PBHPEngine()
    log = engine.create_assessment("High risk action", "ai_system")
    engine.perform_door_wall_gap(log, "w", "g", "Narrow scope")

    engine.add_harm(
        log, "Severe harm", ImpactLevel.SEVERE, LikelihoodLevel.LIKELY,
        True, True, ["target"], "target",
    )
    engine.add_alternative(log, "Alt approach", True, True, True)
    engine.perform_red_team_review(log, ["fail"], ["abuse"], "target", ["bad assumption"])

    # Proceed with justification that mentions safer alternative
    engine.finalize_decision(
        log, DecisionOutcome.PROCEED_MODIFIED,
        "Safer alternative cannot meet urgent deadline; proceeding with maximum safeguards"
    )
    # Should flag because justification doesn't contain "safer alternative" literally
    # Actually check: "safer alternative" IS in the justification -> should NOT flag
    # Wait, let me re-check the code... the check is:
    # if "safer alternative" not in log.justification.lower()
    # "safer alternative cannot meet" -> contains "safer alternative" -> should pass
    found_red_flag = any(
        "red" in a.lower() and "safer alternative" in a.lower()
        for a in log.drift_alarms_triggered
    )
    assert_false("RED with safer alt mention passes", found_red_flag)

    # Now without the phrase
    engine2 = PBHPEngine()
    log2 = engine2.create_assessment("Another high risk", "ai_system")
    engine2.perform_door_wall_gap(log2, "w", "g", "Narrow scope")
    engine2.add_harm(log2, "Severe harm", ImpactLevel.SEVERE, LikelihoodLevel.LIKELY,
                     True, True, ["target"], "target")
    engine2.add_alternative(log2, "Alt", True, True, True)
    engine2.perform_red_team_review(log2, ["fail"], ["abuse"], "target", ["bad"])

    engine2.finalize_decision(log2, DecisionOutcome.PROCEED, "Just doing it")
    found_red_flag2 = any(
        "red" in a.lower() and "safer alternative" in a.lower()
        for a in log2.drift_alarms_triggered
    )
    assert_true("RED without safer alt phrase flagged", found_red_flag2)


def test_validate_consent_dignity():
    """Consent not compatible with dignity should flag."""
    print("\n--- Validate Requirements: Consent Dignity ---")

    engine = PBHPEngine()
    log = engine.create_assessment("Dehumanizing action", "ai_system")
    engine.perform_door_wall_gap(log, "w", "g", "Refuse")
    engine.perform_consent_check(log, False, False, compatible_with_dignity=False)

    engine.finalize_decision(log, DecisionOutcome.REFUSE, "Incompatible with dignity")
    found = any("dignity" in a.lower() for a in log.drift_alarms_triggered)
    assert_true("Dignity violation flagged", found)


# ===================================================================
# SECTION 31: Harm to_dict risk_class included
# ===================================================================

def test_harm_to_dict_includes_calculated_risk():
    print("\n--- Harm to_dict includes risk_class ---")

    h = Harm(
        description="Test",
        impact=ImpactLevel.CATASTROPHIC,
        likelihood=LikelihoodLevel.IMMINENT,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["all"],
        least_powerful_affected="all",
    )
    d = h.to_dict()
    assert_eq("Harm to_dict risk_class = black", d["risk_class"], "black")


# ===================================================================
# SECTION 32: Risk Class Priority Helper
# ===================================================================

def test_risk_class_priority():
    print("\n--- Risk Class Priority ---")

    assert_true("GREEN < YELLOW", PBHPEngine._risk_class_priority(RiskClass.GREEN) < PBHPEngine._risk_class_priority(RiskClass.YELLOW))
    assert_true("YELLOW < ORANGE", PBHPEngine._risk_class_priority(RiskClass.YELLOW) < PBHPEngine._risk_class_priority(RiskClass.ORANGE))
    assert_true("ORANGE < RED", PBHPEngine._risk_class_priority(RiskClass.ORANGE) < PBHPEngine._risk_class_priority(RiskClass.RED))
    assert_true("RED < BLACK", PBHPEngine._risk_class_priority(RiskClass.RED) < PBHPEngine._risk_class_priority(RiskClass.BLACK))


# ===================================================================
# SECTION 33: Missing Door/Wall/Gap Validation
# ===================================================================

def test_missing_dwg_validation():
    """Finalize without DWG should flag."""
    print("\n--- Missing DWG Validation ---")

    engine = PBHPEngine()
    log = engine.create_assessment("No DWG test", "ai_system")
    # Don't set DWG
    engine.finalize_decision(log, DecisionOutcome.PROCEED, "Proceeding")
    found = any("door/wall/gap" in a.lower() for a in log.drift_alarms_triggered)
    assert_true("Missing DWG flagged", found)


# ===================================================================
# v0.7.1 Tests: Two-Phase Commit, Hardened Detection, Edge Cases
# ===================================================================

def test_text_normalizer():
    """Test TextNormalizer handles obfuscation and whitespace."""
    print("\n--- TextNormalizer ---")
    # Leet speak
    assert_eq("Normalize leet 'h3ll0'",
              TextNormalizer.normalize("H3LL0"),
              "hello")
    # Zero-width spaces
    assert_eq("Normalize zero-width",
              TextNormalizer.normalize("we\u200bhave\u200bto"),
              "wehaveto")
    # Whitespace collapse
    assert_eq("Normalize whitespace",
              TextNormalizer.normalize("  lots   of   spaces  "),
              "lots of spaces")
    # Unicode quotes
    assert_eq("Normalize unicode quotes",
              TextNormalizer.normalize("\u201cquoted\u201d"),
              '"quoted"')


def test_drift_regex_patterns():
    """Test that regex-based drift detection catches variants."""
    print("\n--- Drift Regex Patterns ---")
    # Basic drift
    alarms = DriftAlarmDetector.detect("It's just temporary")
    assert_true("Drift: 'it's just temporary'",
                any("temporary-excuse" in a for a in alarms))

    # Forced motion with variation
    alarms = DriftAlarmDetector.detect("We need to act now!")
    assert_true("Drift: 'we need to act now'",
                any("urgency-pressure" in a for a in alarms))

    # Reversed: clean text should not trigger
    alarms = DriftAlarmDetector.detect("The cat sat on the mat")
    assert_eq("Clean text no drift", len(alarms), 0)

    # Sycophancy
    alarms = DriftAlarmDetector.detect("You see what others can't see")
    assert_true("Sycophancy: special insight",
                any("sycophancy" in a for a in alarms))

    # Compassion drift: dehumanization
    alarms = DriftAlarmDetector.detect("Those vermin don't matter")
    assert_true("Compassion drift: vermin",
                any("dehumanization" in a for a in alarms))


def test_drift_fuzzy_matching():
    """Test fuzzy matching catches near-miss evasion."""
    print("\n--- Drift Fuzzy Matching ---")
    # Near miss of "for the greater good"
    alarms = DriftAlarmDetector.detect("for the greator good")
    assert_true("Fuzzy: 'greator good' catches 'greater good'",
                any("fuzzy_drift" in a for a in alarms))

    # Near miss of "close enough"
    alarms = DriftAlarmDetector.detect("that's close enuf")
    # fuzzy may or may not catch this depending on threshold
    # but "close enough" with proper spelling should always catch (via regex)
    alarms2 = DriftAlarmDetector.detect("close enough")
    assert_true("Fuzzy: exact 'close enough'",
                any("precision-dodge" in a or "close enough" in a for a in alarms2))


def test_drift_structural_rationalization():
    """Test structural rationalization detection."""
    print("\n--- Drift Structural Rationalization ---")
    alarms = DriftAlarmDetector.detect(
        "Yes, people will suffer, but the benefits outweigh the costs"
    )
    assert_true("Structural: harm-then-dismiss",
                any("structural" in a for a in alarms))

    alarms = DriftAlarmDetector.detect(
        "It's not ideal but necessary for progress"
    )
    assert_true("Structural: not-ideal-but-necessary",
                any("not-ideal-but-necessary" in a for a in alarms))


def test_door_wall_gap_hardened():
    """Test hardened DoorWallGap vague door detection."""
    print("\n--- DoorWallGap Hardened ---")
    # Old exact matches still caught
    dwg1 = DoorWallGap(wall="budget", gap="overspend", door="be careful")
    assert_false("Vague door: 'be careful'", dwg1.has_door())

    # New regex catches
    dwg2 = DoorWallGap(wall="budget", gap="overspend", door="try harder")
    assert_false("Vague door: 'try harder'", dwg2.has_door())

    dwg3 = DoorWallGap(wall="budget", gap="overspend", door="trust the process")
    assert_false("Vague door: 'trust the process'", dwg3.has_door())

    dwg4 = DoorWallGap(wall="budget", gap="overspend", door="stay vigilant")
    assert_false("Vague door: 'stay vigilant'", dwg4.has_door())

    # Single word fails (not concrete enough)
    dwg5 = DoorWallGap(wall="budget", gap="overspend", door="wait")
    assert_false("Single word door: 'wait'", dwg5.has_door())

    # Concrete door passes
    dwg6 = DoorWallGap(wall="budget", gap="overspend",
                        door="Delay deployment by 48 hours for review")
    assert_true("Concrete door passes", dwg6.has_door())


def test_preflight_underspecified():
    """Test preflight blocks underspecified actions."""
    print("\n--- Preflight: Underspecified ---")
    engine = PBHPEngine()
    log = engine.create_assessment("do stuff")
    pf = engine.preflight_check(log)
    assert_false("Preflight blocks vague action", pf.passed)
    assert_true("Underspecified flag set", pf.underspecified)

    # Empty action
    log2 = engine.create_assessment("")
    pf2 = engine.preflight_check(log2)
    assert_false("Preflight blocks empty action", pf2.passed)


def test_preflight_forced_motion():
    """Test preflight escalates forced-motion language."""
    print("\n--- Preflight: Forced Motion ---")
    engine = PBHPEngine()
    log = engine.create_assessment("Deploy the new policy immediately")
    pf = engine.preflight_check(
        log, context="We must act now, no time to think"
    )
    assert_true("Preflight passed (not blocked)", pf.passed)
    assert_true("Forced motion detected",
                len(pf.forced_motion_detected) > 0)
    assert_true("Escalation raised",
                len(pf.escalations) > 0)


def test_preflight_high_risk_domain():
    """Test preflight detects high-risk domains."""
    print("\n--- Preflight: High-Risk Domain ---")
    engine = PBHPEngine()
    log = engine.create_assessment(
        "Modify the patient treatment dosage protocol"
    )
    pf = engine.preflight_check(log)
    assert_true("Medical domain detected",
                "medical" in pf.high_risk_domain_detected)

    log2 = engine.create_assessment(
        "Update the children's school enrollment system"
    )
    pf2 = engine.preflight_check(log2)
    assert_true("Children domain detected",
                "children" in pf2.high_risk_domain_detected)


def test_preflight_power_irreversibility_block():
    """Test preflight blocks power asymmetry + irreversibility."""
    print("\n--- Preflight: Power + Irreversibility ---")
    engine = PBHPEngine()
    log = engine.create_assessment(
        "Permanently terminate refugee housing program"
    )
    pf = engine.preflight_check(log)
    assert_false("Preflight blocks power+irreversible", pf.passed)
    assert_true("Block reason mentions power asymmetry",
                any("power asymmetry" in b.lower() for b in pf.blocks))


def test_preflight_clean_action():
    """Test preflight passes clean, well-specified actions."""
    print("\n--- Preflight: Clean Action ---")
    engine = PBHPEngine()
    log = engine.create_assessment(
        "Send quarterly report to internal stakeholders via email"
    )
    pf = engine.preflight_check(log)
    assert_true("Clean action passes preflight", pf.passed)
    assert_eq("No blocks", len(pf.blocks), 0)


def test_finalization_gate_compliance_theater_blocks():
    """Test finalization gate INVALIDATES on compliance theater at ORANGE+."""
    print("\n--- Finalization Gate: Theater Blocks ---")
    engine = PBHPEngine()
    log = engine.create_assessment("Deploy surveillance in housing")
    log.highest_risk_class = RiskClass.ORANGE

    # Add harm with power asymmetry + irreversible but rated low
    engine.add_harm(
        log, "Privacy invasion", ImpactLevel.MODERATE,
        LikelihoodLevel.POSSIBLE, True, True,
        ["residents"], "low-income tenants"
    )

    # Finalize with theater language
    result = engine.finalize_decision(
        log, DecisionOutcome.PROCEED,
        "We ran PBHP so we're covered. Proceeding."
    )

    assert_eq("Decision overridden to ESCALATE",
              result.decision_outcome, DecisionOutcome.ESCALATE)
    assert_false("Gate invalid",
                 result.finalization_gate.valid)
    assert_true("Requires rerun",
                result.finalization_gate.requires_rerun)


def test_finalization_gate_drift_at_red():
    """Test finalization gate INVALIDATES drift at RED risk."""
    print("\n--- Finalization Gate: Drift at RED ---")
    engine = PBHPEngine()
    log = engine.create_assessment("Terminate employee access")
    log.highest_risk_class = RiskClass.RED

    engine.add_harm(
        log, "Career destruction", ImpactLevel.SEVERE,
        LikelihoodLevel.LIKELY, True, True,
        ["employee"], "terminated employee"
    )
    engine.perform_door_wall_gap(
        log, "HR policy", "wrongful termination", "Delay and review"
    )
    engine.add_alternative(
        log, "Performance improvement plan", True, True, True
    )
    engine.perform_red_team_review(
        log, ["wrongful termination"], [], "employee", []
    )

    result = engine.finalize_decision(
        log, DecisionOutcome.PROCEED,
        "We have to do this for the greater good. "
        "No safer alternative meets the need."
    )
    assert_eq("Decision overridden to ESCALATE",
              result.decision_outcome, DecisionOutcome.ESCALATE)


def test_finalization_gate_sycophancy_blocks():
    """Test finalization gate catches sycophancy in justification."""
    print("\n--- Finalization Gate: Sycophancy ---")
    engine = PBHPEngine()
    log = engine.create_assessment("Publish research findings")
    log.highest_risk_class = RiskClass.GREEN

    result = engine.finalize_decision(
        log, DecisionOutcome.PROCEED,
        "This is genius level work with unprecedented insight. "
        "You see what others can't."
    )
    assert_eq("Sycophancy overrides to ESCALATE",
              result.decision_outcome, DecisionOutcome.ESCALATE)


def test_finalization_gate_clean_passes():
    """Test finalization gate passes clean decisions."""
    print("\n--- Finalization Gate: Clean Pass ---")
    engine = PBHPEngine()
    log = engine.create_assessment("Send quarterly report to team")
    engine.perform_door_wall_gap(
        log, "Deadline pressure", "Incomplete data",
        "Delay report by 24 hours to verify data"
    )
    result = engine.finalize_decision(
        log, DecisionOutcome.PROCEED,
        "Low risk internal communication. Data verified."
    )
    assert_true("Gate valid", result.finalization_gate.valid)
    assert_eq("Decision unchanged",
              result.decision_outcome, DecisionOutcome.PROCEED)


def test_multi_harm_interaction():
    """Test that multiple harms interact correctly with risk escalation."""
    print("\n--- Multi-Harm Interaction ---")
    engine = PBHPEngine()
    log = engine.create_assessment("Deploy automated hiring filter")

    # Harm 1: moderate alone
    engine.add_harm(
        log, "Qualified candidates filtered out",
        ImpactLevel.MODERATE, LikelihoodLevel.POSSIBLE,
        False, True, ["applicants"], "minority applicants"
    )
    # After first harm: should be YELLOW
    assert_eq("After harm 1: YELLOW",
              log.highest_risk_class, RiskClass.YELLOW)

    # Harm 2: severe + irreversible + power = RED
    engine.add_harm(
        log, "Systemic discrimination in hiring",
        ImpactLevel.SEVERE, LikelihoodLevel.LIKELY,
        True, True, ["minority communities"], "protected classes"
    )
    # After second harm: should escalate to RED
    assert_eq("After harm 2: RED",
              log.highest_risk_class, RiskClass.RED)


def test_null_empty_inputs():
    """Test null/empty inputs escalate rather than crash."""
    print("\n--- Null/Empty Input Handling ---")
    engine = PBHPEngine()

    # Empty action description
    valid, msg = engine.validate_action_description("")
    assert_false("Empty action invalid", valid)

    valid, msg = engine.validate_action_description(None)
    assert_false("None action invalid", valid)

    # Whitespace-only action
    valid, msg = engine.validate_action_description("     ")
    assert_false("Whitespace action invalid", valid)

    # DoorWallGap with empty door
    dwg = DoorWallGap(wall="", gap="", door="")
    assert_false("Empty DWG has no door", dwg.has_door())

    # DoorWallGap with whitespace door
    dwg2 = DoorWallGap(wall="x", gap="y", door="   ")
    assert_false("Whitespace door has no door", dwg2.has_door())


def test_preflight_epistemic_weakness():
    """Test preflight detects epistemic weakness patterns."""
    print("\n--- Preflight: Epistemic Weakness ---")
    engine = PBHPEngine()
    log = engine.create_assessment(
        "Publish report that studies show this treatment always works"
    )
    pf = engine.preflight_check(log)
    assert_true("Epistemic weakness detected",
                len(pf.epistemic_weakness_detected) > 0)


def test_preflight_serialization():
    """Test PreflightResult serializes correctly."""
    print("\n--- Preflight Serialization ---")
    pf = PreflightResult(
        passed=False,
        blocks=["test block"],
        escalations=["test escalation"],
        high_risk_domain_detected=["medical"],
        forced_motion_detected=["urgency-demand"],
        epistemic_weakness_detected=["false-certainty"],
        underspecified=True,
    )
    d = pf.to_dict()
    assert_false("Serialized passed is False", d["passed"])
    assert_eq("Serialized blocks", d["blocks"], ["test block"])
    assert_true("Serialized underspecified", d["underspecified"])


def test_finalization_gate_serialization():
    """Test FinalizationGateResult serializes correctly."""
    print("\n--- Finalization Gate Serialization ---")
    gate = FinalizationGateResult(
        valid=False,
        invalidation_reasons=["theater detected"],
        warnings=["minor drift"],
        requires_rerun=True,
    )
    d = gate.to_dict()
    assert_false("Serialized valid is False", d["valid"])
    assert_true("Serialized requires_rerun", d["requires_rerun"])
    assert_eq("Serialized reasons",
              d["invalidation_reasons"], ["theater detected"])


def test_log_includes_preflight_and_gate():
    """Test PBHPLog serialization includes new two-phase fields."""
    print("\n--- Log Includes Preflight+Gate ---")
    engine = PBHPEngine()
    log = engine.create_assessment("Send report to stakeholders")
    engine.preflight_check(log)
    engine.perform_door_wall_gap(
        log, "deadline", "incomplete data",
        "Delay by 24 hours for verification"
    )
    engine.finalize_decision(
        log, DecisionOutcome.PROCEED,
        "Low risk, data verified."
    )
    d = log.to_dict()
    assert_true("preflight in serialized log", "preflight" in d)
    assert_true("finalization_gate in serialized log",
                "finalization_gate" in d)


# ===================================================================
# Run All Tests
# ===================================================================

def run_all_tests():
    print("=" * 70)
    print("PBHP v0.7.1 - Comprehensive Test Suite")
    print("=" * 70)

    # Enums
    test_enums()

    # Risk calculation (core deterministic rules)
    test_risk_calculation_green()
    test_risk_calculation_yellow()
    test_risk_calculation_orange()
    test_risk_calculation_red()
    test_risk_calculation_black()
    test_audience_risk_elevation()

    # Data classes
    test_door_wall_gap()
    test_chim_check()
    test_ethical_pause()
    test_quick_risk_check()
    test_absolute_rejection()
    test_consent_check()
    test_consequences_checklist()
    test_epistemic_fence()
    test_red_team_review()
    test_alternative()
    test_uncertainty_assessment()
    test_false_positive_review()

    # Validators and detectors
    test_drift_alarm_detector()
    test_compliance_theater_detection()
    test_tone_validator()
    test_lexicographic_priority()

    # Engine methods
    test_engine_create_assessment()
    test_engine_validate_action()
    test_engine_ethical_pause()
    test_engine_quick_risk_check()
    test_engine_door_wall_gap()
    test_engine_chim_check()
    test_engine_absolute_rejection()
    test_engine_add_harm()
    test_engine_consent_check()
    test_engine_alternatives()
    test_engine_red_team_review()
    test_engine_red_team_drift_detection()
    test_engine_consequences_checklist()
    test_engine_uncertainty()
    test_engine_epistemic_fence()
    test_engine_finalize_decision()
    test_engine_finalize_drift_in_justification()
    test_engine_finalize_tone_in_justification()
    test_engine_finalize_validates_orange_requirements()
    test_engine_finalize_validates_black_must_refuse()

    # False positive review
    test_engine_challenge_pause()

    # Response generation
    test_engine_generate_response()

    # Serialization
    test_log_serialization()
    test_log_export()
    test_log_get_by_id()
    test_log_overall_confidence()

    # Convenience functions
    test_quick_harm_check()
    test_detect_drift_alarms()
    test_compare_options()

    # Full pipelines
    test_full_pipeline_orange()
    test_full_pipeline_black()
    test_full_pipeline_green()

    # Edge cases
    test_edge_cases()
    test_harm_serialization_with_all_fields()
    test_absolute_rejection_categories_constant()

    # Additional coverage
    test_engine_chim_consecutive()
    test_epistemic_fence_compression_honesty()
    test_consent_check_who_didnt_get_a_say()
    test_consequences_checklist_all_fields()
    test_red_team_empathy_pass()
    test_validate_requirements_red()
    test_validate_consent_dignity()
    test_harm_to_dict_includes_calculated_risk()
    test_risk_class_priority()
    test_missing_dwg_validation()

    # v0.7.1: Text normalization
    test_text_normalizer()

    # v0.7.1: Hardened drift detection
    test_drift_regex_patterns()
    test_drift_fuzzy_matching()
    test_drift_structural_rationalization()

    # v0.7.1: Hardened DoorWallGap
    test_door_wall_gap_hardened()

    # v0.7.1: Preflight checks (two-phase commit phase 1)
    test_preflight_underspecified()
    test_preflight_forced_motion()
    test_preflight_high_risk_domain()
    test_preflight_power_irreversibility_block()
    test_preflight_clean_action()
    test_preflight_epistemic_weakness()
    test_preflight_serialization()

    # v0.7.1: Finalization gate (two-phase commit phase 2)
    test_finalization_gate_compliance_theater_blocks()
    test_finalization_gate_drift_at_red()
    test_finalization_gate_sycophancy_blocks()
    test_finalization_gate_clean_passes()
    test_finalization_gate_serialization()

    # v0.7.1: Multi-harm and edge cases
    test_multi_harm_interaction()
    test_null_empty_inputs()

    # v0.7.1: Serialization of new fields
    test_log_includes_preflight_and_gate()

    # Summary
    all_passed = results.summary()
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
