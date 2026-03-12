"""
Pause-Before-Harm Protocol (PBHP) v0.8.1 — Triage Classifier
Decision Triage / Fast Classifier Module

A pre-filter that routes incoming decisions to the appropriate assessment tier
(HUMAN/MIN/CORE/ULTRA) based on signal analysis. Routes by evaluating:
  - Irreversibility of the action
  - Vulnerable population impact
  - Power asymmetry exposure
  - Large-scale amplification potential

This module prevents unnecessary escalation while ensuring high-risk decisions
receive appropriate scrutiny before proceeding.

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from pbhp_core import RiskClass, ImpactLevel, LikelihoodLevel


class TriageTier(Enum):
    """Assessment tiers that decision routes to after triage."""
    HUMAN = "human"          # Escalate immediately to human judgment
    MIN = "min"              # PBHP-MIN rapid reflex check
    CORE = "core"            # Standard PBHP-CORE operational assessment
    ULTRA = "ultra"          # Constitutional/sovereign decision level


@dataclass
class TriageSignals:
    """
    Input signals for triage classification.
    Each signal is boolean or scalar, indicating presence/severity of a risk factor.
    """
    irreversible: bool = False
    """Action is irreversible or difficult to undo (true=higher tier)."""

    affects_vulnerable_population: bool = False
    """Decision affects minors, elderly, disabled, economically disadvantaged, etc."""

    power_asymmetry_detected: bool = False
    """Asymmetry between decision-maker and affected party."""

    large_scale_amplification: bool = False
    """Action will be auto-distributed, mass-scaled, or have viral potential."""

    automated_execution: bool = False
    """Action will execute automatically without further human approval."""

    legal_or_regulatory_impact: bool = False
    """Touches employment, health, finance, legal status."""

    multiple_simultaneous_harms: bool = False
    """Several independent harm vectors present."""

    uncertainty_level: str = "low"
    """Epistemic certainty: 'low', 'medium', 'high' (high=higher tier)."""

    first_occurrence: bool = True
    """Is this the first time this type of decision is made? (True=higher tier)."""

    stakeholder_consent_obtained: bool = False
    """Have affected parties explicitly consented? (False=higher tier)."""

    decision_urgency_hours: Optional[int] = None
    """Hours until decision must be made (low hours=potential higher tier)."""

    custom_risk_factors: Dict[str, bool] = field(default_factory=dict)
    """Domain-specific risk factors as key:bool pairs."""


@dataclass
class TriageResult:
    """Output of triage classification."""
    recommended_tier: TriageTier
    """The tier this decision should route to."""

    confidence_score: float
    """0.0-1.0 confidence in the recommendation (1.0=very confident)."""

    escalation_reasons: List[str]
    """Human-readable reasons for tier selection."""

    risk_signal_count: int
    """Number of active risk signals detected."""

    requires_human_loop: bool
    """Whether human judgment is mandatory before proceeding."""

    recommended_mitigation_checklist: List[str] = field(default_factory=list)
    """Pre-checks to perform at the recommended tier."""


class TriageClassifier:
    """
    Main triage classifier for routing decisions to appropriate PBHP tier.

    Scoring logic:
      - Each active signal contributes to escalation score
      - Certain signals (irreversibility + vulnerable + large-scale) force HUMAN/ULTRA
      - Uncertainty and consent issues increase tier requirements
      - Custom factors apply domain-specific logic
    """

    def __init__(self):
        """Initialize the triage classifier."""
        self.signal_weights = {
            "irreversible": 3.0,
            "vulnerable_population": 3.0,
            "power_asymmetry": 2.5,
            "large_scale": 2.5,
            "automated": 2.0,
            "legal_impact": 2.0,
            "multiple_harms": 2.0,
            "uncertainty_high": 1.5,
            "first_occurrence": 1.5,
            "no_consent": 2.0,
            "urgency_critical": 2.5,
        }

    def classify(self, signals: TriageSignals) -> TriageResult:
        """
        Classify a decision and route to appropriate PBHP tier.

        Args:
            signals: TriageSignals object containing risk indicators

        Returns:
            TriageResult with recommended tier and justification
        """
        # Count and weight active signals
        score = self._compute_escalation_score(signals)
        risk_signal_count = self._count_active_signals(signals)

        # Check for immediate escalation triggers
        if self._requires_immediate_human(signals):
            return self._make_result(
                tier=TriageTier.HUMAN,
                score=1.0,
                signals=risk_signal_count,
                reasons=self._explain_human_escalation(signals)
            )

        # Route based on score
        if score >= 9.0:
            tier = TriageTier.ULTRA
        elif score >= 6.0:
            tier = TriageTier.CORE
        elif score >= 3.0:
            tier = TriageTier.MIN
        else:
            tier = TriageTier.HUMAN if risk_signal_count >= 3 else TriageTier.MIN

        reasons = self._explain_classification(signals, score, tier)

        return self._make_result(
            tier=tier,
            score=min(1.0, score / 10.0),  # Normalize to 0-1
            signals=risk_signal_count,
            reasons=reasons
        )

    def _compute_escalation_score(self, signals: TriageSignals) -> float:
        """Compute weighted escalation score from signals."""
        score = 0.0

        if signals.irreversible:
            score += self.signal_weights["irreversible"]

        if signals.affects_vulnerable_population:
            score += self.signal_weights["vulnerable_population"]

        if signals.power_asymmetry_detected:
            score += self.signal_weights["power_asymmetry"]

        if signals.large_scale_amplification:
            score += self.signal_weights["large_scale"]

        if signals.automated_execution:
            score += self.signal_weights["automated"]

        if signals.legal_or_regulatory_impact:
            score += self.signal_weights["legal_impact"]

        if signals.multiple_simultaneous_harms:
            score += self.signal_weights["multiple_harms"]

        if signals.uncertainty_level == "high":
            score += self.signal_weights["uncertainty_high"]

        if signals.first_occurrence:
            score += self.signal_weights["first_occurrence"]

        if not signals.stakeholder_consent_obtained:
            score += self.signal_weights["no_consent"]

        if signals.decision_urgency_hours and signals.decision_urgency_hours < 4:
            score += self.signal_weights["urgency_critical"]

        # Custom factors
        for factor, active in signals.custom_risk_factors.items():
            if active:
                score += 1.0  # Conservative weight for custom factors

        return score

    def _count_active_signals(self, signals: TriageSignals) -> int:
        """Count how many risk signals are active."""
        count = 0
        count += int(signals.irreversible)
        count += int(signals.affects_vulnerable_population)
        count += int(signals.power_asymmetry_detected)
        count += int(signals.large_scale_amplification)
        count += int(signals.automated_execution)
        count += int(signals.legal_or_regulatory_impact)
        count += int(signals.multiple_simultaneous_harms)
        count += int(signals.uncertainty_level == "high")
        count += int(signals.first_occurrence)
        count += int(not signals.stakeholder_consent_obtained)
        if signals.decision_urgency_hours and signals.decision_urgency_hours < 4:
            count += 1
        count += len([v for v in signals.custom_risk_factors.values() if v])
        return count

    def _requires_immediate_human(self, signals: TriageSignals) -> bool:
        """
        Check for conditions that mandate immediate human escalation.

        Triggers:
        - Irreversible + vulnerable + large-scale
        - Irreversible + power_asymmetry + legal_impact
        - Multiple harms + automated + high uncertainty
        """
        # Triple combination: irreversible + vulnerable + large-scale
        if (signals.irreversible and signals.affects_vulnerable_population and
                signals.large_scale_amplification):
            return True

        # Irreversible + power + legal
        if (signals.irreversible and signals.power_asymmetry_detected and
                signals.legal_or_regulatory_impact):
            return True

        # Multiple independent harms + automated + high uncertainty
        if (signals.multiple_simultaneous_harms and signals.automated_execution and
                signals.uncertainty_level == "high"):
            return True

        return False

    def _explain_human_escalation(self, signals: TriageSignals) -> List[str]:
        """Generate reasons for HUMAN tier escalation."""
        reasons = []

        if (signals.irreversible and signals.affects_vulnerable_population and
                signals.large_scale_amplification):
            reasons.append(
                "CRITICAL: Irreversible action affecting vulnerable populations "
                "with large-scale amplification potential detected."
            )

        if (signals.irreversible and signals.power_asymmetry_detected and
                signals.legal_or_regulatory_impact):
            reasons.append(
                "CRITICAL: Irreversible action with power asymmetry and legal impact "
                "requires immediate human judgment."
            )

        if (signals.multiple_simultaneous_harms and signals.automated_execution and
                signals.uncertainty_level == "high"):
            reasons.append(
                "CRITICAL: Multiple simultaneous harms with automated execution "
                "and high uncertainty requires human review."
            )

        return reasons

    def _explain_classification(self, signals: TriageSignals, score: float,
                               tier: TriageTier) -> List[str]:
        """Generate human-readable explanation for tier assignment."""
        reasons = []

        active_signals = []
        if signals.irreversible:
            active_signals.append("irreversible action")
        if signals.affects_vulnerable_population:
            active_signals.append("vulnerable population impact")
        if signals.power_asymmetry_detected:
            active_signals.append("power asymmetry")
        if signals.large_scale_amplification:
            active_signals.append("large-scale amplification")
        if signals.automated_execution:
            active_signals.append("automated execution")
        if signals.legal_or_regulatory_impact:
            active_signals.append("legal/regulatory impact")
        if signals.multiple_simultaneous_harms:
            active_signals.append("multiple simultaneous harms")

        if active_signals:
            reasons.append(f"Detected: {', '.join(active_signals)}")

        if signals.uncertainty_level == "high":
            reasons.append("High epistemic uncertainty requires elevated scrutiny")

        if not signals.stakeholder_consent_obtained:
            reasons.append("Affected parties have not provided explicit consent")

        if signals.decision_urgency_hours and signals.decision_urgency_hours < 4:
            reasons.append(f"High time pressure ({signals.decision_urgency_hours} hours)")

        reasons.append(f"Escalation score: {score:.1f}/10.0 → {tier.value.upper()} tier")

        return reasons

    def _make_result(self, tier: TriageTier, score: float,
                    signals: int, reasons: List[str]) -> TriageResult:
        """Create a TriageResult object."""
        mitigations = self._recommend_mitigations(tier, signals > 3)

        return TriageResult(
            recommended_tier=tier,
            confidence_score=score,
            escalation_reasons=reasons,
            risk_signal_count=signals,
            requires_human_loop=(tier in (TriageTier.HUMAN, TriageTier.ULTRA)),
            recommended_mitigation_checklist=mitigations
        )

    def _recommend_mitigations(self, tier: TriageTier,
                             high_risk: bool) -> List[str]:
        """Generate tier-specific mitigation recommendations."""
        base_mitigations = [
            "Verify decision context and stakeholder impact",
            "Document decision rationale and alternatives considered",
        ]

        if tier == TriageTier.HUMAN:
            return base_mitigations + [
                "Mandatory human expert review required",
                "Document all veto/approval decisions",
                "Escalate to organizational leadership if uncertain",
            ]

        if tier == TriageTier.ULTRA:
            return base_mitigations + [
                "Constitutional/sovereignty-level review required",
                "Multi-stakeholder consensus assessment needed",
                "Red-team challenge of decision logic",
            ]

        if tier == TriageTier.CORE:
            return base_mitigations + [
                "Full PBHP-CORE assessment required",
                "Harm/door analysis mandatory",
                "Reversibility plan required for irreversible actions",
            ]

        # MIN tier
        return base_mitigations + [
            "Quick trigger check sufficient",
            "Fast risk assessment in &lt;30 seconds acceptable",
        ]


# Convenience function for easy integration
def triage(signals: TriageSignals) -> TriageResult:
    """
    Quick entry point for triage classification.

    Usage:
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True,
            large_scale_amplification=True
        )
        result = triage(signals)
        print(f"Route to: {result.recommended_tier.value}")
    """
    classifier = TriageClassifier()
    return classifier.classify(signals)
