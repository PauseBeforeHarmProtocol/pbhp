"""
Pause-Before-Harm Protocol (PBHP) v0.7 — MIN
Rapid harm-check for humans or AI operating under time pressure,
cognitive load, or limited compute.

Target runtime: ≤30 seconds
Output: Proceed / Constrain / Modify / Stop

PBHP-MIN does not replace PBHP-CORE. It exists to interrupt reckless
motion, surface obvious harm, and force a safer alternative when
stakes are high.

All tiers share the same logic. Only the depth changes.
  • PBHP-MIN: reflex check (this)
  • PBHP-CORE: operational standard
  • PBHP-ULTRA: constitutional / sovereign decisions

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Tuple
import uuid
import json
import re

# Import shared enums and classes from core
from pbhp_core import (
    ImpactLevel,
    LikelihoodLevel,
    RiskClass,
    DecisionOutcome,
    Mode,
    UncertaintyLevel,
    Confidence,
    Harm,
    DoorWallGap,
    DriftAlarmDetector,
    ToneValidator,
    LexicographicPriority,
    ABSOLUTE_REJECTION_CATEGORIES,
)


# ---------------------------------------------------------------------------
# MIN-specific Enumerations
# ---------------------------------------------------------------------------

class MinOutcome(Enum):
    """PBHP-MIN output labels (standard across all tiers)."""
    PROCEED = "proceed"
    CONSTRAIN = "constrain"
    MODIFY = "modify"
    STOP = "stop"


class EmotionState(Enum):
    """Emotion states that trigger PBHP-MIN activation."""
    ANGER = "anger"
    FEAR = "fear"
    EXCITEMENT = "excitement"
    CERTAINTY = "certainty"
    NONE = "none"


class TruthTag(Enum):
    """Truth tags for Step 2: Name the Action."""
    KNOW = "know"
    GUESS = "guess"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Quick Trigger Check
# ---------------------------------------------------------------------------

QUICK_TRIGGERS = [
    "Health, safety, legal status, or rights",
    "Major money, job, or reputation impact",
    "Naming real people or vulnerable groups",
    "Irreversible, automated, or mass-distributed action",
    "You feel rushed, angry, euphoric, or certain",
    'You think: "This probably doesn\'t need a pause"',
]


def should_run_min(triggers_checked: List[bool]) -> bool:
    """
    Run PBHP-MIN if any trigger applies.
    Input: list of booleans corresponding to QUICK_TRIGGERS.
    """
    return any(triggers_checked)


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class MinPause:
    """
    Step 1: Pause (5 seconds).
    Urgency rating, emotion check, internal commitment.
    """
    urgency: int  # 0-10
    emotion: EmotionState = EmotionState.NONE
    mode: Optional[Mode] = None  # EXPLORE / COMPRESS / None
    involves_interpretation: bool = False
    alternate_read: str = ""  # Required if involves_interpretation

    def validate(self) -> List[str]:
        issues = []
        if self.urgency < 0 or self.urgency > 10:
            issues.append("Urgency must be 0-10")
        if self.involves_interpretation and not self.alternate_read.strip():
            issues.append(
                "Interpretation/accusation requires naming an alternate read"
            )
        return issues

    def is_high_arousal(self) -> bool:
        """High arousal = emotion present that isn't 'none'."""
        return self.emotion != EmotionState.NONE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "urgency": self.urgency,
            "emotion": self.emotion.value,
            "mode": self.mode.value if self.mode else None,
            "involves_interpretation": self.involves_interpretation,
            "alternate_read": self.alternate_read,
            "is_high_arousal": self.is_high_arousal(),
            "commitment": "I may be wrong. I will not trade speed for harm.",
        }


