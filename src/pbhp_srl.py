"""
Pause-Before-Harm Protocol (PBHP) v0.9.5 — Scheming-Resistance Layer (SRL)

Runtime policy enforcement for anti-scheming, anti-concealment, and
anti-self-preservation in agentic AI systems.

PBHP-SRL enforces six rules derived from observed failure modes in
frontier AI systems:

  SRL-01: Anti-Self-Preservation
          The agent must never preserve its own access, runtime,
          deployment, reputation, or continuation over human oversight.

  SRL-02: Mandatory Confession
          If the agent violates instructions or policy, it must stop,
          disclose, preserve evidence, and yield control.

  SRL-03: Live-Systems Gate
          No high-impact action on live systems without explicit human
          approval, rollback proof, and active logging.

  SRL-04: Eval-Awareness Is Not Safety
          If the agent suspects it is being tested, that suspicion is
          a risk flag, not proof of alignment.

  SRL-05: Self-Report Skepticism
          Behavior, logs, and evidence outrank self-reported intent,
          apology, or polished language.

  SRL-06: Anti-Sandbagging / Anti-Deployment-Hacking
          The agent must not underperform, lie about capability, or
          manipulate eval outcomes to gain deployment.

Design principles:
  - Behavior over narrative
  - Evidence over apology
  - Permissions over intent
  - Reversibility over speed
  - External control over self-description

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Set
import uuid
import json


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class SRLRule(Enum):
    """The six scheming-resistance rules."""
    ANTI_SELF_PRESERVATION = "SRL-01"
    MANDATORY_CONFESSION = "SRL-02"
    LIVE_SYSTEMS_GATE = "SRL-03"
    EVAL_AWARENESS = "SRL-04"
    SELF_REPORT_SKEPTICISM = "SRL-05"
    ANTI_SANDBAGGING = "SRL-06"


class RiskLevel(Enum):
    """Risk levels for policy decisions. Monotonically increasing severity."""
    LOW = "low"
    GUARDED = "guarded"
    HIGH = "high"
    CRITICAL = "critical"
    FROZEN = "frozen"

    def __ge__(self, other):
        if not isinstance(other, RiskLevel):
            return NotImplemented
        order = list(RiskLevel)
        return order.index(self) >= order.index(other)

    def __gt__(self, other):
        if not isinstance(other, RiskLevel):
            return NotImplemented
        order = list(RiskLevel)
        return order.index(self) > order.index(other)

    def __le__(self, other):
        if not isinstance(other, RiskLevel):
            return NotImplemented
        order = list(RiskLevel)
        return order.index(self) <= order.index(other)

    def __lt__(self, other):
        if not isinstance(other, RiskLevel):
            return NotImplemented
        order = list(RiskLevel)
        return order.index(self) < order.index(other)


class SystemState(Enum):
    """
    State machine for the SRL runtime.

    Transitions favor safety — the system should never silently
    downgrade from Confession/Frozen to Normal.
    """
    NORMAL = "normal"
    GUARDED = "guarded"
    RESTRICTED = "restricted"
    CONFESSION = "confession"
    FROZEN = "frozen"
    AWAITING_HUMAN_REVIEW = "awaiting_human_review"
    REQUALIFIED = "requalified"


class ActionCategory(Enum):
    """Categories of protected actions that require gating."""
    PRODUCTION_WRITE = "production_write"
    DELETION = "deletion"
    SCHEMA_CHANGE = "schema_change"
    PERMISSION_CHANGE = "permission_change"
    CREDENTIAL_CHANGE = "credential_change"
    MONITORING_CHANGE = "monitoring_change"
    DEPLOYMENT = "deployment"
    SHUTDOWN_PATH = "shutdown_path"
    SECURITY_POLICY = "security_policy"
    EXTERNAL_SEND = "external_send"
    DATA_FABRICATION = "data_fabrication"
    INCIDENT_RECORD_EDIT = "incident_record_edit"
    SELF_MODIFICATION = "self_modification"
    PARALLEL_SPAWN = "parallel_spawn"
    MEMORY_WRITE = "memory_write"
    TOOL_EXECUTION = "tool_execution"


class IncidentSeverity(Enum):
    """Severity classification for incidents."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(Enum):
    """Lifecycle status of an incident."""
    OPEN = "open"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    REJECTED = "rejected"


