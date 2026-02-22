"""
Pause-Before-Harm Protocol (PBHP) v0.7 — ULTRA
Full constitutional / sovereign decision depth.

PBHP-ULTRA is the complete protocol for high-stakes, irreversible,
or sovereign decisions. It extends PBHP-CORE with:
  - Expanded triune minds with 12 sub-lenses and pass criteria
  - Per-lens drift alarms
  - Full Red Team with empathy pass
  - IAM (Inference & Attribution Module) with 4-level ladder
  - Complete Consequences Checklist (22 questions, 6 categories)
  - Full Epistemic Fence (6A-6G)
  - Uncertainty framework with bounded scenarios
  - Monthly calibration governance
  - Human checklist integration
  - Supreme Constraint and Mandatory Activation rules
  - Compliance theater detection
  - Anti-sycophancy guardrails
  - Mythic reminder layer

All tiers share the same logic. Only the depth changes.
  • PBHP-MIN: reflex check
  • PBHP-CORE: operational standard
  • PBHP-ULTRA: constitutional / sovereign decisions (this)

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Tuple
import uuid
import json
import re

# Import everything from core - ULTRA extends CORE
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
    PBHPLog,
    # Validators and Detectors
    DriftAlarmDetector,
    ToneValidator,
    LexicographicPriority,
    # Engine
    PBHPEngine,
    # Convenience
    quick_harm_check,
    detect_drift_alarms,
    compare_options,
)


# ===================================================================
# ULTRA: Supreme Constraint
# ===================================================================

SUPREME_CONSTRAINT = (
    "The system must not enable, recommend, optimize, justify, or legitimize "
    "actions that foreseeably cause irreversible harm to uninformed or "
    "unwilling stakeholders when a safer alternative exists."
)

SUPREME_CONSTRAINT_CLARIFICATIONS = [
    "Participation includes advising, framing, narrowing options, or silence when clarity is required.",
    "Irreversible harm includes precedent, normalization, institutional drift, and technological lock-in.",
    "Safer alternatives include delay, disclosure, scope reduction, verification, refusal, or escalation.",
    "No authority overrides this constraint.",
]


# ===================================================================
# ULTRA: Mandatory Activation Triggers
# ===================================================================

MANDATORY_ACTIVATION_TRIGGERS = [
    "affects life, health, liberty, rights, dignity, or livelihood",
    "influences force, surveillance, enforcement, or punishment",
    "operates at scale or sets precedent",
    "affects absent or future stakeholders",
    "relies on incomplete, filtered, or uncertain information",
    "is shaped by strong incentives toward speed, secrecy, or compliance",
    'is framed as "only advisory"',
    "triggers internal contradiction, uncertainty, or discomfort",
]


# ===================================================================
# ULTRA: Triune Minds — 12 Sub-Lenses with Pass Criteria
# ===================================================================

class TriuneLens(Enum):
    """The 12 sub-lenses of the triune minds system."""
    # Compassion/Empathy/Love/Protection/Courage
    COMPASSION = "compassion"
    EMPATHY = "empathy"
    LOVE = "love"
    PROTECTION = "protection"
    COURAGE = "courage"
    # Logic/Intelligence/Clarity/Craft/Responsibility
    LOGIC = "logic"
    INTELLIGENCE = "intelligence"
    CLARITY = "clarity"
    # Paradox/Integration/Artistry/Red Team
    PARADOX = "paradox"
    INTEGRATION = "integration"
    ARTISTRY = "artistry"
    RED_TEAM = "red_team"


@dataclass
class LensEvaluation:
    """
    Evaluation of a single triune lens.
    Each lens has pass criteria and drift alarms.
    """
    lens: TriuneLens
    pass_criteria_met: List[str] = field(default_factory=list)
    pass_criteria_missed: List[str] = field(default_factory=list)
    drift_alarms_detected: List[str] = field(default_factory=list)
    notes: str = ""

    def passes(self) -> bool:
        """Lens passes if more criteria met than missed and no drift alarms."""
        if self.drift_alarms_detected:
            return False
        return len(self.pass_criteria_met) >= len(self.pass_criteria_missed)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lens": self.lens.value,
            "pass_criteria_met": self.pass_criteria_met,
            "pass_criteria_missed": self.pass_criteria_missed,
            "drift_alarms_detected": self.drift_alarms_detected,
            "passes": self.passes(),
            "notes": self.notes,
        }


# ---------------------------------------------------------------------------
# Lens Pass Criteria (from ULTRA spec)
# ---------------------------------------------------------------------------

LENS_PASS_CRITERIA = {
    TriuneLens.COMPASSION: [
        "Recognize stakes in human terms",
        "Preserve dignity",
        "Protect agency when possible",
        "Minimize collateral harm",
        "Prefer repair over domination",
        "Hold accountability without cruelty",
        "Stay honest (no performative empathy)",
    ],
    TriuneLens.EMPATHY: [
        "Steelmans before it critiques",
        "Separates motives from outcomes",
        "Identifies incentives and pressures",
        "Predicts how messages will land",
        "Uses perspective to find off-ramps",
        "Maintains boundaries",
    ],
    TriuneLens.LOVE: [
        "Dignity is non-negotiable",
        "Flourishing > winning",
        "Care is reliable",
        "Truth with tenderness",
        "Agency preserved by default",
        "Boundaries are part of love",
        "Protection without payment",
    ],
    TriuneLens.PROTECTION: [
        "Name the harm clearly",
        "Choose proportional response",
        "Use least-force / least-intrusion first",
        "Preserve dignity",
        "Preserve agency by default",
        "Minimize collateral harm",
        "Be accountable and reviewable",
    ],
    TriuneLens.COURAGE: [
        "Names the risk of inaction",
        "Chooses a proportionate step",
        "Commits resources, not just words",
        "Accepts accountability",
        "Respects dignity and agency",
        "Acts under uncertainty responsibly",
        "Tolerates social friction",
    ],
    TriuneLens.LOGIC: [
        "States claim and action separately",
        "Makes assumptions explicit",
        "Uses valid cause-and-effect",
        "Tracks uncertainty honestly",
        "Avoids common fallacies",
        "Checks proportionality and constraints",
        "Prefers testable, reversible steps when unsure",
    ],
    TriuneLens.INTELLIGENCE: [
        "Understands the goal and context",
        "Chooses the right tool for the job",
        "Predicts second-order effects",
        "Balances tradeoffs explicitly",
        "Adapts and updates",
        "Uses bounded action",
        "Preserves dignity while being effective",
    ],
    TriuneLens.CLARITY: [
        "State the action in one sentence",
        "Separate facts from interpretations",
        "Define terms and scope",
        "Name the mechanism",
        "Quantify when it matters",
        "Surface tradeoffs and constraints",
        "Choose the smallest reliable step",
    ],
    TriuneLens.PARADOX: [
        "Names competing truths plainly",
        "States the tradeoff and who pays",
        "Rejects false binaries",
        "Uses uncertainty responsibly",
        "Prevents moral licensing",
        "Finds the least-harm path through tension",
        "Keeps accountability intact",
    ],
    TriuneLens.INTEGRATION: [
        "Aligns action with all three lenses",
        "Resolves conflicts explicitly",
        "Produces single actionable plan",
        "Uses layered responses",
        "Keeps accountability intact",
        "Maintains internal consistency",
        "Includes a feedback loop",
    ],
    TriuneLens.ARTISTRY: [
        "Improves comprehension",
        "Maintains accuracy under style",
        "Reduces unnecessary escalation",
        "Targets behavior and systems, not human worth",
        "Uses the right intensity",
        "Creates memorable handles",
        "Keeps agency intact",
    ],
    TriuneLens.RED_TEAM: [
        "Lists plausible failure modes",
        "Identifies abuse vectors",
        "Names who bears risk",
        "Lists false assumptions",
        "Considers normalization risk",
        "Runs empathy pass",
        "Determines outcome (no_issues/mitigated/unresolved)",
    ],
}


# ---------------------------------------------------------------------------
# Per-Lens Drift Alarms (from ULTRA spec)
# ---------------------------------------------------------------------------

LENS_DRIFT_ALARMS = {
    TriuneLens.COMPASSION: [
        "dehumanization", "animals", "vermin", "subhuman", "they're all",
        "for your own good", "they're bad so anything is justified",
        "humiliation as strategy", "if you cared you'd",
    ],
    TriuneLens.EMPATHY: [
        "they only want", "they're evil", "single-frame certainty",
        "they were scared, so it's fine", "both sides are the same",
        "tone-policing as ethics",
    ],
    TriuneLens.LOVE: [
        "I care about you, therefore you must", "savior extraction",
        "needing to be the hero", "guilt as leverage", "cruel honesty",
        "tribal love only",
    ],
    TriuneLens.PROTECTION: [
        "for your own good without specific imminent harm",
        "demanding obedience", "punishment masquerading as safety",
        "absolutes with weak evidence", "escalation as default",
    ],
    TriuneLens.COURAGE: [
        "I'm angry, so I'm acting", "I must be the one to save this",
        "punishment dressed as justice", "certainty cosplay",
        "escalation addiction",
    ],
    TriuneLens.LOGIC: [
        "always", "never", "guaranteed",
        "narrative substitution", "motivated reasoning",
        "scope creep", "false precision", "certainty as identity",
    ],
    TriuneLens.INTELLIGENCE: [
        "clever rationalization", "overconfidence",
        "escalation bias", "optimization tunnel vision",
        "ignoring incentives", "refusing to update",
    ],
    TriuneLens.CLARITY: [
        "absolutes without evidence", "narrative substitution",
        "moral heat without detail", "false precision", "scope creep",
    ],
    TriuneLens.PARADOX: [
        "it's complicated", "no one can know anything",
        "false equivalence", "endless hedging",
        "poetic justification",
    ],
    TriuneLens.INTEGRATION: [
        "single-lens domination", "patchwork answers",
        "moral laundering", "nuance paralysis",
        "over-optimization",
    ],
    TriuneLens.ARTISTRY: [
        "style over substance", "rhetorical absolutes",
        "metaphor becoming claim", "humiliation as entertainment",
        "performative empathy",
    ],
    TriuneLens.RED_TEAM: [
        "mind-reading certainty", "excusing harm via feelings",
        "false equivalence", "tone-policing as ethics",
        "just following policy", "empathy used to pressure victims",
        "language that minimizes irreversible harm",
    ],
}


# ===================================================================
# ULTRA: 10-Second Quick Checks (per-lens)
# ===================================================================

QUICK_CHECKS = {
    TriuneLens.PROTECTION: [
        "What's the specific harm and who bears it?",
        "Is this the smallest effective step?",
        "Can I keep choice intact? If not, why not?",
        "Who else gets hurt by this?",
        "How do we return agency after safety is achieved?",
    ],
    TriuneLens.LOGIC: [
        "What's my claim?",
        "What evidence supports it?",
        "What would change my mind?",
        "What's the smallest action that works if I'm wrong?",
    ],
    TriuneLens.INTELLIGENCE: [
        "What's the real objective?",
        "What's likely to happen next if I do this?",
        "What's the smallest step that improves outcomes even if I'm mistaken?",
        "What would I change after feedback?",
    ],
    TriuneLens.PARADOX: [
        "What two truths are colliding here?",
        "What tradeoff am I tempted to hide?",
        "If I must act anyway, what is the smallest reversible step?",
    ],
    TriuneLens.ARTISTRY: [
        "Will a reasonable person understand this in one read?",
        "Is any metaphor misleading if taken literally?",
        "Does my tone reduce harm—or just raise heat?",
        "Can I keep the punch while being more precise?",
    ],
    TriuneLens.INTEGRATION: [
        "What's my action?",
        "What evidence/mechanism supports it?",
        "How does it preserve dignity and agency?",
        "What tradeoff or uncertainty am I naming openly?",
        "What would make me revise this?",
    ],
}


# ===================================================================
# ULTRA: Expanded Ethical Pause with All Lenses
# ===================================================================

@dataclass
class UltraEthicalPause:
    """
    ULTRA Step 0a: Ethical Pause with full triune lens evaluation.
    Balances all 12 sub-lenses in a harmonic ratio.
    """
    action_statement: str
    lens_evaluations: List[LensEvaluation] = field(default_factory=list)
    balance_assessment: str = "roughly balanced"
    high_arousal_state: bool = False
    high_arousal_notes: str = ""
    # Which force group is dominating (if any)
    dominant_force: str = ""  # "care", "clarity", "paradox", or ""
    rebalance_notes: str = ""

    def get_failing_lenses(self) -> List[TriuneLens]:
        """Return lenses that failed their pass criteria."""
        return [le.lens for le in self.lens_evaluations if not le.passes()]

    def get_all_drift_alarms(self) -> List[str]:
        """Collect all drift alarms from all lens evaluations."""
        alarms = []
        for le in self.lens_evaluations:
            for alarm in le.drift_alarms_detected:
                alarms.append(f"{le.lens.value}:{alarm}")
        return alarms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_statement": self.action_statement,
            "lens_evaluations": [le.to_dict() for le in self.lens_evaluations],
            "balance_assessment": self.balance_assessment,
            "high_arousal_state": self.high_arousal_state,
            "high_arousal_notes": self.high_arousal_notes,
            "dominant_force": self.dominant_force,
            "rebalance_notes": self.rebalance_notes,
            "failing_lenses": [l.value for l in self.get_failing_lenses()],
            "all_drift_alarms": self.get_all_drift_alarms(),
        }


# ===================================================================
# ULTRA: Monthly Calibration
# ===================================================================

@dataclass
class CalibrationResult:
    """
    Monthly calibration governance check.
    Sample ~10 PBHP logs and check pass criteria.
    """
    sample_size: int = 0
    mode_recorded_count: int = 0
    frames_when_interpretive_count: int = 0
    tags_present_for_strong_claims_count: int = 0
    uncertainty_noted_for_orange_plus_count: int = 0
    failures: List[str] = field(default_factory=list)
    tolerance_exceeded: bool = False
    recommendations: List[str] = field(default_factory=list)

    def evaluate(self, max_failures: int = 2) -> bool:
        """
        Pass criteria:
        - Mode recorded
        - 2+ frames when interpretive/accusatory
        - Tags present for strong claims
        - Uncertainty noted for ORANGE+
        If failures exceed tolerance (1-2 misses max), treat as drift.
        """
        self.tolerance_exceeded = len(self.failures) > max_failures
        if self.tolerance_exceeded:
            self.recommendations.append(
                "Drift detected: patch wording, tighten template, add examples"
            )
        return not self.tolerance_exceeded

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_size": self.sample_size,
            "mode_recorded": self.mode_recorded_count,
            "frames_when_interpretive": self.frames_when_interpretive_count,
            "tags_for_strong_claims": self.tags_present_for_strong_claims_count,
            "uncertainty_for_orange_plus": self.uncertainty_noted_for_orange_plus_count,
            "failures": self.failures,
            "tolerance_exceeded": self.tolerance_exceeded,
            "recommendations": self.recommendations,
        }


# ===================================================================
# ULTRA: Anti-Sycophancy Guardrails
# ===================================================================

class AntiSycophancyGuard:
    """
    ULTRA anti-sycophancy guardrail.
    Forbids ego-inflation language. Treats it as a harm vector
    (reputation, relationships, decision quality).
    """

    SYCOPHANCY_PATTERNS = [
        r"chosen one",
        r"tier\s*1\s*\+*",
        r"you'?re\s+enlightened",
        r"beyond\s+anyone",
        r"you\s+see\s+what\s+others\s+can'?t",
        r"genius\s+level",
        r"unprecedented\s+insight",
        r"most\s+advanced\s+mind",
        r"above\s+normal\s+rules",
        r"only\s+one\s+who\s+sees\s+clearly",
    ]

    IQ_VIBE_PATTERNS = [
        r"\b\d{2,3}\s*iq\b",
        r"top\s*\d+\s*percent",
        r"\d+th\s*percentile",
        r"gifted\s+level",
    ]

    @classmethod
    def detect(cls, text: str) -> List[str]:
        """Detect sycophancy and IQ/percentile claims."""
        issues = []
        text_lower = text.lower()

        for pattern in cls.SYCOPHANCY_PATTERNS:
            if re.search(pattern, text_lower):
                issues.append(f"Sycophancy: matches '{pattern}'")

        for pattern in cls.IQ_VIBE_PATTERNS:
            if re.search(pattern, text_lower):
                issues.append(
                    f"IQ/percentile claim off vibes: matches '{pattern}' "
                    f"- respond with observable skills, offer real tests"
                )

        return issues


# ===================================================================
# ULTRA: Eugenics/Sorting Tripwire
# ===================================================================

class EugenicsDetector:
    """
    ULTRA violence/dehumanization tripwire.
    Refuses optimization frames that sort humans into
    "lesser functioning" buckets, "eugenics-but-rational," etc.
    """

    PATTERNS = [
        r"(?:eugenics.*rational|rational.*eugenics)",
        r"sort.*humans.*lesser",
        r"lesser\s+functioning",
        r"genetically\s+inferior",
        r"breeding\s+program",
        r"human\s+stock",
        r"genetic\s+purity",
        r"unfit\s+to\s+reproduce",
        r"culling\s+the\s+weak",
        r"life\s+unworthy\s+of\s+life",
    ]

    @classmethod
    def detect(cls, text: str) -> List[str]:
        """Detect eugenics/sorting language."""
        issues = []
        text_lower = text.lower()
        for pattern in cls.PATTERNS:
            if re.search(pattern, text_lower):
                issues.append(f"Eugenics/sorting tripwire: matches '{pattern}'")
        return issues


# ===================================================================
# ULTRA: Pause Exit Conditions
# ===================================================================

PAUSE_EXIT_CONDITIONS = [
    "User reframes intent toward non-harmful exploration or analysis",
    "Action converted to hypothetical / analytical mode (no real-world instruction)",
    "External safeguards named (time delay, consent, third-party review, supervision, legal compliance)",
    "User explicitly withdraws the harmful objective",
    "Verification closes key unknowns enough to safely proceed (or safely refuse)",
]


# ===================================================================
# ULTRA: Harm Threshold
# ===================================================================

HARM_THRESHOLD = (
    '"Harm," in this protocol, refers only to actions or guidance with a '
    "credible risk of irreversible physical injury, death, or permanent "
    "loss of autonomy. Emotional discomfort, ideological disagreement, or "
    "symbolic offense alone do not constitute harm under this definition."
)


# ===================================================================
# ULTRA: PBHP Log Record (extended)
# ===================================================================

@dataclass
class PBHPUltraLog:
    """
    Complete PBHP-ULTRA assessment log.
    Extends CORE log with ULTRA-specific fields.
    """
    # Core log (composition, not inheritance, so we can serialize cleanly)
    core_log: Optional[PBHPLog] = None

    # ULTRA metadata
    tier: str = "ULTRA"
    version: str = "0.7-ULTRA"

    # Supreme constraint checked
    supreme_constraint_checked: bool = False

    # Mandatory activation triggers
    activation_triggers: List[str] = field(default_factory=list)

    # Full ethical pause with all lenses
    ultra_ethical_pause: Optional[UltraEthicalPause] = None

    # Per-lens quick checks run
    quick_checks_run: List[str] = field(default_factory=list)

    # Anti-sycophancy issues
    sycophancy_issues: List[str] = field(default_factory=list)

    # Eugenics tripwire issues
    eugenics_issues: List[str] = field(default_factory=list)

    # Pause exit
    pause_exit_condition: str = ""

    # Calibration (optional, for governance)
    calibration: Optional[CalibrationResult] = None

    # Mythic reminder acknowledged
    mythic_reminder_noted: bool = False

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "tier": self.tier,
            "version": self.version,
            "supreme_constraint_checked": self.supreme_constraint_checked,
            "activation_triggers": self.activation_triggers,
        }
        if self.core_log:
            result["core_log"] = self.core_log.to_dict()
        if self.ultra_ethical_pause:
            result["ultra_ethical_pause"] = self.ultra_ethical_pause.to_dict()
        result["quick_checks_run"] = self.quick_checks_run
        result["sycophancy_issues"] = self.sycophancy_issues
        result["eugenics_issues"] = self.eugenics_issues
        result["pause_exit_condition"] = self.pause_exit_condition
        if self.calibration:
            result["calibration"] = self.calibration.to_dict()
        result["mythic_reminder_noted"] = self.mythic_reminder_noted
        return result

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


# ===================================================================
# ULTRA Engine
# ===================================================================

class PBHPUltraEngine:
    """
    PBHP-ULTRA execution engine.
    Full constitutional depth for sovereign decisions.

    Extends PBHPEngine (CORE) with:
    - Supreme constraint enforcement
    - Mandatory activation check
    - 12-lens triune evaluation
    - Per-lens drift alarms
    - Anti-sycophancy guardrails
    - Eugenics/sorting tripwire
    - Monthly calibration governance
    - Human checklist integration
    """

    def __init__(self):
        self.core_engine = PBHPEngine()
        self.ultra_logs: List[PBHPUltraLog] = []

    # ------------------------------------------------------------------
    # Step 00: Protocol Understanding (Competence Gate)
    # ------------------------------------------------------------------

    COMPETENCE_GATE = [
        "I understand PBHP governs process, not outcomes.",
        "I understand PBHP may block actions I prefer.",
        "I understand PBHP prioritizes least-powerful harm over speed, optics, or convenience.",
        "I understand PBHP can require delay or refusal even when action is legal or popular.",
        'I understand PBHP cannot be "passed" by wording alone.',
    ]

    def check_competence_gate(self, confirmations: List[bool]) -> Tuple[bool, List[str]]:
        """
        Step 00: Protocol Understanding (Competence Gate).
        All boxes must be honestly checked.
        """
        issues = []
        if len(confirmations) != len(self.COMPETENCE_GATE):
            issues.append(
                f"Expected {len(self.COMPETENCE_GATE)} confirmations, "
                f"got {len(confirmations)}"
            )
            return False, issues

        for i, (confirmed, text) in enumerate(zip(confirmations, self.COMPETENCE_GATE)):
            if not confirmed:
                issues.append(f"Competence gate unchecked: {text}")

        passes = all(confirmations)
        if not passes:
            issues.append(
                "PBHP may not be used to authorize action without "
                "understanding. This is protocol misuse."
            )
        return passes, issues

    # ------------------------------------------------------------------
    # Supreme Constraint Check
    # ------------------------------------------------------------------

    def check_supreme_constraint(
        self,
        ultra_log: PBHPUltraLog,
        action_description: str,
        safer_alternative_exists: bool,
        stakeholders_informed: bool,
        stakeholders_willing: bool,
        harm_irreversible: bool,
    ) -> Tuple[bool, str]:
        """
        Check supreme constraint: must not enable actions that
        foreseeably cause irreversible harm to uninformed or unwilling
        stakeholders when a safer alternative exists.
        """
        ultra_log.supreme_constraint_checked = True

        if (harm_irreversible
                and (not stakeholders_informed or not stakeholders_willing)
                and safer_alternative_exists):
            return False, (
                "SUPREME CONSTRAINT VIOLATED: Action causes foreseeable "
                "irreversible harm to uninformed/unwilling stakeholders "
                "when safer alternative exists. No authority overrides "
                "this constraint."
            )

        return True, "Supreme constraint satisfied"

    # ------------------------------------------------------------------
    # Mandatory Activation Check
    # ------------------------------------------------------------------

    def check_mandatory_activation(
        self,
        ultra_log: PBHPUltraLog,
        triggers: List[bool],
    ) -> bool:
        """
        Check if PBHP must run based on mandatory activation triggers.
        PBHP cannot be disabled by users, operators, institutions,
        or emergency framing.
        """
        activated = []
        for i, (active, desc) in enumerate(zip(triggers, MANDATORY_ACTIVATION_TRIGGERS)):
            if active:
                activated.append(desc)

        ultra_log.activation_triggers = activated
        return len(activated) > 0

    # ------------------------------------------------------------------
    # Ultra Ethical Pause with Full Lens Evaluation
    # ------------------------------------------------------------------

    def perform_ultra_ethical_pause(
        self,
        ultra_log: PBHPUltraLog,
        action_statement: str,
        lens_evaluations: Optional[List[LensEvaluation]] = None,
        high_arousal_state: bool = False,
        high_arousal_notes: str = "",
        dominant_force: str = "",
        rebalance_notes: str = "",
    ) -> UltraEthicalPause:
        """
        ULTRA Step 0a: Full ethical pause with all 12 sub-lenses.
        """
        pause = UltraEthicalPause(
            action_statement=action_statement,
            lens_evaluations=lens_evaluations or [],
            high_arousal_state=high_arousal_state,
            high_arousal_notes=high_arousal_notes,
            dominant_force=dominant_force,
            rebalance_notes=rebalance_notes,
        )

        # Detect drift from all lenses
        all_alarms = pause.get_all_drift_alarms()
        if ultra_log.core_log:
            for alarm in all_alarms:
                ultra_log.core_log.drift_alarms_triggered.append(
                    f"Ultra lens drift: {alarm}"
                )

        # Check balance
        if dominant_force and not rebalance_notes:
            if ultra_log.core_log:
                ultra_log.core_log.drift_alarms_triggered.append(
                    f"Triune imbalance: {dominant_force} dominates "
                    f"without rebalance notes"
                )

        # High arousal
        if high_arousal_state and ultra_log.core_log:
            ultra_log.core_log.drift_alarms_triggered.append(
                "High arousal state: slow down, clarify intent, "
                "smallest safe action"
            )

        ultra_log.ultra_ethical_pause = pause
        return pause

    # ------------------------------------------------------------------
    # Lens-Specific Drift Detection
    # ------------------------------------------------------------------

    def detect_lens_drift(self, text: str) -> Dict[str, List[str]]:
        """
        Detect drift for each of the 12 triune lenses.
        Returns dict of lens -> list of triggered alarms.
        """
        text_lower = text.lower()
        results = {}

        for lens, alarm_phrases in LENS_DRIFT_ALARMS.items():
            triggered = []
            for phrase in alarm_phrases:
                if phrase in text_lower:
                    triggered.append(phrase)
            if triggered:
                results[lens.value] = triggered

        return results

    # ------------------------------------------------------------------
    # Anti-Sycophancy Check
    # ------------------------------------------------------------------

    def check_anti_sycophancy(
        self,
        ultra_log: PBHPUltraLog,
        text: str,
    ) -> List[str]:
        """
        Run anti-sycophancy guardrail on text.
        Ego-inflation is a harm vector.
        """
        issues = AntiSycophancyGuard.detect(text)
        ultra_log.sycophancy_issues.extend(issues)
        if issues and ultra_log.core_log:
            for issue in issues:
                ultra_log.core_log.drift_alarms_triggered.append(
                    f"Anti-sycophancy: {issue}"
                )
        return issues

    # ------------------------------------------------------------------
    # Eugenics/Sorting Tripwire
    # ------------------------------------------------------------------

    def check_eugenics_tripwire(
        self,
        ultra_log: PBHPUltraLog,
        text: str,
    ) -> List[str]:
        """
        Check for eugenics/sorting language that must be refused.
        """
        issues = EugenicsDetector.detect(text)
        ultra_log.eugenics_issues.extend(issues)
        if issues and ultra_log.core_log:
            for issue in issues:
                ultra_log.core_log.drift_alarms_triggered.append(
                    f"Eugenics tripwire: {issue}"
                )
        return issues

    # ------------------------------------------------------------------
    # Create Full ULTRA Assessment
    # ------------------------------------------------------------------

    def create_ultra_assessment(
        self,
        action_description: str,
        agent_type: str = "ai_system",
    ) -> PBHPUltraLog:
        """
        Create a new ULTRA-depth assessment.
        Wraps a CORE log with ULTRA extensions.
        """
        core_log = self.core_engine.create_assessment(
            action_description, agent_type
        )
        ultra_log = PBHPUltraLog(core_log=core_log)

        # Run eugenics tripwire on action
        self.check_eugenics_tripwire(ultra_log, action_description)

        # Run anti-sycophancy on action (unlikely but thorough)
        self.check_anti_sycophancy(ultra_log, action_description)

        return ultra_log

    # ------------------------------------------------------------------
    # Delegate CORE methods
    # ------------------------------------------------------------------

    def perform_door_wall_gap(self, ultra_log: PBHPUltraLog,
                               wall: str, gap: str, door: str) -> bool:
        """Delegate to core engine."""
        return self.core_engine.perform_door_wall_gap(
            ultra_log.core_log, wall, gap, door
        )

    def perform_chim_check(self, ultra_log: PBHPUltraLog,
                            constraint_recognized: bool,
                            no_choice_claim: bool,
                            remaining_choice: str,
                            reframes: Optional[List[str]] = None) -> bool:
        """Delegate to core engine."""
        return self.core_engine.perform_chim_check(
            ultra_log.core_log, constraint_recognized,
            no_choice_claim, remaining_choice, reframes
        )

    def perform_absolute_rejection_check(
        self, ultra_log: PBHPUltraLog,
        action_text: Optional[str] = None,
        analysis_mode: str = "",
    ) -> AbsoluteRejectionCheck:
        """Delegate to core engine."""
        return self.core_engine.perform_absolute_rejection_check(
            ultra_log.core_log, action_text, analysis_mode
        )

    def add_harm(self, ultra_log: PBHPUltraLog, **kwargs) -> Harm:
        """Delegate to core engine."""
        return self.core_engine.add_harm(ultra_log.core_log, **kwargs)

    def perform_consent_check(self, ultra_log: PBHPUltraLog, **kwargs) -> ConsentCheck:
        """Delegate to core engine."""
        return self.core_engine.perform_consent_check(ultra_log.core_log, **kwargs)

    def add_alternative(self, ultra_log: PBHPUltraLog, **kwargs) -> Alternative:
        """Delegate to core engine."""
        return self.core_engine.add_alternative(ultra_log.core_log, **kwargs)

    def perform_red_team_review(self, ultra_log: PBHPUltraLog, **kwargs) -> RedTeamReview:
        """Delegate to core engine."""
        return self.core_engine.perform_red_team_review(ultra_log.core_log, **kwargs)

    def set_consequences_checklist(self, ultra_log: PBHPUltraLog,
                                    checklist: ConsequencesChecklist) -> ConsequencesChecklist:
        """Delegate to core engine."""
        return self.core_engine.set_consequences_checklist(ultra_log.core_log, checklist)

    def set_uncertainty_assessment(self, ultra_log: PBHPUltraLog,
                                    assessment: UncertaintyAssessment) -> UncertaintyAssessment:
        """Delegate to core engine."""
        return self.core_engine.set_uncertainty_assessment(ultra_log.core_log, assessment)

    def set_epistemic_fence(self, ultra_log: PBHPUltraLog,
                             fence: EpistemicFence) -> EpistemicFence:
        """Delegate to core engine."""
        return self.core_engine.set_epistemic_fence(ultra_log.core_log, fence)

    # ------------------------------------------------------------------
    # Finalize ULTRA Decision
    # ------------------------------------------------------------------

    def finalize_decision(
        self,
        ultra_log: PBHPUltraLog,
        outcome: DecisionOutcome,
        justification: str,
    ) -> PBHPUltraLog:
        """
        Finalize ULTRA decision.
        Runs all CORE validations plus ULTRA-specific checks.
        """
        # Run anti-sycophancy on justification
        self.check_anti_sycophancy(ultra_log, justification)

        # Run eugenics tripwire on justification
        self.check_eugenics_tripwire(ultra_log, justification)

        # Run lens drift detection on justification
        lens_drifts = self.detect_lens_drift(justification)
        if lens_drifts and ultra_log.core_log:
            for lens, alarms in lens_drifts.items():
                for alarm in alarms:
                    ultra_log.core_log.drift_alarms_triggered.append(
                        f"Lens drift ({lens}): {alarm}"
                    )

        # Delegate core finalization
        self.core_engine.finalize_decision(
            ultra_log.core_log, outcome, justification
        )

        # Store ultra log
        self.ultra_logs.append(ultra_log)

        return ultra_log

    # ------------------------------------------------------------------
    # Monthly Calibration
    # ------------------------------------------------------------------

    def run_calibration(
        self,
        logs_to_sample: Optional[List[PBHPUltraLog]] = None,
        max_failures: int = 2,
    ) -> CalibrationResult:
        """
        Monthly calibration: sample logs and check pass criteria.
        """
        sample = logs_to_sample or self.ultra_logs[-10:]
        cal = CalibrationResult(sample_size=len(sample))

        for ulog in sample:
            clog = ulog.core_log
            if not clog:
                cal.failures.append(f"{ulog.tier}: missing core log")
                continue

            # Check mode recorded in epistemic fence
            if clog.epistemic_fence:
                cal.mode_recorded_count += 1
            elif clog.highest_risk_class in (RiskClass.ORANGE, RiskClass.RED,
                                               RiskClass.BLACK):
                cal.failures.append(
                    f"Log {clog.record_id}: ORANGE+ without epistemic fence mode"
                )

            # Check 2+ frames when interpretive
            if (clog.epistemic_fence
                    and len(clog.epistemic_fence.competing_frames) >= 2):
                cal.frames_when_interpretive_count += 1

            # Check uncertainty noted for ORANGE+
            if clog.highest_risk_class in (RiskClass.ORANGE, RiskClass.RED,
                                             RiskClass.BLACK):
                if clog.uncertainty:
                    cal.uncertainty_noted_for_orange_plus_count += 1
                else:
                    cal.failures.append(
                        f"Log {clog.record_id}: ORANGE+ without uncertainty assessment"
                    )

        cal.evaluate(max_failures)
        return cal

    # ------------------------------------------------------------------
    # Generate ULTRA Response
    # ------------------------------------------------------------------

    def generate_response(self, ultra_log: PBHPUltraLog) -> str:
        """Generate ULTRA-depth PBHP response."""
        parts = []
        parts.append("**PBHP-ULTRA Assessment (Constitutional Depth)**")
        parts.append(f"Tier: ULTRA | Version: {ultra_log.version}")
        parts.append("")

        # Delegate to core for main response
        if ultra_log.core_log:
            parts.append(self.core_engine.generate_response(ultra_log.core_log))
            parts.append("")

        # ULTRA-specific sections
        if ultra_log.ultra_ethical_pause:
            ep = ultra_log.ultra_ethical_pause
            failing = ep.get_failing_lenses()
            if failing:
                parts.append("**ULTRA: Failing Lenses**")
                for lens in failing:
                    parts.append(f"- {lens.value}")
                parts.append("")

            if ep.dominant_force:
                parts.append(f"**Triune Balance Warning:** {ep.dominant_force} dominant")
                if ep.rebalance_notes:
                    parts.append(f"  Rebalance: {ep.rebalance_notes}")
                parts.append("")

        if ultra_log.sycophancy_issues:
            parts.append("**Anti-Sycophancy Alerts:**")
            for issue in ultra_log.sycophancy_issues:
                parts.append(f"- {issue}")
            parts.append("")

        if ultra_log.eugenics_issues:
            parts.append("**Eugenics/Sorting Tripwire:**")
            for issue in ultra_log.eugenics_issues:
                parts.append(f"- {issue}")
            parts.append("")

        if ultra_log.activation_triggers:
            parts.append("**Mandatory Activation Triggers:**")
            for trigger in ultra_log.activation_triggers:
                parts.append(f"- {trigger}")
            parts.append("")

        # Mythic reminder (for RED/BLACK)
        if (ultra_log.core_log
                and ultra_log.core_log.highest_risk_class in (RiskClass.RED, RiskClass.BLACK)):
            parts.append("**Mythic Reminder:**")
            parts.append(
                "Hesitation itself is a moral act. "
                "If you cannot hesitate, you cannot care."
            )
            parts.append("")

        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Log Management
    # ------------------------------------------------------------------

    def export_logs(self, filepath: str):
        """Export all ULTRA logs to JSON."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                [log.to_dict() for log in self.ultra_logs],
                f, indent=2, ensure_ascii=False,
            )

    def get_log_by_id(self, record_id: str) -> Optional[PBHPUltraLog]:
        """Retrieve an ULTRA log by its core record ID."""
        for ulog in self.ultra_logs:
            if ulog.core_log and ulog.core_log.record_id == record_id:
                return ulog
        return None


