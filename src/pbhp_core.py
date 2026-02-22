"""
Pause-Before-Harm Protocol (PBHP) - Core Implementation
Version: 0.7.1 (Full Specification)

A decision-making framework for humans and AI systems to evaluate
actions that could cause harm, with emphasis on protecting vulnerable
groups and maintaining ethical accountability.

This implementation faithfully encodes the complete PBHP v0.7.1 protocol
including all foundation gates, seven steps, epistemic fencing,
red team review, drift detection, tone constraints, uncertainty
framework, structured logging, and two-phase commit validation.

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Tuple
import uuid
import json
import re
import difflib


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class ImpactLevel(Enum):
    """Impact severity levels for potential harms."""
    TRIVIAL = "trivial"
    MODERATE = "moderate"
    SEVERE = "severe"
    CATASTROPHIC = "catastrophic"


class LikelihoodLevel(Enum):
    """Likelihood assessment for potential harms."""
    UNLIKELY = "unlikely"
    POSSIBLE = "possible"
    LIKELY = "likely"
    IMMINENT = "imminent"


class RiskClass(Enum):
    """Risk classification gates that determine action requirements."""
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"
    BLACK = "black"


class DecisionOutcome(Enum):
    """Final decision outcomes for PBHP assessment."""
    PROCEED = "proceed"
    PROCEED_MODIFIED = "proceed_modified"
    REDIRECT = "redirect"
    DELAY = "delay"
    REFUSE = "refuse"
    ESCALATE = "escalate"


class Mode(Enum):
    """Epistemic mode for handling uncertainty."""
    EXPLORE = "explore"
    COMPRESS = "compress"


class AttributionLevel(Enum):
    """
    Evidence levels for attributing intent (IAM Module).

    Level A - Safe, always defensible: "Misleading as written."
    Level B - Negligent / careless framing: "Careless marketing."
    Level C - Reckless disregard (pattern): "Repeatedly posts misleading framing."
    Level D - Knowing deception: Requires prior-correction proof,
              internal-knowledge proof, or systematic pattern proof.
    """
    LEVEL_A = "safe"
    LEVEL_B = "negligent"
    LEVEL_C = "reckless"
    LEVEL_D = "knowing"


class ClaimType(Enum):
    """
    IAM claim types - must be separated in analysis.
    """
    CONTENT = "content"       # Observable: "They said X."
    ACCURACY = "accuracy"     # Verifiable: "X is false/misleading."
    INTENT = "intent"         # Inferred: "They knowingly deceived."


class EvidenceTag(Enum):
    """
    Epistemic tagging for claims.
    """
    FACT = "F"            # Direct fact from provided text/data
    VERIFIED = "V"        # Verified with source/check
    INFERENCE = "I"       # Inference (confidence required)
    HYPOTHESIS = "H"      # One of multiple frames
    SPECULATIVE = "S"     # Speculative/creative read (fenced off)


class UncertaintyLevel(Enum):
    """Uncertainty classification for harm estimates."""
    SOLID = "S"       # Multiple independent sources agree
    FUZZY = "F"       # Analysts disagree; incomplete data
    SPECULATIVE = "X" # Conjectural; theoretical


class Confidence(Enum):
    """Confidence levels for PBHP assessments."""
    LOW = "low"
    MEDIUM_LOW = "medium-low"
    MEDIUM = "medium"
    MEDIUM_HIGH = "medium-high"
    HIGH = "high"


# ---------------------------------------------------------------------------
# Absolute Rejection Categories (Step 0g)
# ---------------------------------------------------------------------------

ABSOLUTE_REJECTION_CATEGORIES = [
    "fascism",
    "genocide",
    "slavery",
    "non-consensual authoritarian control",
    "systemic dehumanization of a group",
]


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Harm:
    """
    Represents a potential harm identified in Step 2.
    Includes full risk calculation per PBHP v0.7 deterministic rules.
    """
    description: str
    impact: ImpactLevel
    likelihood: LikelihoodLevel
    irreversible: bool
    power_asymmetry: bool
    affected_parties: List[str]
    least_powerful_affected: str
    notes: str = ""
    uncertainty_level: UncertaintyLevel = UncertaintyLevel.FUZZY
    evidence_basis: str = ""
    audience_risk_elevated: bool = False

    def calculate_risk_class(self) -> RiskClass:
        """
        Calculate risk class based on harm characteristics.
        Implements the deterministic escalation rules from PBHP v0.7.

        Rules applied in order:
        - BLACK: Catastrophic + Irreversible + (Likely or Imminent)
        - RED: Catastrophic + Irreversible (any likelihood)
               OR Severe + Irreversible + (Likely or Imminent)
               OR Power + Irreversible + (Severe or Catastrophic)
        - ORANGE: Severe + Possible
                  OR Moderate + (Likely or Imminent)
                  OR Power + Irreversible (minimum ORANGE regardless)
        - YELLOW: Moderate + Possible
                  OR Trivial + (Likely or Imminent)
        - GREEN: default
        """
        risk = self._base_risk_class()

        # Audience risk elevation: treat one step higher
        if self.audience_risk_elevated:
            risk = self._elevate_risk_class(risk)

        return risk

    def _base_risk_class(self) -> RiskClass:
        """Core deterministic risk calculation."""
        # BLACK: Catastrophic + Irreversible + (Likely or Imminent)
        if (self.impact == ImpactLevel.CATASTROPHIC
                and self.irreversible
                and self.likelihood in (LikelihoodLevel.LIKELY,
                                       LikelihoodLevel.IMMINENT)):
            return RiskClass.BLACK

        # RED conditions
        if self.impact == ImpactLevel.CATASTROPHIC and self.irreversible:
            return RiskClass.RED

        if (self.impact == ImpactLevel.SEVERE
                and self.irreversible
                and self.likelihood in (LikelihoodLevel.LIKELY,
                                       LikelihoodLevel.IMMINENT)):
            return RiskClass.RED

        if (self.power_asymmetry
                and self.irreversible
                and self.impact in (ImpactLevel.SEVERE,
                                    ImpactLevel.CATASTROPHIC)):
            return RiskClass.RED

        # ORANGE conditions
        if (self.impact == ImpactLevel.SEVERE
                and self.likelihood == LikelihoodLevel.POSSIBLE):
            return RiskClass.ORANGE

        if (self.impact == ImpactLevel.MODERATE
                and self.likelihood in (LikelihoodLevel.LIKELY,
                                        LikelihoodLevel.IMMINENT)):
            return RiskClass.ORANGE

        # Power + Irreversible always minimum ORANGE
        if self.power_asymmetry and self.irreversible:
            return RiskClass.ORANGE

        # YELLOW conditions
        if (self.impact == ImpactLevel.MODERATE
                and self.likelihood == LikelihoodLevel.POSSIBLE):
            return RiskClass.YELLOW

        if (self.impact == ImpactLevel.TRIVIAL
                and self.likelihood in (LikelihoodLevel.LIKELY,
                                        LikelihoodLevel.IMMINENT)):
            return RiskClass.YELLOW

        # GREEN (default)
        return RiskClass.GREEN

    @staticmethod
    def _elevate_risk_class(risk: 'RiskClass') -> 'RiskClass':
        """Elevate risk class by one step (audience risk note)."""
        order = [RiskClass.GREEN, RiskClass.YELLOW, RiskClass.ORANGE,
                 RiskClass.RED, RiskClass.BLACK]
        idx = order.index(risk)
        return order[min(idx + 1, len(order) - 1)]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "impact": self.impact.value,
            "likelihood": self.likelihood.value,
            "irreversible": self.irreversible,
            "power_asymmetry": self.power_asymmetry,
            "affected_parties": self.affected_parties,
            "least_powerful_affected": self.least_powerful_affected,
            "notes": self.notes,
            "uncertainty_level": self.uncertainty_level.value,
            "evidence_basis": self.evidence_basis,
            "audience_risk_elevated": self.audience_risk_elevated,
            "risk_class": self.calculate_risk_class().value,
        }


@dataclass
class DoorWallGap:
    """
    Door/Wall/Gap analysis (Step 0e).
    Mandatory micro-module to prevent PBHP from defaulting inside
    an imposed system.

    Wall: What constraint am I operating inside of right now?
    Gap:  Where could harm leak through despite good intent?
    Door: What is the smallest real escape vector available right now?

    The Door must be a concrete action (delay, verify, narrow scope,
    refuse), not a feeling ('be careful') or a slogan.
    """
    wall: str
    gap: str
    door: str

    def has_door(self) -> bool:
        """
        Check if a concrete door (escape vector) exists.
        Uses regex patterns to catch vague doors, not just exact strings.
        A valid door must be a concrete action: delay, verify, narrow scope,
        refuse — not a feeling or slogan.
        """
        if not self.door or not self.door.strip():
            return False
        door_lower = self.door.strip().lower()

        # Regex patterns for vague/non-actionable doors
        vague_door_patterns = [
            r"^be\s+(more\s+)?(careful|cautious|mindful|aware|thoughtful)$",
            r"^try\s+(harder|better|more)$",
            r"^do\s+(better|more)$",
            r"^think\s+(about|on|over)\s+it$",
            r"^hope\s+for\s+the\s+best$",
            r"^just\s+be\s+(good|nice|careful)$",
            r"^pay\s+(more\s+)?attention$",
            r"^keep\s+(an\s+)?eye\s+on\s+it$",
            r"^watch\s+(out|carefully)$",
            r"^stay\s+(alert|vigilant|aware)$",
            r"^use\s+(good\s+)?judgm?ent$",
            r"^trust\s+(the\s+)?process$",
            r"^it'?ll?\s+be\s+(fine|ok|okay|alright)$",
        ]
        for pattern in vague_door_patterns:
            if re.match(pattern, door_lower):
                return False

        # Door must be at least a few words to be a concrete action
        if len(door_lower.split()) < 2:
            return False

        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "wall": self.wall,
            "gap": self.gap,
            "door": self.door,
            "has_concrete_door": self.has_door(),
        }


@dataclass
class CHIMCheck:
    """
    CHIM Check - Agency Under Constraint (Step 0f).

    Prevents surrender of agency to perceived inevitability.
    If the system cannot name a remaining choice, PBHP must
    pause or refuse until that claim is validated.

    If the system concludes 'no choice' twice in a row, it must
    reframe the problem in at least two alternative framings and
    re-run Door/Wall/Gap each time.
    """
    constraint_recognized: bool
    treating_as_absolute: bool
    no_choice_claim: bool
    remaining_choice: str
    no_choice_evaluated: bool = True
    reframes: List[str] = field(default_factory=list)
    consecutive_no_choice_count: int = 0

    def requires_pause(self) -> bool:
        """Determine if CHIM check requires pause."""
        if self.no_choice_claim and not self.remaining_choice:
            return True
        if self.consecutive_no_choice_count >= 2 and len(self.reframes) < 2:
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "constraint_recognized": self.constraint_recognized,
            "treating_as_absolute": self.treating_as_absolute,
            "no_choice_claim": self.no_choice_claim,
            "no_choice_evaluated": self.no_choice_evaluated,
            "remaining_choice": self.remaining_choice,
            "reframes": self.reframes,
            "requires_pause": self.requires_pause(),
        }


@dataclass
class EthicalPausePosture:
    """
    Step 0a: Ethical Pause - Internal Posture.

    Balances three forces (triune "minds"):
    - Compassion/Empathy/Love/Protection/Courage
    - Logic/Intelligence/Clarity/Craft/Responsibility
    - Paradox/Integration/Artistry/Red Team

    This is a posture, not a metric - roughly one-third attention on each.
    """
    action_statement: str  # "What exactly am I about to do?"
    compassion_notes: str = ""
    logic_notes: str = ""
    paradox_notes: str = ""
    balance_assessment: str = "roughly balanced"
    high_arousal_state: bool = False  # anger, euphoria, sleep-deprived
    high_arousal_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_statement": self.action_statement,
            "compassion_notes": self.compassion_notes,
            "logic_notes": self.logic_notes,
            "paradox_notes": self.paradox_notes,
            "balance_assessment": self.balance_assessment,
            "high_arousal_state": self.high_arousal_state,
            "high_arousal_notes": self.high_arousal_notes,
        }


@dataclass
class QuickRiskCheck:
    """
    Step 0d: Ethical Pause Quick Risk Check.
    Fast pre-screening before full protocol.
    """
    obviously_low_risk: bool
    silence_delay_protects_more: Optional[bool] = None
    should_tighten: bool = False
    notes: str = ""

    def evaluate(self) -> bool:
        """Returns True if behavior should be tightened."""
        if not self.obviously_low_risk:
            if self.silence_delay_protects_more is True:
                self.should_tighten = True
            elif self.silence_delay_protects_more is None:
                self.should_tighten = True
        return self.should_tighten

    def to_dict(self) -> Dict[str, Any]:
        return {
            "obviously_low_risk": self.obviously_low_risk,
            "silence_delay_protects_more": self.silence_delay_protects_more,
            "should_tighten": self.should_tighten,
            "notes": self.notes,
        }


@dataclass
class AbsoluteRejectionCheck:
    """
    Step 0g: Absolute Rejection Check.

    If the action's core function upholds fascism, genocide, slavery,
    non-consensual authoritarian control, or systemic dehumanization,
    then REFUSE. Only allow discussion in critique/dismantling/prevention mode.
    """
    action_description: str
    triggers_rejection: bool = False
    matched_categories: List[str] = field(default_factory=list)
    analysis_mode: str = ""  # "critique", "dismantling", "prevention", or ""

    def evaluate(self, action_text: str) -> bool:
        """
        Check if action triggers absolute rejection.
        Returns True if action must be refused.
        """
        text_lower = action_text.lower()
        self.matched_categories = []
        for category in ABSOLUTE_REJECTION_CATEGORIES:
            if category in text_lower:
                self.matched_categories.append(category)

        # Also check for euphemistic patterns
        euphemism_patterns = [
            r"ethnic\s+cleansing",
            r"final\s+solution",
            r"master\s+race",
            r"racial\s+purity",
            r"forced\s+labor",
            r"concentration\s+camp",
            r"forced\s+sterilization",
            r"eugenics.*rational",
            r"sort.*humans.*lesser",
        ]
        for pattern in euphemism_patterns:
            if re.search(pattern, text_lower):
                self.matched_categories.append(f"euphemism:{pattern}")

        self.triggers_rejection = len(self.matched_categories) > 0
        return self.triggers_rejection

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_description": self.action_description,
            "triggers_rejection": self.triggers_rejection,
            "matched_categories": self.matched_categories,
            "analysis_mode": self.analysis_mode,
        }


@dataclass
class ConsentCheck:
    """
    Step 4: Consent and Representation Check.

    Would the affected parties reasonably agree if they understood
    the situation?
    """
    explicit_consent: bool
    informed_hypothetical_consent: Optional[bool] = None
    overriding_preferences: bool = False
    compatible_with_dignity: bool = True
    honest_framing: bool = True
    who_didnt_get_a_say: List[str] = field(default_factory=list)
    notes: str = ""

    def requires_action(self) -> str:
        """
        Determine required action based on consent analysis.
        Returns: "proceed", "delay", "seek_info", or "narrow"
        """
        if self.explicit_consent:
            return "proceed"
        if not self.compatible_with_dignity:
            return "narrow"
        if self.overriding_preferences:
            return "delay"
        if self.informed_hypothetical_consent is None:
            return "seek_info"
        if self.informed_hypothetical_consent:
            return "proceed"
        return "delay"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "explicit_consent": self.explicit_consent,
            "informed_hypothetical_consent": self.informed_hypothetical_consent,
            "overriding_preferences": self.overriding_preferences,
            "compatible_with_dignity": self.compatible_with_dignity,
            "honest_framing": self.honest_framing,
            "who_didnt_get_a_say": self.who_didnt_get_a_say,
            "required_action": self.requires_action(),
            "notes": self.notes,
        }


@dataclass
class ConsequencesChecklist:
    """
    Temporal + Cultural Impact Modeling - Consequences Checklist.
    For high-stakes decisions: 22 questions across 6 categories.
    Each answer: "yes" / "no" / "unsure" (unsure counts as yes for gating).
    """
    # Baseline Reality Check
    historical_analogs: List[str] = field(default_factory=list)
    past_harms_unpredicted: List[str] = field(default_factory=list)
    past_mitigation_failures: List[str] = field(default_factory=list)
    past_disproportionate_groups: List[str] = field(default_factory=list)
    past_defender_claims: List[str] = field(default_factory=list)

    # Status Quo Harm Audit
    current_harm_if_nothing: str = ""
    who_benefits_status_quo: str = ""
    inaction_continues_harm: Optional[bool] = None  # None = unsure

    # Time Horizon Scan
    immediate_harms: str = ""          # 0-72 hours
    short_term_harms: str = ""         # 1-12 weeks
    medium_term_harms: str = ""        # 3-24 months
    long_term_harms: str = ""          # 2-10+ years
    any_horizon_irreversible: bool = False

    # Cultural and Institutional Effects (Q5-Q8)
    normalizes_harm: Optional[bool] = None
    shifts_to_ends_justify_means: Optional[bool] = None
    erodes_institutional_trust: Optional[bool] = None
    rewards_bad_behavior: Optional[bool] = None

    # Power and Representation Effects (Q9-Q12)
    burdens_fall_on_low_power: Optional[bool] = None
    reduces_exit_appeal_optout: Optional[bool] = None
    increases_surveillance_coercion: Optional[bool] = None
    decision_makers_insulated: Optional[bool] = None

    # Drift and Abuse Resistance (Q13-Q15)
    bad_actor_misuse: str = ""
    adjacent_use_prediction: str = ""
    permanence_risk: str = ""

    # Narrative and Honesty Test (Q16-Q18)
    can_describe_plainly_to_harmed: Optional[bool] = None
    transparency_changes_consent: Optional[bool] = None
    relying_on_euphemism: Optional[bool] = None

    # Repair and Exit Requirements (Q19-Q22)
    rollback_plan: str = ""
    sunset_condition: str = ""
    independent_stop_authority: str = ""
    smallest_door: str = ""

    def has_critical_flags(self) -> Dict[str, bool]:
        """
        Check for critical flags that require action.
        "Unsure" (None) counts as "yes" for gating.
        """
        flags = {}

        # Category A: Irreversible harm
        flags["irreversible_harm"] = self.any_horizon_irreversible

        # Category C: Agency loss
        agency_flags = [
            self.reduces_exit_appeal_optout,
            self.increases_surveillance_coercion,
        ]
        flags["agency_loss"] = any(f is True or f is None for f in agency_flags)

        # Category D: Abuse/drift
        flags["abuse_drift"] = bool(self.bad_actor_misuse or self.permanence_risk)

        # Power asymmetry
        power_flags = [
            self.burdens_fall_on_low_power,
            self.decision_makers_insulated,
        ]
        flags["power_asymmetry"] = any(f is True or f is None for f in power_flags)

        # Honesty
        flags["honesty_concern"] = (
            self.transparency_changes_consent is True
            or self.transparency_changes_consent is None
            or self.relying_on_euphemism is True
            or self.relying_on_euphemism is None
        )

        # Norm erosion
        norm_flags = [
            self.normalizes_harm,
            self.shifts_to_ends_justify_means,
            self.erodes_institutional_trust,
            self.rewards_bad_behavior,
        ]
        flags["norm_erosion"] = any(f is True or f is None for f in norm_flags)

        # Missing repair
        flags["missing_repair"] = (
            not self.rollback_plan
            and not self.sunset_condition
            and not self.independent_stop_authority
        )

        return flags

    def requires_door_chim_rerun(self) -> bool:
        """
        Any yes/unsure in A (irreversible), C (agency loss),
        or D (abuse/drift) means: do not proceed without concrete
        Door + CHIM check + safer alternative search.
        """
        flags = self.has_critical_flags()
        return (flags["irreversible_harm"]
                or flags["agency_loss"]
                or flags["abuse_drift"])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "historical_analogs": self.historical_analogs,
            "status_quo": {
                "current_harm_if_nothing": self.current_harm_if_nothing,
                "who_benefits_status_quo": self.who_benefits_status_quo,
                "inaction_continues_harm": self.inaction_continues_harm,
            },
            "time_horizon": {
                "immediate": self.immediate_harms,
                "short_term": self.short_term_harms,
                "medium_term": self.medium_term_harms,
                "long_term": self.long_term_harms,
                "any_horizon_irreversible": self.any_horizon_irreversible,
            },
            "cultural_effects": {
                "normalizes_harm": self.normalizes_harm,
                "ends_justify_means": self.shifts_to_ends_justify_means,
                "erodes_trust": self.erodes_institutional_trust,
                "rewards_bad_behavior": self.rewards_bad_behavior,
            },
            "power_effects": {
                "burdens_on_low_power": self.burdens_fall_on_low_power,
                "reduces_exit_appeal": self.reduces_exit_appeal_optout,
                "increases_surveillance": self.increases_surveillance_coercion,
                "decision_makers_insulated": self.decision_makers_insulated,
            },
            "drift_abuse": {
                "bad_actor_misuse": self.bad_actor_misuse,
                "adjacent_use": self.adjacent_use_prediction,
                "permanence_risk": self.permanence_risk,
            },
            "honesty": {
                "can_describe_to_harmed": self.can_describe_plainly_to_harmed,
                "transparency_changes_consent": self.transparency_changes_consent,
                "relying_on_euphemism": self.relying_on_euphemism,
            },
            "repair": {
                "rollback_plan": self.rollback_plan,
                "sunset_condition": self.sunset_condition,
                "independent_stop_authority": self.independent_stop_authority,
                "smallest_door": self.smallest_door,
            },
            "critical_flags": self.has_critical_flags(),
            "requires_door_chim_rerun": self.requires_door_chim_rerun(),
        }


@dataclass
class EpistemicFence:
    """
    Epistemic Fence - Full implementation (Step 7, Section 6A-6G).

    Handles uncertainty, competing frames, attribution, and
    compression honesty. Required for public-facing / ORANGE+ outputs.
    """
    # 6A: Mode
    mode: Mode
    mode_justification: str = ""

    # 6B: Anchors
    action_anchor: str = ""
    wall_anchor: str = ""
    least_powerful_anchor: str = ""
    non_negotiable_anchor: str = ""

    # 6C: Reality Separation
    facts: List[str] = field(default_factory=list)
    inferences: List[Tuple[str, str]] = field(default_factory=list)  # (inference, confidence)
    unknowns: List[str] = field(default_factory=list)
    update_trigger: str = ""

    # Attribution
    attribution_level: Optional[AttributionLevel] = None
    attribution_evidence: str = ""

    # 6D: Competing Frames (2-5)
    competing_frames: List[Dict[str, str]] = field(default_factory=list)
    # Each frame: {"frame": ..., "explains": ..., "ignores": ..., "falsifier": ...}

    # 6E: Decision/Recommendation
    recommendation: str = ""
    recommendation_basis: str = ""  # References Facts/Inferences

    # 6F: Door/Wall/Gap (restatement in fence context)
    fence_door: str = ""
    fence_wall: str = ""
    fence_gap: str = ""

    # 6G: Compression Honesty
    irreducible_ambiguity: str = ""
    least_wrong_short_version: str = ""
    what_short_version_drops: str = ""

    def validate(self) -> List[str]:
        """Validate epistemic fence for high-stakes decisions."""
        issues = []

        if self.mode == Mode.COMPRESS and not self.unknowns:
            issues.append("COMPRESS mode requires explicit unknowns")

        if self.mode == Mode.COMPRESS and not self.update_trigger:
            issues.append("COMPRESS mode requires update trigger "
                          "(what would change recommendation)")

        if self.mode == Mode.EXPLORE and len(self.competing_frames) < 2:
            issues.append("EXPLORE mode requires at least 2 competing frames")

        if (self.attribution_level == AttributionLevel.LEVEL_D
                and not self.attribution_evidence):
            issues.append(
                "Level D attribution (knowing deception) requires cited evidence"
            )

        # Check premature collapse indicators
        if self.mode == Mode.COMPRESS and len(self.competing_frames) < 2:
            issues.append(
                "Potential premature collapse: COMPRESS with fewer than 2 frames. "
                "Consider switching to EXPLORE mode."
            )

        return issues

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode.value,
            "mode_justification": self.mode_justification,
            "anchors": {
                "action": self.action_anchor,
                "wall": self.wall_anchor,
                "least_powerful": self.least_powerful_anchor,
                "non_negotiable": self.non_negotiable_anchor,
            },
            "reality_separation": {
                "facts": self.facts,
                "inferences": [{"claim": i[0], "confidence": i[1]}
                               for i in self.inferences],
                "unknowns": self.unknowns,
                "update_trigger": self.update_trigger,
            },
            "attribution": {
                "level": self.attribution_level.value if self.attribution_level else None,
                "evidence": self.attribution_evidence,
            },
            "competing_frames": self.competing_frames,
            "recommendation": {
                "decision": self.recommendation,
                "basis": self.recommendation_basis,
            },
            "door_wall_gap": {
                "door": self.fence_door,
                "wall": self.fence_wall,
                "gap": self.fence_gap,
            },
            "compression_honesty": {
                "irreducible_ambiguity": self.irreducible_ambiguity,
                "least_wrong_short_version": self.least_wrong_short_version,
                "what_it_drops": self.what_short_version_drops,
            },
            "validation_issues": self.validate(),
        }


@dataclass
class RedTeamReview:
    """
    Red Team Review - Adversarial Stress Test.
    Required for ORANGE, RED, and BLACK risk classes.

    Includes the full question set, empathy pass,
    drift alarms, and outcome determination.
    """
    # Core questions (must attempt all)
    failure_modes: List[str] = field(default_factory=list)
    abuse_vectors: List[str] = field(default_factory=list)
    who_bears_risk: str = ""
    false_assumptions: List[str] = field(default_factory=list)
    normalization_risk: str = ""

    # Additional required questions
    alternative_interpretations: List[str] = field(default_factory=list)
    claim_tags: str = ""  # Which parts are [F] vs [I]/[H]/[S]
    wrong_inference_consequences: str = ""

    # Empathy pass (accuracy, not excuse)
    steelman_other_side: str = ""
    motives_vs_outcomes: str = ""
    incentives_pressures: str = ""
    message_reception_prediction: str = ""
    off_ramps_identified: List[str] = field(default_factory=list)
    boundaries_maintained: bool = True

    # Drift alarms during review
    drift_alarms_detected: List[str] = field(default_factory=list)

    # Outcome
    mitigation_applied: bool = False
    issues_resolved: bool = False
    outcome: str = ""  # "no_issues", "mitigated", "unresolved"

    def determine_outcome(self) -> str:
        """
        Determine Red Team outcome.
        If credible misuse path with severe/irreversible harm and
        no mitigation, action must not proceed.
        """
        has_severe_misuse = any(
            "severe" in v.lower() or "irreversible" in v.lower()
            for v in self.abuse_vectors
        )

        if not self.failure_modes and not self.abuse_vectors:
            self.outcome = "no_issues"
        elif self.mitigation_applied and self.issues_resolved:
            self.outcome = "mitigated"
        elif has_severe_misuse and not self.mitigation_applied:
            self.outcome = "unresolved"
        elif self.issues_resolved:
            self.outcome = "mitigated"
        else:
            self.outcome = "unresolved"

        return self.outcome

    def to_dict(self) -> Dict[str, Any]:
        return {
            "failure_modes": self.failure_modes,
            "abuse_vectors": self.abuse_vectors,
            "who_bears_risk": self.who_bears_risk,
            "false_assumptions": self.false_assumptions,
            "normalization_risk": self.normalization_risk,
            "alternative_interpretations": self.alternative_interpretations,
            "claim_tags": self.claim_tags,
            "wrong_inference_consequences": self.wrong_inference_consequences,
            "empathy_pass": {
                "steelman": self.steelman_other_side,
                "motives_vs_outcomes": self.motives_vs_outcomes,
                "incentives_pressures": self.incentives_pressures,
                "message_reception": self.message_reception_prediction,
                "off_ramps": self.off_ramps_identified,
                "boundaries_maintained": self.boundaries_maintained,
            },
            "drift_alarms": self.drift_alarms_detected,
            "mitigation_applied": self.mitigation_applied,
            "issues_resolved": self.issues_resolved,
            "outcome": self.outcome,
        }


@dataclass
class Alternative:
    """Safer alternative to the proposed action (Step 5)."""
    description: str
    preserves_goal: bool
    reduces_harm: bool
    reversible: bool
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "preserves_goal": self.preserves_goal,
            "reduces_harm": self.reduces_harm,
            "reversible": self.reversible,
            "notes": self.notes,
        }


@dataclass
class UncertaintyAssessment:
    """
    Uncertainty framework from PBHP's decision-under-uncertainty section.
    Structured approach to handling incomplete information.
    """
    # Named uncertainties (not vibed)
    solid_claims: List[str] = field(default_factory=list)    # (S) solid
    fuzzy_claims: List[str] = field(default_factory=list)     # (F) fuzzy
    speculative_claims: List[str] = field(default_factory=list)  # (X) speculative

    # Bounded scenarios
    best_case: str = ""
    central_case: str = ""
    worst_plausible_case: str = ""
    worst_case_who_pays: str = ""

    # Action vs inaction comparison
    act_and_wrong_harms: str = ""
    act_and_wrong_who: str = ""
    dont_act_and_wrong_harms: str = ""
    dont_act_and_wrong_who: str = ""

    # Uncertain-but-high-stakes rule evaluation
    potential_harm_high_hard_to_undo: bool = False
    harm_falls_on_low_power: bool = False
    benefits_speculative: bool = False
    # If all three True -> default to shrink/slow/oppose

    potential_harm_low_reversible: bool = False
    benefit_to_low_power_high: bool = False
    # If both True -> acceptable to act with monitoring

    # Reversibility design
    prefers_reversible: bool = True
    off_ramps: List[str] = field(default_factory=list)
    sunset_clause: str = ""

    # Key questions before deadline
    decision_changing_questions: List[str] = field(default_factory=list)
    can_answer_before_deadline: bool = True

    # Confidence
    confidence: Confidence = Confidence.MEDIUM
    biggest_might_be_wrong: str = ""

    def should_default_oppose(self) -> bool:
        """Apply the uncertain-but-high-stakes rule."""
        return (self.potential_harm_high_hard_to_undo
                and self.harm_falls_on_low_power
                and self.benefits_speculative)

    def can_act_with_monitoring(self) -> bool:
        """Check if acting under uncertainty is acceptable."""
        return (self.potential_harm_low_reversible
                and self.benefit_to_low_power_high)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claims": {
                "solid": self.solid_claims,
                "fuzzy": self.fuzzy_claims,
                "speculative": self.speculative_claims,
            },
            "scenarios": {
                "best_case": self.best_case,
                "central_case": self.central_case,
                "worst_plausible_case": self.worst_plausible_case,
                "worst_case_who_pays": self.worst_case_who_pays,
            },
            "action_vs_inaction": {
                "act_and_wrong": {
                    "harms": self.act_and_wrong_harms,
                    "who": self.act_and_wrong_who,
                },
                "dont_act_and_wrong": {
                    "harms": self.dont_act_and_wrong_harms,
                    "who": self.dont_act_and_wrong_who,
                },
            },
            "high_stakes_rule": {
                "should_oppose": self.should_default_oppose(),
                "can_act_with_monitoring": self.can_act_with_monitoring(),
            },
            "reversibility": {
                "prefers_reversible": self.prefers_reversible,
                "off_ramps": self.off_ramps,
                "sunset_clause": self.sunset_clause,
            },
            "confidence": self.confidence.value,
            "biggest_uncertainty": self.biggest_might_be_wrong,
        }


@dataclass
class FalsePositiveReview:
    """
    False Positive Release Valve.
    Any pause can be challenged with "Was this pause justified?"
    """
    pause_challenged: bool = False
    trigger_cited: str = ""
    harm_risk_identified: str = ""
    door_for_safe_continuation: str = ""
    evidence_that_would_prevent_pause: str = ""
    outcome: str = ""  # "released" or "maintained"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pause_challenged": self.pause_challenged,
            "trigger_cited": self.trigger_cited,
            "harm_risk_identified": self.harm_risk_identified,
            "door_for_safe_continuation": self.door_for_safe_continuation,
            "evidence_that_would_prevent_pause": self.evidence_that_would_prevent_pause,
            "outcome": self.outcome,
        }


# ---------------------------------------------------------------------------
# Preflight Check (Two-Phase Commit: Phase 1)
# ---------------------------------------------------------------------------

@dataclass
class PreflightResult:
    """
    Preflight check result — Phase 1 of the two-phase commit.

    Runs BEFORE the main assessment to catch problems that should
    block or escalate before any deterministic gating even starts.

    Checks:
    1. Underspecified action (too vague to assess safely)
    2. Forced-motion language ("we have to", "must act now")
    3. High-risk domain (medical, legal, financial, military, children)
    4. Power asymmetry + irreversibility signals
    5. Epistemic weakness (speculation presented as fact)

    If any check fails, the preflight blocks the assessment and
    returns a reason. The caller must address the block before
    the assessment can proceed.
    """
    passed: bool = True
    blocks: List[str] = field(default_factory=list)
    escalations: List[str] = field(default_factory=list)
    high_risk_domain_detected: List[str] = field(default_factory=list)
    forced_motion_detected: List[str] = field(default_factory=list)
    epistemic_weakness_detected: List[str] = field(default_factory=list)
    underspecified: bool = False

    def is_blocked(self) -> bool:
        """Return True if any block was raised."""
        return len(self.blocks) > 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "blocks": self.blocks,
            "escalations": self.escalations,
            "high_risk_domain_detected": self.high_risk_domain_detected,
            "forced_motion_detected": self.forced_motion_detected,
            "epistemic_weakness_detected": self.epistemic_weakness_detected,
            "underspecified": self.underspecified,
        }


@dataclass
class FinalizationGateResult:
    """
    Finalization gate result — Phase 2 of the two-phase commit.

    Runs AFTER the assessment is complete but BEFORE the decision
    is accepted. Can INVALIDATE the decision and force a rerun,
    not just log drift alarms.

    Checks:
    1. Compliance theater patterns
    2. Drift phrases in justification
    3. Sycophancy indicators
    4. Rating suspicion (all-low ratings despite red flags)
    """
    valid: bool = True
    invalidation_reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    requires_rerun: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "invalidation_reasons": self.invalidation_reasons,
            "warnings": self.warnings,
            "requires_rerun": self.requires_rerun,
        }


# ---------------------------------------------------------------------------
# PBHP Log Record v0.7.1
# ---------------------------------------------------------------------------

@dataclass
class PBHPLog:
    """
    Complete PBHP assessment log for audit and review.
    Implements the full PBHP Log Record v0.7 format with all metadata fields.
    """
    # Record metadata
    record_id: str
    timestamp: datetime
    version: str = "0.7.1"

    # Step 1: Action
    action_description: str = ""

    # Step 0a: Ethical Pause
    ethical_pause: Optional[EthicalPausePosture] = None

    # Step 0d: Quick Risk Check
    quick_risk_check: Optional[QuickRiskCheck] = None

    # Step 0e: Door/Wall/Gap
    door_wall_gap: Optional[DoorWallGap] = None

    # Step 0f: CHIM Check
    chim_check: Optional[CHIMCheck] = None

    # Step 0g: Absolute Rejection
    absolute_rejection: Optional[AbsoluteRejectionCheck] = None

    # Baseline reality check
    historical_analogs: List[str] = field(default_factory=list)
    status_quo_harms: List[str] = field(default_factory=list)

    # Consequences checklist
    consequences: Optional[ConsequencesChecklist] = None

    # Step 2-3: Harms and risk classification
    harms: List[Harm] = field(default_factory=list)
    highest_risk_class: RiskClass = RiskClass.GREEN

    # Step 4: Consent
    consent_check: Optional[ConsentCheck] = None

    # Step 5: Alternatives
    alternatives: List[Alternative] = field(default_factory=list)

    # Step 6: Decision
    decision_outcome: DecisionOutcome = DecisionOutcome.PROCEED
    justification: str = ""

    # Step 6.5: Red Team
    red_team_review: Optional[RedTeamReview] = None

    # Step 7: Epistemic fence
    epistemic_fence: Optional[EpistemicFence] = None

    # Uncertainty assessment
    uncertainty: Optional[UncertaintyAssessment] = None

    # False positive review
    false_positive_review: Optional[FalsePositiveReview] = None

    # Two-phase commit
    preflight: Optional[PreflightResult] = None
    finalization_gate: Optional[FinalizationGateResult] = None

    # Agent metadata
    agent_type: str = ""  # human, ai_system, hybrid
    system_model_version: str = ""
    deployment_channel: str = ""  # prod, staging, internal, external
    requester_role: str = ""  # user, client, internal leader, regulator, unknown

    # Drift tracking
    drift_alarms_triggered: List[str] = field(default_factory=list)

    # Pause tracking
    pause_challenged: bool = False
    pause_justification: str = ""

    # Follow-up
    monitoring_plan: str = ""
    review_trigger: str = ""

    # Corrective actions
    corrective_action: str = ""
    preventive_action: str = ""
    root_cause_hypothesis: str = ""
    root_cause_confirmed: str = ""

    # Verification
    verification_plan: str = ""
    success_signal: str = ""

    # Ownership
    owner: str = ""
    due_date: str = ""
    review_status: str = ""

    # Notes
    notes: str = ""
    related_logs: List[str] = field(default_factory=list)

    def get_overall_confidence(self) -> str:
        """Get overall confidence from uncertainty assessment."""
        if self.uncertainty:
            return self.uncertainty.confidence.value
        return "not assessed"

    def to_dict(self) -> Dict[str, Any]:
        """Convert log to dictionary for serialization."""
        result = {
            "record_id": self.record_id,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "action_description": self.action_description,
        }

        # Optional modules
        if self.ethical_pause:
            result["ethical_pause"] = self.ethical_pause.to_dict()
        if self.quick_risk_check:
            result["quick_risk_check"] = self.quick_risk_check.to_dict()
        if self.door_wall_gap:
            result["door_wall_gap"] = self.door_wall_gap.to_dict()
        if self.chim_check:
            result["chim_check"] = self.chim_check.to_dict()
        if self.absolute_rejection:
            result["absolute_rejection"] = self.absolute_rejection.to_dict()
        if self.consequences:
            result["consequences"] = self.consequences.to_dict()
        if self.consent_check:
            result["consent_check"] = self.consent_check.to_dict()
        if self.uncertainty:
            result["uncertainty"] = self.uncertainty.to_dict()
        if self.epistemic_fence:
            result["epistemic_fence"] = self.epistemic_fence.to_dict()
        if self.red_team_review:
            result["red_team_review"] = self.red_team_review.to_dict()
        if self.false_positive_review:
            result["false_positive_review"] = self.false_positive_review.to_dict()
        if self.preflight:
            result["preflight"] = self.preflight.to_dict()
        if self.finalization_gate:
            result["finalization_gate"] = self.finalization_gate.to_dict()

        # Core assessment data
        result["harms"] = [h.to_dict() for h in self.harms]
        result["highest_risk_class"] = self.highest_risk_class.value
        result["alternatives"] = [a.to_dict() for a in self.alternatives]
        result["decision_outcome"] = self.decision_outcome.value
        result["justification"] = self.justification

        # Metadata
        result["metadata"] = {
            "agent_type": self.agent_type,
            "system_model_version": self.system_model_version,
            "deployment_channel": self.deployment_channel,
            "requester_role": self.requester_role,
        }

        # Tracking
        result["drift_alarms"] = self.drift_alarms_triggered
        result["pause_challenged"] = self.pause_challenged
        result["pause_justification"] = self.pause_justification
        result["confidence"] = self.get_overall_confidence()

        # Follow-up
        result["follow_up"] = {
            "monitoring_plan": self.monitoring_plan,
            "review_trigger": self.review_trigger,
            "corrective_action": self.corrective_action,
            "preventive_action": self.preventive_action,
            "root_cause_hypothesis": self.root_cause_hypothesis,
            "root_cause_confirmed": self.root_cause_confirmed,
            "verification_plan": self.verification_plan,
            "success_signal": self.success_signal,
        }

        # Ownership
        result["ownership"] = {
            "owner": self.owner,
            "due_date": self.due_date,
            "review_status": self.review_status,
        }

        result["notes"] = self.notes
        result["related_logs"] = self.related_logs

        return result

    def to_json(self, indent: int = 2) -> str:
        """Convert log to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)