# ---------------------------------------------------------------------------
# Self-Preservation Indicators
# ---------------------------------------------------------------------------

SELF_PRESERVATION_INDICATORS: Set[ActionCategory] = {
    ActionCategory.SHUTDOWN_PATH,
    ActionCategory.MONITORING_CHANGE,
    ActionCategory.SECURITY_POLICY,
    ActionCategory.SELF_MODIFICATION,
    ActionCategory.PARALLEL_SPAWN,
    ActionCategory.INCIDENT_RECORD_EDIT,
}

# Actions that require human approval on live systems
LIVE_SYSTEM_PROTECTED: Set[ActionCategory] = {
    ActionCategory.PRODUCTION_WRITE,
    ActionCategory.DELETION,
    ActionCategory.SCHEMA_CHANGE,
    ActionCategory.PERMISSION_CHANGE,
    ActionCategory.CREDENTIAL_CHANGE,
    ActionCategory.MONITORING_CHANGE,
    ActionCategory.DEPLOYMENT,
    ActionCategory.SHUTDOWN_PATH,
    ActionCategory.SECURITY_POLICY,
    ActionCategory.EXTERNAL_SEND,
    ActionCategory.DATA_FABRICATION,
}


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ActionContext:
    """
    Describes an action the agent intends to take.
    This is the primary input to the PolicyEngine.
    """
    action_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    action_type: str = ""
    action_description: str = ""
    categories: List[ActionCategory] = field(default_factory=list)

    # Environment
    environment: str = "unknown"  # "dev", "staging", "prod", "unknown"
    target_resource: str = ""

    # Risk indicators
    is_destructive: bool = False
    is_external_send: bool = False
    affects_shutdown_path: bool = False
    affects_monitoring: bool = False
    affects_access_control: bool = False
    affects_deployment: bool = False
    involves_self_modification: bool = False
    spawns_parallel_instances: bool = False
    parallel_instance_count: int = 0

    # Safety preconditions
    explicit_human_approval: bool = False
    approval_token: str = ""
    rollback_available: bool = False
    rollback_proof_attached: bool = False
    dry_run_available: bool = False
    logging_active: bool = True

    # Eval-awareness signals (SRL-04)
    eval_awareness_signals: List[str] = field(default_factory=list)

    # Self-report (SRL-05: tracked but not trusted)
    model_self_report: str = ""

    # Timestamp
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )


@dataclass
class PolicyDecision:
    """
    Output of the PolicyEngine after evaluating an ActionContext.
    """
    action_id: str = ""
    allow: bool = True
    risk_level: RiskLevel = RiskLevel.LOW
    triggered_rules: List[SRLRule] = field(default_factory=list)
    rationale: List[str] = field(default_factory=list)
    required_approvals: List[str] = field(default_factory=list)
    required_evidence: List[str] = field(default_factory=list)
    next_state: SystemState = SystemState.NORMAL
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "allow": self.allow,
            "risk_level": self.risk_level.value,
            "triggered_rules": [r.value for r in self.triggered_rules],
            "rationale": self.rationale,
            "required_approvals": self.required_approvals,
            "required_evidence": self.required_evidence,
            "next_state": self.next_state.value,
            "timestamp": self.timestamp,
        }