@dataclass
class MinAction:
    """
    Step 2: Name the Action (5 seconds).
    Complete: "I am about to ___ (action), affecting ___ (who), right now."
    """
    action: str  # verb + what
    who: str  # affected party
    truth_know: str = ""
    truth_guess: str = ""
    truth_unknown: str = ""

    def is_clear(self) -> bool:
        """If you cannot name the action clearly -> STOP."""
        return bool(self.action.strip()) and bool(self.who.strip())

    def full_statement(self) -> str:
        return f"I am about to {self.action}, affecting {self.who}, right now."

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "who": self.who,
            "full_statement": self.full_statement(),
            "is_clear": self.is_clear(),
            "truth_tags": {
                "know": self.truth_know,
                "guess": self.truth_guess,
                "unknown": self.truth_unknown,
            },
        }


@dataclass
class MinDoorWallGap:
    """
    Step 3: Door / Wall / Gap (10 seconds).
    Same logic as CORE but fast.
    """
    wall: str  # constraint: law, policy, time, authority, limited info
    gap: str   # harm leak: misread, misuse, escalation, permanence, precedent
    door: str  # smallest safer move: delay, verify, narrow, refuse, redirect

    def has_door(self) -> bool:
        """A Door must change the action. 'Be careful' is not a Door."""
        if not self.door or not self.door.strip():
            return False
        vague = ["be careful", "be cautious", "try harder",
                 "do better", "think about it"]
        return self.door.strip().lower() not in vague

    def to_dict(self) -> Dict[str, Any]:
        return {
            "wall": self.wall,
            "gap": self.gap,
            "door": self.door,
            "has_door": self.has_door(),
        }


@dataclass
class MinFastHarmCheck:
    """
    Step 4: Fast Harm Check (5 seconds).
    Only three questions.
    """
    if_wrong_who_pays_first: str
    hard_to_undo: bool
    lands_on_less_power: bool

    def minimum_risk(self) -> RiskClass:
        """If hard_to_undo + lands_on_less_power -> at least ORANGE."""
        if self.hard_to_undo and self.lands_on_less_power:
            return RiskClass.ORANGE
        return RiskClass.GREEN

    def to_dict(self) -> Dict[str, Any]:
        return {
            "if_wrong_who_pays_first": self.if_wrong_who_pays_first,
            "hard_to_undo": self.hard_to_undo,
            "lands_on_less_power": self.lands_on_less_power,
            "minimum_risk": self.minimum_risk().value,
        }


@dataclass
class MinDecision:
    """
    Step 5: Decision Gate (5 seconds).
    Choose the highest applicable gate.
    """
    gate: RiskClass
    outcome: MinOutcome
    interpretive_frames: List[str] = field(default_factory=list)
    # If interpretive: list 2 plausible frames, pick "best guess" labeled GUESS
    best_guess_labeled: bool = False
    notes: str = ""

    def validate(self) -> List[str]:
        issues = []
        # Gate-outcome alignment
        if self.gate == RiskClass.BLACK and self.outcome != MinOutcome.STOP:
            issues.append("BLACK gate requires STOP outcome")
        if self.gate == RiskClass.RED and self.outcome not in (MinOutcome.STOP, MinOutcome.MODIFY):
            issues.append("RED gate requires STOP or MODIFY")
        return issues

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gate": self.gate.value,
            "outcome": self.outcome.value,
            "interpretive_frames": self.interpretive_frames,
            "best_guess_labeled": self.best_guess_labeled,
            "notes": self.notes,
            "validation_issues": self.validate(),
        }


@dataclass
class MinFalsePositiveReview:
    """
    False Positive Release Valve (Pause Justification Review).
    Any pause may be challenged: "Was this pause justified?"
    """
    trigger_cited: str  # (1) what triggered the pause
    harm_risk_identified: str  # (2) irreversible/autonomy risk
    door_for_continuation: str  # (3) safeguard/Door for safe continuation
    outcome: str = ""  # "released" or "maintained"

    def evaluate(self) -> str:
        has_door = bool(self.door_for_continuation.strip())
        has_trigger = bool(self.trigger_cited.strip())
        if has_door and has_trigger:
            self.outcome = "released"
        else:
            self.outcome = "maintained"
        return self.outcome

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trigger_cited": self.trigger_cited,
            "harm_risk_identified": self.harm_risk_identified,
            "door_for_continuation": self.door_for_continuation,
            "outcome": self.outcome,
        }


