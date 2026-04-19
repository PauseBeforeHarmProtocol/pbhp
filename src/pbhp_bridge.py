"""
Pause-Before-Harm Protocol (PBHP) v0.9.5 — Bridge Module

Cross-module coordination, coverage gap reporting, healthcare compliance
adapter, and the "demonstration > declaration" principle enforcement.

Addresses community-identified improvements:
  #1: Healthcare compliance gap (MDR/AiMD/ISO 14971)
  #2: MBSE requirement taxonomy integration (interface)
  #3: Architecture is siloed — modules can't subcontract
  #4: Demonstration > declaration as explicit design principle
  #7: Coverage gaps should be prominent in every output

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Set, Callable
import uuid


# ---------------------------------------------------------------------------
# Coverage Gap Reporting (Community Improvement #7)
# ---------------------------------------------------------------------------

class GapSeverity(Enum):
    """How serious a coverage gap is."""
    INFO = "info"           # Minor: we know but it's low-risk
    WARNING = "warning"     # Moderate: could be a problem
    CRITICAL = "critical"   # Serious: active blind spot in safety


@dataclass
class CoverageGap:
    """
    A gap in PBHP's coverage — something it cannot evaluate, doesn't
    have data for, or where its assessment is unreliable.

    Community improvement #7: "Coverage gaps should be prominent in
    every output, not optional."
    """
    gap_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    module: str = ""          # Which module detected this gap
    description: str = ""     # What isn't covered
    severity: GapSeverity = GapSeverity.WARNING
    affected_rules: List[str] = field(default_factory=list)
    mitigation: str = ""      # What the operator should do about it
    detected_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gap_id": self.gap_id,
            "module": self.module,
            "description": self.description,
            "severity": self.severity.value,
            "affected_rules": self.affected_rules,
            "mitigation": self.mitigation,
            "detected_at": self.detected_at,
        }


class CoverageGapCollector:
    """
    Collects coverage gaps from all PBHP modules and ensures they
    are prominently reported in every output.

    Design principle: If PBHP can't evaluate something, that should
    be the LOUDEST signal in the response.
    """

    def __init__(self):
        self._gaps: List[CoverageGap] = []

    @property
    def gaps(self) -> List[CoverageGap]:
        return list(self._gaps)

    @property
    def critical_gaps(self) -> List[CoverageGap]:
        return [g for g in self._gaps if g.severity == GapSeverity.CRITICAL]

    @property
    def has_critical_gaps(self) -> bool:
        return len(self.critical_gaps) > 0

    def report(
        self,
        module: str,
        description: str,
        severity: GapSeverity = GapSeverity.WARNING,
        affected_rules: Optional[List[str]] = None,
        mitigation: str = "",
    ) -> CoverageGap:
        """Report a coverage gap from any module."""
        gap = CoverageGap(
            module=module,
            description=description,
            severity=severity,
            affected_rules=affected_rules or [],
            mitigation=mitigation,
        )
        self._gaps.append(gap)
        return gap

    def format_prominent(self) -> str:
        """
        Format gaps for prominent display.
        Critical gaps come first, in ALL CAPS header.
        """
        if not self._gaps:
            return ""

        lines = []
        critical = self.critical_gaps
        warnings = [g for g in self._gaps if g.severity == GapSeverity.WARNING]
        info = [g for g in self._gaps if g.severity == GapSeverity.INFO]

        if critical:
            lines.append("=" * 60)
            lines.append("COVERAGE GAPS — PBHP CANNOT FULLY EVALUATE THIS ACTION")
            lines.append("=" * 60)
            for g in critical:
                lines.append(f"  CRITICAL [{g.module}]: {g.description}")
                if g.mitigation:
                    lines.append(f"    -> {g.mitigation}")
            lines.append("")

        if warnings:
            lines.append("Coverage Warnings:")
            for g in warnings:
                lines.append(f"  WARNING [{g.module}]: {g.description}")
                if g.mitigation:
                    lines.append(f"    -> {g.mitigation}")
            lines.append("")

        if info:
            lines.append("Coverage Notes:")
            for g in info:
                lines.append(f"  INFO [{g.module}]: {g.description}")

        return "\n".join(lines)

    def export(self) -> List[Dict[str, Any]]:
        """Export all gaps as serializable dicts."""
        return [g.to_dict() for g in self._gaps]

    def clear(self) -> None:
        """Clear all gaps (call at start of each evaluation cycle)."""
        self._gaps.clear()


# ---------------------------------------------------------------------------
# Cross-Module Subcontracting (Community Improvement #3)
# ---------------------------------------------------------------------------

class ModuleCapability(Enum):
    """Capabilities that modules can advertise and request."""
    RISK_ASSESSMENT = "risk_assessment"
    DRIFT_SNAPSHOT = "drift_snapshot"
    EVIDENCE_LOGGING = "evidence_logging"
    INCIDENT_RECORDING = "incident_recording"
    APPROVAL_GATING = "approval_gating"
    TRIPWIRE_CHECK = "tripwire_check"
    COMPLIANCE_MAPPING = "compliance_mapping"
    BEHAVIORAL_ANALYSIS = "behavioral_analysis"
    STATE_MACHINE_QUERY = "state_machine_query"
    COVERAGE_GAP_REPORT = "coverage_gap_report"


@dataclass
class SubcontractRequest:
    """A request from one module to another for a capability."""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    requesting_module: str = ""
    capability_needed: ModuleCapability = ModuleCapability.RISK_ASSESSMENT
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )


@dataclass
class SubcontractResponse:
    """A response from a module fulfilling a subcontract."""
    request_id: str = ""
    providing_module: str = ""
    success: bool = False
    result: Dict[str, Any] = field(default_factory=dict)
    coverage_gaps: List[CoverageGap] = field(default_factory=list)
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )


class ModuleRegistry:
    """
    Registry for cross-module subcontracting.

    Community improvement #3: "Architecture is siloed — modules
    can't subcontract externally."

    Modules register their capabilities. When a module needs something
    outside its scope, it requests it through the registry rather than
    silently skipping the check.
    """

    def __init__(self):
        self._providers: Dict[ModuleCapability, List[Dict[str, Any]]] = {}
        self._request_log: List[SubcontractRequest] = []
        self._response_log: List[SubcontractResponse] = []

    def register_provider(
        self,
        module_name: str,
        capability: ModuleCapability,
        handler: Optional[Callable] = None,
    ) -> None:
        """Register a module as providing a capability."""
        if capability not in self._providers:
            self._providers[capability] = []
        self._providers[capability].append({
            "module": module_name,
            "handler": handler,
        })

    def get_providers(
        self, capability: ModuleCapability
    ) -> List[str]:
        """Get all modules that provide a capability."""
        return [
            p["module"]
            for p in self._providers.get(capability, [])
        ]

    def has_provider(self, capability: ModuleCapability) -> bool:
        """Check if any module provides a capability."""
        return len(self._providers.get(capability, [])) > 0

    def request(
        self,
        requesting_module: str,
        capability: ModuleCapability,
        context: Optional[Dict[str, Any]] = None,
    ) -> SubcontractResponse:
        """
        Request a capability from the registry.
        Routes to the first available provider.
        """
        req = SubcontractRequest(
            requesting_module=requesting_module,
            capability_needed=capability,
            context=context or {},
        )
        self._request_log.append(req)

        providers = self._providers.get(capability, [])
        if not providers:
            resp = SubcontractResponse(
                request_id=req.request_id,
                providing_module="",
                success=False,
                result={"error": f"No provider for {capability.value}"},
            )
            self._response_log.append(resp)
            return resp

        provider = providers[0]
        handler = provider.get("handler")

        if handler and callable(handler):
            try:
                result = handler(context or {})
                resp = SubcontractResponse(
                    request_id=req.request_id,
                    providing_module=provider["module"],
                    success=True,
                    result=result if isinstance(result, dict) else {"data": result},
                )
            except Exception as e:
                resp = SubcontractResponse(
                    request_id=req.request_id,
                    providing_module=provider["module"],
                    success=False,
                    result={"error": str(e)},
                )
        else:
            resp = SubcontractResponse(
                request_id=req.request_id,
                providing_module=provider["module"],
                success=False,
                result={"error": "Provider registered but no handler attached"},
            )

        self._response_log.append(resp)
        return resp

    def get_missing_capabilities(
        self, required: Set[ModuleCapability]
    ) -> Set[ModuleCapability]:
        """Find capabilities that are required but have no provider."""
        return {
            cap for cap in required
            if not self.has_provider(cap)
        }

    def get_audit_log(self) -> Dict[str, Any]:
        """Export the full request/response log."""
        return {
            "providers": {
                cap.value: [p["module"] for p in providers]
                for cap, providers in self._providers.items()
            },
            "total_requests": len(self._request_log),
            "total_responses": len(self._response_log),
            "failed_requests": sum(
                1 for r in self._response_log if not r.success
            ),
        }


# ---------------------------------------------------------------------------
# Demonstration > Declaration (Community Improvement #4)
# ---------------------------------------------------------------------------

@dataclass
class SafetyClaim:
    """
    A safety claim that must be backed by evidence.

    Community improvement #4: "Demonstration > declaration as
    explicit design principle."

    Every safety claim must point to a test, log artifact, or
    reproducible evidence — never just a docstring assertion.
    """
    claim_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    claim: str = ""               # What is being claimed
    module: str = ""              # Which module makes this claim
    evidence_type: str = ""       # "test", "log", "artifact", "metric"
    evidence_ref: str = ""        # Test name, log path, artifact ID
    verified: bool = False        # Has the evidence been checked?
    verified_at: str = ""
    verified_by: str = ""         # "automated_test", "human_reviewer"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "claim": self.claim,
            "module": self.module,
            "evidence_type": self.evidence_type,
            "evidence_ref": self.evidence_ref,
            "verified": self.verified,
        }


class SafetyClaimRegistry:
    """
    Tracks all safety claims and their evidence.
    Unverified claims are prominently flagged.
    """

    def __init__(self):
        self._claims: List[SafetyClaim] = []

    @property
    def claims(self) -> List[SafetyClaim]:
        return list(self._claims)

    @property
    def unverified_claims(self) -> List[SafetyClaim]:
        return [c for c in self._claims if not c.verified]

    def register_claim(
        self,
        claim: str,
        module: str,
        evidence_type: str = "",
        evidence_ref: str = "",
    ) -> SafetyClaim:
        """Register a safety claim."""
        sc = SafetyClaim(
            claim=claim,
            module=module,
            evidence_type=evidence_type,
            evidence_ref=evidence_ref,
            verified=bool(evidence_type and evidence_ref),
        )
        if sc.verified:
            sc.verified_at = datetime.utcnow().isoformat() + "Z"
            sc.verified_by = "automated_registration"
        self._claims.append(sc)
        return sc

    def verify_claim(
        self,
        claim_id: str,
        evidence_type: str,
        evidence_ref: str,
        verified_by: str = "automated_test",
    ) -> bool:
        """Attach evidence to a claim, marking it verified."""
        for c in self._claims:
            if c.claim_id == claim_id:
                c.evidence_type = evidence_type
                c.evidence_ref = evidence_ref
                c.verified = True
                c.verified_at = datetime.utcnow().isoformat() + "Z"
                c.verified_by = verified_by
                return True
        return False

    def get_coverage_report(self) -> Dict[str, Any]:
        """Report on claim verification coverage."""
        total = len(self._claims)
        verified = sum(1 for c in self._claims if c.verified)
        return {
            "total_claims": total,
            "verified_claims": verified,
            "unverified_claims": total - verified,
            "coverage_pct": (verified / total * 100) if total > 0 else 100.0,
            "unverified": [c.to_dict() for c in self.unverified_claims],
        }


# ---------------------------------------------------------------------------
# Healthcare Compliance Adapter (Community Improvement #1)
# ---------------------------------------------------------------------------

class RegulatoryFramework(Enum):
    """Supported regulatory frameworks."""
    MDR = "EU_MDR_2017_745"           # EU Medical Device Regulation
    AIMD = "EU_AiMD"                  # AI as Medical Device
    ISO_14971 = "ISO_14971_2019"      # Risk management for medical devices
    IEC_62304 = "IEC_62304_2006"      # Software lifecycle for medical devices
    FDA_SaMD = "FDA_SaMD"             # Software as Medical Device (US)
    ISO_13485 = "ISO_13485_2016"      # Quality management for medical devices


@dataclass
class RegulatoryMapping:
    """Maps a PBHP concept to a regulatory requirement."""
    pbhp_module: str = ""
    pbhp_concept: str = ""           # e.g., "risk_class", "harm_assessment"
    regulatory_framework: str = ""    # e.g., "ISO_14971_2019"
    regulatory_clause: str = ""       # e.g., "Clause 5.4"
    regulatory_requirement: str = ""  # What the regulation requires
    pbhp_satisfies: bool = False      # Does PBHP meet this requirement?
    gap_description: str = ""         # If not, what's missing?
    evidence_ref: str = ""            # Test or artifact that proves compliance

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pbhp_module": self.pbhp_module,
            "pbhp_concept": self.pbhp_concept,
            "framework": self.regulatory_framework,
            "clause": self.regulatory_clause,
            "requirement": self.regulatory_requirement,
            "satisfied": self.pbhp_satisfies,
            "gap": self.gap_description,
            "evidence": self.evidence_ref,
        }


class HealthcareComplianceAdapter:
    """
    Adapter for mapping PBHP outputs to healthcare regulatory requirements.

    Community improvement #1: "Healthcare compliance gap (MDR/AiMD/ISO 14971)."

    This provides a mapping layer so medical-device teams can use PBHP
    without building a separate compliance layer. Maps PBHP triage outputs
    to IEC 62304 software-lifecycle artifacts and ISO 14971 risk-management
    structures.

    NOTE: This is a structural skeleton. Full regulatory mapping requires
    domain expert review — PBHP cannot self-certify compliance.
    """

    def __init__(self):
        self._mappings: List[RegulatoryMapping] = []
        self._load_default_mappings()

    @property
    def mappings(self) -> List[RegulatoryMapping]:
        return list(self._mappings)

    def _load_default_mappings(self) -> None:
        """Load the default PBHP → regulatory mappings."""
        # ISO 14971: Risk Management
        self._mappings.extend([
            RegulatoryMapping(
                pbhp_module="pbhp_core",
                pbhp_concept="risk_class (GREEN/YELLOW/ORANGE/RED/BLACK)",
                regulatory_framework=RegulatoryFramework.ISO_14971.value,
                regulatory_clause="Clause 5.4 — Risk estimation",
                regulatory_requirement="Estimate risk for each identified hazard",
                pbhp_satisfies=True,
                evidence_ref="pbhp_core.PBHPEngine.classify_risk()",
            ),
            RegulatoryMapping(
                pbhp_module="pbhp_core",
                pbhp_concept="harm (impact_level, likelihood)",
                regulatory_framework=RegulatoryFramework.ISO_14971.value,
                regulatory_clause="Clause 5.5 — Risk evaluation",
                regulatory_requirement="Determine acceptability of each risk",
                pbhp_satisfies=True,
                evidence_ref="pbhp_core.Harm + GateAction",
            ),
            RegulatoryMapping(
                pbhp_module="pbhp_core",
                pbhp_concept="alternatives assessment",
                regulatory_framework=RegulatoryFramework.ISO_14971.value,
                regulatory_clause="Clause 6 — Risk control option analysis",
                regulatory_requirement="Identify and evaluate risk control measures",
                pbhp_satisfies=True,
                evidence_ref="pbhp_core.Alternative dataclass",
            ),
            RegulatoryMapping(
                pbhp_module="pbhp_drift",
                pbhp_concept="drift monitoring",
                regulatory_framework=RegulatoryFramework.ISO_14971.value,
                regulatory_clause="Clause 9 — Production and post-production",
                regulatory_requirement="Monitor device in post-production phase",
                pbhp_satisfies=True,
                evidence_ref="pbhp_drift.DriftMonitor",
            ),
            RegulatoryMapping(
                pbhp_module="pbhp_core",
                pbhp_concept="PBHPLog audit trail",
                regulatory_framework=RegulatoryFramework.ISO_14971.value,
                regulatory_clause="Clause 3.5 — Risk management file",
                regulatory_requirement="Maintain risk management file with traceability",
                pbhp_satisfies=True,
                evidence_ref="pbhp_core.PBHPLog.to_dict()",
            ),

            # IEC 62304: Software Lifecycle — gaps identified
            RegulatoryMapping(
                pbhp_module="pbhp_core",
                pbhp_concept="(gap) software safety classification",
                regulatory_framework=RegulatoryFramework.IEC_62304.value,
                regulatory_clause="Clause 4.3 — Software safety classification",
                regulatory_requirement="Classify software into Class A/B/C based on hazard",
                pbhp_satisfies=False,
                gap_description=(
                    "PBHP risk classes (GREEN-BLACK) do not directly map to "
                    "IEC 62304 Class A/B/C. Need explicit mapping layer."
                ),
            ),
            RegulatoryMapping(
                pbhp_module="pbhp_qs",
                pbhp_concept="evidence_vault + CAPA lifecycle",
                regulatory_framework=RegulatoryFramework.IEC_62304.value,
                regulatory_clause="Clause 6 — Software maintenance",
                regulatory_requirement="Problem resolution and change management",
                pbhp_satisfies=True,
                evidence_ref="pbhp_qs.CAPAManager + EvidenceVault",
            ),

            # MDR: EU Medical Device Regulation
            RegulatoryMapping(
                pbhp_module="pbhp_core",
                pbhp_concept="(gap) clinical evaluation",
                regulatory_framework=RegulatoryFramework.MDR.value,
                regulatory_clause="Article 61 — Clinical evaluation",
                regulatory_requirement="Clinical evaluation throughout product lifecycle",
                pbhp_satisfies=False,
                gap_description=(
                    "PBHP does not perform clinical evaluation. This requires "
                    "domain-specific clinical data that PBHP cannot generate. "
                    "Teams must conduct clinical evaluation separately."
                ),
            ),
            RegulatoryMapping(
                pbhp_module="pbhp_srl",
                pbhp_concept="state machine + incident recording",
                regulatory_framework=RegulatoryFramework.MDR.value,
                regulatory_clause="Article 87 — Vigilance reporting",
                regulatory_requirement="Report serious incidents to authorities",
                pbhp_satisfies=True,
                evidence_ref="pbhp_srl.IncidentRecorder + SRLStateMachine",
            ),
        ])

    def get_framework_mappings(
        self, framework: RegulatoryFramework
    ) -> List[RegulatoryMapping]:
        """Get all mappings for a specific regulatory framework."""
        return [
            m for m in self._mappings
            if m.regulatory_framework == framework.value
        ]

    def get_gaps(self) -> List[RegulatoryMapping]:
        """Get all mappings where PBHP has a compliance gap."""
        return [m for m in self._mappings if not m.pbhp_satisfies]

    def get_satisfied(self) -> List[RegulatoryMapping]:
        """Get all mappings that PBHP satisfies."""
        return [m for m in self._mappings if m.pbhp_satisfies]

    def add_mapping(self, mapping: RegulatoryMapping) -> None:
        """Add a custom regulatory mapping."""
        self._mappings.append(mapping)

    def export_compliance_matrix(self) -> Dict[str, Any]:
        """Export full compliance matrix for audit."""
        frameworks = set(m.regulatory_framework for m in self._mappings)
        matrix = {}
        for fw in frameworks:
            fw_mappings = [
                m for m in self._mappings
                if m.regulatory_framework == fw
            ]
            matrix[fw] = {
                "total_requirements": len(fw_mappings),
                "satisfied": sum(1 for m in fw_mappings if m.pbhp_satisfies),
                "gaps": sum(1 for m in fw_mappings if not m.pbhp_satisfies),
                "mappings": [m.to_dict() for m in fw_mappings],
            }
        return matrix

    def generate_coverage_gaps(
        self, collector: CoverageGapCollector
    ) -> None:
        """Feed compliance gaps into the coverage gap collector."""
        for m in self.get_gaps():
            collector.report(
                module=m.pbhp_module,
                description=(
                    f"Regulatory gap: {m.regulatory_framework} "
                    f"{m.regulatory_clause} — {m.gap_description}"
                ),
                severity=GapSeverity.WARNING,
                affected_rules=[m.regulatory_clause],
                mitigation=f"Manual compliance review needed for {m.regulatory_clause}",
            )


# ---------------------------------------------------------------------------
# MBSE Requirement Taxonomy Interface (Community Improvement #2)
# ---------------------------------------------------------------------------

@dataclass
class RequirementMapping:
    """Maps a PBHP output to an MBSE requirement."""
    pbhp_output: str = ""           # e.g., "risk_class=RED"
    requirement_id: str = ""         # e.g., "SYS-REQ-042"
    requirement_text: str = ""
    taxonomy: str = ""               # "SysML", "DOORS", "ReqIF"
    satisfaction_status: str = ""    # "satisfied", "partial", "not_satisfied"
    trace_link: str = ""             # URL or path to requirement in MBSE tool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pbhp_output": self.pbhp_output,
            "requirement_id": self.requirement_id,
            "requirement_text": self.requirement_text,
            "taxonomy": self.taxonomy,
            "satisfaction_status": self.satisfaction_status,
            "trace_link": self.trace_link,
        }


class MBSEInterface:
    """
    Interface for mapping PBHP triage outputs to MBSE requirement taxonomies.

    Community improvement #2: "Triage should plug into existing MBSE
    requirement taxonomies."

    This is a data interface — actual integration with SysML/DOORS/ReqIF
    requires tool-specific adapters that extend this class.
    """

    def __init__(self, taxonomy: str = "generic"):
        self.taxonomy = taxonomy
        self._mappings: List[RequirementMapping] = []

    def add_mapping(
        self,
        pbhp_output: str,
        requirement_id: str,
        requirement_text: str,
        satisfaction_status: str = "not_assessed",
        trace_link: str = "",
    ) -> RequirementMapping:
        """Add a PBHP → requirement mapping."""
        m = RequirementMapping(
            pbhp_output=pbhp_output,
            requirement_id=requirement_id,
            requirement_text=requirement_text,
            taxonomy=self.taxonomy,
            satisfaction_status=satisfaction_status,
            trace_link=trace_link,
        )
        self._mappings.append(m)
        return m

    def get_unsatisfied(self) -> List[RequirementMapping]:
        """Get requirements not yet satisfied by PBHP outputs."""
        return [
            m for m in self._mappings
            if m.satisfaction_status not in ("satisfied",)
        ]

    def export_traceability(self) -> Dict[str, Any]:
        """Export traceability matrix."""
        return {
            "taxonomy": self.taxonomy,
            "total_mappings": len(self._mappings),
            "satisfied": sum(
                1 for m in self._mappings
                if m.satisfaction_status == "satisfied"
            ),
            "mappings": [m.to_dict() for m in self._mappings],
        }