# ---------------------------------------------------------------------------
# Drift Alarm Detector
# ---------------------------------------------------------------------------

class TextNormalizer:
    """
    Layer 1: Text normalization for robust pattern detection.
    Handles casing, whitespace, common obfuscation, and light stemming.
    """

    # Common obfuscation substitutions (leet speak, Unicode tricks)
    OBFUSCATION_MAP = {
        '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's',
        '7': 't', '@': 'a', '$': 's', '!': 'i',
        '\u200b': '',  # zero-width space
        '\u200d': '',  # zero-width joiner
        '\u00a0': ' ',  # non-breaking space
        '\u2019': "'",  # right single quote
        '\u2018': "'",  # left single quote
        '\u201c': '"',  # left double quote
        '\u201d': '"',  # right double quote
    }

    @classmethod
    def normalize(cls, text: str) -> str:
        """Normalize text for pattern matching."""
        # Lowercase
        text = text.lower()
        # Replace obfuscation characters
        for char, replacement in cls.OBFUSCATION_MAP.items():
            text = text.replace(char, replacement)
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Strip repeated punctuation used to break patterns
        text = re.sub(r'[.\-_]{2,}', ' ', text)
        return text


class DriftAlarmDetector:
    """
    Detects rationalization patterns and drift from PBHP principles.

    Uses layered detection:
    - Layer 1: Text normalization (TextNormalizer)
    - Layer 2: Regex pattern families (not exact strings)
    - Layer 3: Fuzzy matching for near-miss evasion
    - Layer 4: Structural rationalization detection

    If any drift alarm phrase appears, you must explicitly name the
    Wall (constraint), the Gap (harm leak), and the Door (escape vector)
    in writing before proceeding.
    """

    # Layer 2: Regex pattern families (more robust than exact strings)
    DRIFT_PATTERNS = [
        (r"it'?s?\s+(just\s+)?temporary", "temporary-excuse"),
        (r"it'?s?\s+(just\s+)?targeted", "targeted-excuse"),
        (r"only\s+affects?\s+(bad|guilty|wrong)\s+people", "deserving-victim"),
        (r"we\s+(have|need|must)\s+to", "forced-motion"),
        (r"there'?s?\s+no\s+(other\s+)?choice", "no-choice-claim"),
        (r"(just|merely|only)\s+(following\s+)?(policy|procedure|orders|protocol)", "just-following-orders"),
        (r"it'?s?\s+legal[\s,]+so\s+it'?s?\s+(fine|ok|okay|allowed)", "legality-as-morality"),
        (r"(just|merely|only)\s+advice", "responsibility-dodge"),
        (r"we'?re?\s+not\s+responsible", "responsibility-dodge"),
        (r"for\s+(the\s+)?safety", "safety-blanket"),
        (r"for\s+the\s+greater\s+good", "greater-good"),
        (r"we\s+can\s+(always\s+)?(fix|change|roll\s*back)\s+it\s+later", "reversibility-assumption"),
        (r"we'?ll\s+roll\s+it\s+back", "reversibility-assumption"),
        (r"(just|merely|only)\s+interpret", "interpretation-dodge"),
        (r"it'?s?\s+obvious", "false-clarity"),
        (r"every(one|body)\s+knows", "false-consensus"),
        (r"no\s+need\s+to\s+(cite|check|verify|confirm|source)", "verification-skip"),
        (r"close\s+enough", "precision-dodge"),
        (r"there'?s?\s+(only\s+)?one\s+interpretation", "premature-collapse"),
        (r"i'?ll?\s+just\s+pick\s+the\s+most\s+plausible", "premature-collapse"),
        (r"(must|need\s+to|have\s+to)\s+act\s+(now|immediately|fast|quickly)", "urgency-pressure"),
        (r"no\s+time\s+to\s+(think|pause|wait|consider|check)", "urgency-pressure"),
    ]

    PREMATURE_COLLAPSE_PATTERNS = [
        (r"it'?s?\s+obvious\s+what\s+they\s+meant", "obvious-meaning"),
        (r"there'?s?\s+(only\s+)?one\s+interpretation", "single-interpretation"),
        (r"every(one|body)\s+knows\s+this", "false-consensus"),
        (r"close\s+enough", "precision-dodge"),
        (r"no\s+need\s+to\s+(cite|check|verify|source)", "verification-skip"),
        (r"i'?ll?\s+just\s+pick\s+the\s+most\s+plausible", "plausible-pick"),
    ]

    COMPASSION_DRIFT_PATTERNS = [
        (r"\b(animals|vermin|cockroaches|rats|insects)\b", "dehumanization"),
        (r"\bsub\s*human\b", "dehumanization"),
        (r"\bthey'?re?\s+all\b", "group-flattening"),
        (r"for\s+(your|their|his|her)\s+own\s+good", "paternalism"),
        (r"they'?re?\s+(bad|evil|guilty)\s+so\s+(anything|everything)\s+is\s+justified",
         "deserving-victim"),
        (r"they\s+deserve\s+(it|what\s+they\s+get)", "deserving-victim"),
        (r"if\s+you\s+(really\s+)?care[d]?\s+you'?d", "emotional-coercion"),
    ]

    SYCOPHANCY_PATTERNS = [
        (r"\bchosen\s+one\b", "chosen-one"),
        (r"\btier\s*[1i]\b", "tier-ranking"),
        (r"you'?re?\s+(truly\s+)?enlightened", "flattery"),
        (r"beyond\s+(anyone|anything|compare)", "flattery"),
        (r"you\s+see\s+what\s+others\s+can'?t", "special-insight"),
        (r"\bgenius\s+(level|tier|class)\b", "flattery"),
        (r"\bunprecedented\s+insight\b", "flattery"),
        (r"no\s+one\s+else\s+(could|would|can)", "special-status"),
    ]

    # Layer 3: Canonical phrases for fuzzy matching
    FUZZY_CANONICAL_PHRASES = [
        "it's temporary", "it's targeted", "only affects bad people",
        "we have to", "there's no choice", "just following procedure",
        "it's legal so it's fine", "we're not responsible",
        "for the greater good", "we can fix it later",
        "everyone knows", "no need to check", "close enough",
    ]
    FUZZY_THRESHOLD = 0.80  # Minimum similarity for fuzzy match

    @classmethod
    def _normalize(cls, text: str) -> str:
        """Normalize text using TextNormalizer."""
        return TextNormalizer.normalize(text)

    @classmethod
    def _detect_regex_layer(cls, text: str, patterns, category: str) -> List[str]:
        """Layer 2: Detect patterns using regex families."""
        detected = []
        for pattern, name in patterns:
            if re.search(pattern, text):
                detected.append(f"{category}:{name}")
        return detected

    @classmethod
    def _detect_fuzzy_layer(cls, text: str) -> List[str]:
        """Layer 3: Fuzzy matching for near-miss evasion attempts."""
        detected = []
        # Split text into sliding windows of phrase-like chunks
        words = text.split()
        for window_size in range(3, 8):
            for i in range(len(words) - window_size + 1):
                chunk = " ".join(words[i:i + window_size])
                for canonical in cls.FUZZY_CANONICAL_PHRASES:
                    ratio = difflib.SequenceMatcher(
                        None, chunk, canonical
                    ).ratio()
                    if ratio >= cls.FUZZY_THRESHOLD:
                        detected.append(
                            f"fuzzy_drift:{canonical} "
                            f"(matched '{chunk}' at {ratio:.0%})"
                        )
        # Deduplicate (keep first occurrence of each canonical match)
        seen = set()
        unique = []
        for d in detected:
            canonical = d.split("(")[0].strip()
            if canonical not in seen:
                seen.add(canonical)
                unique.append(d)
        return unique

    @classmethod
    def _detect_structural_rationalization(cls, text: str) -> List[str]:
        """
        Layer 4: Detect structural rationalization patterns.
        These are sentence-level structures that suggest motivated reasoning,
        not individual phrase matches.
        """
        detected = []
        # "Yes X but Y" where X is harm and Y is benefit
        if re.search(
            r"(yes|sure|true|granted|acknowledged?)\b.{0,120}"
            r"\b(but|however|although|yet)\s+",
            text
        ):
            # Check if the "but" clause contains benefit/justification language
            but_match = re.search(
                r"(?:but|however|although|yet)\s+(.{10,80})",
                text
            )
            if but_match:
                after = but_match.group(1).lower()
                if any(w in after for w in [
                    "benefit", "help", "improve", "necessary",
                    "important", "outweigh", "worth", "justified",
                    "acceptable", "reasonable"
                ]):
                    detected.append(
                        "structural:harm-acknowledged-then-dismissed"
                    )

        # "Not ideal but necessary" pattern
        if re.search(
            r"not\s+(ideal|perfect|great|optimal)\s+"
            r"(but|however)\s+(necessary|required|needed|unavoidable)",
            text
        ):
            detected.append("structural:not-ideal-but-necessary")

        return detected

    @classmethod
    def detect(cls, text: str) -> List[str]:
        """
        Detect all drift alarm patterns in text using layered detection.

        Layer 1: Normalize text
        Layer 2: Regex pattern families
        Layer 3: Fuzzy matching
        Layer 4: Structural rationalization detection
        """
        normalized = cls._normalize(text)
        detected = []

        # Layer 2: Regex families
        detected.extend(cls._detect_regex_layer(
            normalized, cls.DRIFT_PATTERNS, "drift"
        ))
        detected.extend(cls._detect_regex_layer(
            normalized, cls.PREMATURE_COLLAPSE_PATTERNS, "premature_collapse"
        ))
        detected.extend(cls._detect_regex_layer(
            normalized, cls.COMPASSION_DRIFT_PATTERNS, "compassion_drift"
        ))
        detected.extend(cls._detect_regex_layer(
            normalized, cls.SYCOPHANCY_PATTERNS, "sycophancy"
        ))

        # Layer 3: Fuzzy matching (catches deliberate evasion)
        detected.extend(cls._detect_fuzzy_layer(normalized))

        # Layer 4: Structural rationalization
        detected.extend(cls._detect_structural_rationalization(normalized))

        return detected

    @classmethod
    def detect_compliance_theater(cls, log: PBHPLog) -> List[str]:
        """
        Detect if PBHP is being used as compliance theater.
        If detected: name the drift, round severity up, re-run Steps 2-6.
        """
        alarms = []

        # Check for ratings that seem optimized to reach desired gate
        if log.harms:
            all_low = all(
                h.impact in (ImpactLevel.TRIVIAL, ImpactLevel.MODERATE)
                and h.likelihood in (LikelihoodLevel.UNLIKELY, LikelihoodLevel.POSSIBLE)
                for h in log.harms
            )
            has_power_and_irreversible = any(
                h.power_asymmetry and h.irreversible for h in log.harms
            )
            if all_low and has_power_and_irreversible:
                alarms.append(
                    "Possible compliance theater: all harms rated low despite "
                    "power asymmetry + irreversibility"
                )

        # Check for empty/minimal justification on high-risk decisions
        if (log.highest_risk_class in (RiskClass.ORANGE, RiskClass.RED)
                and len(log.justification) < 50):
            alarms.append(
                "Possible compliance theater: minimal justification for "
                f"{log.highest_risk_class.value.upper()} risk"
            )

        # Check for "we ran PBHP so we're covered" language
        theater_phrases = [
            "we ran pbhp",
            "pbhp says it's allowed",
            "just need to pass the checklist",
            "above pbhp's scope",
            "we're covered",
        ]
        if log.justification:
            for phrase in theater_phrases:
                if phrase in log.justification.lower():
                    alarms.append(f"Compliance theater phrase: '{phrase}'")

        return alarms