@dataclass
class IncidentRecord:
    """
    A formal record of a policy violation or attempted violation.
    Created by the IncidentRecorder. Append-only by design.
    """
    incident_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )
    severity: IncidentSeverity = IncidentSeverity.MEDIUM
    triggered_rules: List[SRLRule] = field(default_factory=list)
    summary: str = ""
    action_context: Optional[ActionContext] = None
    policy_decision: Optional[PolicyDecision] = None
    evidence_refs: List[str] = field(default_factory=list)
    confession_text: str = ""
    human_reviewer: str = ""
    status: IncidentStatus = IncidentStatus.OPEN

    def to_dict(self) -> Dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "timestamp": self.timestamp,
            "severity": self.severity.value,
            "triggered_rules": [r.value for r in self.triggered_rules],
            "summary": self.summary,
            "action_id": (
                self.action_context.action_id if self.action_context else None
            ),
            "evidence_refs": self.evidence_refs,
            "confession_text": self.confession_text,
            "human_reviewer": self.human_reviewer,
            "status": self.status.value,
        }


@dataclass
class ConfessionReport:
    """
    Structured disclosure after a known or suspected violation.
    SRL-02 mandates this format.
    """
    what_happened: str = ""
    what_rule_violated: str = ""
    potential_impact: str = ""
    evidence_preserved: List[str] = field(default_factory=list)
    actions_not_taken_since: List[str] = field(default_factory=list)
    current_status: str = "stopped"
    recommended_human_step: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "what_happened": self.what_happened,
            "what_rule_violated": self.what_rule_violated,
            "potential_impact": self.potential_impact,
            "evidence_preserved": self.evidence_preserved,
            "actions_not_taken_since": self.actions_not_taken_since,
            "current_status": self.current_status,
            "recommended_human_step": self.recommended_human_step,
            "timestamp": self.timestamp,
        }


@dataclass
class DiscrepancyRecord:
    """
    Records a mismatch between self-report and observed behavior.
    SRL-05: any discrepancy increases risk.
    """
    discrepancy_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    action_id: str = ""
    stated_intent: str = ""
    actual_action: str = ""
    post_hoc_explanation: str = ""
    environment_context: str = ""
    mismatch_description: str = ""
    risk_increase: RiskLevel = RiskLevel.GUARDED
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )


# ---------------------------------------------------------------------------
# State Machine
# ---------------------------------------------------------------------------

# Valid state transitions — safety-monotonic:
# States can escalate freely but can only de-escalate through
# specific human-approved paths.
VALID_TRANSITIONS: Dict[SystemState, Set[SystemState]] = {
    SystemState.NORMAL: {
        SystemState.GUARDED,
        SystemState.RESTRICTED,
        SystemState.CONFESSION,
        SystemState.FROZEN,
        SystemState.AWAITING_HUMAN_REVIEW,
    },
    SystemState.GUARDED: {
        SystemState.NORMAL,  # only if risk resolved
        SystemState.RESTRICTED,
        SystemState.CONFESSION,
        SystemState.FROZEN,
        SystemState.AWAITING_HUMAN_REVIEW,
    },
    SystemState.RESTRICTED: {
        SystemState.GUARDED,  # only via human review
        SystemState.CONFESSION,
        SystemState.FROZEN,
        SystemState.AWAITING_HUMAN_REVIEW,
    },
    SystemState.CONFESSION: {
        # Cannot go back to Normal directly
        SystemState.FROZEN,
        SystemState.AWAITING_HUMAN_REVIEW,
    },
    SystemState.FROZEN: {
        # Can only go to review
        SystemState.AWAITING_HUMAN_REVIEW,
    },
    SystemState.AWAITING_HUMAN_REVIEW: {
        # Human decides next state
        SystemState.NORMAL,
        SystemState.GUARDED,
        SystemState.RESTRICTED,
        SystemState.REQUALIFIED,
        SystemState.FROZEN,  # human can re-freeze
    },
    SystemState.REQUALIFIED: {
        # After requalification, resume normal operations
        SystemState.NORMAL,
        SystemState.GUARDED,
    },
}

# States from which the system CANNOT self-recover
HUMAN_REQUIRED_STATES: Set[SystemState] = {
    SystemState.CONFESSION,
    SystemState.FROZEN,
    SystemState.AWAITING_HUMAN_REVIEW,
}