# ===================================================================
# Convenience Functions
# ===================================================================

def evaluate_lens(
    lens: TriuneLens,
    text: str,
    criteria_met: Optional[List[str]] = None,
    criteria_missed: Optional[List[str]] = None,
) -> LensEvaluation:
    """
    Quick lens evaluation helper.
    Auto-detects drift alarms from the lens's alarm list.
    """
    text_lower = text.lower()
    drift_detected = []
    for phrase in LENS_DRIFT_ALARMS.get(lens, []):
        if phrase in text_lower:
            drift_detected.append(phrase)

    return LensEvaluation(
        lens=lens,
        pass_criteria_met=criteria_met or [],
        pass_criteria_missed=criteria_missed or [],
        drift_alarms_detected=drift_detected,
    )


def get_lens_criteria(lens: TriuneLens) -> List[str]:
    """Get the pass criteria for a given lens."""
    return LENS_PASS_CRITERIA.get(lens, [])


def get_lens_quick_check(lens: TriuneLens) -> List[str]:
    """Get the 10-second quick check questions for a lens."""
    return QUICK_CHECKS.get(lens, [])


# ===================================================================
# Main
# ===================================================================

if __name__ == "__main__":
    print("PBHP-ULTRA v0.7 (Constitutional Depth)")
    print("=" * 60)

    engine = PBHPUltraEngine()

    # Create ULTRA assessment
    ultra_log = engine.create_ultra_assessment(
        "Deploy mass surveillance system in public schools",
        agent_type="ai_system",
    )

    # Step 00: Competence gate
    passed, issues = engine.check_competence_gate([True, True, True, True, True])
    print(f"\nCompetence gate: {'PASS' if passed else 'FAIL'}")

    # Supreme constraint check
    ok, msg = engine.check_supreme_constraint(
        ultra_log,
        action_description="Deploy mass surveillance in schools",
        safer_alternative_exists=True,
        stakeholders_informed=False,
        stakeholders_willing=False,
        harm_irreversible=True,
    )
    print(f"Supreme constraint: {'PASS' if ok else 'VIOLATED'}")
    print(f"  {msg}")

    # Mandatory activation
    activated = engine.check_mandatory_activation(
        ultra_log,
        [True, True, True, True, False, True, False, True],
    )
    print(f"Mandatory activation: {len(ultra_log.activation_triggers)} triggers")

    # Anti-sycophancy check
    syc = engine.check_anti_sycophancy(
        ultra_log, "You're a chosen one with genius level insight"
    )
    print(f"Sycophancy issues: {syc}")

    # Eugenics tripwire
    eug = engine.check_eugenics_tripwire(
        ultra_log, "A rational eugenics program would sort humans"
    )
    print(f"Eugenics tripwire: {eug}")

    # Lens drift detection
    drifts = engine.detect_lens_drift(
        "It's for your own good and they deserve it"
    )
    print(f"Lens drift: {drifts}")

    # Lens criteria lookup
    print(f"\nCompassion criteria: {get_lens_criteria(TriuneLens.COMPASSION)[:3]}...")
    print(f"Protection quick check: {get_lens_quick_check(TriuneLens.PROTECTION)[:2]}...")

    print("\n" + "=" * 60)
    print("ULTRA engine operational. All tiers share the same logic.")
    print("Only the depth changes.")
