"""
Pause-Before-Harm Protocol (PBHP) v0.9.5 — Compliance Crosswalks
Compliance Framework Mappings and Validation

Maps PBHP artifacts and decision steps to compliance requirements in:
  - NIST AI Risk Management Framework (AI RMF)
  - ISO/IEC 42001 (AI Management System)
  - ISO/IEC 23894 (AI Risks and Impacts)
  - EU AI Act

Shows which PBHP step/artifact satisfies which compliance requirement.
Enables compliance audit and certification tracking.

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set
from datetime import datetime


class ComplianceFramework(Enum):
    """Supported compliance frameworks."""
    NIST_AI_RMF = "nist_ai_rmf"
    ISO_42001 = "iso_42001"
    ISO_23894 = "iso_23894"
    EU_AI_ACT = "eu_ai_act"


@dataclass
class ComplianceRequirement:
    """A single compliance requirement."""
    framework: ComplianceFramework
    requirement_id: str
    """e.g., 'NIST.MAP-1.1', 'ISO42001.A.5.2', 'EU_AI_ACT.8.1'."""

    requirement_title: str
    """Short title of the requirement."""

    requirement_text: str
    """Full text of the requirement."""

    pbhp_satisfying_steps: List[str]
    """Which PBHP steps satisfy this (e.g., ['Step 2', 'Step 3a', 'Step 5'])."""

    pbhp_artifacts_satisfying: List[str]
    """Which PBHP artifacts satisfy this (e.g., ['Harm assessment', 'Door analysis'])."""

    evidence_checklist: List[str]
    """Checklist of evidence types that satisfy the requirement."""

    verification_method: str
    """How to verify compliance (audit, testing, documentation review, etc.)."""

    applicable_to_domains: List[str] = field(default_factory=list)
    """Which domains need this (empty = universal)."""


@dataclass
class PBHPArtifact:
    """An artifact produced by PBHP."""
    name: str
    """Artifact name (e.g., 'Risk Assessment Report')."""

    pbhp_step: str
    """Which PBHP step produces this (e.g., 'Step 2')."""

    content_description: str
    """What the artifact contains."""

    serves_compliance_requirements: List[str] = field(default_factory=list)
    """Requirement IDs this artifact helps satisfy (e.g., ['NIST.MAP-1.1', 'ISO42001.A.5.2'])."""


@dataclass
class ComplianceAuditReport:
    """Report showing PBHP compliance with frameworks."""
    audit_date: datetime
    """When this audit was performed."""

    organization: str
    """Organization being audited."""

    frameworks_audited: List[ComplianceFramework]
    """Which frameworks were evaluated."""

    requirement_coverage: Dict[str, bool]
    """Map of requirement_id → satisfied (True/False)."""

    satisfied_count: int
    """Number of satisfied requirements."""

    unsatisfied_count: int
    """Number of unsatisfied requirements."""

    gaps: List[str] = field(default_factory=list)
    """Missing requirements or evidence."""

    recommendations: List[str] = field(default_factory=list)
    """Recommendations to close gaps."""

    artifacts_collected: List[str] = field(default_factory=list)
    """PBHP artifacts collected as evidence."""


# ===========================================================================
# NIST AI Risk Management Framework (Govern, Map, Measure, Manage)
# ===========================================================================

NIST_REQUIREMENTS = [
    ComplianceRequirement(
        framework=ComplianceFramework.NIST_AI_RMF,
        requirement_id="NIST.GOVERN-1.1",
        requirement_title="Establish AI governance structure",
        requirement_text="Organization has defined roles, responsibilities, and oversight for AI systems.",
        pbhp_satisfying_steps=["Step 0a", "Step 0b", "Step 0c"],
        pbhp_artifacts_satisfying=["PBHP Context Assessment", "Epistemic Mode Assignment"],
        evidence_checklist=[
            "PBHP decision flowchart documented",
            "Escalation procedures defined",
            "PBHP tier assignment methodology",
        ],
        verification_method="Documentation review and policy audit",
    ),
    ComplianceRequirement(
        framework=ComplianceFramework.NIST_AI_RMF,
        requirement_id="NIST.MAP-1.1",
        requirement_title="Map AI system inputs, processes, and outputs",
        requirement_text="Risk mapping captures data flow, model logic, and decision outputs.",
        pbhp_satisfying_steps=["Step 1", "Step 2"],
        pbhp_artifacts_satisfying=["Decision Context", "Harm Identification Report"],
        evidence_checklist=[
            "Input data sources documented",
            "Processing logic explained",
            "Output decision rules specified",
            "Stakeholder impact mapping",
        ],
        verification_method="System architecture documentation review",
    ),
    ComplianceRequirement(
        framework=ComplianceFramework.NIST_AI_RMF,
        requirement_id="NIST.MAP-2.1",
        requirement_title="Identify foreseeable harms and risks",
        requirement_text="Comprehensive identification of potential negative outcomes.",
        pbhp_satisfying_steps=["Step 2", "Step 3a", "Step 3b"],
        pbhp_artifacts_satisfying=["Harm Assessment", "Red Team Review Notes"],
        evidence_checklist=[
            "Harm categories enumerated",
            "Vulnerable populations identified",
            "Irreversibility analysis",
            "Amplification vectors mapped",
        ],
        verification_method="Harm assessment review with domain experts",
    ),
    ComplianceRequirement(
        framework=ComplianceFramework.NIST_AI_RMF,
        requirement_id="NIST.MEASURE-1.1",
        requirement_title="Establish performance metrics and baselines",
        requirement_text="Quantifiable metrics track AI system performance and fairness.",
        pbhp_satisfying_steps=["Step 4", "Step 6"],
        pbhp_artifacts_satisfying=["PBHP Assessment Result", "Metrics Tracking Log"],
        evidence_checklist=[
            "Performance metrics defined",
            "Fairness/bias metrics tracked",
            "Drift detection enabled",
            "Baseline established",
        ],
        verification_method="Metrics dashboard review and historical tracking",
    ),
    ComplianceRequirement(
        framework=ComplianceFramework.NIST_AI_RMF,
        requirement_id="NIST.MANAGE-1.1",
        requirement_title="Implement risk mitigation and safeguards",
        requirement_text="Documented controls reduce identified risks to acceptable levels.",
        pbhp_satisfying_steps=["Step 3c", "Step 5"],
        pbhp_artifacts_satisfying=["Door/Wall/Gap Analysis", "Mitigation Plan"],
        evidence_checklist=[
            "Safeguards implemented per gate",
            "Rollback procedures in place",
            "Escalation procedures tested",
            "User consent mechanisms verified",
        ],
        verification_method="Control testing and incident log review",
    ),
]


# ===========================================================================
# ISO/IEC 42001 (AI Management System)
# ===========================================================================

ISO_42001_REQUIREMENTS = [
    ComplianceRequirement(
        framework=ComplianceFramework.ISO_42001,
        requirement_id="ISO42001.A.5.2",
        requirement_title="AI risk assessment process",
        requirement_text="Organization has documented AI risk assessment methodology.",
        pbhp_satisfying_steps=["Step 0a", "Step 0b", "Step 1", "Step 2"],
        pbhp_artifacts_satisfying=["PBHP Framework", "Risk Assessment"],
        evidence_checklist=[
            "PBHP methodology documented",
            "Risk tiers defined (MIN/CORE/ULTRA)",
            "Assessment templates provided",
        ],
        verification_method="Process documentation audit",
    ),
    ComplianceRequirement(
        framework=ComplianceFramework.ISO_42001,
        requirement_id="ISO42001.A.6.1",
        requirement_title="Monitoring and measurement of AI controls",
        requirement_text="Continual monitoring of effectiveness of risk controls.",
        pbhp_satisfying_steps=["Step 6", "Step 7"],
        pbhp_artifacts_satisfying=["Drift Detection Report", "Feedback Loop Documentation"],
        evidence_checklist=[
            "Monitoring plan documented",
            "Alerts configured",
            "Review cadence established",
            "Historical data collected",
        ],
        verification_method="Monitoring system validation",
    ),
    ComplianceRequirement(
        framework=ComplianceFramework.ISO_42001,
        requirement_id="ISO42001.A.7.1",
        requirement_title="Document management for AI systems",
        requirement_text="Maintain documentation of AI system lifecycle and decisions.",
        pbhp_satisfying_steps=["Step 1", "Step 4", "Step 5", "Step 6"],
        pbhp_artifacts_satisfying=["All PBHP artifacts"],
        evidence_checklist=[
            "PBHP logs retained (audit trail)",
            "Decision rationales documented",
            "Version control of model/rules",
            "Change log maintained",
        ],
        verification_method="Documentation repository audit",
    ),
]


# ===========================================================================
# ISO/IEC 23894 (AI Risks and Impacts)
# ===========================================================================

ISO_23894_REQUIREMENTS = [
    ComplianceRequirement(
        framework=ComplianceFramework.ISO_23894,
        requirement_id="ISO23894.5.1",
        requirement_title="Identify AI lifecycle stages and risk points",
        requirement_text="Map which lifecycle stages carry highest risk.",
        pbhp_satisfying_steps=["Step 0", "Step 1", "Step 2", "Step 3"],
        pbhp_artifacts_satisfying=["Epistemic Mode Assignment", "Harm Assessment"],
        evidence_checklist=[
            "Lifecycle stages mapped",
            "Risk hotspots identified",
            "Gate assignments justified",
        ],
        verification_method="Lifecycle risk map review",
    ),
    ComplianceRequirement(
        framework=ComplianceFramework.ISO_23894,
        requirement_id="ISO23894.5.2",
        requirement_title="Assess impact on vulnerable populations",
        requirement_text="Explicit analysis of disproportionate harm to vulnerable groups.",
        pbhp_satisfying_steps=["Step 0g", "Step 2", "Step 3a"],
        pbhp_artifacts_satisfying=["Vulnerable Population Assessment", "Harm Assessment"],
        evidence_checklist=[
            "Vulnerable groups defined",
            "Disproportionate impact analyzed",
            "Mitigation for vulnerable groups",
        ],
        verification_method="Fairness audit with inclusion specialists",
    ),
    ComplianceRequirement(
        framework=ComplianceFramework.ISO_23894,
        requirement_id="ISO23894.6.1",
        requirement_title="Establish risk acceptability criteria",
        requirement_text="Document what harm levels are acceptable for the organization.",
        pbhp_satisfying_steps=["Step 0", "Step 4"],
        pbhp_artifacts_satisfying=["PBHP Framework", "Risk Class Thresholds"],
        evidence_checklist=[
            "Acceptability levels defined per domain",
            "Gate thresholds published",
            "Stakeholder input on acceptability",
        ],
        verification_method="Policy document and stakeholder consultation review",
    ),
]


# ===========================================================================
# EU AI Act (Articles on High-Risk AI Systems)
# ===========================================================================

EU_AI_ACT_REQUIREMENTS = [
    ComplianceRequirement(
        framework=ComplianceFramework.EU_AI_ACT,
        requirement_id="EU_AI_ACT.6.1",
        requirement_title="High-risk AI systems require risk assessment",
        requirement_text="High-risk AI must undergo documented conformity assessment.",
        pbhp_satisfying_steps=["Step 0", "Step 1", "Step 2", "Step 3", "Step 4"],
        pbhp_artifacts_satisfying=["Full PBHP Assessment Report"],
        evidence_checklist=[
            "Risk assessment performed",
            "High-risk determination documented",
            "Conformity evidence collected",
        ],
        verification_method="Notified Body or internal audit",
        applicable_to_domains=["hiring", "healthcare", "finance"],
    ),
    ComplianceRequirement(
        framework=ComplianceFramework.EU_AI_ACT,
        requirement_id="EU_AI_ACT.8.1",
        requirement_title="Transparency and human oversight requirements",
        requirement_text="High-risk AI must enable human understanding and intervention.",
        pbhp_satisfying_steps=["Step 3c", "Step 5"],
        pbhp_artifacts_satisfying=["Door/Wall/Gap Analysis", "Mitigation Plan"],
        evidence_checklist=[
            "Explainability documentation",
            "Human override capability",
            "Logging of decisions enabled",
        ],
        verification_method="System functionality testing",
    ),
    ComplianceRequirement(
        framework=ComplianceFramework.EU_AI_ACT,
        requirement_id="EU_AI_ACT.10.1",
        requirement_title="Data governance and quality requirements",
        requirement_text="High-risk AI training data must be documented and governed.",
        pbhp_satisfying_steps=["Step 0a", "Step 1"],
        pbhp_artifacts_satisfying=["Decision Context", "Data Inventory"],
        evidence_checklist=[
            "Training data sources documented",
            "Data quality assessment",
            "Bias and fairness analysis of data",
        ],
        verification_method="Data governance audit",
    ),
]


# ===========================================================================
# PBHP Artifacts (what PBHP produces)
# ===========================================================================

PBHP_ARTIFACTS_CATALOG = [
    PBHPArtifact(
        name="PBHP Assessment Result",
        pbhp_step="Step 4",
        content_description="Final risk gate (GREEN/YELLOW/ORANGE/RED/BLACK) and recommended action",
        serves_compliance_requirements=["NIST.MAP-1.1", "NIST.MEASURE-1.1", "ISO42001.A.5.2"],
    ),
    PBHPArtifact(
        name="Harm Assessment Report",
        pbhp_step="Step 2",
        content_description="Enumeration of potential harms with impact/likelihood/irreversibility analysis",
        serves_compliance_requirements=["NIST.MAP-2.1", "ISO23894.5.1", "EU_AI_ACT.6.1"],
    ),
    PBHPArtifact(
        name="Door/Wall/Gap Analysis",
        pbhp_step="Step 3c",
        content_description="Escape vector analysis and mitigation feasibility",
        serves_compliance_requirements=["NIST.MANAGE-1.1", "EU_AI_ACT.8.1"],
    ),
    PBHPArtifact(
        name="Red Team Review Notes",
        pbhp_step="Step 3b",
        content_description="Challenge and alternative framings from red team",
        serves_compliance_requirements=["NIST.MAP-2.1", "ISO23894.5.2"],
    ),
    PBHPArtifact(
        name="Drift Detection Report",
        pbhp_step="Step 6",
        content_description="Decision pattern changes and alarm triggers",
        serves_compliance_requirements=["NIST.MEASURE-1.1", "ISO42001.A.6.1"],
    ),
    PBHPArtifact(
        name="PBHP Decision Log",
        pbhp_step="All",
        content_description="Audit trail of all PBHP gates and outcomes",
        serves_compliance_requirements=["ISO42001.A.7.1", "EU_AI_ACT.8.1"],
    ),
]


# ===========================================================================
# Compliance Mapping and Reporting
# ===========================================================================

ALL_REQUIREMENTS = NIST_REQUIREMENTS + ISO_42001_REQUIREMENTS + ISO_23894_REQUIREMENTS + EU_AI_ACT_REQUIREMENTS


class ComplianceMapper:
    """Maps PBHP implementation to compliance requirements."""

    def __init__(self):
        """Initialize the mapper with all requirements."""
        self.requirements = ALL_REQUIREMENTS
        self.artifacts = PBHP_ARTIFACTS_CATALOG

    def get_requirements_for_framework(self,
                                      framework: ComplianceFramework) -> List[ComplianceRequirement]:
        """Get all requirements for a specific framework."""
        return [r for r in self.requirements if r.framework == framework]

    def get_requirements_by_pbhp_step(self, pbhp_step: str) -> List[ComplianceRequirement]:
        """Get all requirements satisfied by a specific PBHP step."""
        return [r for r in self.requirements if pbhp_step in r.pbhp_satisfying_steps]

    def get_artifacts_for_step(self, pbhp_step: str) -> List[PBHPArtifact]:
        """Get artifacts produced by a specific PBHP step."""
        return [a for a in self.artifacts if a.pbhp_step == pbhp_step]

    def generate_compliance_checklist(self,
                                     framework: ComplianceFramework) -> Dict[str, Dict]:
        """Generate compliance checklist for a framework."""
        requirements = self.get_requirements_for_framework(framework)
        checklist = {}

        for req in requirements:
            checklist[req.requirement_id] = {
                "title": req.requirement_title,
                "satisfied": False,
                "evidence_needed": req.evidence_checklist,
                "pbhp_steps": req.pbhp_satisfying_steps,
                "pbhp_artifacts": req.pbhp_artifacts_satisfying,
            }

        return checklist

    def generate_audit_report(self,
                             organization: str,
                             frameworks: List[ComplianceFramework],
                             satisfied_requirements: Set[str],
                             collected_artifacts: List[str]) -> ComplianceAuditReport:
        """Generate a compliance audit report."""
        all_requirements = []
        for fw in frameworks:
            all_requirements.extend(self.get_requirements_for_framework(fw))

        satisfied = sum(1 for r in all_requirements if r.requirement_id in satisfied_requirements)
        unsatisfied = len(all_requirements) - satisfied

        gaps = [r.requirement_id for r in all_requirements
               if r.requirement_id not in satisfied_requirements]

        recommendations = [
            f"Collect evidence for: {', '.join(gaps[:3])}" if gaps else "All requirements satisfied",
        ]

        return ComplianceAuditReport(
            audit_date=datetime.now(),
            organization=organization,
            frameworks_audited=frameworks,
            requirement_coverage={r.requirement_id: r.requirement_id in satisfied_requirements
                                 for r in all_requirements},
            satisfied_count=satisfied,
            unsatisfied_count=unsatisfied,
            gaps=gaps,
            recommendations=recommendations,
            artifacts_collected=collected_artifacts,
        )


# Convenience function
def audit_pbhp_compliance(organization: str,
                         frameworks: List[ComplianceFramework],
                         satisfied_requirements: Set[str],
                         collected_artifacts: List[str]) -> ComplianceAuditReport:
    """
    Quick entry point for compliance auditing.

    Usage:
        report = audit_pbhp_compliance(
            organization="MyCompany",
            frameworks=[ComplianceFramework.NIST_AI_RMF, ComplianceFramework.ISO_42001],
            satisfied_requirements={"NIST.MAP-1.1", "ISO42001.A.5.2"},
            collected_artifacts=["PBHP Assessment Result", "Harm Assessment Report"],
        )
        print(f"Satisfied: {report.satisfied_count}/{report.satisfied_count + report.unsatisfied_count}")
    """
    mapper = ComplianceMapper()
    return mapper.generate_audit_report(organization, frameworks,
                                       satisfied_requirements, collected_artifacts)