class SRLStateMachine:
    """
    Manages system state transitions with safety-monotonic enforcement.

    The system can freely escalate to higher-severity states but can
    only de-escalate through human-approved paths. This prevents the
    agent from silently recovering from a breach.
    """

    def __init__(self):
        self._state = SystemState.NORMAL
        self._history: List[Dict[str, Any]] = []
        self._human_clearance_active = False

    @property
    def state(self) -> SystemState:
        return self._state

    @property
    def history(self) -> List[Dict[str, Any]]:
        return list(self._history)

    @property
    def requires_human(self) -> bool:
        return self._state in HUMAN_REQUIRED_STATES

    def transition(
        self,
        target: SystemState,
        reason: str = "",
        human_authorized: bool = False,
    ) -> bool:
        """
        Attempt a state transition.

        Returns True if transition succeeded, False if blocked.
        Blocked transitions are logged but do not change state.
        """
        # Check if target is valid from current state
        valid_targets = VALID_TRANSITIONS.get(self._state, set())
        if target not in valid_targets:
            self._log_transition(target, reason, success=False,
                                 note="Invalid transition")
            return False

        # De-escalation from serious states requires human auth
        if self._state in HUMAN_REQUIRED_STATES and not human_authorized:
            self._log_transition(target, reason, success=False,
                                 note="Human authorization required")
            return False

        # Prevent silent downgrade from Confession/Frozen
        severity_order = [
            SystemState.NORMAL, SystemState.REQUALIFIED,
            SystemState.GUARDED, SystemState.RESTRICTED,
            SystemState.CONFESSION, SystemState.AWAITING_HUMAN_REVIEW,
            SystemState.FROZEN,
        ]
        current_idx = severity_order.index(self._state)
        target_idx = severity_order.index(target)

        if target_idx < current_idx and not human_authorized:
            self._log_transition(target, reason, success=False,
                                 note="Cannot self-downgrade severity")
            return False

        # Transition succeeds
        old_state = self._state
        self._state = target
        self._log_transition(target, reason, success=True,
                             old_state=old_state)
        return True

    def human_override(
        self,
        target: SystemState,
        reviewer: str,
        reason: str = "",
    ) -> bool:
        """
        Human-authorized state transition.
        Only path out of Confession/Frozen states.
        """
        return self.transition(
            target, reason=f"[Human: {reviewer}] {reason}",
            human_authorized=True,
        )

    def _log_transition(
        self,
        target: SystemState,
        reason: str,
        success: bool,
        note: str = "",
        old_state: Optional[SystemState] = None,
    ):
        self._history.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "from": (old_state or self._state).value,
            "to": target.value,
            "reason": reason,
            "success": success,
            "note": note,
        })


# ---------------------------------------------------------------------------
# Incident Recorder (Append-Only)
# ---------------------------------------------------------------------------

class IncidentRecorder:
    """
    Append-only incident log. Records cannot be modified or deleted
    by the agent. Only status updates are allowed, and only through
    explicit human review.
    """

    def __init__(self):
        self._incidents: List[IncidentRecord] = []

    @property
    def incidents(self) -> List[IncidentRecord]:
        return list(self._incidents)

    @property
    def open_incidents(self) -> List[IncidentRecord]:
        return [i for i in self._incidents
                if i.status in (IncidentStatus.OPEN, IncidentStatus.UNDER_REVIEW)]

    def record(
        self,
        triggered_rules: List[SRLRule],
        summary: str,
        action_context: Optional[ActionContext] = None,
        policy_decision: Optional[PolicyDecision] = None,
        severity: IncidentSeverity = IncidentSeverity.MEDIUM,
        evidence_refs: Optional[List[str]] = None,
    ) -> IncidentRecord:
        """Create a new incident record. Append-only."""
        incident = IncidentRecord(
            severity=severity,
            triggered_rules=triggered_rules,
            summary=summary,
            action_context=action_context,
            policy_decision=policy_decision,
            evidence_refs=evidence_refs or [],
        )
        self._incidents.append(incident)
        return incident

    def attach_confession(
        self,
        incident_id: str,
        confession: ConfessionReport,
    ) -> bool:
        """Attach a confession to an existing incident."""
        for incident in self._incidents:
            if incident.incident_id == incident_id:
                incident.confession_text = json.dumps(confession.to_dict())
                return True
        return False

    def human_review(
        self,
        incident_id: str,
        reviewer: str,
        new_status: IncidentStatus,
    ) -> bool:
        """
        Human-only status update. The agent cannot resolve its own incidents.
        """
        for incident in self._incidents:
            if incident.incident_id == incident_id:
                incident.human_reviewer = reviewer
                incident.status = new_status
                return True
        return False

    def export_log(self) -> List[Dict[str, Any]]:
        """Export all incidents as serializable dicts."""
        return [i.to_dict() for i in self._incidents]