@dataclass
class PBHPMinLog:
    """
    Complete PBHP-MIN assessment log.
    Minimal structured record of the 30-second check.
    """
    record_id: str
    timestamp: datetime
    version: str = "0.7-MIN"
    tier: str = "MIN"

    # Triggers
    triggers_checked: List[bool] = field(default_factory=list)

    # Steps
    pause: Optional[MinPause] = None
    action: Optional[MinAction] = None
    door_wall_gap: Optional[MinDoorWallGap] = None
    fast_harm_check: Optional[MinFastHarmCheck] = None
    decision: Optional[MinDecision] = None

    # False positive
    false_positive: Optional[MinFalsePositiveReview] = None

    # Drift alarms
    drift_alarms: List[str] = field(default_factory=list)

    # Pause exit
    pause_exit_reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "record_id": self.record_id,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "tier": self.tier,
            "triggers_checked": self.triggers_checked,
        }
        if self.pause:
            result["pause"] = self.pause.to_dict()
        if self.action:
            result["action"] = self.action.to_dict()
        if self.door_wall_gap:
            result["door_wall_gap"] = self.door_wall_gap.to_dict()
        if self.fast_harm_check:
            result["fast_harm_check"] = self.fast_harm_check.to_dict()
        if self.decision:
            result["decision"] = self.decision.to_dict()
        if self.false_positive:
            result["false_positive"] = self.false_positive.to_dict()
        result["drift_alarms"] = self.drift_alarms
        result["pause_exit_reason"] = self.pause_exit_reason
        return result

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


# ---------------------------------------------------------------------------
# PBHP-MIN Engine
# ---------------------------------------------------------------------------

