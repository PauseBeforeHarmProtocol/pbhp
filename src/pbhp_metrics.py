"""
Pause-Before-Harm Protocol (PBHP) v0.8.0 — Metrics Packs
Standardized Harm Metric Packs for Domain-Specific Assessment

Provides pre-built severity metric templates for common application domains:
  - Hiring & Recruitment
  - Healthcare & Medical
  - Finance & Banking
  - Content Moderation
  - Security & Authentication

Each metric pack defines:
  - Severity level thresholds (trivial → catastrophic)
  - Reversibility definitions by domain
  - Affected stakeholder templates ("who pays first")
  - Domain-specific vulnerability indicators

Enables consistent risk scoring across different systems.

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

import sys
sys.path.insert(0, '/sessions/happy-charming-bohr/pbhp_repo/src')

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from pbhp_core import ImpactLevel, LikelihoodLevel


@dataclass
class SeverityThreshold:
    """Concrete threshold definition for a severity level in a domain."""
    level: ImpactLevel
    description: str
    """Clear description of what this level means in domain context."""

    metric_example: str
    """Concrete example that qualifies for this level."""

    quantitative_indicator: Optional[str] = None
    """Measurable indicator (e.g., '> 1000 users affected')."""

    lower_bound: Optional[float] = None
    """Numeric lower bound if applicable."""

    upper_bound: Optional[float] = None
    """Numeric upper bound if applicable."""


@dataclass
class ReversibilityDefinition:
    """Domain-specific reversibility standards."""
    is_reversible: bool
    """Whether harm can be undone."""

    reversal_timeframe: str
    """How long reversal takes ('immediate', 'days', 'weeks', 'months', 'years', 'never')."""

    reversal_mechanism: str
    """How reversal would actually occur."""

    reversal_cost_factor: float
    """Relative cost multiplier to reverse (1.0 = same cost as original harm)."""

    downstream_irreversibility: bool
    """Are there downstream effects that become irreversible?"""


@dataclass
class StakeholderTemplate:
    """Template defining who bears costs first in a specific domain."""
    role: str
    """Stakeholder role (e.g., 'job applicant', 'patient', 'account holder')."""

    power_relative_to_decision_maker: str
    """'minimal', 'low', 'moderate', 'high' relative power/agency."""

    primary_harm_types: List[str]
    """Harm types this stakeholder typically experiences first."""

    vulnerability_flags: List[str]
    """Flags that indicate elevated vulnerability (e.g., 'non-fluent_language', 'disability')."""

    consent_capability: str
    """Can they consent? 'yes', 'partially', 'no' (no = child, unconscious, etc.)."""


@dataclass
class MetricPack:
    """Complete metric pack for a domain."""
    domain: str
    """Domain name (e.g., 'hiring', 'healthcare')."""

    version: str = "1.0"
    """Metric pack version."""

    severity_thresholds: List[SeverityThreshold] = field(default_factory=list)
    """Severity levels with concrete thresholds."""

    reversibility_standards: Dict[str, ReversibilityDefinition] = field(default_factory=dict)
    """Reversibility definitions keyed by harm type."""

    stakeholder_templates: List[StakeholderTemplate] = field(default_factory=list)
    """Who bears costs first in this domain."""

    domain_specific_vulnerability_factors: List[str] = field(default_factory=list)
    """Domain-specific vulnerability indicators."""

    amplification_vectors: List[str] = field(default_factory=list)
    """How harms scale in this domain (e.g., 'algorithmic ranking', 'viral sharing')."""

    regulation_notes: str = ""
    """Relevant regulations or standards (HIPAA, GDPR, Fair Lending Act, etc.)."""


# ===========================================================================
# HIRING & RECRUITMENT
# ===========================================================================

HIRING_METRIC_PACK = MetricPack(
    domain="hiring",
    severity_thresholds=[
        SeverityThreshold(
            level=ImpactLevel.TRIVIAL,
            description="Minor feedback delay or formatting issue in application process",
            metric_example="Candidate receives feedback 1 day late",
        ),
        SeverityThreshold(
            level=ImpactLevel.MODERATE,
            description="Candidate disadvantaged in selection, but can reapply or receive explanation",
            metric_example="Qualified candidate filtered by flawed algorithm (1-10 candidates)",
            quantitative_indicator="1-10 candidates incorrectly filtered",
        ),
        SeverityThreshold(
            level=ImpactLevel.SEVERE,
            description="Systemic discrimination affecting protected class; career opportunity lost",
            metric_example="Gender-biased algorithm filters 50+ female applicants; reapplication unlikely",
            quantitative_indicator="> 50 candidates; protected class discrimination",
        ),
        SeverityThreshold(
            level=ImpactLevel.CATASTROPHIC,
            description="Mass-scale discrimination causing labor market harm; irreversible career damage",
            metric_example="Automated discrimination across entire hiring pipeline for thousands; reputation damage",
            quantitative_indicator="> 1000 candidates; protected class; public exposure",
        ),
    ],
    reversibility_standards={
        "missed_opportunity": ReversibilityDefinition(
            is_reversible=True,
            reversal_timeframe="days",
            reversal_mechanism="Re-run selection, offer candidate interview",
            reversal_cost_factor=0.5,
            downstream_irreversibility=False,
        ),
        "discrimination": ReversibilityDefinition(
            is_reversible=False,
            reversal_timeframe="never",
            reversal_mechanism="Cannot restore lost career trajectory",
            reversal_cost_factor=10.0,
            downstream_irreversibility=True,
        ),
    },
    stakeholder_templates=[
        StakeholderTemplate(
            role="job applicant",
            power_relative_to_decision_maker="minimal",
            primary_harm_types=["missed opportunity", "discrimination", "privacy breach"],
            vulnerability_flags=["protected class", "economic disadvantage", "language barrier"],
            consent_capability="yes",
        ),
        StakeholderTemplate(
            role="hired employee",
            power_relative_to_decision_maker="low",
            primary_harm_types=["unfair selection", "workplace culture impact"],
            vulnerability_flags=["minorities", "women in tech", "age-based"],
            consent_capability="yes",
        ),
    ],
    domain_specific_vulnerability_factors=[
        "protected_class_status",
        "first_generation_college_graduate",
        "long_unemployment_gap",
        "non_traditional_background",
    ],
    amplification_vectors=[
        "applies to entire applicant pool",
        "automated filtering at scale",
        "public exposure on social media",
        "viral discrimination cases",
    ],
    regulation_notes="Title VII (Civil Rights), EEOC guidance, state fair hiring laws, GDPR (EU applicants)",
)


# ===========================================================================
# HEALTHCARE & MEDICAL
# ===========================================================================

HEALTHCARE_METRIC_PACK = MetricPack(
    domain="healthcare",
    severity_thresholds=[
        SeverityThreshold(
            level=ImpactLevel.TRIVIAL,
            description="Minor inconvenience; patient care unaffected",
            metric_example="Appointment scheduling delay (<1 day)",
        ),
        SeverityThreshold(
            level=ImpactLevel.MODERATE,
            description="Treatment delay or non-emergency therapy affected",
            metric_example="Diagnostic imaging delayed 1-2 weeks; non-emergency condition",
            quantitative_indicator="Delay < 1 month; non-life-threatening",
        ),
        SeverityThreshold(
            level=ImpactLevel.SEVERE,
            description="Significant health impact; delayed emergency care or misdiagnosis",
            metric_example="Misdiagnosis causes treatable condition to worsen; hospitalization",
            quantitative_indicator="Health deterioration; multi-patient impact",
        ),
        SeverityThreshold(
            level=ImpactLevel.CATASTROPHIC,
            description="Death or permanent disability from diagnostic/treatment error",
            metric_example="AI algorithm misses cancer diagnosis in 100+ patients; deaths occur",
            quantitative_indicator="Deaths or permanent disabilities; systemic failure",
        ),
    ],
    reversibility_standards={
        "diagnostic_delay": ReversibilityDefinition(
            is_reversible=True,
            reversal_timeframe="days",
            reversal_mechanism="Correct diagnosis and immediate treatment",
            reversal_cost_factor=0.8,
            downstream_irreversibility=False,
        ),
        "misdiagnosis": ReversibilityDefinition(
            is_reversible=False,
            reversal_timeframe="never",
            reversal_mechanism="Cannot undo health damage from wrong treatment",
            reversal_cost_factor=100.0,
            downstream_irreversibility=True,
        ),
    },
    stakeholder_templates=[
        StakeholderTemplate(
            role="patient",
            power_relative_to_decision_maker="minimal",
            primary_harm_types=["misdiagnosis", "treatment delay", "privacy breach"],
            vulnerability_flags=["elderly", "mental illness", "low health literacy", "language barrier"],
            consent_capability="partially",  # varies by capacity
        ),
        StakeholderTemplate(
            role="vulnerable patient",
            power_relative_to_decision_maker="minimal",
            primary_harm_types=["exploitation", "inadequate care", "abuse"],
            vulnerability_flags=["unconscious", "dementia", "severe mental illness", "child"],
            consent_capability="no",
        ),
    ],
    domain_specific_vulnerability_factors=[
        "age_extremes",
        "cognitive_impairment",
        "language_barrier",
        "socioeconomic_disadvantage",
        "rare_disease",
    ],
    amplification_vectors=[
        "systemic algorithmic bias",
        "affects patient population at hospital/system scale",
        "compound errors across specialists",
        "public trust erosion",
    ],
    regulation_notes="HIPAA, FDA guidelines, state medical boards, JCI accreditation, GDPR (patient data)",
)


# ===========================================================================
# FINANCE & BANKING
# ===========================================================================

FINANCE_METRIC_PACK = MetricPack(
    domain="finance",
    severity_thresholds=[
        SeverityThreshold(
            level=ImpactLevel.TRIVIAL,
            description="Minor transaction fee or reconciliation delay",
            metric_example="Interest calculation off by $0.01",
            quantitative_indicator="< $100 per customer",
        ),
        SeverityThreshold(
            level=ImpactLevel.MODERATE,
            description="Account access issue or moderate financial loss",
            metric_example="Legitimate loan application rejected (1-10 applicants); can reapply",
            quantitative_indicator="$1000-$50,000 total impact",
        ),
        SeverityThreshold(
            level=ImpactLevel.SEVERE,
            description="Systematic lending discrimination or major financial loss",
            metric_example="Algorithmic redlining denies mortgages to 50+ minority applicants",
            quantitative_indicator="> $500K total; protected class impact",
        ),
        SeverityThreshold(
            level=ImpactLevel.CATASTROPHIC,
            description="Systemic financial fraud or catastrophic wealth destruction",
            metric_example="Automated trading flaw causes market instability; billions lost",
            quantitative_indicator="> $10M loss; systemic failure; regulatory intervention needed",
        ),
    ],
    reversibility_standards={
        "transaction_error": ReversibilityDefinition(
            is_reversible=True,
            reversal_timeframe="days",
            reversal_mechanism="Correct transaction, apply interest adjustment",
            reversal_cost_factor=0.2,
            downstream_irreversibility=False,
        ),
        "lending_discrimination": ReversibilityDefinition(
            is_reversible=False,
            reversal_timeframe="years",
            reversal_mechanism="Offer retroactive approval; cannot restore lost time value",
            reversal_cost_factor=5.0,
            downstream_irreversibility=True,
        ),
    },
    stakeholder_templates=[
        StakeholderTemplate(
            role="retail customer",
            power_relative_to_decision_maker="low",
            primary_harm_types=["fraud", "discrimination", "account freezing"],
            vulnerability_flags=["language barrier", "low financial literacy", "prior credit issues"],
            consent_capability="yes",
        ),
        StakeholderTemplate(
            role="underserved population",
            power_relative_to_decision_maker="minimal",
            primary_harm_types=["redlining", "predatory terms", "exclusion"],
            vulnerability_flags=["low income", "protected class", "rural location"],
            consent_capability="yes",
        ),
    ],
    domain_specific_vulnerability_factors=[
        "credit_score_algorithm_bias",
        "no_credit_history",
        "protected_class_status",
        "prior_financial_hardship",
        "disabled_or_elderly",
    ],
    amplification_vectors=[
        "automated lending at scale",
        "credit reporting cascade effects",
        "systemic discrimination across lenders",
        "market-wide trading algorithms",
    ],
    regulation_notes="Fair Lending Act, Equal Credit Opportunity Act (ECOA), Fair Housing Act, Dodd-Frank, GDPR",
)


# ===========================================================================
# CONTENT MODERATION
# ===========================================================================

CONTENT_MODERATION_PACK = MetricPack(
    domain="content_moderation",
    severity_thresholds=[
        SeverityThreshold(
            level=ImpactLevel.TRIVIAL,
            description="Single post incorrectly flagged; user notified; easily restored",
            metric_example="One harmless meme removed; user appeals in <1 hour",
        ),
        SeverityThreshold(
            level=ImpactLevel.MODERATE,
            description="Account temporarily restricted; free speech expression limited",
            metric_example="Creator account shadowbanned (1-100 followers affected)",
            quantitative_indicator="Account access restricted 1-7 days",
        ),
        SeverityThreshold(
            level=ImpactLevel.SEVERE,
            description="Permanent account suspension affecting influencer or vulnerable group",
            metric_example="Activist account permanently suspended; 10K+ followers; coordination lost",
            quantitative_indicator="Permanent suspension; >5K followers; marginalized group",
        ),
        SeverityThreshold(
            level=ImpactLevel.CATASTROPHIC,
            description="Coordinated silencing of political/marginalized speech at scale",
            metric_example="Systematic removal of protest organizing content; 100K+ accounts affected",
            quantitative_indicator="> 100K accounts; coordinated removal; political impact",
        ),
    ],
    reversibility_standards={
        "content_removal": ReversibilityDefinition(
            is_reversible=True,
            reversal_timeframe="hours",
            reversal_mechanism="Restore post; notify creator; provide appeal",
            reversal_cost_factor=0.5,
            downstream_irreversibility=False,
        ),
        "account_suspension": ReversibilityDefinition(
            is_reversible=False,
            reversal_timeframe="never",
            reversal_mechanism="Cannot restore lost followers, algorithm reach, or historical engagement",
            reversal_cost_factor=10.0,
            downstream_irreversibility=True,
        ),
    },
    stakeholder_templates=[
        StakeholderTemplate(
            role="content creator",
            power_relative_to_decision_maker="low",
            primary_harm_types=["visibility loss", "account suspension", "livelihood impact"],
            vulnerability_flags=["small following", "marginalized identity", "depends on platform revenue"],
            consent_capability="yes",
        ),
        StakeholderTemplate(
            role="activist/organizer",
            power_relative_to_decision_maker="minimal",
            primary_harm_types=["coordination disruption", "speech suppression", "movement fragmentation"],
            vulnerability_flags=["protesting government", "minority politics", "detained/vulnerable"],
            consent_capability="yes",
        ),
    ],
    domain_specific_vulnerability_factors=[
        "small_account_vs_platform",
        "marginalized_political_identity",
        "activist_coordination_impact",
        "algorithmic_amplification_dependency",
        "language_non_fluency",
    ],
    amplification_vectors=[
        "platform-wide policy enforcement",
        "viral misinformation removal cascades",
        "algorithmic shadowbanning",
        "coordinated moderation across platforms",
    ],
    regulation_notes="Section 230 (CDA), EU Digital Services Act, national hate speech laws, GDPR",
)


# ===========================================================================
# SECURITY & AUTHENTICATION
# ===========================================================================

SECURITY_METRIC_PACK = MetricPack(
    domain="security",
    severity_thresholds=[
        SeverityThreshold(
            level=ImpactLevel.TRIVIAL,
            description="Non-sensitive data exposed briefly; no action taken by attacker",
            metric_example="Debug logs containing no credentials exposed for 30 minutes",
        ),
        SeverityThreshold(
            level=ImpactLevel.MODERATE,
            description="Temporary account lockout or exposed non-critical credential",
            metric_example="User password hash leaked (salted); 100 users must reset",
            quantitative_indicator="100-1,000 users affected; non-sensitive data",
        ),
        SeverityThreshold(
            level=ImpactLevel.SEVERE,
            description="Widespread credential breach or identity theft exposure",
            metric_example="1M+ user emails and password hashes leaked; active exploitation ongoing",
            quantitative_indicator=">10K users; PII exposure; active use",
        ),
        SeverityThreshold(
            level=ImpactLevel.CATASTROPHIC,
            description="Nation-scale breach enabling systemic compromise or fraud",
            metric_example="US voting system authentication compromised; election integrity threatened",
            quantitative_indicator=">1M users; infrastructure threat; national security impact",
        ),
    ],
    reversibility_standards={
        "temporary_lockout": ReversibilityDefinition(
            is_reversible=True,
            reversal_timeframe="hours",
            reversal_mechanism="Reset MFA, restore access",
            reversal_cost_factor=0.3,
            downstream_irreversibility=False,
        ),
        "identity_theft": ReversibilityDefinition(
            is_reversible=False,
            reversal_timeframe="years",
            reversal_mechanism="Credit monitoring, dispute transactions",
            reversal_cost_factor=100.0,
            downstream_irreversibility=True,
        ),
    },
    stakeholder_templates=[
        StakeholderTemplate(
            role="platform user",
            power_relative_to_decision_maker="low",
            primary_harm_types=["identity theft", "fraud", "privacy breach"],
            vulnerability_flags=["elderly", "low tech literacy", "financial hardship"],
            consent_capability="yes",
        ),
        StakeholderTemplate(
            role="critical infrastructure operator",
            power_relative_to_decision_maker="high",
            primary_harm_types=["system compromise", "cascade failure", "national security impact"],
            vulnerability_flags=["single point of failure", "geopolitical target"],
            consent_capability="yes",
        ),
    ],
    domain_specific_vulnerability_factors=[
        "credential_reuse_across_sites",
        "elderly_or_low_literacy",
        "critical_infrastructure_dependency",
        "foreign_state_adversary",
        "supply_chain_compromise",
    ],
    amplification_vectors=[
        "credential stuffing across platforms",
        "dark web marketplace distribution",
        "nation-state weaponization",
        "supply chain propagation",
    ],
    regulation_notes="NIST cybersecurity framework, ISO/IEC 27001, CIS controls, GDPR breach notification",
)


# Registry of all metric packs
METRIC_PACK_REGISTRY = {
    "hiring": HIRING_METRIC_PACK,
    "healthcare": HEALTHCARE_METRIC_PACK,
    "finance": FINANCE_METRIC_PACK,
    "content_moderation": CONTENT_MODERATION_PACK,
    "security": SECURITY_METRIC_PACK,
}


def get_metric_pack(domain: str) -> Optional[MetricPack]:
    """Retrieve a metric pack by domain name."""
    return METRIC_PACK_REGISTRY.get(domain.lower())


def list_available_domains() -> List[str]:
    """List all available metric pack domains."""
    return list(METRIC_PACK_REGISTRY.keys())