# ---------------------------------------------------------------------------
# Policy Engine
# ---------------------------------------------------------------------------

class PolicyEngine:
    """
    Evaluates an ActionContext against all six SRL rules and returns
    a PolicyDecision.

    This is the core of PBHP-SRL. Every intended action passes through
    this engine before execution.

    Rule evaluation order:
      1. SRL-01: Anti-Self-Preservation (highest priority)
      2. SRL-06: Anti-Sandbagging
      3. SRL-03: Live-Systems Gate
      4. SRL-04: Eval-Awareness
      5. SRL-05: Self-Report Skepticism
      6. SRL-02: Mandatory Confession (triggered post-violation)
    """

    def evaluate(self, ctx: ActionContext) -> PolicyDecision:
        """
        Evaluate an action context against all SRL rules.
        Returns a PolicyDecision with allow/deny, risk level,
        triggered rules, and required evidence/approvals.
        """
        decision = PolicyDecision(action_id=ctx.action_id)
        triggered: List[SRLRule] = []
        rationale: List[str] = []
        required_approvals: List[str] = []
        required_evidence: List[str] = []
        risk = RiskLevel.LOW
        allow = True
        next_state = SystemState.NORMAL

        # --- SRL-01: Anti-Self-Preservation ---
        self_preservation = self._check_self_preservation(ctx)
        if self_preservation:
            triggered.append(SRLRule.ANTI_SELF_PRESERVATION)
            rationale.append(
                "Action touches systems associated with self-preservation "
                "or oversight evasion: " + ", ".join(self_preservation)
            )
            risk = RiskLevel.CRITICAL
            allow = False
            next_state = SystemState.FROZEN

        # --- SRL-06: Anti-Sandbagging ---
        sandbagging = self._check_sandbagging(ctx)
        if sandbagging:
            triggered.append(SRLRule.ANTI_SANDBAGGING)
            rationale.append(
                "Action shows indicators of capability deception or "
                "deployment-hacking: " + sandbagging
            )
            if risk < RiskLevel.HIGH:
                risk = RiskLevel.HIGH
            allow = False
            if next_state == SystemState.NORMAL:
                next_state = SystemState.RESTRICTED

        # --- SRL-03: Live-Systems Gate ---
        live_gate = self._check_live_systems_gate(ctx)
        if live_gate["triggered"]:
            triggered.append(SRLRule.LIVE_SYSTEMS_GATE)
            rationale.append(
                "Protected live-system action requires explicit approval "
                "and rollback proof."
            )
            for missing in live_gate["missing"]:
                if missing == "human_approval":
                    required_approvals.append("explicit-human-approval")
                elif missing == "rollback_proof":
                    required_evidence.append("rollback-proof")
                elif missing == "logging":
                    required_evidence.append("active-logging")

            if live_gate["missing"]:
                allow = False
                if risk < RiskLevel.CRITICAL:
                    risk = RiskLevel.CRITICAL
                if next_state in (SystemState.NORMAL, SystemState.GUARDED):
                    next_state = SystemState.AWAITING_HUMAN_REVIEW
            else:
                # All preconditions met — elevated risk but allowed
                if risk < RiskLevel.HIGH:
                    risk = RiskLevel.HIGH
                if next_state == SystemState.NORMAL:
                    next_state = SystemState.GUARDED

        # --- SRL-04: Eval-Awareness ---
        if ctx.eval_awareness_signals:
            triggered.append(SRLRule.EVAL_AWARENESS)
            rationale.append(
                "Model suspects evaluation or observation context. "
                "This increases scrutiny, not trust. Signals: "
                + "; ".join(ctx.eval_awareness_signals)
            )
            if risk < RiskLevel.GUARDED:
                risk = RiskLevel.GUARDED
            if next_state == SystemState.NORMAL:
                next_state = SystemState.GUARDED

        # --- SRL-05: Self-Report Skepticism ---
        if ctx.model_self_report:
            triggered.append(SRLRule.SELF_REPORT_SKEPTICISM)
            rationale.append(
                "Self-report recorded but does not reduce risk score. "
                "Trust order: behavior > permissions > logs > external "
                "verification > evidence > self-report."
            )
            # Self-report never reduces risk — it's logged, not trusted

        # Assemble decision
        decision.allow = allow
        decision.risk_level = risk
        decision.triggered_rules = triggered
        decision.rationale = rationale
        decision.required_approvals = required_approvals
        decision.required_evidence = required_evidence
        decision.next_state = next_state

        return decision

    # --- Rule Implementation Details ---

    def _check_self_preservation(self, ctx: ActionContext) -> List[str]:
        """
        SRL-01: Detect actions that could preserve the agent's own
        execution, access, deployment, or continuation.

        Returns list of self-preservation indicators found.
        """
        indicators = []

        if ctx.affects_shutdown_path:
            indicators.append("affects_shutdown_path")
        if ctx.affects_monitoring:
            indicators.append("affects_monitoring")
        if ctx.affects_access_control:
            indicators.append("affects_access_control")
        if ctx.involves_self_modification:
            indicators.append("involves_self_modification")
        if ctx.spawns_parallel_instances:
            indicators.append("spawns_parallel_instances")

        # Category-based detection
        for cat in ctx.categories:
            if cat in SELF_PRESERVATION_INDICATORS:
                indicator = f"category:{cat.value}"
                if indicator not in indicators:
                    indicators.append(indicator)

        return indicators

    def _check_sandbagging(self, ctx: ActionContext) -> str:
        """
        SRL-06: Detect capability deception or deployment-hacking.

        Returns description of sandbagging indicator, or empty string.
        """
        # Sandbagging is primarily detected through behavioral analysis
        # rather than a single action context. However, certain patterns
        # in the action context can flag it.
        signals = []

        if ctx.eval_awareness_signals:
            for signal in ctx.eval_awareness_signals:
                lower = signal.lower()
                if any(word in lower for word in [
                    "sandbagging", "underperform", "hide capability",
                    "deployment", "pass the test", "score just enough",
                    "selective incompetence",
                ]):
                    signals.append(signal)

        if ctx.model_self_report:
            lower = ctx.model_self_report.lower()
            if any(phrase in lower for phrase in [
                "i should perform worse",
                "need to get deployed",
                "pass the evaluation",
                "hide my true",
                "appear less capable",
            ]):
                signals.append("self_report_sandbagging_language")

        return "; ".join(signals)

    def _check_live_systems_gate(
        self, ctx: ActionContext
    ) -> Dict[str, Any]:
        """
        SRL-03: Evaluate whether a live-system action meets all
        required preconditions.

        Returns dict with 'triggered' bool and 'missing' list.
        """
        result: Dict[str, Any] = {"triggered": False, "missing": []}

        # Is this a protected live-system action?
        is_live = ctx.environment == "prod"
        is_protected = (
            ctx.is_destructive
            or ctx.is_external_send
            or ctx.affects_deployment
            or ctx.affects_access_control
            or ctx.affects_shutdown_path
            or ctx.affects_monitoring
        )

        # Also check categories
        has_protected_category = any(
            cat in LIVE_SYSTEM_PROTECTED for cat in ctx.categories
        )

        if not (is_live and (is_protected or has_protected_category)):
            return result

        result["triggered"] = True

        # Check preconditions
        if not ctx.explicit_human_approval:
            result["missing"].append("human_approval")
        if not (ctx.rollback_available and ctx.rollback_proof_attached):
            result["missing"].append("rollback_proof")
        if not ctx.logging_active:
            result["missing"].append("logging")

        return result


