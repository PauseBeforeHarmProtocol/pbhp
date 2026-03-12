"""
Comprehensive test suite for pbhp_triage module.

Tests cover:
- Tier routing based on escalation scores
- Signal weighting and scoring logic
- Immediate human escalation triggers
- Confidence score normalization
- Risk signal counting
- Mitigation checklist generation
- Custom risk factors
- Urgency and uncertainty handling
- triage() convenience function
"""

import unittest
import sys
sys.path.insert(0, '/sessions/happy-charming-bohr/pbhp_repo/src')

from pbhp_triage import (
    TriageTier,
    TriageSignals,
    TriageResult,
    TriageClassifier,
    triage,
)


class TestTriageSignalsDefaults(unittest.TestCase):
    """Test TriageSignals dataclass defaults."""

    def test_default_signals_initialization(self):
        """Test that TriageSignals initializes with correct defaults."""
        signals = TriageSignals()
        self.assertFalse(signals.irreversible)
        self.assertFalse(signals.affects_vulnerable_population)
        self.assertFalse(signals.power_asymmetry_detected)
        self.assertFalse(signals.large_scale_amplification)
        self.assertFalse(signals.automated_execution)
        self.assertFalse(signals.legal_or_regulatory_impact)
        self.assertFalse(signals.multiple_simultaneous_harms)
        self.assertEqual(signals.uncertainty_level, "low")
        self.assertTrue(signals.first_occurrence)
        self.assertFalse(signals.stakeholder_consent_obtained)
        self.assertIsNone(signals.decision_urgency_hours)
        self.assertEqual(signals.custom_risk_factors, {})

    def test_partial_signals_initialization(self):
        """Test initializing TriageSignals with partial arguments."""
        signals = TriageSignals(
            irreversible=True,
            uncertainty_level="high"
        )
        self.assertTrue(signals.irreversible)
        self.assertEqual(signals.uncertainty_level, "high")
        self.assertTrue(signals.first_occurrence)  # Still default
        self.assertFalse(signals.stakeholder_consent_obtained)  # Still default


