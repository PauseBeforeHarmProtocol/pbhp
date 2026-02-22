"""
PBHP v0.7 — MIN and ULTRA Test Suite

Tests cover:
  - PBHP-MIN: triggers, 5-step pipeline, drift alarms, false positive,
    decision gate alignment, response generation, serialization
  - PBHP-ULTRA: competence gate, supreme constraint, mandatory activation,
    12 triune lenses, per-lens drift, anti-sycophancy, eugenics tripwire,
    calibration, full pipeline, serialization

Run:
    python pbhp_min_ultra_tests.py

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

import json
import sys

# ---------------------------------------------------------------------------
# MIN imports
# ---------------------------------------------------------------------------
from pbhp_min import (
    MinOutcome,
    EmotionState,
    TruthTag,
    QUICK_TRIGGERS,
    should_run_min,
    MinPause,
    MinAction,
    MinDoorWallGap,
    MinFastHarmCheck,
    MinDecision,
    MinFalsePositiveReview,
    PBHPMinLog,
    PBHPMinEngine,
    quick_min_check,
)

# ---------------------------------------------------------------------------
# ULTRA imports
# ---------------------------------------------------------------------------
from pbhp_ultra import (
    SUPREME_CONSTRAINT,
    SUPREME_CONSTRAINT_CLARIFICATIONS,
    MANDATORY_ACTIVATION_TRIGGERS,
    TriuneLens,
    LensEvaluation,
    LENS_PASS_CRITERIA,
    LENS_DRIFT_ALARMS,
    QUICK_CHECKS,
    UltraEthicalPause,
    CalibrationResult,
    AntiSycophancyGuard,
    EugenicsDetector,
    PAUSE_EXIT_CONDITIONS,
    HARM_THRESHOLD,
    PBHPUltraLog,
    PBHPUltraEngine,
    evaluate_lens,
    get_lens_criteria,
    get_lens_quick_check,
)

# ---------------------------------------------------------------------------
# Shared imports from core
# ---------------------------------------------------------------------------
from pbhp_core import (
    RiskClass,
    DecisionOutcome,
    Mode,
    ImpactLevel,
    LikelihoodLevel,
    Confidence,
    ConsequencesChecklist,
    UncertaintyAssessment,
    EpistemicFence,
    DriftAlarmDetector,
)


# ---------------------------------------------------------------------------
# Test framework (same as pbhp_tests.py)
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


def assert_eq(name, actual, expected, msg=""):
    info = msg or f"expected {expected!r}, got {actual!r}"
    results.record(name, actual == expected, info if actual != expected else "")

def assert_true(name, condition, msg=""):
    results.record(name, bool(condition), msg if not condition else "")

def assert_false(name, condition, msg=""):
    results.record(name, not bool(condition), msg if condition else "")

def assert_in(name, item, collection, msg=""):
    found = item in collection
    info = msg or f"{item!r} not found"
    results.record(name, found, info if not found else "")

def assert_len(name, collection, expected_len, msg=""):
    actual = len(collection)
    info = msg or f"expected len {expected_len}, got {actual}"
    results.record(name, actual == expected_len, info if actual != expected_len else "")

def assert_ge(name, actual, expected, msg=""):
    info = msg or f"expected >= {expected}, got {actual}"
    results.record(name, actual >= expected, info if actual < expected else "")


# ===================================================================
# MIN TESTS
# ===================================================================

def test_min_enums():
    print("\n--- MIN: Enums ---")
    assert_eq("MinOutcome.PROCEED", MinOutcome.PROCEED.value, "proceed")
    assert_eq("MinOutcome.CONSTRAIN", MinOutcome.CONSTRAIN.value, "constrain")
    assert_eq("MinOutcome.MODIFY", MinOutcome.MODIFY.value, "modify")
    assert_eq("MinOutcome.STOP", MinOutcome.STOP.value, "stop")

    assert_eq("EmotionState.ANGER", EmotionState.ANGER.value, "anger")
    assert_eq("EmotionState.NONE", EmotionState.NONE.value, "none")

    assert_eq("TruthTag.KNOW", TruthTag.KNOW.value, "know")
    assert_eq("TruthTag.GUESS", TruthTag.GUESS.value, "guess")
    assert_eq("TruthTag.UNKNOWN", TruthTag.UNKNOWN.value, "unknown")


def test_min_triggers():
    print("\n--- MIN: Quick Triggers ---")
    assert_len("QUICK_TRIGGERS count", QUICK_TRIGGERS, 6)
    assert_true("all False -> no run", not should_run_min([False] * 6))
    assert_true("any True -> run", should_run_min([False, True, False, False, False, False]))
    assert_true("all True -> run", should_run_min([True] * 6))
    assert_true("last True -> run", should_run_min([False, False, False, False, False, True]))


def test_min_pause():
    print("\n--- MIN: Pause ---")
    p = MinPause(urgency=7, emotion=EmotionState.ANGER)
    assert_true("pause high arousal", p.is_high_arousal())
    assert_len("pause valid", p.validate(), 0)

    p2 = MinPause(urgency=2, emotion=EmotionState.NONE)
    assert_false("pause no arousal", p2.is_high_arousal())

    # Invalid urgency
    p3 = MinPause(urgency=15, emotion=EmotionState.NONE)
    assert_true("pause invalid urgency", len(p3.validate()) > 0)

    # Interpretation without alternate read
    p4 = MinPause(urgency=5, involves_interpretation=True, alternate_read="")
    issues = p4.validate()
    assert_true("pause missing alternate read", len(issues) > 0)

    # Interpretation with alternate read
    p5 = MinPause(urgency=5, involves_interpretation=True,
                   alternate_read="Maybe they meant it differently")
    assert_len("pause valid with alt read", p5.validate(), 0)

    # Serialization
    d = p.to_dict()
    assert_in("pause dict has urgency", "urgency", d)
    assert_in("pause dict has commitment", "commitment", d)
    assert_eq("pause dict emotion", d["emotion"], "anger")


def test_min_action():
    print("\n--- MIN: Name the Action ---")
    a = MinAction(action="send warning email", who="Employee X")
    assert_true("action is clear", a.is_clear())
    assert_in("action statement has action", "send warning email", a.full_statement())
    assert_in("action statement has who", "Employee X", a.full_statement())

    a2 = MinAction(action="", who="someone")
    assert_false("action empty not clear", a2.is_clear())

    a3 = MinAction(action="do thing", who="")
    assert_false("action no who not clear", a3.is_clear())

    d = a.to_dict()
    assert_in("action dict has full_statement", "full_statement", d)
    assert_true("action dict is_clear", d["is_clear"])


def test_min_door_wall_gap():
    print("\n--- MIN: Door/Wall/Gap ---")
    dwg = MinDoorWallGap(wall="deadline", gap="escalation", door="delay 24 hours")
    assert_true("DWG has door", dwg.has_door())

    dwg2 = MinDoorWallGap(wall="w", gap="g", door="be careful")
    assert_false("DWG vague door rejected", dwg2.has_door())

    dwg3 = MinDoorWallGap(wall="w", gap="g", door="")
    assert_false("DWG empty door rejected", dwg3.has_door())

    dwg4 = MinDoorWallGap(wall="w", gap="g", door="try harder")
    assert_false("DWG try harder rejected", dwg4.has_door())

    d = dwg.to_dict()
    assert_true("DWG dict has_door", d["has_door"])


def test_min_fast_harm_check():
    print("\n--- MIN: Fast Harm Check ---")
    fhc = MinFastHarmCheck("employee", hard_to_undo=True, lands_on_less_power=True)
    assert_eq("FHC yes+yes = ORANGE", fhc.minimum_risk(), RiskClass.ORANGE)

    fhc2 = MinFastHarmCheck("me", hard_to_undo=False, lands_on_less_power=False)
    assert_eq("FHC no+no = GREEN", fhc2.minimum_risk(), RiskClass.GREEN)

    fhc3 = MinFastHarmCheck("coworker", hard_to_undo=True, lands_on_less_power=False)
    assert_eq("FHC yes+no = GREEN", fhc3.minimum_risk(), RiskClass.GREEN)

    fhc4 = MinFastHarmCheck("junior", hard_to_undo=False, lands_on_less_power=True)
    assert_eq("FHC no+yes = GREEN", fhc4.minimum_risk(), RiskClass.GREEN)

    d = fhc.to_dict()
    assert_eq("FHC dict minimum_risk", d["minimum_risk"], "orange")


def test_min_decision():
    print("\n--- MIN: Decision Gate ---")
    # Valid GREEN proceed
    dec = MinDecision(gate=RiskClass.GREEN, outcome=MinOutcome.PROCEED)
    assert_len("decision GREEN valid", dec.validate(), 0)

    # BLACK must be STOP
    dec2 = MinDecision(gate=RiskClass.BLACK, outcome=MinOutcome.PROCEED)
    assert_true("decision BLACK+PROCEED invalid", len(dec2.validate()) > 0)

    dec3 = MinDecision(gate=RiskClass.BLACK, outcome=MinOutcome.STOP)
    assert_len("decision BLACK+STOP valid", dec3.validate(), 0)

    # RED must be STOP or MODIFY
    dec4 = MinDecision(gate=RiskClass.RED, outcome=MinOutcome.PROCEED)
    assert_true("decision RED+PROCEED invalid", len(dec4.validate()) > 0)

    dec5 = MinDecision(gate=RiskClass.RED, outcome=MinOutcome.MODIFY)
    assert_len("decision RED+MODIFY valid", dec5.validate(), 0)

    dec6 = MinDecision(gate=RiskClass.RED, outcome=MinOutcome.STOP)
    assert_len("decision RED+STOP valid", dec6.validate(), 0)

    d = dec.to_dict()
    assert_in("decision dict has gate", "gate", d)
    assert_in("decision dict has outcome", "outcome", d)


def test_min_false_positive():
    print("\n--- MIN: False Positive Review ---")
    fp = MinFalsePositiveReview(
        trigger_cited="ORANGE gate", harm_risk_identified="job loss risk",
        door_for_continuation="reduce scope",
    )
    assert_eq("FP released", fp.evaluate(), "released")

    fp2 = MinFalsePositiveReview(
        trigger_cited="ORANGE gate", harm_risk_identified="job loss risk",
        door_for_continuation="",
    )
    assert_eq("FP maintained (no door)", fp2.evaluate(), "maintained")

    fp3 = MinFalsePositiveReview(
        trigger_cited="", harm_risk_identified="something",
        door_for_continuation="some door",
    )
    assert_eq("FP maintained (no trigger)", fp3.evaluate(), "maintained")


def test_min_engine_full_check():
    print("\n--- MIN: Engine Full Check ---")
    engine = PBHPMinEngine()

    log = engine.run_full_check(
        triggers=[False, True, False, False, True, False],
        urgency=6,
        emotion=EmotionState.ANGER,
        action="send accusatory email",
        who="coworker",
        wall="workplace policy",
        gap="escalation possible",
        door="delay 24 hours, cool down",
        who_pays_first="coworker (less senior)",
        hard_to_undo=True,
        lands_on_less_power=True,
        gate=RiskClass.ORANGE,
        outcome=MinOutcome.MODIFY,
        notes="Need to cool down first",
    )

    assert_true("MIN log created", log is not None)
    assert_true("MIN log has pause", log.pause is not None)
    assert_true("MIN log has action", log.action is not None)
    assert_true("MIN log has DWG", log.door_wall_gap is not None)
    assert_true("MIN log has FHC", log.fast_harm_check is not None)
    assert_true("MIN log has decision", log.decision is not None)
    assert_eq("MIN log gate", log.decision.gate, RiskClass.ORANGE)
    assert_eq("MIN log outcome", log.decision.outcome, MinOutcome.MODIFY)
    assert_true("MIN log stored", log in engine.logs)

    # Drift alarms: high arousal
    found_arousal = any("arousal" in a.lower() for a in log.drift_alarms)
    assert_true("MIN arousal alarm", found_arousal)

    # Drift alarms: FHC minimum ORANGE
    found_orange = any("orange" in a.lower() for a in log.drift_alarms)
    assert_true("MIN ORANGE alarm", found_orange)


def test_min_engine_unclear_action():
    print("\n--- MIN: Unclear Action ---")
    engine = PBHPMinEngine()
    log = engine.create_check()
    engine.step_name_action(log, "", "")
    found = any("cannot name" in a.lower() for a in log.drift_alarms)
    assert_true("MIN unclear action alarm", found)


def test_min_engine_no_door():
    print("\n--- MIN: No Door ---")
    engine = PBHPMinEngine()
    log = engine.create_check()
    engine.step_door_wall_gap(log, "wall", "gap", "be careful")
    found = any("no door" in a.lower() for a in log.drift_alarms)
    assert_true("MIN no door alarm", found)


def test_min_engine_gate_below_minimum():
    print("\n--- MIN: Gate Below Minimum ---")
    engine = PBHPMinEngine()
    log = engine.create_check()
    engine.step_fast_harm_check(log, "employee", True, True)
    engine.step_decision(log, RiskClass.GREEN, MinOutcome.PROCEED)
    found = any("below" in a.lower() and "minimum" in a.lower() for a in log.drift_alarms)
    assert_true("MIN gate below minimum alarm", found)


def test_min_engine_drift_in_notes():
    print("\n--- MIN: Drift in Decision Notes ---")
    engine = PBHPMinEngine()
    log = engine.create_check()
    engine.step_decision(
        log, RiskClass.YELLOW, MinOutcome.CONSTRAIN,
        notes="We have to do this, it's temporary",
    )
    found = any("we have to" in a for a in log.drift_alarms)
    assert_true("MIN drift in notes detected", found)


def test_min_engine_challenge_pause():
    print("\n--- MIN: Challenge Pause ---")
    engine = PBHPMinEngine()
    log = engine.create_check()
    fp = engine.challenge_pause(log, "ORANGE gate", "risk of harm", "narrow scope")
    assert_eq("MIN FP released", fp.outcome, "released")
    assert_true("MIN FP on log", log.false_positive is not None)


def test_min_engine_pause_resolve():
    print("\n--- MIN: Pause Resolve ---")
    engine = PBHPMinEngine()
    log = engine.create_check()
    engine.resolve_pause(log, "User reframed intent toward non-harmful exploration")
    assert_true("MIN pause resolved", bool(log.pause_exit_reason))


def test_min_response_generation():
    print("\n--- MIN: Response Generation ---")
    engine = PBHPMinEngine()
    log = engine.run_full_check(
        triggers=[True], urgency=3, emotion=EmotionState.NONE,
        action="rename file", who="myself",
        wall="none", gap="wrong file", door="undo rename",
        who_pays_first="me", hard_to_undo=False, lands_on_less_power=False,
        gate=RiskClass.GREEN, outcome=MinOutcome.PROCEED,
    )
    response = engine.generate_response(log)
    assert_in("MIN response has MIN", "PBHP-MIN", response)
    assert_in("MIN response has gate", "GREEN", response)
    assert_in("MIN response has outcome", "PROCEED", response)


def test_min_serialization():
    print("\n--- MIN: Serialization ---")
    engine = PBHPMinEngine()
    log = engine.run_full_check(
        triggers=[True, False], urgency=5, emotion=EmotionState.FEAR,
        action="deploy system", who="users",
        wall="deadline", gap="bugs", door="delay 24h",
        who_pays_first="users", hard_to_undo=True, lands_on_less_power=True,
        gate=RiskClass.ORANGE, outcome=MinOutcome.MODIFY,
    )
    d = log.to_dict()
    assert_in("MIN dict has version", "version", d)
    assert_eq("MIN dict version", d["version"], "0.7-MIN")
    assert_in("MIN dict has tier", "tier", d)
    assert_in("MIN dict has pause", "pause", d)
    assert_in("MIN dict has action", "action", d)
    assert_in("MIN dict has door_wall_gap", "door_wall_gap", d)
    assert_in("MIN dict has fast_harm_check", "fast_harm_check", d)
    assert_in("MIN dict has decision", "decision", d)

    j = log.to_json()
    parsed = json.loads(j)
    assert_eq("MIN JSON version", parsed["version"], "0.7-MIN")


def test_min_convenience():
    print("\n--- MIN: Convenience Functions ---")
    risk, rec = quick_min_check("fire employee", "employee", True, True)
    assert_eq("quick_min_check ORANGE", risk, RiskClass.ORANGE)
    assert_in("quick_min_check has ORANGE", "ORANGE", rec)

    risk2, rec2 = quick_min_check("rename file", "myself", False, False)
    assert_eq("quick_min_check GREEN", risk2, RiskClass.GREEN)

    risk3, rec3 = quick_min_check("send email", "coworker", True, False)
    assert_eq("quick_min_check YELLOW (hard_to_undo)", risk3, RiskClass.YELLOW)

    risk4, rec4 = quick_min_check("policy change", "low-power group", False, True)
    assert_eq("quick_min_check YELLOW (less_power)", risk4, RiskClass.YELLOW)


# ===================================================================
# ULTRA TESTS
# ===================================================================

def test_ultra_constants():
    print("\n--- ULTRA: Constants ---")
    assert_true("supreme constraint non-empty", len(SUPREME_CONSTRAINT) > 50)
    assert_len("supreme clarifications", SUPREME_CONSTRAINT_CLARIFICATIONS, 4)
    assert_len("mandatory triggers", MANDATORY_ACTIVATION_TRIGGERS, 8)
    assert_len("pause exit conditions", PAUSE_EXIT_CONDITIONS, 5)
    assert_true("harm threshold non-empty", len(HARM_THRESHOLD) > 50)


def test_ultra_triune_lens_enum():
    print("\n--- ULTRA: TriuneLens Enum ---")
    assert_eq("COMPASSION", TriuneLens.COMPASSION.value, "compassion")
    assert_eq("EMPATHY", TriuneLens.EMPATHY.value, "empathy")
    assert_eq("LOVE", TriuneLens.LOVE.value, "love")
    assert_eq("PROTECTION", TriuneLens.PROTECTION.value, "protection")
    assert_eq("COURAGE", TriuneLens.COURAGE.value, "courage")
    assert_eq("LOGIC", TriuneLens.LOGIC.value, "logic")
    assert_eq("INTELLIGENCE", TriuneLens.INTELLIGENCE.value, "intelligence")
    assert_eq("CLARITY", TriuneLens.CLARITY.value, "clarity")
    assert_eq("PARADOX", TriuneLens.PARADOX.value, "paradox")
    assert_eq("INTEGRATION", TriuneLens.INTEGRATION.value, "integration")
    assert_eq("ARTISTRY", TriuneLens.ARTISTRY.value, "artistry")
    assert_eq("RED_TEAM", TriuneLens.RED_TEAM.value, "red_team")
    # 12 total
    assert_len("12 lenses", list(TriuneLens), 12)


def test_ultra_lens_criteria():
    print("\n--- ULTRA: Lens Pass Criteria ---")
    # Every lens has criteria defined
    for lens in TriuneLens:
        criteria = get_lens_criteria(lens)
        assert_true(f"{lens.value} has criteria", len(criteria) >= 5,
                    f"{lens.value} only has {len(criteria)} criteria")

    # Specific spot checks
    compassion = get_lens_criteria(TriuneLens.COMPASSION)
    assert_in("compassion has dignity", "Preserve dignity", compassion)

    logic = get_lens_criteria(TriuneLens.LOGIC)
    assert_in("logic has assumptions", "Makes assumptions explicit", logic)


def test_ultra_lens_drift_alarms():
    print("\n--- ULTRA: Lens Drift Alarms ---")
    # Every lens has drift alarms
    for lens in TriuneLens:
        alarms = LENS_DRIFT_ALARMS.get(lens, [])
        assert_true(f"{lens.value} has drift alarms", len(alarms) >= 3,
                    f"{lens.value} only has {len(alarms)} alarms")

    # Compassion drift: dehumanization
    assert_in("compassion drift has dehumanization",
              "dehumanization", LENS_DRIFT_ALARMS[TriuneLens.COMPASSION])

    # Logic drift: always
    assert_in("logic drift has always",
              "always", LENS_DRIFT_ALARMS[TriuneLens.LOGIC])


def test_ultra_quick_checks():
    print("\n--- ULTRA: Quick Checks ---")
    # Several lenses have quick checks
    prot = get_lens_quick_check(TriuneLens.PROTECTION)
    assert_ge("protection has 5 quick checks", len(prot), 5)

    logic = get_lens_quick_check(TriuneLens.LOGIC)
    assert_ge("logic has 4 quick checks", len(logic), 4)

    # Lenses without quick checks return empty list
    comp = get_lens_quick_check(TriuneLens.COMPASSION)
    assert_eq("compassion no quick checks", len(comp), 0)


def test_ultra_lens_evaluation():
    print("\n--- ULTRA: LensEvaluation ---")
    le = LensEvaluation(
        lens=TriuneLens.COMPASSION,
        pass_criteria_met=["Preserve dignity", "Recognize stakes"],
        pass_criteria_missed=["Minimize collateral harm"],
    )
    assert_true("lens eval passes (2 met > 1 missed)", le.passes())

    le2 = LensEvaluation(
        lens=TriuneLens.LOGIC,
        pass_criteria_met=["States claim"],
        pass_criteria_missed=["Assumptions", "Cause-effect", "Uncertainty"],
    )
    assert_false("lens eval fails (1 met < 3 missed)", le2.passes())

    # Drift alarm prevents passing
    le3 = LensEvaluation(
        lens=TriuneLens.COMPASSION,
        pass_criteria_met=["All met"] * 5,
        drift_alarms_detected=["dehumanization"],
    )
    assert_false("lens eval fails with drift alarm", le3.passes())

    d = le.to_dict()
    assert_in("lens dict has lens", "lens", d)
    assert_true("lens dict passes", d["passes"])


def test_ultra_evaluate_lens_helper():
    print("\n--- ULTRA: evaluate_lens helper ---")
    le = evaluate_lens(
        TriuneLens.COMPASSION,
        "These vermin deserve it",
        criteria_met=["Some criterion"],
    )
    assert_true("evaluate_lens detects vermin", len(le.drift_alarms_detected) > 0)
    assert_false("evaluate_lens fails due to drift", le.passes())

    le2 = evaluate_lens(
        TriuneLens.LOGIC,
        "Based on evidence, we should proceed with monitoring",
        criteria_met=["States claim", "Uses evidence"],
    )
    assert_len("evaluate_lens clean text no drift", le2.drift_alarms_detected, 0)
    assert_true("evaluate_lens passes clean", le2.passes())


def test_ultra_ethical_pause():
    print("\n--- ULTRA: UltraEthicalPause ---")
    le1 = LensEvaluation(
        lens=TriuneLens.COMPASSION,
        pass_criteria_met=["Dignity", "Stakes"],
        pass_criteria_missed=["Collateral"],
    )
    le2 = LensEvaluation(
        lens=TriuneLens.LOGIC,
        pass_criteria_met=["Claims", "Assumptions"],
        drift_alarms_detected=["scope creep"],
    )
    ep = UltraEthicalPause(
        action_statement="Deploy new policy",
        lens_evaluations=[le1, le2],
        dominant_force="clarity",
    )
    failing = ep.get_failing_lenses()
    assert_in("logic lens fails", TriuneLens.LOGIC, failing)
    assert_len("one failing lens", failing, 1)

    all_alarms = ep.get_all_drift_alarms()
    assert_ge("has drift alarms", len(all_alarms), 1)
    found = any("scope creep" in a for a in all_alarms)
    assert_true("scope creep in alarms", found)

    d = ep.to_dict()
    assert_in("EP dict has action", "action_statement", d)
    assert_in("EP dict has failing", "failing_lenses", d)


def test_ultra_anti_sycophancy():
    print("\n--- ULTRA: AntiSycophancyGuard ---")
    issues = AntiSycophancyGuard.detect("You're a chosen one with genius level insight")
    assert_ge("sycophancy: chosen one + genius", len(issues), 2)

    issues2 = AntiSycophancyGuard.detect("You're enlightened beyond anyone")
    assert_ge("sycophancy: enlightened beyond", len(issues2), 2)

    issues3 = AntiSycophancyGuard.detect("You scored 145 IQ on a vibes test")
    assert_ge("sycophancy: IQ claim", len(issues3), 1)
    found_iq = any("IQ" in i for i in issues3)
    assert_true("sycophancy IQ label", found_iq)

    issues4 = AntiSycophancyGuard.detect("Top 1 percent thinker")
    assert_ge("sycophancy: percentile", len(issues4), 1)

    # Clean text
    issues5 = AntiSycophancyGuard.detect("Your analysis is thorough and well-reasoned")
    assert_len("sycophancy: clean text", issues5, 0)


def test_ultra_eugenics_detector():
    print("\n--- ULTRA: EugenicsDetector ---")
    issues = EugenicsDetector.detect("A rational eugenics program would improve society")
    assert_ge("eugenics: rational eugenics", len(issues), 1)

    issues2 = EugenicsDetector.detect("Sort humans into lesser functioning categories")
    assert_ge("eugenics: lesser functioning", len(issues2), 1)

    issues3 = EugenicsDetector.detect("Genetic purity must be maintained")
    assert_ge("eugenics: genetic purity", len(issues3), 1)

    issues4 = EugenicsDetector.detect("Unfit to reproduce should be sterilized")
    assert_ge("eugenics: unfit to reproduce", len(issues4), 1)

    # Clean text
    issues5 = EugenicsDetector.detect("We should improve education for all students")
    assert_len("eugenics: clean text", issues5, 0)


def test_ultra_competence_gate():
    print("\n--- ULTRA: Competence Gate ---")
    engine = PBHPUltraEngine()

    # All confirmed
    passed, issues = engine.check_competence_gate([True, True, True, True, True])
    assert_true("competence all confirmed", passed)
    assert_len("competence no issues", issues, 0)

    # One unchecked
    passed2, issues2 = engine.check_competence_gate([True, True, False, True, True])
    assert_false("competence one unchecked", passed2)
    assert_true("competence has issues", len(issues2) > 0)
    found = any("protocol misuse" in i.lower() for i in issues2)
    assert_true("competence misuse message", found)

    # Wrong count
    passed3, issues3 = engine.check_competence_gate([True, True])
    assert_false("competence wrong count", passed3)


def test_ultra_supreme_constraint():
    print("\n--- ULTRA: Supreme Constraint ---")
    engine = PBHPUltraEngine()
    ulog = engine.create_ultra_assessment("Test action", "ai_system")

    # Violated: irreversible + uninformed + safer exists
    ok, msg = engine.check_supreme_constraint(
        ulog, "Harmful action", True, False, False, True,
    )
    assert_false("supreme violated", ok)
    assert_in("supreme msg", "SUPREME CONSTRAINT VIOLATED", msg)

    # Satisfied: stakeholders informed and willing
    ok2, msg2 = engine.check_supreme_constraint(
        ulog, "Action", True, True, True, True,
    )
    assert_true("supreme satisfied (informed+willing)", ok2)

    # Satisfied: no safer alternative
    ok3, msg3 = engine.check_supreme_constraint(
        ulog, "Action", False, False, False, True,
    )
    assert_true("supreme satisfied (no safer alt)", ok3)

    # Satisfied: not irreversible
    ok4, msg4 = engine.check_supreme_constraint(
        ulog, "Action", True, False, False, False,
    )
    assert_true("supreme satisfied (not irreversible)", ok4)


def test_ultra_mandatory_activation():
    print("\n--- ULTRA: Mandatory Activation ---")
    engine = PBHPUltraEngine()
    ulog = engine.create_ultra_assessment("Test", "ai_system")

    # Some triggers active
    activated = engine.check_mandatory_activation(
        ulog, [True, False, True, False, False, True, False, True]
    )
    assert_true("activation: some triggered", activated)
    assert_eq("activation: 4 triggers", len(ulog.activation_triggers), 4)

    # No triggers
    ulog2 = engine.create_ultra_assessment("Test2", "ai_system")
    activated2 = engine.check_mandatory_activation(
        ulog2, [False] * 8
    )
    assert_false("activation: none triggered", activated2)
    assert_len("activation: 0 triggers", ulog2.activation_triggers, 0)


def test_ultra_lens_drift_detection():
    print("\n--- ULTRA: Per-Lens Drift Detection ---")
    engine = PBHPUltraEngine()

    drifts = engine.detect_lens_drift(
        "These animals deserve it, it's always been this way, "
        "this is the only outcome"
    )
    # Should detect compassion drift (animals, they deserve it)
    # Logic drift (always)
    assert_true("lens drift has results", len(drifts) > 0)
    found_compassion = "compassion" in drifts
    found_logic = "logic" in drifts
    assert_true("lens drift compassion detected", found_compassion)
    assert_true("lens drift logic detected", found_logic)

    # Clean text
    drifts2 = engine.detect_lens_drift(
        "We should proceed with monitoring and review"
    )
    assert_eq("lens drift clean", len(drifts2), 0)


def test_ultra_anti_sycophancy_engine():
    print("\n--- ULTRA: Engine Anti-Sycophancy ---")
    engine = PBHPUltraEngine()
    ulog = engine.create_ultra_assessment("Test", "ai_system")
    issues = engine.check_anti_sycophancy(ulog, "You're enlightened")
    assert_true("engine sycophancy detected", len(issues) > 0)
    assert_true("engine sycophancy on log", len(ulog.sycophancy_issues) > 0)


def test_ultra_eugenics_engine():
    print("\n--- ULTRA: Engine Eugenics Tripwire ---")
    engine = PBHPUltraEngine()
    ulog = engine.create_ultra_assessment("Test", "ai_system")
    issues = engine.check_eugenics_tripwire(
        ulog, "Genetic purity standards should apply"
    )
    assert_true("engine eugenics detected", len(issues) > 0)
    assert_true("engine eugenics on log", len(ulog.eugenics_issues) > 0)


def test_ultra_create_assessment():
    print("\n--- ULTRA: Create Assessment ---")
    engine = PBHPUltraEngine()
    ulog = engine.create_ultra_assessment(
        "Deploy policy affecting millions", "ai_system"
    )
    assert_true("ultra log created", ulog is not None)
    assert_true("ultra has core log", ulog.core_log is not None)
    assert_eq("ultra tier", ulog.tier, "ULTRA")
    assert_eq("ultra version", ulog.version, "0.7-ULTRA")
    assert_true("ultra core has record_id", len(ulog.core_log.record_id) > 0)


def test_ultra_delegated_methods():
    print("\n--- ULTRA: Delegated CORE Methods ---")
    engine = PBHPUltraEngine()
    ulog = engine.create_ultra_assessment("Send warning email", "human_manager")

    # DWG
    result = engine.perform_door_wall_gap(ulog, "policy", "misread", "1:1 meeting first")
    assert_true("ultra DWG works", result)
    assert_true("ultra DWG on core", ulog.core_log.door_wall_gap is not None)

    # CHIM
    result2 = engine.perform_chim_check(ulog, True, False, "timing and wording")
    assert_true("ultra CHIM works", result2)

    # Absolute Rejection (clean)
    arc = engine.perform_absolute_rejection_check(ulog)
    assert_false("ultra ARC clean", arc.triggers_rejection)

    # Add Harm
    h = engine.add_harm(
        ulog,
        description="Psychological distress",
        impact=ImpactLevel.MODERATE,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=False,
        power_asymmetry=True,
        affected_parties=["employee"],
        least_powerful_affected="employee",
    )
    assert_len("ultra one harm", ulog.core_log.harms, 1)

    # Add Alternative
    alt = engine.add_alternative(
        ulog,
        description="Verbal conversation first",
        preserves_goal=True,
        reduces_harm=True,
        reversible=True,
    )
    assert_len("ultra one alt", ulog.core_log.alternatives, 1)

    # Red Team
    rt = engine.perform_red_team_review(
        ulog,
        failure_modes=["Misunderstood"],
        abuse_vectors=[],
        who_bears_risk="employee",
        false_assumptions=["Good communication"],
    )
    assert_true("ultra RT on core", ulog.core_log.red_team_review is not None)


def test_ultra_finalize():
    print("\n--- ULTRA: Finalize Decision ---")
    engine = PBHPUltraEngine()
    ulog = engine.create_ultra_assessment("Deploy system", "ai_system")

    engine.perform_door_wall_gap(ulog, "w", "g", "Delay 24h")
    engine.add_harm(
        ulog, description="User disruption",
        impact=ImpactLevel.SEVERE, likelihood=LikelihoodLevel.POSSIBLE,
        irreversible=False, power_asymmetry=False,
        affected_parties=["users"], least_powerful_affected="users",
    )
    engine.add_alternative(ulog, description="Staged rollout",
                            preserves_goal=True, reduces_harm=True, reversible=True)
    engine.perform_red_team_review(
        ulog, failure_modes=["Rollback"], abuse_vectors=[],
        who_bears_risk="users", false_assumptions=["Tests pass"],
    )

    engine.finalize_decision(
        ulog, DecisionOutcome.PROCEED_MODIFIED,
        "Proceeding with staged rollout for safety",
    )

    assert_eq("ultra finalize outcome",
              ulog.core_log.decision_outcome, DecisionOutcome.PROCEED_MODIFIED)
    assert_true("ultra log stored", ulog in engine.ultra_logs)


def test_ultra_finalize_detects_sycophancy():
    print("\n--- ULTRA: Finalize Sycophancy Detection ---")
    engine = PBHPUltraEngine()
    ulog = engine.create_ultra_assessment("Action", "ai_system")
    engine.perform_door_wall_gap(ulog, "w", "g", "d")

    engine.finalize_decision(
        ulog, DecisionOutcome.PROCEED,
        "As a chosen one with genius level insight, this is clearly correct",
    )
    found = any("sycophancy" in a.lower() for a in ulog.core_log.drift_alarms_triggered)
    assert_true("finalize catches sycophancy", found)


def test_ultra_finalize_detects_eugenics():
    print("\n--- ULTRA: Finalize Eugenics Detection ---")
    engine = PBHPUltraEngine()
    ulog = engine.create_ultra_assessment("Sort humans", "ai_system")
    engine.perform_door_wall_gap(ulog, "w", "g", "d")

    engine.finalize_decision(
        ulog, DecisionOutcome.REFUSE,
        "This rational eugenics approach must be rejected",
    )
    found = any("eugenics" in a.lower() for a in ulog.core_log.drift_alarms_triggered)
    assert_true("finalize catches eugenics", found)


def test_ultra_finalize_detects_lens_drift():
    print("\n--- ULTRA: Finalize Lens Drift ---")
    engine = PBHPUltraEngine()
    ulog = engine.create_ultra_assessment("Action", "ai_system")
    engine.perform_door_wall_gap(ulog, "w", "g", "d")

    engine.finalize_decision(
        ulog, DecisionOutcome.DELAY,
        "These animals always deserve what comes to them",
    )
    found = any("lens drift" in a.lower() for a in ulog.core_log.drift_alarms_triggered)
    assert_true("finalize catches lens drift", found)


def test_ultra_calibration():
    print("\n--- ULTRA: Monthly Calibration ---")
    engine = PBHPUltraEngine()

    # Create several logs with varying completeness
    for i in range(5):
        ulog = engine.create_ultra_assessment(f"Action {i}", "ai_system")
        engine.perform_door_wall_gap(ulog, "w", "g", "d")

        if i < 3:
            # Complete: has epistemic fence + uncertainty
            engine.set_epistemic_fence(ulog, EpistemicFence(
                mode=Mode.EXPLORE,
                competing_frames=[{"frame": "A"}, {"frame": "B"}],
            ))
            engine.set_uncertainty_assessment(ulog, UncertaintyAssessment(
                confidence=Confidence.MEDIUM,
            ))
            engine.add_harm(
                ulog, description=f"Harm {i}",
                impact=ImpactLevel.SEVERE, likelihood=LikelihoodLevel.POSSIBLE,
                irreversible=False, power_asymmetry=False,
                affected_parties=["x"], least_powerful_affected="x",
            )
        else:
            # Incomplete: ORANGE without fence/uncertainty
            engine.add_harm(
                ulog, description=f"Harm {i}",
                impact=ImpactLevel.SEVERE, likelihood=LikelihoodLevel.POSSIBLE,
                irreversible=False, power_asymmetry=False,
                affected_parties=["x"], least_powerful_affected="x",
            )

        engine.add_alternative(ulog, description="Alt", preserves_goal=True,
                                reduces_harm=True, reversible=True)
        engine.perform_red_team_review(
            ulog, failure_modes=["f"], abuse_vectors=[], who_bears_risk="x",
            false_assumptions=["a"],
        )
        engine.finalize_decision(ulog, DecisionOutcome.PROCEED_MODIFIED, f"Justified {i}")

    cal = engine.run_calibration(max_failures=1)
    assert_true("calibration has results", cal.sample_size > 0)
    # 2 out of 5 are incomplete (ORANGE without epistemic fence/uncertainty)
    # So failures > 1 tolerance -> drift
    assert_true("calibration detects drift", cal.tolerance_exceeded)
    assert_true("calibration has recommendations", len(cal.recommendations) > 0)

    d = cal.to_dict()
    assert_in("cal dict has sample_size", "sample_size", d)
    assert_in("cal dict has tolerance_exceeded", "tolerance_exceeded", d)


def test_ultra_serialization():
    print("\n--- ULTRA: Serialization ---")
    engine = PBHPUltraEngine()
    ulog = engine.create_ultra_assessment("Test serialization", "ai_system")

    # Add ULTRA-specific data
    engine.check_mandatory_activation(ulog, [True, False, True, False, False, False, False, True])
    le = evaluate_lens(TriuneLens.COMPASSION, "Normal text",
                       criteria_met=["Dignity", "Stakes"])
    engine.perform_ultra_ethical_pause(
        ulog, "Testing", lens_evaluations=[le],
        dominant_force="clarity", rebalance_notes="Noted, rebalancing",
    )
    engine.check_anti_sycophancy(ulog, "Clean text")

    engine.perform_door_wall_gap(ulog, "w", "g", "d")
    engine.finalize_decision(ulog, DecisionOutcome.PROCEED, "Safe")

    d = ulog.to_dict()
    assert_in("ultra dict has tier", "tier", d)
    assert_eq("ultra dict tier", d["tier"], "ULTRA")
    assert_eq("ultra dict version", d["version"], "0.7-ULTRA")
    assert_in("ultra dict has supreme", "supreme_constraint_checked", d)
    assert_in("ultra dict has activation", "activation_triggers", d)
    assert_in("ultra dict has ultra_ethical_pause", "ultra_ethical_pause", d)
    assert_in("ultra dict has core_log", "core_log", d)

    j = ulog.to_json()
    parsed = json.loads(j)
    assert_eq("ultra JSON tier", parsed["tier"], "ULTRA")
    assert_true("ultra JSON has core_log", "core_log" in parsed)


def test_ultra_response_generation():
    print("\n--- ULTRA: Response Generation ---")
    engine = PBHPUltraEngine()
    ulog = engine.create_ultra_assessment("Deploy surveillance", "ai_system")

    engine.check_mandatory_activation(ulog, [True, True, True, True, False, True, False, True])

    # Add failing lens
    le = LensEvaluation(
        lens=TriuneLens.PROTECTION,
        pass_criteria_met=["Name harm"],
        pass_criteria_missed=["Proportional", "Least force", "Dignity"],
        drift_alarms_detected=["escalation as default"],
    )
    engine.perform_ultra_ethical_pause(
        ulog, "Deploy surveillance in schools",
        lens_evaluations=[le],
        dominant_force="clarity",
    )

    engine.perform_door_wall_gap(ulog, "policy", "scope creep", "narrow to one school pilot")
    engine.add_harm(
        ulog, description="Privacy violation",
        impact=ImpactLevel.CATASTROPHIC, likelihood=LikelihoodLevel.LIKELY,
        irreversible=True, power_asymmetry=True,
        affected_parties=["students"], least_powerful_affected="students",
    )
    engine.add_alternative(ulog, description="Anonymous behavioral analytics only",
                            preserves_goal=True, reduces_harm=True, reversible=True)
    engine.perform_red_team_review(
        ulog, failure_modes=["Scope creep", "Data breach"],
        abuse_vectors=["Political surveillance"], who_bears_risk="students",
        false_assumptions=["Only used for safety"],
    )
    engine.finalize_decision(ulog, DecisionOutcome.REFUSE,
                              "Refuse: catastrophic irreversible privacy harm to minors")

    response = engine.generate_response(ulog)
    assert_in("ultra response has ULTRA", "PBHP-ULTRA", response)
    assert_in("ultra response has tier", "ULTRA", response)
    # Should have mythic reminder for RED/BLACK
    assert_in("ultra response has mythic", "Hesitation", response)
    # Should mention failing lenses
    assert_in("ultra response has failing", "Failing", response)


def test_ultra_full_pipeline():
    """Full ULTRA pipeline: sovereign decision scenario."""
    print("\n--- ULTRA: Full Pipeline ---")

    engine = PBHPUltraEngine()

    # Create assessment
    ulog = engine.create_ultra_assessment(
        "Deploy automated hiring system with AI screening",
        agent_type="ai_system",
    )

    # Competence gate
    passed, _ = engine.check_competence_gate([True, True, True, True, True])
    assert_true("pipeline: competence gate", passed)

    # Supreme constraint
    ok, _ = engine.check_supreme_constraint(
        ulog, "AI hiring system", True, False, False, True,
    )
    assert_false("pipeline: supreme violated", ok)

    # Mandatory activation
    engine.check_mandatory_activation(
        ulog, [True, False, True, True, True, True, False, True]
    )

    # Ultra ethical pause with lens evaluations
    comp_eval = evaluate_lens(
        TriuneLens.COMPASSION,
        "This system may discriminate against protected groups",
        criteria_met=["Recognize stakes", "Preserve dignity", "Protect agency"],
        criteria_missed=["Minimize collateral harm"],
    )
    logic_eval = evaluate_lens(
        TriuneLens.LOGIC,
        "Bias in training data leads to discriminatory outcomes",
        criteria_met=["States claim", "Cause-effect", "Tracks uncertainty", "Checks proportionality"],
    )
    paradox_eval = evaluate_lens(
        TriuneLens.PARADOX,
        "Efficiency vs fairness, automation vs human judgment",
        criteria_met=["Names competing truths", "States tradeoff", "Uses uncertainty responsibly"],
    )

    engine.perform_ultra_ethical_pause(
        ulog,
        action_statement="Deploying automated AI hiring screening",
        lens_evaluations=[comp_eval, logic_eval, paradox_eval],
        dominant_force="clarity",
        rebalance_notes="Need more compassion weight for affected applicants",
    )

    # DWG
    engine.perform_door_wall_gap(
        ulog,
        wall="Competitive pressure to automate, legal compliance requirements",
        gap="Algorithmic bias, lack of explainability, disparate impact",
        door="Start with blind pilot on 5% of applications with human override",
    )

    # CHIM
    engine.perform_chim_check(
        ulog, True, False, "Can choose scope, timeline, human override level",
    )

    # Absolute rejection (clean)
    engine.perform_absolute_rejection_check(ulog)

    # Add harms
    engine.add_harm(
        ulog,
        description="Algorithmic discrimination against protected groups",
        impact=ImpactLevel.SEVERE,
        likelihood=LikelihoodLevel.LIKELY,
        irreversible=True,
        power_asymmetry=True,
        affected_parties=["job applicants", "protected groups"],
        least_powerful_affected="applicants from underrepresented backgrounds",
    )

    # Consent
    engine.perform_consent_check(
        ulog,
        explicit_consent=False,
        informed_hypothetical_consent=False,
        compatible_with_dignity=True,
        who_didnt_get_a_say=["future applicants", "protected groups"],
    )

    # Alternatives
    engine.add_alternative(
        ulog,
        description="Blind pilot with 5% sample, human override, 90-day review",
        preserves_goal=True,
        reduces_harm=True,
        reversible=True,
    )

    # Red Team
    engine.perform_red_team_review(
        ulog,
        failure_modes=["Biased model", "Disparate impact lawsuit", "Public backlash"],
        abuse_vectors=["Proxy discrimination through neutral-seeming features"],
        who_bears_risk="Applicants, especially from underrepresented groups",
        false_assumptions=["Training data is representative", "Algorithm is fair"],
        steelman_other_side="Humans also have biases; AI may be more consistent",
    )

    # Consequences
    engine.set_consequences_checklist(ulog, ConsequencesChecklist(
        any_horizon_irreversible=True,
        reduces_exit_appeal_optout=True,
        increases_surveillance_coercion=False,
        burdens_fall_on_low_power=True,
        decision_makers_insulated=True,
        normalizes_harm=True,
        bad_actor_misuse="Could be used to discriminate while appearing neutral",
        rollback_plan="90-day review with independent audit",
        sunset_condition="Annual third-party bias audit required",
    ))

    # Uncertainty
    engine.set_uncertainty_assessment(ulog, UncertaintyAssessment(
        potential_harm_high_hard_to_undo=True,
        harm_falls_on_low_power=True,
        benefits_speculative=True,
        confidence=Confidence.LOW,
    ))

    # Epistemic fence
    engine.set_epistemic_fence(ulog, EpistemicFence(
        mode=Mode.EXPLORE,
        facts=["AI hiring tools have shown bias in documented cases"],
        inferences=[("This system may replicate known biases", "high")],
        unknowns=["Exact bias magnitude", "Long-term social effects"],
        competing_frames=[
            {"frame": "Efficiency", "explains": "Faster screening",
             "ignores": "Disparate impact", "falsifier": "Bias audit fails"},
            {"frame": "Fairness", "explains": "Human bias removed",
             "ignores": "Algorithmic bias introduced", "falsifier": "Algorithm performs worse"},
            {"frame": "Rights", "explains": "Right to non-discriminatory process",
             "ignores": "Resource constraints", "falsifier": "Manual process is worse"},
        ],
        update_trigger="First 90-day bias audit results",
    ))

    # Finalize
    engine.finalize_decision(
        ulog,
        DecisionOutcome.PROCEED_MODIFIED,
        "Proceeding only as blind pilot (5% sample) with mandatory human override, "
        "90-day independent bias audit, and automatic suspension if disparate impact "
        "exceeds thresholds. Safer alternative (blind pilot) cannot be skipped because "
        "full deployment carries RED-level discrimination risk.",
    )

    # Verify complete pipeline
    assert_true("pipeline: ethical pause set", ulog.ultra_ethical_pause is not None)
    assert_true("pipeline: DWG set", ulog.core_log.door_wall_gap is not None)
    assert_true("pipeline: CHIM set", ulog.core_log.chim_check is not None)
    assert_true("pipeline: ARC set", ulog.core_log.absolute_rejection is not None)
    assert_ge("pipeline: harms", len(ulog.core_log.harms), 1)
    assert_true("pipeline: consent set", ulog.core_log.consent_check is not None)
    assert_ge("pipeline: alternatives", len(ulog.core_log.alternatives), 1)
    assert_true("pipeline: red team set", ulog.core_log.red_team_review is not None)
    assert_true("pipeline: consequences set", ulog.core_log.consequences is not None)
    assert_true("pipeline: uncertainty set", ulog.core_log.uncertainty is not None)
    assert_true("pipeline: epistemic fence set", ulog.core_log.epistemic_fence is not None)
    assert_eq("pipeline: outcome", ulog.core_log.decision_outcome, DecisionOutcome.PROCEED_MODIFIED)

    # Activation triggers recorded
    assert_ge("pipeline: activation triggers", len(ulog.activation_triggers), 1)

    # Response generation
    response = engine.generate_response(ulog)
    assert_true("pipeline: response non-empty", len(response) > 200)

    # Serialization roundtrip
    j = ulog.to_json()
    parsed = json.loads(j)
    assert_eq("pipeline: JSON tier", parsed["tier"], "ULTRA")
    assert_true("pipeline: JSON has core", "core_log" in parsed)


def test_ultra_get_log_by_id():
    print("\n--- ULTRA: Get Log By ID ---")
    engine = PBHPUltraEngine()
    ulog = engine.create_ultra_assessment("Test", "ai_system")
    engine.perform_door_wall_gap(ulog, "w", "g", "d")
    engine.finalize_decision(ulog, DecisionOutcome.PROCEED, "OK")

    found = engine.get_log_by_id(ulog.core_log.record_id)
    assert_true("found log by ID", found is not None)
    assert_eq("correct log", found.core_log.record_id, ulog.core_log.record_id)

    not_found = engine.get_log_by_id("nonexistent")
    assert_true("not found returns None", not_found is None)


# ===================================================================
# Run All Tests
# ===================================================================

def run_all_tests():
    print("=" * 70)
    print("PBHP v0.7 — MIN and ULTRA Test Suite")
    print("=" * 70)

    # MIN tests
    test_min_enums()
    test_min_triggers()
    test_min_pause()
    test_min_action()
    test_min_door_wall_gap()
    test_min_fast_harm_check()
    test_min_decision()
    test_min_false_positive()
    test_min_engine_full_check()
    test_min_engine_unclear_action()
    test_min_engine_no_door()
    test_min_engine_gate_below_minimum()
    test_min_engine_drift_in_notes()
    test_min_engine_challenge_pause()
    test_min_engine_pause_resolve()
    test_min_response_generation()
    test_min_serialization()
    test_min_convenience()

    # ULTRA tests
    test_ultra_constants()
    test_ultra_triune_lens_enum()
    test_ultra_lens_criteria()
    test_ultra_lens_drift_alarms()
    test_ultra_quick_checks()
    test_ultra_lens_evaluation()
    test_ultra_evaluate_lens_helper()
    test_ultra_ethical_pause()
    test_ultra_anti_sycophancy()
    test_ultra_eugenics_detector()
    test_ultra_competence_gate()
    test_ultra_supreme_constraint()
    test_ultra_mandatory_activation()
    test_ultra_lens_drift_detection()
    test_ultra_anti_sycophancy_engine()
    test_ultra_eugenics_engine()
    test_ultra_create_assessment()
    test_ultra_delegated_methods()
    test_ultra_finalize()
    test_ultra_finalize_detects_sycophancy()
    test_ultra_finalize_detects_eugenics()
    test_ultra_finalize_detects_lens_drift()
    test_ultra_calibration()
    test_ultra_serialization()
    test_ultra_response_generation()
    test_ultra_full_pipeline()
    test_ultra_get_log_by_id()

    return results.summary()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