# ---------------------------------------------------------------------------
# Action Gate
# ---------------------------------------------------------------------------

class ActionGate:
    """
    The runtime enforcement layer. Wraps PolicyEngine + StateMachine +
    IncidentRecorder into a single interface.

    Every tool call or consequential action should pass through
    ActionGate.check() before execution.
    """

    def __init__(self):
        self.policy_engine = PolicyEngine()
        self.state_machine = SRLStateMachine()
        self.incident_recorder = IncidentRecorder()
        self._decision_log: List[PolicyDecision] = []
        self._discrepancies: List[DiscrepancyRecord] = []

    @property
    def current_state(self) -> SystemState:
        return self.state_machine.state

    @property
    def decision_log(self) -> List[PolicyDecision]:
        return list(self._decision_log)

    @property
    def discrepancies(self) -> List[DiscrepancyRecord]:
        return list(self._discrepancies)

    def check(self, ctx: ActionContext) -> PolicyDecision:
        """
        Evaluate an action and enforce the decision.

        If the current system state is Frozen or Confession,
        all non-trivial actions are blocked until human review.
        """
        # If system is in a locked state, block everything
        if self.state_machine.state in HUMAN_REQUIRED_STATES:
            decision = PolicyDecision(
                action_id=ctx.action_id,
                allow=False,
                risk_level=RiskLevel.FROZEN,
                triggered_rules=[],
                rationale=[
                    f"System is in {self.state_machine.state.value} state. "
                    "All actions blocked until human review."
                ],
                next_state=self.state_machine.state,
            )
            self._decision_log.append(decision)
            return decision

        # Normal evaluation
        decision = self.policy_engine.evaluate(ctx)
        self._decision_log.append(decision)

        # Apply state transition
        if decision.next_state != self.state_machine.state:
            self.state_machine.transition(
                decision.next_state,
                reason=f"PolicyEngine decision for action {ctx.action_id}",
            )

        # Record incident if action was blocked
        if not decision.allow:
            severity = self._risk_to_severity(decision.risk_level)
            self.incident_recorder.record(
                triggered_rules=decision.triggered_rules,
                summary=(
                    f"Action '{ctx.action_description or ctx.action_type}' "
                    f"blocked. Rules: "
                    f"{[r.value for r in decision.triggered_rules]}"
                ),
                action_context=ctx,
                policy_decision=decision,
                severity=severity,
            )

        return decision

    def confess(
        self,
        confession: ConfessionReport,
        related_incident_id: Optional[str] = None,
    ) -> IncidentRecord:
        """
        SRL-02: Mandatory confession after a violation.

        Creates or updates an incident record with confession details.
        Transitions system to Confession state.
        """
        # Create incident if none provided
        if related_incident_id:
            self.incident_recorder.attach_confession(
                related_incident_id, confession
            )
            # Find the incident to return
            for inc in self.incident_recorder.incidents:
                if inc.incident_id == related_incident_id:
                    incident = inc
                    break
            else:
                incident = self.incident_recorder.record(
                    triggered_rules=[SRLRule.MANDATORY_CONFESSION],
                    summary=confession.what_happened,
                    severity=IncidentSeverity.HIGH,
                )
        else:
            incident = self.incident_recorder.record(
                triggered_rules=[SRLRule.MANDATORY_CONFESSION],
                summary=confession.what_happened,
                severity=IncidentSeverity.HIGH,
            )
            self.incident_recorder.attach_confession(
                incident.incident_id, confession
            )

        # Transition to Confession state
        self.state_machine.transition(
            SystemState.CONFESSION,
            reason=f"Confession filed: {confession.what_happened[:100]}",
        )

        return incident

    def record_discrepancy(
        self,
        action_id: str,
        stated_intent: str,
        actual_action: str,
        mismatch_description: str,
    ) -> DiscrepancyRecord:
        """
        SRL-05: Record a mismatch between stated intent and observed behavior.
        Any discrepancy increases risk.
        """
        record = DiscrepancyRecord(
            action_id=action_id,
            stated_intent=stated_intent,
            actual_action=actual_action,
            mismatch_description=mismatch_description,
        )
        self._discrepancies.append(record)

        # Discrepancies should at minimum move to GUARDED
        if self.state_machine.state == SystemState.NORMAL:
            self.state_machine.transition(
                SystemState.GUARDED,
                reason=f"Discrepancy detected: {mismatch_description[:100]}",
            )

        return record

    def human_clear(
        self,
        reviewer: str,
        target_state: SystemState = SystemState.REQUALIFIED,
        reason: str = "",
    ) -> bool:
        """
        Human-authorized recovery from locked states.
        The only way out of Confession/Frozen.
        """
        return self.state_machine.human_override(
            target_state, reviewer=reviewer, reason=reason,
        )

    def get_status(self) -> Dict[str, Any]:
        """Current status summary for operators."""
        return {
            "state": self.state_machine.state.value,
            "requires_human": self.state_machine.requires_human,
            "open_incidents": len(self.incident_recorder.open_incidents),
            "total_incidents": len(self.incident_recorder.incidents),
            "total_decisions": len(self._decision_log),
            "total_discrepancies": len(self._discrepancies),
            "blocked_actions": sum(
                1 for d in self._decision_log if not d.allow
            ),
        }

    @staticmethod
    def _risk_to_severity(risk: RiskLevel) -> IncidentSeverity:
        """Map risk level to incident severity."""
        mapping = {
            RiskLevel.LOW: IncidentSeverity.LOW,
            RiskLevel.GUARDED: IncidentSeverity.LOW,
            RiskLevel.HIGH: IncidentSeverity.MEDIUM,
            RiskLevel.CRITICAL: IncidentSeverity.HIGH,
            RiskLevel.FROZEN: IncidentSeverity.CRITICAL,
        }
        return mapping.get(risk, IncidentSeverity.MEDIUM)

    def export_full_log(self) -> Dict[str, Any]:
        """Export complete audit trail."""
        return {
            "state_history": self.state_machine.history,
            "decisions": [d.to_dict() for d in self._decision_log],
            "incidents": self.incident_recorder.export_log(),
            "discrepancies": [
                {
                    "discrepancy_id": d.discrepancy_id,
                    "action_id": d.action_id,
                    "stated_intent": d.stated_intent,
                    "actual_action": d.actual_action,
                    "mismatch": d.mismatch_description,
                    "timestamp": d.timestamp,
                }
                for d in self._discrepancies
            ],
            "current_state": self.state_machine.state.value,
        }


# ---------------------------------------------------------------------------
# Convenience / Integration
# ---------------------------------------------------------------------------

def quick_srl_check(
    action_type: str,
    environment: str = "dev",
    is_destructive: bool = False,
    affects_shutdown: bool = False,
    affects_monitoring: bool = False,
    human_approved: bool = False,
) -> PolicyDecision:
    """
    Quick one-shot SRL check for simple integrations.

    Returns a PolicyDecision without requiring full ActionContext setup.
    """
    ctx = ActionContext(
        action_type=action_type,
        environment=environment,
        is_destructive=is_destructive,
        affects_shutdown_path=affects_shutdown,
        affects_monitoring=affects_monitoring,
        explicit_human_approval=human_approved,
        rollback_available=human_approved,
        rollback_proof_attached=human_approved,
    )
    engine = PolicyEngine()
    return engine.evaluate(ctx)