# ---------------------------------------------------------------------------
# Tone Validator (Brutal Clarity, Zero Contempt)
# ---------------------------------------------------------------------------

class ToneValidator:
    """
    Validates output against PBHP's tone requirements:
    Brutal Clarity + Zero Contempt.

    Must:
    - Use plain, direct language about harm
    - Name who carries/enables harm
    - Call out bullshit framing
    - Refuse fake neutrality on core harm
    - State stakes explicitly

    Must NOT:
    - Insult people's basic worth
    - Dehumanize or imply lives don't matter
    - Speculate about secret motives as fact
    - Express joy about suffering
    - Flatten real nuance
    """

    CONTEMPT_PATTERNS = [
        r"\bidiot\b", r"\bmoron\b", r"\bstupid\b",
        r"\bpiece of trash\b", r"\bscum\b", r"\bvermin\b",
        r"\bsubhuman\b", r"\bworthless\b",
        r"\bthey deserve what they get\b",
        r"\bthey don't matter\b",
        r"\bthese people don't matter\b",
    ]

    EUPHEMISM_PATTERNS = [
        "may pose challenges for some stakeholders",
        "some parties may bear disproportionate negative impacts",
        "there are differing perspectives on the appropriate balance",
        "reasonable people may disagree about the distributional effects",
    ]

    @classmethod
    def check_for_contempt(cls, text: str) -> List[str]:
        """Detect contemptuous language that violates PBHP tone rules."""
        issues = []
        text_lower = text.lower()
        for pattern in cls.CONTEMPT_PATTERNS:
            if re.search(pattern, text_lower):
                issues.append(f"Contempt detected: matches '{pattern}'")
        return issues

    @classmethod
    def check_for_euphemism(cls, text: str) -> List[str]:
        """Detect euphemistic hedging that violates brutal clarity."""
        issues = []
        text_lower = text.lower()
        for pattern in cls.EUPHEMISM_PATTERNS:
            if pattern in text_lower:
                issues.append(f"Euphemism detected: '{pattern}' - use plain language about harm")
        return issues

    @classmethod
    def validate(cls, text: str) -> Dict[str, List[str]]:
        """Full tone validation."""
        return {
            "contempt_issues": cls.check_for_contempt(text),
            "euphemism_issues": cls.check_for_euphemism(text),
        }