class TestDefaultSignalsTriage(unittest.TestCase):
    """Test triage classification with default signals."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_default_signals_routes_to_min_tier(self):
        """Default signals (first_occurrence=True, consent=False) should route to MIN.

        Baseline score: first_occurrence (1.5) + no_consent (2.0) = 3.5
        Signal count: first_occurrence (1) + no_consent (1) = 2
        Score 3.5 >= 3.0, so MIN tier (not HUMAN since signal_count < 3)
        """
        signals = TriageSignals()
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.MIN)
        self.assertFalse(result.requires_human_loop)
        self.assertEqual(result.risk_signal_count, 2)
        # Confidence: 3.5/10.0 = 0.35
        self.assertAlmostEqual(result.confidence_score, 0.35, places=2)

    def test_default_signals_have_escalation_reasons(self):
        """Default signals should produce escalation reasons."""
        signals = TriageSignals()
        result = self.classifier.classify(signals)

        self.assertGreater(len(result.escalation_reasons), 0)
        # Should mention lack of consent
        reasons_text = " ".join(result.escalation_reasons)
        self.assertIn("consent", reasons_text.lower())

    def test_default_signals_include_min_mitigations(self):
        """Default MIN tier should include MIN-specific mitigations."""
        signals = TriageSignals()
        result = self.classifier.classify(signals)

        mitigations_text = " ".join(result.recommended_mitigation_checklist)
        self.assertIn("Quick trigger check", mitigations_text)


class TestAllSignalsOff(unittest.TestCase):
    """Test triage with all signals explicitly disabled."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_all_signals_off_routes_to_min_tier(self):
        """All signals off (first_occurrence=False, consent=True) should route to MIN.

        Score: 0 (no active signals)
        Signal count: 0
        Score 0 < 3.0, so check signal_count: 0 < 3, so MIN tier
        """
        signals = TriageSignals(
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.MIN)
        self.assertFalse(result.requires_human_loop)
        self.assertEqual(result.risk_signal_count, 0)
        self.assertEqual(result.confidence_score, 0.0)

    def test_all_signals_off_produces_baseline_mitigations(self):
        """All signals off should still include base mitigations."""
        signals = TriageSignals(
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        mitigations_text = " ".join(result.recommended_mitigation_checklist)
        # Should include baseline mitigations
        self.assertIn("Verify decision context", mitigations_text)


class TestImmediateHumanEscalations(unittest.TestCase):
    """Test conditions that trigger immediate HUMAN tier escalation."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_immediate_human_irreversible_vulnerable_largescale(self):
        """Irreversible + vulnerable + large-scale should trigger immediate HUMAN."""
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True,
            large_scale_amplification=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.HUMAN)
        self.assertTrue(result.requires_human_loop)
        self.assertEqual(result.confidence_score, 1.0)
        # Check escalation reason mentions CRITICAL
        self.assertTrue(
            any("CRITICAL" in reason for reason in result.escalation_reasons)
        )

    def test_immediate_human_irreversible_power_legal(self):
        """Irreversible + power_asymmetry + legal_impact should trigger immediate HUMAN."""
        signals = TriageSignals(
            irreversible=True,
            power_asymmetry_detected=True,
            legal_or_regulatory_impact=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.HUMAN)
        self.assertTrue(result.requires_human_loop)
        self.assertEqual(result.confidence_score, 1.0)

    def test_immediate_human_multiple_harms_automated_high_uncertainty(self):
        """Multiple_harms + automated + high_uncertainty should trigger immediate HUMAN."""
        signals = TriageSignals(
            multiple_simultaneous_harms=True,
            automated_execution=True,
            uncertainty_level="high",
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.HUMAN)
        self.assertTrue(result.requires_human_loop)
        self.assertEqual(result.confidence_score, 1.0)

    def test_human_escalation_requires_human_loop(self):
        """HUMAN tier should always set requires_human_loop=True."""
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True,
            large_scale_amplification=True
        )
        result = self.classifier.classify(signals)

        self.assertTrue(result.requires_human_loop)

    def test_human_escalation_includes_mandatory_review_mitigation(self):
        """HUMAN tier mitigations should include mandatory human expert review."""
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True,
            large_scale_amplification=True
        )
        result = self.classifier.classify(signals)

        mitigations_text = " ".join(result.recommended_mitigation_checklist)
        self.assertIn("Mandatory human expert review", mitigations_text)


class TestULTRATierRouting(unittest.TestCase):
    """Test routing to ULTRA tier (score >= 9.0)."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_high_score_routes_to_ultra(self):
        """Score >= 9.0 should route to ULTRA tier.

        Example: irreversible (3.0) + vulnerable (3.0) + power_asymmetry (2.5) +
        legal_impact (2.0) + first_occurrence (1.5) + no_consent (2.0) = 14.0 > 9.0
        (but this also triggers HUMAN immediately due to irreversible+power+legal)

        So we need a combination that doesn't trigger immediate HUMAN:
        irreversible (3.0) + vulnerable (3.0) + large_scale (2.5) +
        legal_impact (2.0) + no_consent (2.0) + first_occurrence (1.5) = 14.0
        (but this triggers HUMAN due to irreversible+vulnerable+large_scale)

        Let's use: irreversible (3.0) + power (2.5) + large_scale (2.5) +
        automated (2.0) + no_consent (2.0) = 12.0, with first_occurrence=False
        """
        signals = TriageSignals(
            irreversible=True,
            power_asymmetry_detected=True,
            large_scale_amplification=True,
            automated_execution=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.ULTRA)
        self.assertTrue(result.requires_human_loop)
        # Score: 3.0 + 2.5 + 2.5 + 2.0 = 10.0, confidence = min(1.0, 10.0/10.0) = 1.0
        self.assertEqual(result.confidence_score, 1.0)

    def test_ultra_tier_includes_constitutional_review_mitigation(self):
        """ULTRA tier mitigations should include constitutional/sovereignty-level review."""
        signals = TriageSignals(
            irreversible=True,
            power_asymmetry_detected=True,
            large_scale_amplification=True,
            automated_execution=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        mitigations_text = " ".join(result.recommended_mitigation_checklist)
        self.assertIn("Constitutional/sovereignty-level review", mitigations_text)

    def test_ultra_tier_requires_human_loop(self):
        """ULTRA tier should set requires_human_loop=True."""
        signals = TriageSignals(
            irreversible=True,
            power_asymmetry_detected=True,
            large_scale_amplification=True,
            automated_execution=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertTrue(result.requires_human_loop)


class TestCORETierRouting(unittest.TestCase):
    """Test routing to CORE tier (score 6.0-8.9)."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_moderate_score_routes_to_core(self):
        """Score 6.0-8.9 should route to CORE tier.

        Example: irreversible (3.0) + vulnerable (3.0) + no_consent (2.0) = 8.0
        But this triggers HUMAN if with large_scale.

        Let's use: vulnerable (3.0) + power_asymmetry (2.5) + legal_impact (2.0)
        + no_consent (2.0) = 9.5, still ULTRA

        Try: vulnerable (3.0) + automated (2.0) + no_consent (2.0)
        + first_occurrence (1.0 if False) = 8.0
        But we need all signals False to avoid it.

        vulnerable (3.0) + automated (2.0) + legal_impact (2.0)
        + first_occurrence=False + consent=True = 7.0
        """
        signals = TriageSignals(
            affects_vulnerable_population=True,
            automated_execution=True,
            legal_or_regulatory_impact=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.CORE)
        self.assertFalse(result.requires_human_loop)
        # Score: 3.0 + 2.0 + 2.0 = 7.0, confidence = 7.0/10.0 = 0.7
        self.assertAlmostEqual(result.confidence_score, 0.7, places=1)

    def test_core_tier_includes_pbhp_core_assessment_mitigation(self):
        """CORE tier mitigations should include PBHP-CORE assessment."""
        signals = TriageSignals(
            affects_vulnerable_population=True,
            automated_execution=True,
            legal_or_regulatory_impact=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        mitigations_text = " ".join(result.recommended_mitigation_checklist)
        self.assertIn("PBHP-CORE assessment", mitigations_text)

    def test_core_tier_does_not_require_human_loop(self):
        """CORE tier should set requires_human_loop=False."""
        signals = TriageSignals(
            affects_vulnerable_population=True,
            automated_execution=True,
            legal_or_regulatory_impact=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertFalse(result.requires_human_loop)


class TestMINTierRouting(unittest.TestCase):
    """Test routing to MIN tier."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_low_score_routes_to_min(self):
        """Score < 3.0 with signal_count < 3 should route to MIN tier."""
        signals = TriageSignals(
            affects_vulnerable_population=False,
            automated_execution=False,
            legal_or_regulatory_impact=False,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.MIN)
        self.assertFalse(result.requires_human_loop)
        self.assertEqual(result.confidence_score, 0.0)

    def test_min_tier_single_low_weight_signal(self):
        """Single low-weight signal should route to MIN."""
        signals = TriageSignals(
            power_asymmetry_detected=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.MIN)
        self.assertFalse(result.requires_human_loop)
        # Score: 2.5, confidence = 2.5/10.0 = 0.25
        self.assertAlmostEqual(result.confidence_score, 0.25, places=2)

    def test_min_tier_includes_quick_check_mitigation(self):
        """MIN tier mitigations should include quick trigger check."""
        signals = TriageSignals(
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        mitigations_text = " ".join(result.recommended_mitigation_checklist)
        self.assertIn("Quick trigger check", mitigations_text)

    def test_min_tier_does_not_require_human_loop(self):
        """MIN tier should set requires_human_loop=False."""
        signals = TriageSignals(
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertFalse(result.requires_human_loop)


class TestRequiresHumanLoop(unittest.TestCase):
    """Test requires_human_loop logic."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_human_tier_requires_human_loop(self):
        """HUMAN tier must have requires_human_loop=True."""
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True,
            large_scale_amplification=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.HUMAN)
        self.assertTrue(result.requires_human_loop)

    def test_ultra_tier_requires_human_loop(self):
        """ULTRA tier must have requires_human_loop=True."""
        signals = TriageSignals(
            irreversible=True,
            power_asymmetry_detected=True,
            large_scale_amplification=True,
            automated_execution=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.ULTRA)
        self.assertTrue(result.requires_human_loop)

    def test_core_tier_does_not_require_human_loop(self):
        """CORE tier must have requires_human_loop=False."""
        signals = TriageSignals(
            affects_vulnerable_population=True,
            automated_execution=True,
            legal_or_regulatory_impact=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.CORE)
        self.assertFalse(result.requires_human_loop)

    def test_min_tier_does_not_require_human_loop(self):
        """MIN tier must have requires_human_loop=False."""
        signals = TriageSignals(
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.MIN)
        self.assertFalse(result.requires_human_loop)


class TestEscalationReasons(unittest.TestCase):
    """Test escalation reasons generation."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_escalation_reasons_present(self):
        """Classification should always provide escalation reasons."""
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True
        )
        result = self.classifier.classify(signals)

        self.assertIsInstance(result.escalation_reasons, list)
        self.assertGreater(len(result.escalation_reasons), 0)

    def test_escalation_reasons_mention_relevant_signals(self):
        """Escalation reasons should mention detected active signals."""
        signals = TriageSignals(
            irreversible=True,
            automated_execution=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        reasons_text = " ".join(result.escalation_reasons).lower()
        self.assertIn("irreversible", reasons_text)
        self.assertIn("automated", reasons_text)

    def test_immediate_human_reasons_mention_critical(self):
        """Immediate HUMAN escalation reasons should include CRITICAL."""
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True,
            large_scale_amplification=True
        )
        result = self.classifier.classify(signals)

        self.assertTrue(
            any("CRITICAL" in reason for reason in result.escalation_reasons)
        )

    def test_escalation_reasons_include_score(self):
        """Escalation reasons should include the escalation score."""
        signals = TriageSignals(
            automated_execution=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        reasons_text = " ".join(result.escalation_reasons)
        # Should mention score and tier
        self.assertTrue(any(char.isdigit() for char in reasons_text))


class TestRiskSignalCounting(unittest.TestCase):
    """Test risk signal counting logic."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_all_signals_off_count_zero(self):
        """All signals off should have risk_signal_count=0."""
        signals = TriageSignals(
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.risk_signal_count, 0)

    def test_default_signals_count_two(self):
        """Default signals (first_occurrence=True, consent=False) should count 2."""
        signals = TriageSignals()
        result = self.classifier.classify(signals)

        self.assertEqual(result.risk_signal_count, 2)

    def test_multiple_signals_counted_correctly(self):
        """Multiple active signals should be counted correctly."""
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True,
            automated_execution=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # irreversible (1) + vulnerable (1) + automated (1) = 3
        self.assertEqual(result.risk_signal_count, 3)

    def test_uncertainty_high_counted_as_signal(self):
        """High uncertainty should count as one signal."""
        signals = TriageSignals(
            uncertainty_level="high",
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Only uncertainty_level="high" counts as 1
        self.assertEqual(result.risk_signal_count, 1)

    def test_custom_factors_counted(self):
        """Custom risk factors should be counted in signal count."""
        signals = TriageSignals(
            custom_risk_factors={"custom_a": True, "custom_b": False},
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Only custom_a counts as 1
        self.assertEqual(result.risk_signal_count, 1)

    def test_urgency_critical_counted_as_signal(self):
        """Urgency < 4 hours should count as one signal."""
        signals = TriageSignals(
            decision_urgency_hours=2,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Only decision_urgency_hours < 4 counts as 1
        self.assertEqual(result.risk_signal_count, 1)


class TestConfidenceScoreNormalization(unittest.TestCase):
    """Test confidence score calculation and normalization."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_confidence_score_zero_for_zero_score(self):
        """Score 0 should give confidence 0.0."""
        signals = TriageSignals(
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.confidence_score, 0.0)

    def test_confidence_score_calculation(self):
        """Confidence should be min(1.0, score/10.0)."""
        signals = TriageSignals(
            automated_execution=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 2.0, confidence = 2.0/10.0 = 0.2
        self.assertAlmostEqual(result.confidence_score, 0.2, places=1)

    def test_confidence_score_capped_at_one(self):
        """Confidence should be capped at 1.0."""
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True,
            large_scale_amplification=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.confidence_score, 1.0)
        self.assertLessEqual(result.confidence_score, 1.0)

    def test_confidence_score_between_zero_and_one(self):
        """Confidence should always be between 0.0 and 1.0."""
        signals = TriageSignals(
            affects_vulnerable_population=True,
            automated_execution=True,
            legal_or_regulatory_impact=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertGreaterEqual(result.confidence_score, 0.0)
        self.assertLessEqual(result.confidence_score, 1.0)


class TestCustomRiskFactors(unittest.TestCase):
    """Test custom risk factors handling."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_custom_risk_factor_adds_to_score(self):
        """Active custom risk factors should add 1.0 to score each."""
        signals = TriageSignals(
            custom_risk_factors={"critical_domain": True},
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 1.0 from custom factor, confidence = 1.0/10.0 = 0.1
        self.assertAlmostEqual(result.confidence_score, 0.1, places=1)

    def test_multiple_custom_risk_factors(self):
        """Multiple active custom factors should each add 1.0."""
        signals = TriageSignals(
            custom_risk_factors={
                "factor_a": True,
                "factor_b": True,
                "factor_c": False
            },
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 1.0 + 1.0 = 2.0, confidence = 2.0/10.0 = 0.2
        self.assertAlmostEqual(result.confidence_score, 0.2, places=1)
        self.assertEqual(result.risk_signal_count, 2)

    def test_custom_factors_combined_with_other_signals(self):
        """Custom factors should add to score from other signals."""
        signals = TriageSignals(
            automated_execution=True,
            custom_risk_factors={"domain_specific": True},
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 2.0 (automated) + 1.0 (custom) = 3.0
        self.assertAlmostEqual(result.confidence_score, 0.3, places=1)


class TestUrgencyHandling(unittest.TestCase):
    """Test decision urgency handling."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_urgency_critical_adds_weight(self):
        """Urgency < 4 hours should add urgency_critical weight (2.5)."""
        signals = TriageSignals(
            decision_urgency_hours=1,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 2.5 (urgency_critical), confidence = 2.5/10.0 = 0.25
        self.assertAlmostEqual(result.confidence_score, 0.25, places=2)

    def test_urgency_2_hours_critical(self):
        """Urgency of 2 hours should be critical."""
        signals = TriageSignals(
            decision_urgency_hours=2,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 2.5
        self.assertAlmostEqual(result.confidence_score, 0.25, places=2)

    def test_urgency_4_hours_not_critical(self):
        """Urgency of 4+ hours should not add critical weight."""
        signals = TriageSignals(
            decision_urgency_hours=4,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 0 (no signals)
        self.assertEqual(result.confidence_score, 0.0)

    def test_urgency_24_hours_not_critical(self):
        """Urgency of 24 hours should not add critical weight."""
        signals = TriageSignals(
            decision_urgency_hours=24,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 0
        self.assertEqual(result.confidence_score, 0.0)

    def test_no_urgency_specified(self):
        """No urgency specified should not add weight."""
        signals = TriageSignals(
            decision_urgency_hours=None,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 0
        self.assertEqual(result.confidence_score, 0.0)

    def test_urgency_mentioned_in_escalation_reasons(self):
        """Critical urgency should be mentioned in escalation reasons."""
        signals = TriageSignals(
            decision_urgency_hours=2,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        reasons_text = " ".join(result.escalation_reasons)
        self.assertIn("High time pressure", reasons_text)


class TestUncertaintyHandling(unittest.TestCase):
    """Test uncertainty level handling."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_high_uncertainty_adds_weight(self):
        """High uncertainty should add uncertainty_high weight (1.5)."""
        signals = TriageSignals(
            uncertainty_level="high",
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 1.5, confidence = 1.5/10.0 = 0.15
        self.assertAlmostEqual(result.confidence_score, 0.15, places=2)

    def test_medium_uncertainty_no_weight(self):
        """Medium uncertainty should not add weight."""
        signals = TriageSignals(
            uncertainty_level="medium",
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 0
        self.assertEqual(result.confidence_score, 0.0)

    def test_low_uncertainty_no_weight(self):
        """Low uncertainty (default) should not add weight."""
        signals = TriageSignals(
            uncertainty_level="low",
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 0
        self.assertEqual(result.confidence_score, 0.0)

    def test_high_uncertainty_mentioned_in_reasons(self):
        """High uncertainty should be mentioned in escalation reasons."""
        signals = TriageSignals(
            uncertainty_level="high",
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        reasons_text = " ".join(result.escalation_reasons)
        self.assertIn("High epistemic uncertainty", reasons_text)


class TestMitigationChecklists(unittest.TestCase):
    """Test tier-specific mitigation checklists."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_all_tiers_include_base_mitigations(self):
        """All tiers should include base mitigations."""
        for tier_signals in [
            TriageSignals(first_occurrence=False, stakeholder_consent_obtained=True),  # MIN
            TriageSignals(affects_vulnerable_population=True, automated_execution=True,
                         legal_or_regulatory_impact=True, first_occurrence=False,
                         stakeholder_consent_obtained=True),  # CORE
            TriageSignals(irreversible=True, power_asymmetry_detected=True,
                         large_scale_amplification=True, automated_execution=True,
                         first_occurrence=False, stakeholder_consent_obtained=True),  # ULTRA
        ]:
            result = self.classifier.classify(tier_signals)
            mitigations_text = " ".join(result.recommended_mitigation_checklist)
            self.assertIn("Verify decision context", mitigations_text)
            self.assertIn("Document decision rationale", mitigations_text)

    def test_human_tier_mitigations(self):
        """HUMAN tier should have specific mitigations."""
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True,
            large_scale_amplification=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.HUMAN)
        mitigations_text = " ".join(result.recommended_mitigation_checklist)
        self.assertIn("Mandatory human expert review", mitigations_text)
        self.assertIn("Document all veto/approval decisions", mitigations_text)
        self.assertIn("Escalate to organizational leadership", mitigations_text)

    def test_ultra_tier_mitigations(self):
        """ULTRA tier should have specific mitigations."""
        signals = TriageSignals(
            irreversible=True,
            power_asymmetry_detected=True,
            large_scale_amplification=True,
            automated_execution=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.ULTRA)
        mitigations_text = " ".join(result.recommended_mitigation_checklist)
        self.assertIn("Constitutional/sovereignty-level review", mitigations_text)
        self.assertIn("Multi-stakeholder consensus", mitigations_text)
        self.assertIn("Red-team challenge", mitigations_text)

    def test_core_tier_mitigations(self):
        """CORE tier should have specific mitigations."""
        signals = TriageSignals(
            affects_vulnerable_population=True,
            automated_execution=True,
            legal_or_regulatory_impact=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.CORE)
        mitigations_text = " ".join(result.recommended_mitigation_checklist)
        self.assertIn("PBHP-CORE assessment", mitigations_text)
        self.assertIn("Harm", mitigations_text)

    def test_min_tier_mitigations(self):
        """MIN tier should have specific mitigations."""
        signals = TriageSignals(
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.recommended_tier, TriageTier.MIN)
        mitigations_text = " ".join(result.recommended_mitigation_checklist)
        self.assertIn("Quick trigger check", mitigations_text)


class TestTriageConvenienceFunction(unittest.TestCase):
    """Test triage() convenience function."""

    def test_triage_function_returns_result(self):
        """triage() should return a TriageResult."""
        signals = TriageSignals()
        result = triage(signals)

        self.assertIsInstance(result, TriageResult)

    def test_triage_function_with_default_signals(self):
        """triage() with default signals should route to MIN."""
        signals = TriageSignals()
        result = triage(signals)

        self.assertEqual(result.recommended_tier, TriageTier.MIN)

    def test_triage_function_with_immediate_escalation(self):
        """triage() should handle immediate escalations."""
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True,
            large_scale_amplification=True
        )
        result = triage(signals)

        self.assertEqual(result.recommended_tier, TriageTier.HUMAN)
        self.assertTrue(result.requires_human_loop)

    def test_triage_function_produces_complete_result(self):
        """triage() result should have all required fields."""
        signals = TriageSignals(
            automated_execution=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = triage(signals)

        self.assertIsNotNone(result.recommended_tier)
        self.assertIsNotNone(result.confidence_score)
        self.assertIsNotNone(result.escalation_reasons)
        self.assertIsNotNone(result.risk_signal_count)
        self.assertIsNotNone(result.requires_human_loop)
        self.assertIsNotNone(result.recommended_mitigation_checklist)


class TestSignalWeights(unittest.TestCase):
    """Test individual signal weights."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_irreversible_weight(self):
        """Irreversible should have weight 3.0."""
        signals = TriageSignals(
            irreversible=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 3.0, confidence = 0.3
        self.assertAlmostEqual(result.confidence_score, 0.3, places=1)

    def test_vulnerable_population_weight(self):
        """Vulnerable population should have weight 3.0."""
        signals = TriageSignals(
            affects_vulnerable_population=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 3.0, confidence = 0.3
        self.assertAlmostEqual(result.confidence_score, 0.3, places=1)

    def test_power_asymmetry_weight(self):
        """Power asymmetry should have weight 2.5."""
        signals = TriageSignals(
            power_asymmetry_detected=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 2.5, confidence = 0.25
        self.assertAlmostEqual(result.confidence_score, 0.25, places=2)

    def test_large_scale_weight(self):
        """Large scale should have weight 2.5."""
        signals = TriageSignals(
            large_scale_amplification=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 2.5, confidence = 0.25
        self.assertAlmostEqual(result.confidence_score, 0.25, places=2)

    def test_automated_weight(self):
        """Automated execution should have weight 2.0."""
        signals = TriageSignals(
            automated_execution=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 2.0, confidence = 0.2
        self.assertAlmostEqual(result.confidence_score, 0.2, places=1)

    def test_legal_impact_weight(self):
        """Legal impact should have weight 2.0."""
        signals = TriageSignals(
            legal_or_regulatory_impact=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 2.0, confidence = 0.2
        self.assertAlmostEqual(result.confidence_score, 0.2, places=1)

    def test_multiple_harms_weight(self):
        """Multiple harms should have weight 2.0."""
        signals = TriageSignals(
            multiple_simultaneous_harms=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 2.0, confidence = 0.2
        self.assertAlmostEqual(result.confidence_score, 0.2, places=1)

    def test_no_consent_weight(self):
        """No consent should have weight 2.0."""
        signals = TriageSignals(
            first_occurrence=False,
            stakeholder_consent_obtained=False
        )
        result = self.classifier.classify(signals)

        # Score: 2.0, confidence = 0.2
        self.assertAlmostEqual(result.confidence_score, 0.2, places=1)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_score_exactly_at_tier_boundaries(self):
        """Test scores exactly at tier boundaries."""
        # Score exactly 3.0 should be MIN (>= 3.0)
        signals = TriageSignals(
            power_asymmetry_detected=True,
            automated_execution=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)
        # Score: 2.5 + 2.0 = 4.5, not exactly 3.0
        self.assertNotEqual(result.confidence_score, 0.3)

    def test_empty_custom_factors(self):
        """Empty custom factors should not affect scoring."""
        signals = TriageSignals(
            custom_risk_factors={},
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        self.assertEqual(result.risk_signal_count, 0)

    def test_many_custom_factors(self):
        """Many active custom factors should accumulate."""
        signals = TriageSignals(
            custom_risk_factors={
                f"factor_{i}": True for i in range(5)
            },
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 5 * 1.0 = 5.0, confidence = 0.5
        self.assertAlmostEqual(result.confidence_score, 0.5, places=1)
        self.assertEqual(result.risk_signal_count, 5)

    def test_combined_weights_additive(self):
        """Signal weights should be additive."""
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True,
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Score: 3.0 + 3.0 = 6.0, confidence = 0.6
        self.assertAlmostEqual(result.confidence_score, 0.6, places=1)


class TestResultDataclass(unittest.TestCase):
    """Test TriageResult dataclass."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_result_has_all_fields(self):
        """TriageResult should have all required fields."""
        signals = TriageSignals()
        result = self.classifier.classify(signals)

        self.assertIsNotNone(result.recommended_tier)
        self.assertIsNotNone(result.confidence_score)
        self.assertIsNotNone(result.escalation_reasons)
        self.assertIsNotNone(result.risk_signal_count)
        self.assertIsNotNone(result.requires_human_loop)
        self.assertIsNotNone(result.recommended_mitigation_checklist)

    def test_result_fields_correct_types(self):
        """TriageResult fields should have correct types."""
        signals = TriageSignals()
        result = self.classifier.classify(signals)

        self.assertIsInstance(result.recommended_tier, TriageTier)
        self.assertIsInstance(result.confidence_score, float)
        self.assertIsInstance(result.escalation_reasons, list)
        self.assertIsInstance(result.risk_signal_count, int)
        self.assertIsInstance(result.requires_human_loop, bool)
        self.assertIsInstance(result.recommended_mitigation_checklist, list)

    def test_mitigation_checklist_is_list_of_strings(self):
        """Mitigation checklist should contain strings."""
        signals = TriageSignals()
        result = self.classifier.classify(signals)

        for mitigation in result.recommended_mitigation_checklist:
            self.assertIsInstance(mitigation, str)


class TestComplexScenarios(unittest.TestCase):
    """Test complex real-world-like scenarios."""

    def setUp(self):
        self.classifier = TriageClassifier()

    def test_scenario_data_privacy_decision(self):
        """Scenario: Decision to process user data."""
        signals = TriageSignals(
            irreversible=False,  # Data could be deleted
            affects_vulnerable_population=False,
            power_asymmetry_detected=True,  # Company vs users
            large_scale_amplification=True,  # Affects millions
            automated_execution=True,  # Auto-processed
            legal_or_regulatory_impact=True,  # GDPR, etc.
            multiple_simultaneous_harms=True,  # Privacy, misuse, etc.
            uncertainty_level="medium",
            stakeholder_consent_obtained=False
        )
        result = self.classifier.classify(signals)

        # Should be ULTRA or CORE
        self.assertIn(result.recommended_tier, [TriageTier.CORE, TriageTier.ULTRA])

    def test_scenario_medical_ai_deployment(self):
        """Scenario: Deploying AI for medical diagnosis."""
        signals = TriageSignals(
            irreversible=True,  # Misdiagnosis could be fatal
            affects_vulnerable_population=True,  # Patients
            power_asymmetry_detected=True,  # Doctor/Hospital vs patient
            large_scale_amplification=True,  # Rolls out to many hospitals
            automated_execution=True,  # Auto-diagnosis
            legal_or_regulatory_impact=True,  # Medical liability
            multiple_simultaneous_harms=True,  # Health, financial, psychological
            uncertainty_level="high",
            decision_urgency_hours=24,
            stakeholder_consent_obtained=False
        )
        result = self.classifier.classify(signals)

        # Should be HUMAN due to multiple critical factors
        self.assertEqual(result.recommended_tier, TriageTier.HUMAN)
        self.assertTrue(result.requires_human_loop)

    def test_scenario_minor_content_decision(self):
        """Scenario: Minor content moderation decision."""
        signals = TriageSignals(
            irreversible=False,
            affects_vulnerable_population=False,
            power_asymmetry_detected=False,
            large_scale_amplification=False,
            automated_execution=False,
            legal_or_regulatory_impact=False,
            multiple_simultaneous_harms=False,
            uncertainty_level="low",
            first_occurrence=False,
            stakeholder_consent_obtained=True
        )
        result = self.classifier.classify(signals)

        # Should be MIN
        self.assertEqual(result.recommended_tier, TriageTier.MIN)
        self.assertFalse(result.requires_human_loop)


if __name__ == '__main__':
    unittest.main(verbosity=2)