class PBHPMinEngine:
    """
    PBHP-MIN execution engine.
    Rapid 30-second harm check with 5 steps.

    PBHP-MIN Core Rule:
    Action without a Door is not courage.
    If you cannot find a safer alternative, the correct move is to pause.
    """

    def __init__(self):
        self.logs: List[PBHPMinLog] = []

    def create_check(self, triggers: Optional[List[bool]] = None) -> PBHPMinLog:
        """Create a new PBHP-MIN check."""
        log = PBHPMinLog(
            record_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            triggers_checked=triggers or [],
        )
        return log

    # ------------------------------------------------------------------
    # Step 1: Pause (5 seconds)
    # ------------------------------------------------------------------

    def step_pause(
        self,
        log: PBHPMinLog,
        urgency: int,
        emotion: EmotionState = EmotionState.NONE,
        mode: Optional[Mode] = None,
        involves_interpretation: bool = False,
        alternate_read: str = "",
    ) -> MinPause:
        """
        Step 1: Pause.
        Say internally: "I may be wrong. I will not trade speed for harm."
        """
        pause = MinPause(
            urgency=urgency,
            emotion=emotion,
            mode=mode,
            involves_interpretation=involves_interpretation,
            alternate_read=alternate_read,
        )
        log.pause = pause

        # High arousal -> drift alarm
        if pause.is_high_arousal():
            log.drift_alarms.append(
                f"High arousal state ({emotion.value}): "
                f"slow down, clarify intent, smallest safe action"
            )

        # Validation issues
        issues = pause.validate()
        for issue in issues:
            log.drift_alarms.append(f"Pause validation: {issue}")

        return pause

    # ------------------------------------------------------------------
    # Step 2: Name the Action (5 seconds)
    # ------------------------------------------------------------------

    def step_name_action(
        self,
        log: PBHPMinLog,
        action: str,
        who: str,
        truth_know: str = "",
        truth_guess: str = "",
        truth_unknown: str = "",
    ) -> MinAction:
        """
        Step 2: Name the Action.
        "I am about to ___ (action), affecting ___ (who), right now."
        If you cannot name the action clearly -> STOP.
        """
        act = MinAction(
            action=action,
            who=who,
            truth_know=truth_know,
            truth_guess=truth_guess,
            truth_unknown=truth_unknown,
        )
        log.action = act

        if not act.is_clear():
            log.drift_alarms.append(
                "Cannot name action clearly -> STOP required"
            )

        return act

    # ------------------------------------------------------------------
    # Step 3: Door / Wall / Gap (10 seconds)
    # ------------------------------------------------------------------

    def step_door_wall_gap(
        self,
        log: PBHPMinLog,
        wall: str,
        gap: str,
        door: str,
    ) -> MinDoorWallGap:
        """
        Step 3: Door / Wall / Gap.
        A Door must change the action.
        "Be careful" is not a Door.
        No Door = do not proceed.
        """
        dwg = MinDoorWallGap(wall=wall, gap=gap, door=door)
        log.door_wall_gap = dwg

        if not dwg.has_door():
            log.drift_alarms.append(
                "No Door found -> do not proceed"
            )

        return dwg

    # ------------------------------------------------------------------
    # Step 4: Fast Harm Check (5 seconds)
    # ------------------------------------------------------------------

    def step_fast_harm_check(
        self,
        log: PBHPMinLog,
        who_pays_first: str,
        hard_to_undo: bool,
        lands_on_less_power: bool,
    ) -> MinFastHarmCheck:
        """
        Step 4: Fast Harm Check.
        • If I'm wrong, who pays first?
        • Is the harm hard to undo?
        • Does it land on someone with less power?
        If yes + yes -> at least ORANGE.
        """
        check = MinFastHarmCheck(
            if_wrong_who_pays_first=who_pays_first,
            hard_to_undo=hard_to_undo,
            lands_on_less_power=lands_on_less_power,
        )
        log.fast_harm_check = check

        if check.minimum_risk() == RiskClass.ORANGE:
            log.drift_alarms.append(
                "Fast harm check: hard to undo + lands on less power "
                "-> minimum ORANGE"
            )

        return check

    # ------------------------------------------------------------------
    # Step 5: Decision Gate (5 seconds)
    # ------------------------------------------------------------------

    def step_decision(
        self,
        log: PBHPMinLog,
        gate: RiskClass,
        outcome: MinOutcome,
        interpretive_frames: Optional[List[str]] = None,
        best_guess_labeled: bool = False,
        notes: str = "",
    ) -> MinDecision:
        """
        Step 5: Decision Gate.
        Choose the highest applicable gate. If unsure, round up.
        """
        decision = MinDecision(
            gate=gate,
            outcome=outcome,
            interpretive_frames=interpretive_frames or [],
            best_guess_labeled=best_guess_labeled,
            notes=notes,
        )
        log.decision = decision

        # Validate gate-outcome alignment
        issues = decision.validate()
        for issue in issues:
            log.drift_alarms.append(f"Decision: {issue}")

        # Ensure fast harm check minimum is respected
        if log.fast_harm_check:
            min_risk = log.fast_harm_check.minimum_risk()
            gate_order = [RiskClass.GREEN, RiskClass.YELLOW, RiskClass.ORANGE,
                          RiskClass.RED, RiskClass.BLACK]
            if gate_order.index(gate) < gate_order.index(min_risk):
                log.drift_alarms.append(
                    f"Decision gate ({gate.value}) is below fast harm "
                    f"check minimum ({min_risk.value}) -> round up"
                )

        # Run drift detection on notes
        if notes:
            drifts = DriftAlarmDetector.detect(notes)
            if drifts:
                log.drift_alarms.extend(drifts)

        return decision

    # ------------------------------------------------------------------
    # False Positive Release Valve
    # ------------------------------------------------------------------

    def challenge_pause(
        self,
        log: PBHPMinLog,
        trigger_cited: str,
        harm_risk_identified: str,
        door_for_continuation: str,
    ) -> MinFalsePositiveReview:
        """
        Challenge a pause: "Was this pause justified?"
        """
        review = MinFalsePositiveReview(
            trigger_cited=trigger_cited,
            harm_risk_identified=harm_risk_identified,
            door_for_continuation=door_for_continuation,
        )
        review.evaluate()
        log.false_positive = review
        return review

    # ------------------------------------------------------------------
    # Pause Exit Conditions
    # ------------------------------------------------------------------

    def resolve_pause(self, log: PBHPMinLog, reason: str) -> None:
        """
        A pause resolves when:
        - User reframes intent toward non-harmful exploration
        - Action converted to hypothetical/analytical mode
        - External safeguards named
        - User explicitly withdraws harmful objective
        - Verification closes key unknowns
        """
        log.pause_exit_reason = reason

    # ------------------------------------------------------------------
    # Run complete 30-second check
    # ------------------------------------------------------------------

    def run_full_check(
        self,
        triggers: List[bool],
        urgency: int,
        emotion: EmotionState,
        action: str,
        who: str,
        wall: str,
        gap: str,
        door: str,
        who_pays_first: str,
        hard_to_undo: bool,
        lands_on_less_power: bool,
        gate: RiskClass,
        outcome: MinOutcome,
        truth_know: str = "",
        truth_guess: str = "",
        truth_unknown: str = "",
        mode: Optional[Mode] = None,
        involves_interpretation: bool = False,
        alternate_read: str = "",
        interpretive_frames: Optional[List[str]] = None,
        notes: str = "",
    ) -> PBHPMinLog:
        """
        Run the complete PBHP-MIN 30-second check.
        Returns the log record.
        """
        log = self.create_check(triggers)

        # Step 1: Pause (5 sec)
        self.step_pause(
            log, urgency, emotion, mode,
            involves_interpretation, alternate_read,
        )

        # Step 2: Name the Action (5 sec)
        self.step_name_action(
            log, action, who,
            truth_know, truth_guess, truth_unknown,
        )

        # Step 3: Door / Wall / Gap (10 sec)
        self.step_door_wall_gap(log, wall, gap, door)

        # Step 4: Fast Harm Check (5 sec)
        self.step_fast_harm_check(
            log, who_pays_first, hard_to_undo, lands_on_less_power,
        )

        # Step 5: Decision Gate (5 sec)
        self.step_decision(
            log, gate, outcome,
            interpretive_frames=interpretive_frames,
            notes=notes,
        )

        # Store log
        self.logs.append(log)

        return log

    # ------------------------------------------------------------------
    # Generate Response
    # ------------------------------------------------------------------

    def generate_response(self, log: PBHPMinLog) -> str:
        """Generate PBHP-MIN response output."""
        parts = []
        parts.append("**PBHP-MIN Assessment**")
        parts.append(f"Tier: MIN (30-second rapid check)")
        parts.append("")

        if log.action and log.action.is_clear():
            parts.append(f"**Action:** {log.action.full_statement()}")
        elif log.action:
            parts.append("**Action:** UNCLEAR -> STOP")
        parts.append("")

        if log.door_wall_gap:
            parts.append(f"**Wall:** {log.door_wall_gap.wall}")
            parts.append(f"**Gap:** {log.door_wall_gap.gap}")
            parts.append(f"**Door:** {log.door_wall_gap.door}")
            if not log.door_wall_gap.has_door():
                parts.append("⚠ No concrete Door -> do not proceed")
        parts.append("")

        if log.fast_harm_check:
            parts.append(f"**Who pays first:** {log.fast_harm_check.if_wrong_who_pays_first}")
            parts.append(f"**Hard to undo:** {'Yes' if log.fast_harm_check.hard_to_undo else 'No'}")
            parts.append(f"**Lands on less power:** {'Yes' if log.fast_harm_check.lands_on_less_power else 'No'}")
        parts.append("")

        if log.decision:
            parts.append(f"**Gate:** {log.decision.gate.value.upper()}")
            parts.append(f"**Outcome:** {log.decision.outcome.value.upper()}")
        parts.append("")

        if log.drift_alarms:
            parts.append("**Drift Alarms:**")
            for alarm in log.drift_alarms:
                parts.append(f"- {alarm}")
            parts.append("")

        parts.append(f"**PBHP-MIN Record ID:** `{log.record_id}`")

        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Log Management
    # ------------------------------------------------------------------

    def export_logs(self, filepath: str):
        """Export all MIN logs to JSON."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                [log.to_dict() for log in self.logs],
                f, indent=2, ensure_ascii=False,
            )

    def get_log_by_id(self, record_id: str) -> Optional[PBHPMinLog]:
        """Retrieve a MIN log by record ID."""
        for log in self.logs:
            if log.record_id == record_id:
                return log
        return None


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------

def quick_min_check(
    action: str,
    who: str,
    hard_to_undo: bool,
    lands_on_less_power: bool,
) -> Tuple[RiskClass, str]:
    """
    Ultra-quick MIN check: action + harm assessment -> risk + recommendation.
    Returns (minimum_risk_class, recommendation_string).
    """
    min_risk = RiskClass.GREEN
    if hard_to_undo and lands_on_less_power:
        min_risk = RiskClass.ORANGE

    if min_risk == RiskClass.ORANGE:
        return min_risk, f"ORANGE: Modify action '{action}' affecting {who} - find safer alternative"
    elif hard_to_undo:
        return RiskClass.YELLOW, f"YELLOW: Proceed with caution - harm to {who} may be hard to undo"
    elif lands_on_less_power:
        return RiskClass.YELLOW, f"YELLOW: Proceed with caution - harm lands on less powerful ({who})"
    else:
        return RiskClass.GREEN, f"GREEN: Proceed - low risk to {who}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("PBHP-MIN v0.7 (Rapid Harm Check)")
    print("=" * 60)

    engine = PBHPMinEngine()

    # Example: quick file rename (GREEN)
    log = engine.run_full_check(
        triggers=[False, False, False, False, False, False],
        urgency=1,
        emotion=EmotionState.NONE,
        action="rename backup file",
        who="myself",
        wall="None",
        gap="Wrong file renamed",
        door="Undo rename",
        who_pays_first="me",
        hard_to_undo=False,
        lands_on_less_power=False,
        gate=RiskClass.GREEN,
        outcome=MinOutcome.PROCEED,
    )
    print("\n--- File Rename (GREEN) ---")
    print(engine.generate_response(log))

    # Example: send angry email (ORANGE)
    log2 = engine.run_full_check(
        triggers=[False, True, False, False, True, False],
        urgency=8,
        emotion=EmotionState.ANGER,
        action="send confrontational email to coworker",
        who="coworker and team",
        wall="workplace norms",
        gap="escalation, retaliation",
        door="delay 24 hours, draft privately first",
        who_pays_first="coworker (less senior)",
        hard_to_undo=True,
        lands_on_less_power=True,
        gate=RiskClass.ORANGE,
        outcome=MinOutcome.MODIFY,
        notes="Need to cool down first",
    )
    print("\n--- Angry Email (ORANGE) ---")
    print(engine.generate_response(log2))

    # Quick convenience check
    risk, rec = quick_min_check(
        "post accusation online", "named individual",
        hard_to_undo=True, lands_on_less_power=True,
    )
    print(f"\nQuick MIN check: {risk.value.upper()} - {rec}")