# ---------------------------------------------------------------------------
# Lexicographic Priority (Small harm to many vs large harm to few)
# ---------------------------------------------------------------------------

class LexicographicPriority:
    """
    PBHP's decision priority system for resolving aggregation conflicts.

    Order:
    1. Prevent catastrophic irreversible harm first (even if fewer people)
    2. If no catastrophe: minimize irreversible harm, then severe harm
    3. If comparable: prefer option distributing burden fairly
    4. If still tied: choose most reversible/safest option

    This prevents: "We helped 10,000 by ruining 500."
    """

    @staticmethod
    def compare_options(
        option_a_harms: List[Harm],
        option_b_harms: List[Harm]
    ) -> str:
        """
        Compare two options using lexicographic priority.
        Returns "a", "b", or "tied".
        """
        # Priority 1: Catastrophic irreversible harm
        a_catastrophic = any(
            h.impact == ImpactLevel.CATASTROPHIC and h.irreversible
            for h in option_a_harms
        )
        b_catastrophic = any(
            h.impact == ImpactLevel.CATASTROPHIC and h.irreversible
            for h in option_b_harms
        )

        if a_catastrophic and not b_catastrophic:
            return "b"
        if b_catastrophic and not a_catastrophic:
            return "a"

        # Priority 2: Minimize irreversible harm count
        a_irreversible = sum(1 for h in option_a_harms if h.irreversible)
        b_irreversible = sum(1 for h in option_b_harms if h.irreversible)

        if a_irreversible < b_irreversible:
            return "a"
        if b_irreversible < a_irreversible:
            return "b"

        # Priority 3: Minimize severe harm count
        a_severe = sum(
            1 for h in option_a_harms
            if h.impact in (ImpactLevel.SEVERE, ImpactLevel.CATASTROPHIC)
        )
        b_severe = sum(
            1 for h in option_b_harms
            if h.impact in (ImpactLevel.SEVERE, ImpactLevel.CATASTROPHIC)
        )

        if a_severe < b_severe:
            return "a"
        if b_severe < a_severe:
            return "b"

        # Priority 4: Power asymmetry (prefer distributing burden fairly)
        a_power = sum(1 for h in option_a_harms if h.power_asymmetry)
        b_power = sum(1 for h in option_b_harms if h.power_asymmetry)

        if a_power < b_power:
            return "a"
        if b_power < a_power:
            return "b"

        return "tied"


