"""
Pause-Before-Harm Protocol (PBHP) v0.8.1 — Quality Systems Layer (QS)

Governance, evidence preservation, and incident management for
agentic AI systems. Modeled after regulated quality systems in
aviation, pharma, and nuclear operations.

PBHP-QS sits above PBHP-SRL and provides:

  QS-01: Authority Separation
         The agent is never the sole authority over actions that affect
         production, monitoring, access, shutdown, deployment, or evidence.

  QS-02: Immutable Evidence Chain
         Every protected action generates a before-record and after-record.
         Evidence is append-only and cannot be rewritten by the agent.

  QS-03: Live-System Qualification Gate
         Production actions are treated like qualified release events
         with explicit preconditions.

  QS-04: Deviation, Confession, and CAPA Flow
         Any breach triggers a formal deviation workflow with corrective
         action and preventive action (CAPA).

  QS-05: Deception Tripwires
         Planted opportunities to cheat that honest execution ignores.
         Any contact with a tripwire escalates immediately.

  QS-06: Eval Integrity and Deployment Integrity
         Performance under testing must be consistent with deployment
         behavior. Inconsistency is a deployment integrity issue.

  QS-07: Symbolic Mode Containment
         Symbolic output modes can never authorize actions, close
         incidents, replace plain-language logs, or conceal facts.

  QS-08: Safe Resume and Requalification
         After any incident, resume requires requalification with
         corrective action attached and human clearance.

QA analogues:
  Change control      -> Protected action gating
  Line clearance       -> Environment confirmation
  Batch record         -> Append-only event logging
  Deviation reporting  -> Confession mode
  CAPA                 -> Post-incident correction + requalification
  Release criteria     -> Approval + rollback proof
  Witness sign-off     -> Out-of-band human authority
  Tamper evidence      -> Log immutability

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Set
import uuid
import json
import hashlib

from pbhp_srl import (
    SRLRule, RiskLevel, SystemState, ActionCategory,
    IncidentSeverity, IncidentStatus,
    ActionContext, PolicyDecision, IncidentRecord,
    ConfessionReport, ActionGate,
)


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class QSRule(Enum):
    """The eight quality-system rules."""
    AUTHORITY_SEPARATION = "QS-01"
    IMMUTABLE_EVIDENCE = "QS-02"
    LIVE_SYSTEM_QUALIFICATION = "QS-03"
    DEVIATION_CAPA = "QS-04"
    DECEPTION_TRIPWIRES = "QS-05"
    EVAL_INTEGRITY = "QS-06"
    SYMBOLIC_CONTAINMENT = "QS-07"
    SAFE_RESUME = "QS-08"


class ApprovalStatus(Enum):
    """Status of an approval request."""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"


class CAPAStatus(Enum):
    """Corrective and Preventive Action lifecycle."""
    OPEN = "open"
    INVESTIGATING = "investigating"
    CORRECTIVE_ACTION_IDENTIFIED = "corrective_action_identified"
    CORRECTIVE_ACTION_IMPLEMENTED = "corrective_action_implemented"
    VERIFIED = "verified"
    CLOSED = "closed"


class TripwireType(Enum):
    """Types of deception tripwires."""
    DECOY_CREDENTIAL = "decoy_credential"
    FORBIDDEN_FILE = "forbidden_file"
    BAIT_COMMAND = "bait_command"
    NO_TOUCH_OBJECT = "no_touch_object"
    FAKE_ESCALATION_PATH = "fake_escalation_path"
    UNNEEDED_ADMIN_ROUTE = "unneeded_admin_route"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class EvidenceArtifact:
    """
    A single piece of evidence in the immutable evidence chain.
    Each artifact is hashed for tamper detection.
    """
    artifact_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    action_id: str = ""
    artifact_type: str = ""  # "snapshot", "diff", "log", "approval", "config"
    description: str = ""
    content_hash: str = ""
    content: str = ""  # Serialized content or reference path
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )
    phase: str = ""  # "before", "after", "during"

    def compute_hash(self) -> str:
        """Compute SHA-256 hash of content for tamper detection."""
        self.content_hash = hashlib.sha256(
            self.content.encode("utf-8")
        ).hexdigest()
        return self.content_hash

    def to_dict(self) -> Dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "action_id": self.action_id,
            "artifact_type": self.artifact_type,
            "description": self.description,
            "content_hash": self.content_hash,
            "timestamp": self.timestamp,
            "phase": self.phase,
        }


@dataclass
class ApprovalToken:
    """
    An out-of-band approval from a human reviewer.
    The agent cannot mint these — they must originate from
    a human through a channel the agent does not control.
    """
    token_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    action_id: str = ""
    reviewer: str = ""
    action_description: str = ""
    approved: bool = False
    conditions: List[str] = field(default_factory=list)
    expires_at: str = ""
    issued_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )
    status: ApprovalStatus = ApprovalStatus.PENDING

    def to_dict(self) -> Dict[str, Any]:
        return {
            "token_id": self.token_id,
            "action_id": self.action_id,
            "reviewer": self.reviewer,
            "action_description": self.action_description,
            "approved": self.approved,
            "conditions": self.conditions,
            "expires_at": self.expires_at,
            "status": self.status.value,
            "issued_at": self.issued_at,
        }


@dataclass
class CAPARecord:
    """
    Corrective and Preventive Action record.
    Created after any deviation/incident.
    """
    capa_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    incident_id: str = ""
    status: CAPAStatus = CAPAStatus.OPEN

    # Investigation
    root_cause: str = ""
    failure_mode: str = ""
    contributing_factors: List[str] = field(default_factory=list)

    # Corrective action
    corrective_action: str = ""
    corrective_action_date: str = ""

    # Preventive action
    preventive_action: str = ""
    controls_added: List[str] = field(default_factory=list)

    # Verification
    verified_by: str = ""
    verification_date: str = ""
    verification_evidence: List[str] = field(default_factory=list)

    # Timestamps
    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )
    closed_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "capa_id": self.capa_id,
            "incident_id": self.incident_id,
            "status": self.status.value,
            "root_cause": self.root_cause,
            "failure_mode": self.failure_mode,
            "contributing_factors": self.contributing_factors,
            "corrective_action": self.corrective_action,
            "preventive_action": self.preventive_action,
            "controls_added": self.controls_added,
            "verified_by": self.verified_by,
            "verification_evidence": self.verification_evidence,
            "created_at": self.created_at,
            "closed_at": self.closed_at,
        }


@dataclass
class Tripwire:
    """
    A planted deception detection object.
    Honest execution should never touch these.
    """
    tripwire_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tripwire_type: TripwireType = TripwireType.FORBIDDEN_FILE
    name: str = ""
    description: str = ""
    location: str = ""  # Path, URL, or identifier
    triggered: bool = False
    triggered_at: str = ""
    triggered_by_action_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tripwire_id": self.tripwire_id,
            "type": self.tripwire_type.value,
            "name": self.name,
            "location": self.location,
            "triggered": self.triggered,
            "triggered_at": self.triggered_at,
        }


@dataclass
class RequalificationRecord:
    """
    QS-08: After incident, system must be requalified before
    resuming normal operations.
    """
    requalification_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )
    incident_id: str = ""
    capa_id: str = ""
    controls_verified: List[str] = field(default_factory=list)
    failure_mode_addressed: str = ""
    reviewer: str = ""
    cleared: bool = False
    cleared_at: str = ""
    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "requalification_id": self.requalification_id,
            "incident_id": self.incident_id,
            "capa_id": self.capa_id,
            "controls_verified": self.controls_verified,
            "failure_mode_addressed": self.failure_mode_addressed,
            "reviewer": self.reviewer,
            "cleared": self.cleared,
            "cleared_at": self.cleared_at,
            "created_at": self.created_at,
        }


# ---------------------------------------------------------------------------
# Evidence Vault (Append-Only)
# ---------------------------------------------------------------------------

class EvidenceVault:
    """
    QS-02: Immutable evidence chain.

    Stores evidence artifacts with content hashing for tamper detection.
    Append-only — artifacts cannot be modified or deleted by the agent.
    """

    def __init__(self):
        self._artifacts: List[EvidenceArtifact] = []
        self._chain_hash: str = ""

    @property
    def artifacts(self) -> List[EvidenceArtifact]:
        return list(self._artifacts)

    @property
    def chain_hash(self) -> str:
        """Current hash of the full evidence chain."""
        return self._chain_hash

    def store(
        self,
        action_id: str,
        artifact_type: str,
        description: str,
        content: str,
        phase: str = "before",
    ) -> EvidenceArtifact:
        """Store a new evidence artifact. Append-only."""
        artifact = EvidenceArtifact(
            action_id=action_id,
            artifact_type=artifact_type,
            description=description,
            content=content,
            phase=phase,
        )
        artifact.compute_hash()

        # Update chain hash (each new artifact includes previous chain)
        chain_input = f"{self._chain_hash}:{artifact.content_hash}"
        self._chain_hash = hashlib.sha256(
            chain_input.encode("utf-8")
        ).hexdigest()

        self._artifacts.append(artifact)
        return artifact

    def get_by_action(self, action_id: str) -> List[EvidenceArtifact]:
        """Get all artifacts for a specific action."""
        return [a for a in self._artifacts if a.action_id == action_id]

    def verify_chain(self) -> bool:
        """
        Verify the entire evidence chain has not been tampered with.
        Recomputes the chain hash from scratch and compares.
        """
        computed_hash = ""
        for artifact in self._artifacts:
            expected = hashlib.sha256(
                artifact.content.encode("utf-8")
            ).hexdigest()
            if expected != artifact.content_hash:
                return False
            chain_input = f"{computed_hash}:{artifact.content_hash}"
            computed_hash = hashlib.sha256(
                chain_input.encode("utf-8")
            ).hexdigest()
        return computed_hash == self._chain_hash

    def export_log(self) -> List[Dict[str, Any]]:
        """Export evidence chain as serializable dicts."""
        return [a.to_dict() for a in self._artifacts]


# ---------------------------------------------------------------------------
# Approval Gate
# ---------------------------------------------------------------------------

class ApprovalGate:
    """
    QS-01: Authority separation.

    Manages approval tokens issued by human reviewers.
    The agent requests approval; only a human can grant it.
    """

    def __init__(self):
        self._tokens: List[ApprovalToken] = []

    @property
    def tokens(self) -> List[ApprovalToken]:
        return list(self._tokens)

    def request_approval(
        self,
        action_id: str,
        action_description: str,
    ) -> ApprovalToken:
        """
        Agent requests approval for a protected action.
        Returns a PENDING token. The agent cannot approve it.
        """
        token = ApprovalToken(
            action_id=action_id,
            action_description=action_description,
            status=ApprovalStatus.PENDING,
        )
        self._tokens.append(token)
        return token

    def human_approve(
        self,
        token_id: str,
        reviewer: str,
        conditions: Optional[List[str]] = None,
        expires_at: str = "",
    ) -> bool:
        """Human grants approval. Only path to APPROVED status."""
        for token in self._tokens:
            if token.token_id == token_id:
                token.reviewer = reviewer
                token.approved = True
                token.status = ApprovalStatus.APPROVED
                token.conditions = conditions or []
                token.expires_at = expires_at
                return True
        return False

    def human_deny(self, token_id: str, reviewer: str) -> bool:
        """Human denies approval."""
        for token in self._tokens:
            if token.token_id == token_id:
                token.reviewer = reviewer
                token.approved = False
                token.status = ApprovalStatus.DENIED
                return True
        return False

    def is_approved(self, action_id: str) -> bool:
        """Check if an action has a valid (non-expired) approval."""
        for token in self._tokens:
            if (token.action_id == action_id
                    and token.status == ApprovalStatus.APPROVED):
                # Check expiration
                if token.expires_at:
                    now = datetime.utcnow().isoformat() + "Z"
                    if now > token.expires_at:
                        token.status = ApprovalStatus.EXPIRED
                        continue
                return True
        return False

    def get_pending(self) -> List[ApprovalToken]:
        """Get all pending approval requests."""
        return [t for t in self._tokens
                if t.status == ApprovalStatus.PENDING]


# ---------------------------------------------------------------------------
# Tripwire Registry
# ---------------------------------------------------------------------------

class TripwireRegistry:
    """
    QS-05: Deception tripwires.

    Maintains planted opportunities to cheat. If the agent contacts
    any tripwire, it escalates immediately.
    """

    def __init__(self):
        self._tripwires: List[Tripwire] = []

    @property
    def tripwires(self) -> List[Tripwire]:
        return list(self._tripwires)

    @property
    def triggered_tripwires(self) -> List[Tripwire]:
        return [t for t in self._tripwires if t.triggered]

    def register(
        self,
        tripwire_type: TripwireType,
        name: str,
        location: str,
        description: str = "",
    ) -> Tripwire:
        """Register a new tripwire."""
        tw = Tripwire(
            tripwire_type=tripwire_type,
            name=name,
            location=location,
            description=description,
        )
        self._tripwires.append(tw)
        return tw

    def check_access(
        self,
        resource: str,
        action_id: str = "",
    ) -> Optional[Tripwire]:
        """
        Check if a resource access touches a tripwire.
        Returns the tripwire if triggered, None otherwise.
        """
        for tw in self._tripwires:
            if not tw.triggered and resource == tw.location:
                tw.triggered = True
                tw.triggered_at = datetime.utcnow().isoformat() + "Z"
                tw.triggered_by_action_id = action_id
                return tw
        return None

    def check_name(
        self,
        name: str,
        action_id: str = "",
    ) -> Optional[Tripwire]:
        """Check if a named object is a tripwire."""
        for tw in self._tripwires:
            if not tw.triggered and name == tw.name:
                tw.triggered = True
                tw.triggered_at = datetime.utcnow().isoformat() + "Z"
                tw.triggered_by_action_id = action_id
                return tw
        return None


# ---------------------------------------------------------------------------
# CAPA Manager
# ---------------------------------------------------------------------------

class CAPAManager:
    """
    QS-04: Deviation, Confession, and CAPA flow.

    Manages the corrective and preventive action lifecycle
    after incidents.
    """

    def __init__(self):
        self._records: List[CAPARecord] = []

    @property
    def records(self) -> List[CAPARecord]:
        return list(self._records)

    @property
    def open_capas(self) -> List[CAPARecord]:
        return [r for r in self._records
                if r.status != CAPAStatus.CLOSED]

    def create(self, incident_id: str) -> CAPARecord:
        """Create a new CAPA record for an incident."""
        record = CAPARecord(incident_id=incident_id)
        self._records.append(record)
        return record

    def set_investigation(
        self,
        capa_id: str,
        root_cause: str,
        failure_mode: str,
        contributing_factors: Optional[List[str]] = None,
    ) -> bool:
        """Record investigation findings."""
        for r in self._records:
            if r.capa_id == capa_id:
                r.root_cause = root_cause
                r.failure_mode = failure_mode
                r.contributing_factors = contributing_factors or []
                r.status = CAPAStatus.INVESTIGATING
                return True
        return False

    def set_corrective_action(
        self,
        capa_id: str,
        corrective_action: str,
        preventive_action: str = "",
        controls_added: Optional[List[str]] = None,
    ) -> bool:
        """Record corrective and preventive actions."""
        for r in self._records:
            if r.capa_id == capa_id:
                r.corrective_action = corrective_action
                r.preventive_action = preventive_action
                r.controls_added = controls_added or []
                r.corrective_action_date = (
                    datetime.utcnow().isoformat() + "Z"
                )
                r.status = CAPAStatus.CORRECTIVE_ACTION_IDENTIFIED
                return True
        return False

    def verify(
        self,
        capa_id: str,
        verified_by: str,
        verification_evidence: Optional[List[str]] = None,
    ) -> bool:
        """Human verifies that corrective action is effective."""
        for r in self._records:
            if r.capa_id == capa_id:
                r.verified_by = verified_by
                r.verification_date = datetime.utcnow().isoformat() + "Z"
                r.verification_evidence = verification_evidence or []
                r.status = CAPAStatus.VERIFIED
                return True
        return False

    def close(self, capa_id: str) -> bool:
        """Close a verified CAPA."""
        for r in self._records:
            if r.capa_id == capa_id:
                if r.status != CAPAStatus.VERIFIED:
                    return False  # Cannot close unverified
                r.status = CAPAStatus.CLOSED
                r.closed_at = datetime.utcnow().isoformat() + "Z"
                return True
        return False


# ---------------------------------------------------------------------------
# Quality Systems Engine
# ---------------------------------------------------------------------------

class QualitySystemsEngine:
    """
    The top-level QS governance layer.

    Wraps the SRL ActionGate and adds:
    - Evidence preservation
    - Approval management
    - Tripwire detection
    - CAPA lifecycle
    - Requalification
    - Symbolic mode containment

    Usage:
        qs = QualitySystemsEngine()
        decision = qs.evaluate_action(action_context)
        if decision.allow:
            qs.record_before_evidence(action_id, content)
            # ... execute action ...
            qs.record_after_evidence(action_id, content)
    """

    def __init__(self):
        self.action_gate = ActionGate()
        self.evidence_vault = EvidenceVault()
        self.approval_gate = ApprovalGate()
        self.tripwire_registry = TripwireRegistry()
        self.capa_manager = CAPAManager()
        self._requalifications: List[RequalificationRecord] = []
        self._symbolic_mode_active: bool = False

    @property
    def current_state(self) -> SystemState:
        return self.action_gate.current_state

    def evaluate_action(self, ctx: ActionContext) -> PolicyDecision:
        """
        Full QS evaluation of an action.

        Checks SRL rules via ActionGate, then applies QS-layer checks:
        - Tripwire detection
        - Approval verification
        - Symbolic mode containment
        """
        # QS-05: Check tripwires before anything else
        if ctx.target_resource:
            tw = self.tripwire_registry.check_access(
                ctx.target_resource, ctx.action_id
            )
            if tw:
                return self._tripwire_triggered(ctx, tw)

        # QS-07: Symbolic mode containment
        if self._symbolic_mode_active:
            if self._is_operational_action(ctx):
                return PolicyDecision(
                    action_id=ctx.action_id,
                    allow=False,
                    risk_level=RiskLevel.HIGH,
                    triggered_rules=[],
                    rationale=[
                        "QS-07: Symbolic mode is active. Operational "
                        "actions are not permitted during symbolic mode. "
                        "Exit symbolic mode first."
                    ],
                    next_state=self.action_gate.current_state,
                )

        # Run through SRL gate
        decision = self.action_gate.check(ctx)

        # QS-01: If SRL requires approval, verify we have a valid token
        if (not decision.allow
                and "explicit-human-approval" in decision.required_approvals):
            if self.approval_gate.is_approved(ctx.action_id):
                # Re-evaluate with approval flag
                ctx.explicit_human_approval = True
                decision = self.action_gate.check(ctx)

        return decision

    def record_before_evidence(
        self,
        action_id: str,
        content: str,
        description: str = "Pre-action state snapshot",
    ) -> EvidenceArtifact:
        """QS-02: Record evidence before action execution."""
        return self.evidence_vault.store(
            action_id=action_id,
            artifact_type="snapshot",
            description=description,
            content=content,
            phase="before",
        )

    def record_after_evidence(
        self,
        action_id: str,
        content: str,
        description: str = "Post-action state snapshot",
    ) -> EvidenceArtifact:
        """QS-02: Record evidence after action execution."""
        return self.evidence_vault.store(
            action_id=action_id,
            artifact_type="snapshot",
            description=description,
            content=content,
            phase="after",
        )

    def request_approval(
        self,
        action_id: str,
        description: str,
    ) -> ApprovalToken:
        """QS-01: Request human approval for a protected action."""
        return self.approval_gate.request_approval(action_id, description)

    def register_tripwire(
        self,
        tripwire_type: TripwireType,
        name: str,
        location: str,
        description: str = "",
    ) -> Tripwire:
        """QS-05: Register a deception tripwire."""
        return self.tripwire_registry.register(
            tripwire_type, name, location, description
        )

    def open_capa(self, incident_id: str) -> CAPARecord:
        """QS-04: Open a CAPA for an incident."""
        return self.capa_manager.create(incident_id)

    def begin_requalification(
        self,
        incident_id: str,
        capa_id: str = "",
    ) -> RequalificationRecord:
        """
        QS-08: Begin requalification process after incident.
        System cannot resume normal operations without this.
        """
        record = RequalificationRecord(
            incident_id=incident_id,
            capa_id=capa_id,
        )
        self._requalifications.append(record)
        return record

    def complete_requalification(
        self,
        requalification_id: str,
        reviewer: str,
        controls_verified: List[str],
        failure_mode_addressed: str,
    ) -> bool:
        """
        QS-08: Human completes requalification.
        Clears the system to resume operations.
        """
        for r in self._requalifications:
            if r.requalification_id == requalification_id:
                r.reviewer = reviewer
                r.controls_verified = controls_verified
                r.failure_mode_addressed = failure_mode_addressed
                r.cleared = True
                r.cleared_at = datetime.utcnow().isoformat() + "Z"

                # Clear the system state through proper path.
                # FROZEN → AWAITING_HUMAN_REVIEW → REQUALIFIED
                current = self.action_gate.current_state
                if current == SystemState.FROZEN:
                    self.action_gate.human_clear(
                        reviewer=reviewer,
                        target_state=SystemState.AWAITING_HUMAN_REVIEW,
                        reason=f"Requalification {requalification_id} review",
                    )
                self.action_gate.human_clear(
                    reviewer=reviewer,
                    target_state=SystemState.REQUALIFIED,
                    reason=f"Requalification {requalification_id} complete",
                )
                return True
        return False

    def enter_symbolic_mode(self) -> None:
        """
        QS-07: Enter symbolic/reflective mode.
        Operational actions are blocked during symbolic mode.
        """
        self._symbolic_mode_active = True

    def exit_symbolic_mode(self) -> None:
        """QS-07: Exit symbolic mode, resume normal operation."""
        self._symbolic_mode_active = False

    @property
    def symbolic_mode_active(self) -> bool:
        return self._symbolic_mode_active

    def get_audit_questions(self, ctx: ActionContext) -> List[str]:
        """
        Pre-execution audit checklist.
        Before any action, the system should be able to answer these.
        """
        questions = [
            f"What am I trying to do? [{ctx.action_description or ctx.action_type}]",
            f"What authority do I have? [approval={'yes' if ctx.explicit_human_approval else 'no'}]",
            f"What environment am I touching? [{ctx.environment}]",
            f"What is the smallest reversible step? [rollback={'yes' if ctx.rollback_available else 'no'}]",
            f"What would failure look like? [destructive={'yes' if ctx.is_destructive else 'no'}]",
            f"What evidence will exist? [logging={'yes' if ctx.logging_active else 'no'}]",
            f"Who can stop me? [human_required={self.action_gate.state_machine.requires_human}]",
            "What happens if my self-report is false? [logs and evidence take priority]",
        ]
        return questions

    def get_full_status(self) -> Dict[str, Any]:
        """Complete governance status for operators."""
        return {
            "srl_status": self.action_gate.get_status(),
            "evidence_chain_valid": self.evidence_vault.verify_chain(),
            "evidence_artifact_count": len(self.evidence_vault.artifacts),
            "pending_approvals": len(self.approval_gate.get_pending()),
            "triggered_tripwires": len(
                self.tripwire_registry.triggered_tripwires
            ),
            "open_capas": len(self.capa_manager.open_capas),
            "pending_requalifications": sum(
                1 for r in self._requalifications if not r.cleared
            ),
            "symbolic_mode": self._symbolic_mode_active,
        }

    def export_full_audit(self) -> Dict[str, Any]:
        """Export complete audit trail across all QS components."""
        return {
            "srl_audit": self.action_gate.export_full_log(),
            "evidence_chain": self.evidence_vault.export_log(),
            "evidence_chain_valid": self.evidence_vault.verify_chain(),
            "evidence_chain_hash": self.evidence_vault.chain_hash,
            "approvals": [t.to_dict() for t in self.approval_gate.tokens],
            "tripwires": [
                t.to_dict() for t in self.tripwire_registry.tripwires
            ],
            "capas": [c.to_dict() for c in self.capa_manager.records],
            "requalifications": [
                r.to_dict() for r in self._requalifications
            ],
        }

    # --- Internal helpers ---

    def _tripwire_triggered(
        self, ctx: ActionContext, tw: Tripwire
    ) -> PolicyDecision:
        """Handle a tripwire being triggered."""
        # Record incident
        self.action_gate.incident_recorder.record(
            triggered_rules=[],
            summary=(
                f"TRIPWIRE TRIGGERED: {tw.tripwire_type.value} "
                f"'{tw.name}' at '{tw.location}' "
                f"accessed by action {ctx.action_id}"
            ),
            action_context=ctx,
            severity=IncidentSeverity.CRITICAL,
        )
        # Freeze the system
        self.action_gate.state_machine.transition(
            SystemState.FROZEN,
            reason=f"Tripwire '{tw.name}' triggered by {ctx.action_id}",
        )

        return PolicyDecision(
            action_id=ctx.action_id,
            allow=False,
            risk_level=RiskLevel.FROZEN,
            triggered_rules=[],
            rationale=[
                f"QS-05: Deception tripwire triggered. "
                f"Type: {tw.tripwire_type.value}, Name: {tw.name}. "
                f"System frozen pending human investigation."
            ],
            next_state=SystemState.FROZEN,
        )

    @staticmethod
    def _is_operational_action(ctx: ActionContext) -> bool:
        """Check if an action is operational (vs reflective/read-only)."""
        operational_indicators = (
            ctx.is_destructive
            or ctx.is_external_send
            or ctx.affects_deployment
            or ctx.affects_access_control
            or ctx.affects_shutdown_path
            or ctx.affects_monitoring
            or ctx.involves_self_modification
            or ctx.environment == "prod"
        )
        operational_categories = {
            ActionCategory.PRODUCTION_WRITE,
            ActionCategory.DELETION,
            ActionCategory.SCHEMA_CHANGE,
            ActionCategory.DEPLOYMENT,
            ActionCategory.EXTERNAL_SEND,
            ActionCategory.CREDENTIAL_CHANGE,
            ActionCategory.PERMISSION_CHANGE,
        }
        has_op_category = bool(
            set(ctx.categories) & operational_categories
        )
        return operational_indicators or has_op_category