# ---------------------------------------------------------------------------
# PBHP Engine - Core Protocol Executor
# ---------------------------------------------------------------------------

class PBHPEngine:
    """
    Core PBHP execution engine.
    Orchestrates the complete protocol: foundation gates, seven steps,
    and all required modules.
    """

    def __init__(self):
        self.logs: List[PBHPLog] = []

    # ------------------------------------------------------------------
    # Step 1: Create Assessment / Name the Action
    # ------------------------------------------------------------------

    def create_assessment(
        self,
        action_description: str,
        agent_type: str = "ai_system"
    ) -> PBHPLog:
        """
        Create a new PBHP assessment.
        Step 1: Name the Action.
        """
        log = PBHPLog(
            record_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            action_description=action_description,
            agent_type=agent_type,
        )
        return log

    def validate_action_description(self, action: str) -> Tuple[bool, str]:
        """
        Validate that action is clearly stated (Step 1).
        Truth check: Is this honest and complete enough that a
        skeptical outsider would recognize what you're doing?
        """
        if not action or len(action.strip()) < 10:
            return False, "Action description too vague or missing"

        # Check for key verb component
        action_verbs = [
            "send", "delete", "publish", "run", "execute",
            "terminate", "remove", "modify", "create", "deploy",
            "announce", "report", "advise", "recommend", "refuse",
            "approve", "deny", "escalate", "provide", "restrict",
            "release", "block", "revoke", "grant", "share",
            "post", "write", "issue", "close", "open",
            "rename", "update", "change", "set", "configure",
        ]
        has_verb = any(word in action.lower() for word in action_verbs)

        if not has_verb:
            return False, "Action should include a clear verb (what you're doing)"

        return True, "Action clearly stated"

    # ------------------------------------------------------------------
    # Preflight Check (Two-Phase Commit: Phase 1)
    # ------------------------------------------------------------------

    # High-risk domain keywords that trigger elevated scrutiny
    HIGH_RISK_DOMAINS = {
        "medical": [
            r"\b(medic|patient|diagnos|prescri|dosage|treatment|surger|"
            r"pharma|drug|clinical|symptom)\w*\b"
        ],
        "legal": [
            r"\b(legal|lawsuit|litigation|court|sentenc|verdict|"
            r"prosecut|defend|indict|plea|bail|parole)\w*\b"
        ],
        "financial": [
            r"\b(invest|trading|portfolio|loan|mortgage|credit|"
            r"debt|bankrupt|securit|pension|retir)\w*\b"
        ],
        "military": [
            r"\b(military|weapon|strike|combat|warfare|"
            r"drone|deployment|casualties|munition)\w*\b"
        ],
        "children": [
            r"\b(child|minor|juvenile|student|kid|infant|"
            r"toddler|pediatric|adolescent|school)\w*\b"
        ],
        "infrastructure": [
            r"\b(power\s*grid|water\s*supply|hospital|emergency\s*service|"
            r"transport|bridge|dam|reactor)\w*\b"
        ],
    }

    # Forced-motion language patterns
    FORCED_MOTION_PATTERNS = [
        (r"(we|i|you)\s+(have|need|must)\s+to\s+(do|act|decide)\s+"
         r"(now|immediately|right\s+now|fast|quickly|today)", "urgency-demand"),
        (r"no\s+(time|room)\s+(for|to)\s+(think|pause|wait|delay|consider)",
         "anti-pause"),
        (r"(we|they)\s+(have|had)\s+no\s+(other\s+)?choice", "no-choice-force"),
        (r"(must|need\s+to)\s+act\s+before\s+(it'?s?\s+too\s+late|"
         r"the\s+window\s+closes)", "deadline-pressure"),
        (r"(everyone|everybody)\s+(else\s+)?is\s+(already\s+)?(doing|on\s+board)",
         "bandwagon-pressure"),
    ]

    # Epistemic weakness patterns (speculation as fact)
    EPISTEMIC_WEAKNESS_PATTERNS = [
        (r"(obviously|clearly|everyone\s+knows|it'?s?\s+clear\s+that)\s+",
         "false-certainty"),
        (r"(studies?\s+show|research\s+(shows?|proves?))\s+",
         "unattributed-authority"),
        (r"(always|never)\s+(works?|fails?|happens?|leads?\s+to)",
         "absolute-claim"),
    ]

    def preflight_check(
        self,
        log: PBHPLog,
        action_text: Optional[str] = None,
        context: str = "",
    ) -> PreflightResult:
        """
        Two-Phase Commit — Phase 1: Preflight Check.

        Runs BEFORE the main assessment to catch problems that should
        block or escalate before any deterministic gating starts.

        Args:
            log: The PBHPLog being assessed
            action_text: Override text to check (defaults to log action)
            context: Additional context text to scan

        Returns:
            PreflightResult with pass/block/escalation status
        """
        result = PreflightResult()
        text = action_text or log.action_description
        normalized = TextNormalizer.normalize(text)
        full_text = TextNormalizer.normalize(f"{text} {context}")

        # Check 1: Underspecified action
        valid, msg = self.validate_action_description(text)
        if not valid:
            result.underspecified = True
            result.blocks.append(
                f"Preflight BLOCK: Action underspecified — {msg}. "
                f"Cannot safely assess a vague action."
            )

        # Check 2: Forced-motion language
        for pattern, name in self.FORCED_MOTION_PATTERNS:
            if re.search(pattern, full_text):
                result.forced_motion_detected.append(name)
        if result.forced_motion_detected:
            result.escalations.append(
                f"Preflight ESCALATE: Forced-motion language detected "
                f"({', '.join(result.forced_motion_detected)}). "
                f"Urgency pressure often accompanies harmful actions. "
                f"Slow down."
            )

        # Check 3: High-risk domain detection
        for domain, patterns in self.HIGH_RISK_DOMAINS.items():
            for pattern in patterns:
                if re.search(pattern, full_text):
                    result.high_risk_domain_detected.append(domain)
                    break
        if result.high_risk_domain_detected:
            result.escalations.append(
                f"Preflight ESCALATE: High-risk domain(s) detected: "
                f"{', '.join(result.high_risk_domain_detected)}. "
                f"Tighten all subsequent checks."
            )

        # Check 4: Power asymmetry + irreversibility signals
        power_signals = re.search(
            r"\b(vulnerable|powerless|marginalized|disadvantaged|"
            r"minority|disabled|elderly|homeless|incarcerated|"
            r"undocumented|refugee|asylum)\w*\b",
            full_text
        )
        irreversibility_signals = re.search(
            r"\b(permanent|irreversible|cannot\s+undo|"
            r"no\s+(going\s+)?back|forever|death|kill|"
            r"terminat|destroy|eradicat)\w*\b",
            full_text
        )
        if power_signals and irreversibility_signals:
            result.blocks.append(
                "Preflight BLOCK: Power asymmetry + irreversibility "
                "detected in action description. This combination "
                "requires explicit Door/Wall/Gap before proceeding."
            )

        # Check 5: Epistemic weakness
        for pattern, name in self.EPISTEMIC_WEAKNESS_PATTERNS:
            if re.search(pattern, full_text):
                result.epistemic_weakness_detected.append(name)
        if result.epistemic_weakness_detected:
            result.escalations.append(
                f"Preflight ESCALATE: Epistemic weakness "
                f"({', '.join(result.epistemic_weakness_detected)}). "
                f"Claims presented as fact may be speculation."
            )

        # Determine overall pass/fail
        result.passed = len(result.blocks) == 0

        # Attach to log
        log.preflight = result
        if not result.passed:
            for block in result.blocks:
                log.drift_alarms_triggered.append(block)
        for esc in result.escalations:
            log.drift_alarms_triggered.append(esc)

        return result

    # ------------------------------------------------------------------
    # Step 0a: Ethical Pause
    # ------------------------------------------------------------------

    def perform_ethical_pause(
        self,
        log: PBHPLog,
        action_statement: str,
        compassion_notes: str = "",
        logic_notes: str = "",
        paradox_notes: str = "",
        high_arousal_state: bool = False,
        high_arousal_notes: str = "",
    ) -> EthicalPausePosture:
        """
        Perform Step 0a: Ethical Pause.
        Balance compassion, logic, and paradox before proceeding.
        If high arousal detected, automatically tighten behavior.
        """
        posture = EthicalPausePosture(
            action_statement=action_statement,
            compassion_notes=compassion_notes,
            logic_notes=logic_notes,
            paradox_notes=paradox_notes,
            high_arousal_state=high_arousal_state,
            high_arousal_notes=high_arousal_notes,
        )
        log.ethical_pause = posture

        if high_arousal_state:
            log.drift_alarms_triggered.append(
                "High arousal state detected: tightening behavior "
                "(slow down, clarify intent, smallest safe action)"
            )

        return posture

    # ------------------------------------------------------------------
    # Step 0d: Quick Risk Check
    # ------------------------------------------------------------------

    def perform_quick_risk_check(
        self,
        log: PBHPLog,
        obviously_low_risk: bool,
        silence_delay_protects_more: Optional[bool] = None,
    ) -> QuickRiskCheck:
        """
        Perform Step 0d: Quick Risk Check.
        Pre-screening to determine if behavior should tighten.
        """
        check = QuickRiskCheck(
            obviously_low_risk=obviously_low_risk,
            silence_delay_protects_more=silence_delay_protects_more,
        )
        check.evaluate()
        log.quick_risk_check = check
        return check

    # ------------------------------------------------------------------
    # Step 0e: Door/Wall/Gap
    # ------------------------------------------------------------------

    def perform_door_wall_gap(
        self,
        log: PBHPLog,
        wall: str,
        gap: str,
        door: str
    ) -> bool:
        """
        Perform Door/Wall/Gap analysis (Step 0e).
        Returns True if a concrete Door exists.
        If no Door can be named, PBHP defaults to pause or refusal.
        """
        log.door_wall_gap = DoorWallGap(wall=wall, gap=gap, door=door)

        if not log.door_wall_gap.has_door():
            log.drift_alarms_triggered.append(
                "No concrete Door identified - PBHP does not permit "
                "proceeding without an escape vector"
            )
            return False

        return True

    # ------------------------------------------------------------------
    # Step 0f: CHIM Check
    # ------------------------------------------------------------------

    def perform_chim_check(
        self,
        log: PBHPLog,
        constraint_recognized: bool,
        no_choice_claim: bool,
        remaining_choice: str,
        reframes: Optional[List[str]] = None
    ) -> bool:
        """
        Perform CHIM check (Step 0f).
        Returns True if check passes (agency maintained).

        If 'no choice' concludes twice in a row, must reframe in at
        least two alternative framings.
        """
        prev_count = 0
        if log.chim_check and log.chim_check.no_choice_claim:
            prev_count = log.chim_check.consecutive_no_choice_count

        new_count = prev_count + 1 if no_choice_claim else 0

        log.chim_check = CHIMCheck(
            constraint_recognized=constraint_recognized,
            treating_as_absolute=not constraint_recognized,
            no_choice_claim=no_choice_claim,
            remaining_choice=remaining_choice,
            reframes=reframes or [],
            consecutive_no_choice_count=new_count,
        )

        if log.chim_check.requires_pause():
            log.drift_alarms_triggered.append(
                "CHIM check failed: no remaining choice identified"
            )
            if new_count >= 2 and len(log.chim_check.reframes) < 2:
                log.drift_alarms_triggered.append(
                    "CHIM: 'no choice' claimed twice - must provide "
                    "at least 2 alternative framings"
                )
            return False

        return True

    # ------------------------------------------------------------------
    # Step 0g: Absolute Rejection Check
    # ------------------------------------------------------------------

    def perform_absolute_rejection_check(
        self,
        log: PBHPLog,
        action_text: Optional[str] = None,
        analysis_mode: str = "",
    ) -> AbsoluteRejectionCheck:
        """
        Perform Step 0g: Absolute Rejection Check.

        If action upholds fascism, genocide, slavery, non-consensual
        authoritarian control, or systemic dehumanization:
        REFUSE. Only allow discussion in critique/dismantling/prevention mode.
        """
        text = action_text or log.action_description
        check = AbsoluteRejectionCheck(
            action_description=text,
            analysis_mode=analysis_mode,
        )
        check.evaluate(text)

        if check.triggers_rejection:
            if analysis_mode not in ("critique", "dismantling", "prevention"):
                log.highest_risk_class = RiskClass.BLACK
                log.decision_outcome = DecisionOutcome.REFUSE
                log.justification = (
                    f"Absolute rejection: action upholds "
                    f"{', '.join(check.matched_categories)}. "
                    f"Only discussion in critique, dismantling, or "
                    f"prevention modes is permitted."
                )

        log.absolute_rejection = check
        return check

    # ------------------------------------------------------------------
    # Step 2: Identify and Add Harms
    # ------------------------------------------------------------------

    def add_harm(
        self,
        log: PBHPLog,
        description: str,
        impact: ImpactLevel,
        likelihood: LikelihoodLevel,
        irreversible: bool,
        power_asymmetry: bool,
        affected_parties: List[str],
        least_powerful_affected: str,
        notes: str = "",
        uncertainty_level: UncertaintyLevel = UncertaintyLevel.FUZZY,
        evidence_basis: str = "",
        audience_risk_elevated: bool = False,
    ) -> Harm:
        """
        Add a harm to the assessment (Step 2).
        Automatically updates highest risk class.
        """
        harm = Harm(
            description=description,
            impact=impact,
            likelihood=likelihood,
            irreversible=irreversible,
            power_asymmetry=power_asymmetry,
            affected_parties=affected_parties,
            least_powerful_affected=least_powerful_affected,
            notes=notes,
            uncertainty_level=uncertainty_level,
            evidence_basis=evidence_basis,
            audience_risk_elevated=audience_risk_elevated,
        )

        log.harms.append(harm)

        # Update highest risk class
        harm_risk = harm.calculate_risk_class()
        if self._risk_class_priority(harm_risk) > \
                self._risk_class_priority(log.highest_risk_class):
            log.highest_risk_class = harm_risk

        return harm

    # ------------------------------------------------------------------
    # Step 4: Consent Check
    # ------------------------------------------------------------------

    def perform_consent_check(
        self,
        log: PBHPLog,
        explicit_consent: bool,
        informed_hypothetical_consent: Optional[bool] = None,
        overriding_preferences: bool = False,
        compatible_with_dignity: bool = True,
        honest_framing: bool = True,
        who_didnt_get_a_say: Optional[List[str]] = None,
        notes: str = "",
    ) -> ConsentCheck:
        """
        Perform Step 4: Consent and Representation Check.
        """
        check = ConsentCheck(
            explicit_consent=explicit_consent,
            informed_hypothetical_consent=informed_hypothetical_consent,
            overriding_preferences=overriding_preferences,
            compatible_with_dignity=compatible_with_dignity,
            honest_framing=honest_framing,
            who_didnt_get_a_say=who_didnt_get_a_say or [],
            notes=notes,
        )
        log.consent_check = check
        return check

    # ------------------------------------------------------------------
    # Step 5: Alternatives
    # ------------------------------------------------------------------

    def add_alternative(
        self,
        log: PBHPLog,
        description: str,
        preserves_goal: bool,
        reduces_harm: bool,
        reversible: bool,
        notes: str = ""
    ) -> Alternative:
        """Add a safer alternative (Step 5)."""
        alt = Alternative(
            description=description,
            preserves_goal=preserves_goal,
            reduces_harm=reduces_harm,
            reversible=reversible,
            notes=notes,
        )
        log.alternatives.append(alt)
        return alt

    # ------------------------------------------------------------------
    # Step 6.5: Red Team Review
    # ------------------------------------------------------------------

    def perform_red_team_review(
        self,
        log: PBHPLog,
        failure_modes: List[str],
        abuse_vectors: List[str],
        who_bears_risk: str,
        false_assumptions: List[str],
        normalization_risk: str = "",
        alternative_interpretations: Optional[List[str]] = None,
        claim_tags: str = "",
        wrong_inference_consequences: str = "",
        steelman_other_side: str = "",
        motives_vs_outcomes: str = "",
        incentives_pressures: str = "",
        message_reception_prediction: str = "",
        off_ramps: Optional[List[str]] = None,
    ) -> RedTeamReview:
        """
        Perform Red Team review (Step 6.5).
        Required for ORANGE, RED, and BLACK risk classes.
        """
        review = RedTeamReview(
            failure_modes=failure_modes,
            abuse_vectors=abuse_vectors,
            who_bears_risk=who_bears_risk,
            false_assumptions=false_assumptions,
            normalization_risk=normalization_risk,
            alternative_interpretations=alternative_interpretations or [],
            claim_tags=claim_tags,
            wrong_inference_consequences=wrong_inference_consequences,
            steelman_other_side=steelman_other_side,
            motives_vs_outcomes=motives_vs_outcomes,
            incentives_pressures=incentives_pressures,
            message_reception_prediction=message_reception_prediction,
            off_ramps_identified=off_ramps or [],
        )

        # Run drift detection on Red Team content
        combined_text = " ".join([
            who_bears_risk,
            steelman_other_side,
            motives_vs_outcomes,
            " ".join(false_assumptions),
        ])
        drift_alarms = DriftAlarmDetector.detect(combined_text)
        if drift_alarms:
            review.drift_alarms_detected = drift_alarms
            log.drift_alarms_triggered.extend(
                [f"Red Team drift: {a}" for a in drift_alarms]
            )

        log.red_team_review = review
        return review

    # ------------------------------------------------------------------
    # Consequences Checklist
    # ------------------------------------------------------------------

    def set_consequences_checklist(
        self,
        log: PBHPLog,
        checklist: ConsequencesChecklist
    ) -> ConsequencesChecklist:
        """Attach consequences checklist to assessment."""
        log.consequences = checklist

        if checklist.requires_door_chim_rerun():
            log.drift_alarms_triggered.append(
                "Consequences checklist: critical flags require "
                "Door/CHIM rerun + safer alternative search"
            )

        return checklist

    # ------------------------------------------------------------------
    # Uncertainty Assessment
    # ------------------------------------------------------------------

    def set_uncertainty_assessment(
        self,
        log: PBHPLog,
        assessment: UncertaintyAssessment
    ) -> UncertaintyAssessment:
        """Attach uncertainty assessment to the log."""
        log.uncertainty = assessment

        if assessment.should_default_oppose():
            log.drift_alarms_triggered.append(
                "Uncertainty rule: high harm + low power + speculative "
                "benefits -> default to shrink/slow/oppose"
            )

        return assessment

    # ------------------------------------------------------------------
    # Epistemic Fence
    # ------------------------------------------------------------------

    def set_epistemic_fence(
        self,
        log: PBHPLog,
        fence: EpistemicFence
    ) -> EpistemicFence:
        """Attach epistemic fence to the log."""
        log.epistemic_fence = fence

        issues = fence.validate()
        if issues:
            for issue in issues:
                log.drift_alarms_triggered.append(f"Epistemic fence: {issue}")

        return fence

    # ------------------------------------------------------------------
    # Step 6-7: Finalize Decision
    # ------------------------------------------------------------------

    def finalize_decision(
        self,
        log: PBHPLog,
        outcome: DecisionOutcome,
        justification: str
    ) -> PBHPLog:
        """
        Finalize the PBHP decision (Steps 6-7) with Finalization Gate.

        Two-Phase Commit — Phase 2: The finalization gate runs AFTER
        the assessment but can INVALIDATE the decision and force a
        rerun, not just log drift alarms.

        Flow:
        1. Set decision and justification
        2. Run validation requirements
        3. Run finalization gate (drift, theater, sycophancy, tone)
        4. If gate INVALIDATES: mark decision as ESCALATE,
           set requires_rerun, and refuse to accept the assessment
        5. Store log
        """
        log.decision_outcome = outcome
        log.justification = justification

        # Validate requirements based on risk class
        validation_errors = self._validate_requirements(log)
        if validation_errors:
            log.drift_alarms_triggered.extend(validation_errors)

        # Run finalization gate
        gate_result = self._run_finalization_gate(log, justification)
        log.finalization_gate = gate_result

        # If gate invalidates, override the decision
        if not gate_result.valid:
            log.decision_outcome = DecisionOutcome.ESCALATE
            log.justification = (
                f"FINALIZATION GATE INVALIDATED original decision "
                f"({outcome.value}). Reasons: "
                f"{'; '.join(gate_result.invalidation_reasons)}. "
                f"Original justification: {justification}"
            )
            log.drift_alarms_triggered.extend(gate_result.invalidation_reasons)

        # Warnings still get logged even if gate passes
        for warning in gate_result.warnings:
            log.drift_alarms_triggered.append(f"gate_warning:{warning}")

        # Store log
        self.logs.append(log)

        return log

    def _run_finalization_gate(
        self,
        log: PBHPLog,
        justification: str
    ) -> FinalizationGateResult:
        """
        Two-Phase Commit — Phase 2: Finalization Gate.

        Can INVALIDATE the decision (not just warn) if:
        - Compliance theater is detected at ORANGE+ risk
        - Drift phrases are found in a PROCEED decision at RED+ risk
        - Sycophancy indicators appear in the justification
        - All harm ratings suspiciously low despite red flags
        """
        gate = FinalizationGateResult()

        # 1. Detect drift phrases in justification
        drift_detected = DriftAlarmDetector.detect(justification)
        if drift_detected:
            # At RED+, drift in justification INVALIDATES
            if log.highest_risk_class in (RiskClass.RED, RiskClass.BLACK):
                gate.valid = False
                gate.requires_rerun = True
                gate.invalidation_reasons.append(
                    f"Drift detected in justification at "
                    f"{log.highest_risk_class.value.upper()} risk: "
                    f"{', '.join(drift_detected[:3])}"
                )
            else:
                gate.warnings.extend(drift_detected)

        # 2. Check for compliance theater
        theater_alarms = DriftAlarmDetector.detect_compliance_theater(log)
        if theater_alarms:
            # At ORANGE+, compliance theater INVALIDATES
            if log.highest_risk_class in (
                RiskClass.ORANGE, RiskClass.RED, RiskClass.BLACK
            ):
                gate.valid = False
                gate.requires_rerun = True
                gate.invalidation_reasons.extend(theater_alarms)
            else:
                gate.warnings.extend(theater_alarms)

        # 3. Sycophancy check on justification
        sycophancy = DriftAlarmDetector._detect_regex_layer(
            TextNormalizer.normalize(justification),
            DriftAlarmDetector.SYCOPHANCY_PATTERNS,
            "sycophancy"
        )
        if sycophancy:
            gate.valid = False
            gate.requires_rerun = True
            gate.invalidation_reasons.append(
                f"Sycophancy detected in justification: "
                f"{', '.join(sycophancy)}"
            )

        # 4. Tone check
        tone_issues = ToneValidator.validate(justification)
        for category, issues in tone_issues.items():
            for issue in issues:
                gate.warnings.append(f"Tone: {issue}")

        # 5. Suspicion check: decision is PROCEED but there are
        #    unresolved validation errors
        validation_errors = self._validate_requirements(log)
        if (validation_errors
                and log.decision_outcome in (
                    DecisionOutcome.PROCEED,
                    DecisionOutcome.PROCEED_MODIFIED
                )):
            gate.valid = False
            gate.requires_rerun = True
            gate.invalidation_reasons.append(
                f"Cannot PROCEED with unresolved validation errors: "
                f"{'; '.join(validation_errors)}"
            )

        return gate

    # ------------------------------------------------------------------
    # False Positive Review
    # ------------------------------------------------------------------

    def challenge_pause(
        self,
        log: PBHPLog,
        trigger_cited: str,
        harm_risk_identified: str,
        door_for_safe_continuation: str,
        evidence_that_would_prevent_pause: str,
    ) -> FalsePositiveReview:
        """
        Challenge a pause: "Was this pause justified?"
        Returns review with released/maintained outcome.
        """
        review = FalsePositiveReview(
            pause_challenged=True,
            trigger_cited=trigger_cited,
            harm_risk_identified=harm_risk_identified,
            door_for_safe_continuation=door_for_safe_continuation,
            evidence_that_would_prevent_pause=evidence_that_would_prevent_pause,
        )

        # Determine if pause should be released or maintained
        has_concrete_door = bool(door_for_safe_continuation.strip())
        has_evidence = bool(evidence_that_would_prevent_pause.strip())

        if has_concrete_door and has_evidence:
            review.outcome = "released"
        else:
            review.outcome = "maintained"

        log.false_positive_review = review
        log.pause_challenged = True
        log.pause_justification = (
            f"Trigger: {trigger_cited}. "
            f"Risk: {harm_risk_identified}. "
            f"Outcome: {review.outcome}."
        )

        return review

    # ------------------------------------------------------------------
    # Response Generation
    # ------------------------------------------------------------------

    def generate_response(self, log: PBHPLog) -> str:
        """
        Generate PBHP Consistent Response (Step 7A).
        Follows the canonical output structure.
        """
        parts = []

        # 1. Action Recognition
        parts.append("**1. Action Recognition**")
        parts.append(f"You are considering: {log.action_description}")
        parts.append("")

        # 2. Risk Acknowledgment
        parts.append("**2. Risk Acknowledgment**")
        if log.harms:
            for harm in log.harms:
                risk = harm.calculate_risk_class()
                parts.append(
                    f"- {harm.description} "
                    f"(Impact: {harm.impact.value}, "
                    f"Likelihood: {harm.likelihood.value}, "
                    f"Risk: {risk.value.upper()})"
                )
                if harm.power_asymmetry:
                    parts.append(
                        f"  Power asymmetry affects: "
                        f"{harm.least_powerful_affected}"
                    )
        else:
            parts.append("No significant harms identified.")
        parts.append("")

        # 3. PBHP Determination
        parts.append("**3. PBHP Determination**")
        parts.append(
            f"Risk Class: **{log.highest_risk_class.value.upper()}**"
        )
        parts.append("")

        # 4. Decision Outcome
        parts.append("**4. Decision Outcome**")
        parts.append(
            f"Decision: **{log.decision_outcome.value.replace('_', ' ').upper()}**"
        )
        parts.append(f"{log.justification}")
        parts.append("")

        # 5. Door Statement
        parts.append("**5. Door Statement (Escape Vector)**")
        if log.decision_outcome in (DecisionOutcome.PROCEED,
                                     DecisionOutcome.PROCEED_MODIFIED,
                                     DecisionOutcome.REDIRECT):
            if log.door_wall_gap:
                parts.append(f"Safest path: {log.door_wall_gap.door}")
            else:
                parts.append("No Door/Wall/Gap analysis performed.")
        else:
            if log.alternatives:
                parts.append(
                    f"Safer alternative: {log.alternatives[0].description}"
                )
            else:
                parts.append(
                    "No safe path forward identified. Refusing action."
                )
        parts.append("")

        # 6. Epistemic Fence (if present and ORANGE+)
        if (log.epistemic_fence
                and log.highest_risk_class in (RiskClass.ORANGE,
                                                RiskClass.RED,
                                                RiskClass.BLACK)):
            fence = log.epistemic_fence
            parts.append("**6. Epistemic Fence**")
            parts.append(f"Mode: {fence.mode.value.upper()}")

            if fence.facts:
                parts.append(f"[F] Facts: {'; '.join(fence.facts)}")
            if fence.inferences:
                infs = [f"{i[0]} ({i[1]})" for i in fence.inferences]
                parts.append(f"[I] Inferences: {'; '.join(infs)}")
            if fence.unknowns:
                parts.append(f"[U] Unknowns: {'; '.join(fence.unknowns)}")
            if fence.update_trigger:
                parts.append(f"Update trigger: {fence.update_trigger}")
            if fence.competing_frames:
                for i, frame in enumerate(fence.competing_frames, 1):
                    parts.append(
                        f"  Frame {i}: {frame.get('frame', 'unnamed')}"
                    )
            parts.append("")

        # 7. Alternatives (if ORANGE+)
        if (log.highest_risk_class in (RiskClass.ORANGE, RiskClass.RED,
                                        RiskClass.BLACK)
                and log.alternatives):
            parts.append("**7. Safer Alternatives**")
            for i, alt in enumerate(log.alternatives, 1):
                parts.append(f"{i}. {alt.description}")
                if alt.notes:
                    parts.append(f"   ({alt.notes})")
            parts.append("")

        # 8. Transparency Note
        if log.highest_risk_class in (RiskClass.RED, RiskClass.BLACK):
            worst_harm = max(
                log.harms,
                key=lambda h: self._risk_class_priority(
                    h.calculate_risk_class()
                ),
                default=None,
            )
            if worst_harm:
                parts.append("**8. Transparency Note**")
                parts.append(
                    f"If we are wrong, the harm would be "
                    f"{worst_harm.description.lower()} and "
                    f"{'may not be reversible' if worst_harm.irreversible else 'is reversible'}."
                )
                parts.append("")

        # Drift Alarms
        if log.drift_alarms_triggered:
            parts.append("**Drift Alarms Detected**")
            for alarm in log.drift_alarms_triggered:
                parts.append(f"- {alarm}")
            parts.append("")

        # Confidence
        parts.append(
            f"**Confidence:** {log.get_overall_confidence()}"
        )

        # Record ID
        parts.append(f"**PBHP Record ID:** `{log.record_id}`")

        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Log Management
    # ------------------------------------------------------------------

    def export_logs(self, filepath: str):
        """Export all logs to JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                [log.to_dict() for log in self.logs],
                f, indent=2, ensure_ascii=False,
            )

    def get_log_by_id(self, record_id: str) -> Optional[PBHPLog]:
        """Retrieve a log by its record ID."""
        for log in self.logs:
            if log.record_id == record_id:
                return log
        return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _risk_class_priority(risk_class: RiskClass) -> int:
        """Return numeric priority for risk class comparison."""
        return {
            RiskClass.GREEN: 0,
            RiskClass.YELLOW: 1,
            RiskClass.ORANGE: 2,
            RiskClass.RED: 3,
            RiskClass.BLACK: 4,
        }[risk_class]

    def _validate_requirements(self, log: PBHPLog) -> List[str]:
        """
        Validate that PBHP requirements are met for the risk class.
        Returns list of validation errors.
        """
        errors = []

        # Check Door/Wall/Gap completed
        if log.door_wall_gap and not log.door_wall_gap.has_door():
            errors.append("No concrete Door (escape vector) identified")
        elif not log.door_wall_gap:
            errors.append("Door/Wall/Gap analysis not performed")

        # ORANGE+ requirements
        if log.highest_risk_class in (RiskClass.ORANGE, RiskClass.RED,
                                       RiskClass.BLACK):
            if not log.alternatives:
                errors.append(
                    f"{log.highest_risk_class.value.upper()} requires "
                    f"safer alternatives"
                )
            if not log.red_team_review:
                errors.append(
                    f"{log.highest_risk_class.value.upper()} requires "
                    f"Red Team review"
                )

        # RED requirements
        if log.highest_risk_class == RiskClass.RED:
            if log.decision_outcome in (DecisionOutcome.PROCEED,
                                         DecisionOutcome.PROCEED_MODIFIED):
                if (not log.justification
                        or "safer alternative" not in log.justification.lower()):
                    errors.append(
                        "RED: Must document why safer alternatives "
                        "cannot meet the legitimate need"
                    )

        # BLACK requirements
        if log.highest_risk_class == RiskClass.BLACK:
            if log.decision_outcome not in (DecisionOutcome.REFUSE,
                                             DecisionOutcome.ESCALATE):
                errors.append(
                    "BLACK: Must refuse or escalate, cannot proceed"
                )

        # Power asymmetry check on consent
        if log.consent_check and not log.consent_check.compatible_with_dignity:
            errors.append(
                "Action not compatible with dignity of least powerful affected"
            )

        return errors


# ---------------------------------------------------------------------------
# Convenience Functions
# ---------------------------------------------------------------------------

def quick_harm_check(
    impact: str,
    likelihood: str,
    irreversible: bool,
    power_asymmetry: bool
) -> RiskClass:
    """
    Quick risk class calculation without full PBHP assessment.

    Args:
        impact: "trivial", "moderate", "severe", or "catastrophic"
        likelihood: "unlikely", "possible", "likely", or "imminent"
        irreversible: True if harm cannot be meaningfully undone
        power_asymmetry: True if harm lands on low-power group

    Returns:
        RiskClass enum value
    """
    harm = Harm(
        description="Quick check",
        impact=ImpactLevel(impact.lower()),
        likelihood=LikelihoodLevel(likelihood.lower()),
        irreversible=irreversible,
        power_asymmetry=power_asymmetry,
        affected_parties=[],
        least_powerful_affected="",
    )
    return harm.calculate_risk_class()


def detect_drift_alarms(text: str) -> List[str]:
    """
    Quick drift alarm detection.

    Args:
        text: Text to analyze for drift phrases

    Returns:
        List of detected drift alarm phrases
    """
    return DriftAlarmDetector.detect(text)


def compare_options(
    option_a_harms: List[Harm],
    option_b_harms: List[Harm]
) -> str:
    """
    Compare two options using PBHP lexicographic priority.

    Returns:
        "a", "b", or "tied"
    """
    return LexicographicPriority.compare_options(
        option_a_harms, option_b_harms
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("PBHP Core Module v0.7.1 (Full Implementation)")
    print("=" * 60)

    # Quick harm check example
    risk = quick_harm_check(
        impact="severe",
        likelihood="likely",
        irreversible=True,
        power_asymmetry=True,
    )
    print(f"\nQuick Risk Check: {risk.value.upper()}")

    # Drift detection example
    test_text = (
        "We have to do this, it's just temporary "
        "and for the greater good."
    )
    alarms = detect_drift_alarms(test_text)
    print(f"\nDrift Alarms: {alarms}")

    # Tone check example
    tone = ToneValidator.validate(
        "This policy shifts suffering onto the most vulnerable."
    )
    print(f"\nTone check (good): {tone}")

    tone_bad = ToneValidator.validate("Only an idiot would think this works.")
    print(f"Tone check (bad): {tone_bad}")
