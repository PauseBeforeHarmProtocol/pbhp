"""
Comprehensive test suite for pbhp_metrics module.

Tests cover:
- All 5 metric packs exist in registry
- list_available_domains returns correct domains
- get_metric_pack retrieves correct packs
- Structure and content of each metric pack
- Severity thresholds, reversibility standards, stakeholder templates
- Domain-specific vulnerability factors and amplification vectors
- Regulation notes presence
- Pack version consistency
- Valid ImpactLevel and consent_capability values
- Positive reversal_cost_factor values
- Domain-specific pack content validation
"""

import unittest
import sys
sys.path.insert(0, '/sessions/happy-charming-bohr/pbhp_repo/src')

from pbhp_metrics import (
    SeverityThreshold,
    ReversibilityDefinition,
    StakeholderTemplate,
    MetricPack,
    HIRING_METRIC_PACK,
    HEALTHCARE_METRIC_PACK,
    FINANCE_METRIC_PACK,
    CONTENT_MODERATION_PACK,
    SECURITY_METRIC_PACK,
    METRIC_PACK_REGISTRY,
    get_metric_pack,
    list_available_domains,
)
from pbhp_core import ImpactLevel


class TestMetricPackRegistry(unittest.TestCase):
    """Test metric pack registry existence and retrieval."""

    def test_all_five_packs_in_registry(self):
        """Verify all 5 metric packs are registered."""
        self.assertEqual(len(METRIC_PACK_REGISTRY), 5)
        self.assertIn("hiring", METRIC_PACK_REGISTRY)
        self.assertIn("healthcare", METRIC_PACK_REGISTRY)
        self.assertIn("finance", METRIC_PACK_REGISTRY)
        self.assertIn("content_moderation", METRIC_PACK_REGISTRY)
        self.assertIn("security", METRIC_PACK_REGISTRY)

    def test_list_available_domains_returns_five_domains(self):
        """Verify list_available_domains returns exactly 5 domains."""
        domains = list_available_domains()
        self.assertEqual(len(domains), 5)
        self.assertIn("hiring", domains)
        self.assertIn("healthcare", domains)
        self.assertIn("finance", domains)
        self.assertIn("content_moderation", domains)
        self.assertIn("security", domains)

    def test_get_metric_pack_hiring(self):
        """Verify get_metric_pack returns HIRING_METRIC_PACK for 'hiring' domain."""
        pack = get_metric_pack("hiring")
        self.assertIsNotNone(pack)
        self.assertEqual(pack.domain, "hiring")
        self.assertIs(pack, HIRING_METRIC_PACK)

    def test_get_metric_pack_healthcare(self):
        """Verify get_metric_pack returns HEALTHCARE_METRIC_PACK for 'healthcare' domain."""
        pack = get_metric_pack("healthcare")
        self.assertIsNotNone(pack)
        self.assertEqual(pack.domain, "healthcare")
        self.assertIs(pack, HEALTHCARE_METRIC_PACK)

    def test_get_metric_pack_finance(self):
        """Verify get_metric_pack returns FINANCE_METRIC_PACK for 'finance' domain."""
        pack = get_metric_pack("finance")
        self.assertIsNotNone(pack)
        self.assertEqual(pack.domain, "finance")
        self.assertIs(pack, FINANCE_METRIC_PACK)

    def test_get_metric_pack_content_moderation(self):
        """Verify get_metric_pack returns CONTENT_MODERATION_PACK for 'content_moderation' domain."""
        pack = get_metric_pack("content_moderation")
        self.assertIsNotNone(pack)
        self.assertEqual(pack.domain, "content_moderation")
        self.assertIs(pack, CONTENT_MODERATION_PACK)

    def test_get_metric_pack_security(self):
        """Verify get_metric_pack returns SECURITY_METRIC_PACK for 'security' domain."""
        pack = get_metric_pack("security")
        self.assertIsNotNone(pack)
        self.assertEqual(pack.domain, "security")
        self.assertIs(pack, SECURITY_METRIC_PACK)

    def test_get_metric_pack_case_insensitive(self):
        """Verify get_metric_pack is case-insensitive."""
        pack = get_metric_pack("HIRING")
        self.assertIsNotNone(pack)
        self.assertEqual(pack.domain, "hiring")

    def test_get_metric_pack_unknown_domain_returns_none(self):
        """Verify get_metric_pack returns None for unknown domain."""
        pack = get_metric_pack("unknown_domain")
        self.assertIsNone(pack)


class TestSeverityThresholds(unittest.TestCase):
    """Test severity threshold structure across all packs."""

    def test_hiring_has_four_severity_thresholds(self):
        """Verify hiring pack has 4 severity thresholds."""
        pack = get_metric_pack("hiring")
        self.assertEqual(len(pack.severity_thresholds), 4)

    def test_healthcare_has_four_severity_thresholds(self):
        """Verify healthcare pack has 4 severity thresholds."""
        pack = get_metric_pack("healthcare")
        self.assertEqual(len(pack.severity_thresholds), 4)

    def test_finance_has_four_severity_thresholds(self):
        """Verify finance pack has 4 severity thresholds."""
        pack = get_metric_pack("finance")
        self.assertEqual(len(pack.severity_thresholds), 4)

    def test_content_moderation_has_four_severity_thresholds(self):
        """Verify content moderation pack has 4 severity thresholds."""
        pack = get_metric_pack("content_moderation")
        self.assertEqual(len(pack.severity_thresholds), 4)

    def test_security_has_four_severity_thresholds(self):
        """Verify security pack has 4 severity thresholds."""
        pack = get_metric_pack("security")
        self.assertEqual(len(pack.severity_thresholds), 4)

    def test_severity_thresholds_use_correct_impact_levels(self):
        """Verify all packs use correct ImpactLevel values in correct order."""
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            self.assertEqual(pack.severity_thresholds[0].level, ImpactLevel.TRIVIAL)
            self.assertEqual(pack.severity_thresholds[1].level, ImpactLevel.MODERATE)
            self.assertEqual(pack.severity_thresholds[2].level, ImpactLevel.SEVERE)
            self.assertEqual(pack.severity_thresholds[3].level, ImpactLevel.CATASTROPHIC)

    def test_severity_thresholds_have_descriptions(self):
        """Verify all severity thresholds have non-empty descriptions."""
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            for threshold in pack.severity_thresholds:
                self.assertIsNotNone(threshold.description)
                self.assertTrue(len(threshold.description) > 0)

    def test_severity_thresholds_have_metric_examples(self):
        """Verify all severity thresholds have non-empty metric examples."""
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            for threshold in pack.severity_thresholds:
                self.assertIsNotNone(threshold.metric_example)
                self.assertTrue(len(threshold.metric_example) > 0)

    def test_healthcare_catastrophic_mentions_death_or_disability(self):
        """Verify healthcare catastrophic threshold mentions death or disability."""
        pack = get_metric_pack("healthcare")
        catastrophic = pack.severity_thresholds[3]
        self.assertEqual(catastrophic.level, ImpactLevel.CATASTROPHIC)
        combined_text = (catastrophic.description + " " + catastrophic.metric_example).lower()
        # Check for death or disability keywords
        self.assertTrue(
            "death" in combined_text or "disability" in combined_text,
            "Healthcare catastrophic should mention death or disability"
        )


class TestReversibilityStandards(unittest.TestCase):
    """Test reversibility standards structure across all packs."""

    def test_all_packs_have_reversibility_standards(self):
        """Verify all packs have non-empty reversibility_standards."""
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            self.assertGreater(len(pack.reversibility_standards), 0)

    def test_reversibility_cost_factor_is_positive(self):
        """Verify all reversibility cost factors are positive."""
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            for harm_type, reversibility_def in pack.reversibility_standards.items():
                self.assertGreater(
                    reversibility_def.reversal_cost_factor,
                    0,
                    f"{domain}/{harm_type}: reversal_cost_factor must be positive"
                )

    def test_hiring_has_discrimination_reversibility(self):
        """Verify hiring pack has 'discrimination' reversibility definition."""
        pack = get_metric_pack("hiring")
        self.assertIn("discrimination", pack.reversibility_standards)
        discrim = pack.reversibility_standards["discrimination"]
        self.assertFalse(discrim.is_reversible)

    def test_finance_has_lending_discrimination_reversibility(self):
        """Verify finance pack has 'lending_discrimination' reversibility definition."""
        pack = get_metric_pack("finance")
        self.assertIn("lending_discrimination", pack.reversibility_standards)
        lending_discrim = pack.reversibility_standards["lending_discrimination"]
        self.assertFalse(lending_discrim.is_reversible)

    def test_security_has_identity_theft_reversibility(self):
        """Verify security pack has 'identity_theft' reversibility definition."""
        pack = get_metric_pack("security")
        self.assertIn("identity_theft", pack.reversibility_standards)
        identity_theft = pack.reversibility_standards["identity_theft"]
        self.assertFalse(identity_theft.is_reversible)

    def test_content_moderation_has_account_suspension(self):
        """Verify content moderation pack has 'account_suspension' reversibility definition."""
        pack = get_metric_pack("content_moderation")
        self.assertIn("account_suspension", pack.reversibility_standards)
        account_susp = pack.reversibility_standards["account_suspension"]
        self.assertFalse(account_susp.is_reversible)

    def test_reversibility_has_required_fields(self):
        """Verify all reversibility definitions have required fields."""
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            for harm_type, rev_def in pack.reversibility_standards.items():
                self.assertIsNotNone(rev_def.is_reversible)
                self.assertIsNotNone(rev_def.reversal_timeframe)
                self.assertIsNotNone(rev_def.reversal_mechanism)
                self.assertIsNotNone(rev_def.reversal_cost_factor)
                self.assertIsNotNone(rev_def.downstream_irreversibility)


class TestStakeholderTemplates(unittest.TestCase):
    """Test stakeholder template structure across all packs."""

    def test_all_packs_have_stakeholder_templates(self):
        """Verify all packs have non-empty stakeholder_templates."""
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            self.assertGreater(len(pack.stakeholder_templates), 0)

    def test_stakeholder_templates_have_required_fields(self):
        """Verify all stakeholder templates have required fields."""
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            for template in pack.stakeholder_templates:
                self.assertIsNotNone(template.role)
                self.assertTrue(len(template.role) > 0)
                self.assertIsNotNone(template.power_relative_to_decision_maker)
                self.assertTrue(len(template.power_relative_to_decision_maker) > 0)
                self.assertIsNotNone(template.primary_harm_types)
                self.assertGreater(len(template.primary_harm_types), 0)
                self.assertIsNotNone(template.vulnerability_flags)
                self.assertIsNotNone(template.consent_capability)
                self.assertTrue(len(template.consent_capability) > 0)

    def test_stakeholder_consent_capability_valid_values(self):
        """Verify stakeholder consent_capability uses valid values: 'yes', 'partially', 'no'."""
        valid_values = {"yes", "partially", "no"}
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            for template in pack.stakeholder_templates:
                self.assertIn(
                    template.consent_capability,
                    valid_values,
                    f"{domain}/{template.role}: invalid consent_capability '{template.consent_capability}'"
                )

    def test_stakeholder_power_levels_valid(self):
        """Verify stakeholder power_relative_to_decision_maker uses valid values."""
        valid_values = {"minimal", "low", "moderate", "high"}
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            for template in pack.stakeholder_templates:
                self.assertIn(
                    template.power_relative_to_decision_maker,
                    valid_values,
                    f"{domain}/{template.role}: invalid power level '{template.power_relative_to_decision_maker}'"
                )


class TestDomainSpecificContent(unittest.TestCase):
    """Test domain-specific vulnerability factors and amplification vectors."""

    def test_all_packs_have_vulnerability_factors(self):
        """Verify all packs have non-empty domain_specific_vulnerability_factors."""
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            self.assertGreater(
                len(pack.domain_specific_vulnerability_factors),
                0,
                f"{domain}: missing domain_specific_vulnerability_factors"
            )

    def test_all_packs_have_amplification_vectors(self):
        """Verify all packs have non-empty amplification_vectors."""
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            self.assertGreater(
                len(pack.amplification_vectors),
                0,
                f"{domain}: missing amplification_vectors"
            )

    def test_all_packs_have_regulation_notes(self):
        """Verify all packs have non-empty regulation_notes."""
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            self.assertIsNotNone(pack.regulation_notes)
            self.assertGreater(
                len(pack.regulation_notes),
                0,
                f"{domain}: missing regulation_notes"
            )


class TestPackVersions(unittest.TestCase):
    """Test metric pack versions."""

    def test_all_packs_have_version_1_0(self):
        """Verify all metric packs have version '1.0'."""
        for domain in ["hiring", "healthcare", "finance", "content_moderation", "security"]:
            pack = get_metric_pack(domain)
            self.assertEqual(pack.version, "1.0")


class TestHiringMetricPack(unittest.TestCase):
    """Specific tests for hiring metric pack."""

    def setUp(self):
        self.pack = get_metric_pack("hiring")

    def test_hiring_domain_name(self):
        """Verify hiring pack domain is 'hiring'."""
        self.assertEqual(self.pack.domain, "hiring")

    def test_hiring_has_discrimination_reversibility(self):
        """Verify hiring pack has irreversible discrimination harm."""
        self.assertIn("discrimination", self.pack.reversibility_standards)
        self.assertFalse(self.pack.reversibility_standards["discrimination"].is_reversible)

    def test_hiring_has_two_stakeholder_templates(self):
        """Verify hiring pack has job applicant and hired employee stakeholders."""
        self.assertEqual(len(self.pack.stakeholder_templates), 2)
        roles = [s.role for s in self.pack.stakeholder_templates]
        self.assertIn("job applicant", roles)
        self.assertIn("hired employee", roles)


class TestHealthcareMetricPack(unittest.TestCase):
    """Specific tests for healthcare metric pack."""

    def setUp(self):
        self.pack = get_metric_pack("healthcare")

    def test_healthcare_domain_name(self):
        """Verify healthcare pack domain is 'healthcare'."""
        self.assertEqual(self.pack.domain, "healthcare")

    def test_healthcare_catastrophic_mentions_death(self):
        """Verify healthcare catastrophic level mentions death or permanent disability."""
        catastrophic = self.pack.severity_thresholds[3]
        combined = (catastrophic.description + " " + catastrophic.metric_example).lower()
        self.assertTrue("death" in combined or "disability" in combined)

    def test_healthcare_has_misdiagnosis_reversibility(self):
        """Verify healthcare pack has irreversible misdiagnosis harm."""
        self.assertIn("misdiagnosis", self.pack.reversibility_standards)
        self.assertFalse(self.pack.reversibility_standards["misdiagnosis"].is_reversible)

    def test_healthcare_has_two_stakeholder_templates(self):
        """Verify healthcare pack has patient stakeholders."""
        self.assertEqual(len(self.pack.stakeholder_templates), 2)
        roles = [s.role for s in self.pack.stakeholder_templates]
        self.assertIn("patient", roles)
        self.assertIn("vulnerable patient", roles)


class TestFinanceMetricPack(unittest.TestCase):
    """Specific tests for finance metric pack."""

    def setUp(self):
        self.pack = get_metric_pack("finance")

    def test_finance_domain_name(self):
        """Verify finance pack domain is 'finance'."""
        self.assertEqual(self.pack.domain, "finance")

    def test_finance_has_lending_discrimination_reversibility(self):
        """Verify finance pack has irreversible lending discrimination harm."""
        self.assertIn("lending_discrimination", self.pack.reversibility_standards)
        self.assertFalse(self.pack.reversibility_standards["lending_discrimination"].is_reversible)

    def test_finance_has_two_stakeholder_templates(self):
        """Verify finance pack has retail customer and underserved population."""
        self.assertEqual(len(self.pack.stakeholder_templates), 2)
        roles = [s.role for s in self.pack.stakeholder_templates]
        self.assertIn("retail customer", roles)
        self.assertIn("underserved population", roles)


class TestContentModerationMetricPack(unittest.TestCase):
    """Specific tests for content moderation metric pack."""

    def setUp(self):
        self.pack = get_metric_pack("content_moderation")

    def test_content_moderation_domain_name(self):
        """Verify content moderation pack domain is 'content_moderation'."""
        self.assertEqual(self.pack.domain, "content_moderation")

    def test_content_moderation_has_account_suspension_reversibility(self):
        """Verify content moderation pack has irreversible account suspension harm."""
        self.assertIn("account_suspension", self.pack.reversibility_standards)
        self.assertFalse(self.pack.reversibility_standards["account_suspension"].is_reversible)

    def test_content_moderation_has_two_stakeholder_templates(self):
        """Verify content moderation pack has content creator and activist stakeholders."""
        self.assertEqual(len(self.pack.stakeholder_templates), 2)
        roles = [s.role for s in self.pack.stakeholder_templates]
        self.assertIn("content creator", roles)
        self.assertIn("activist/organizer", roles)


class TestSecurityMetricPack(unittest.TestCase):
    """Specific tests for security metric pack."""

    def setUp(self):
        self.pack = get_metric_pack("security")

    def test_security_domain_name(self):
        """Verify security pack domain is 'security'."""
        self.assertEqual(self.pack.domain, "security")

    def test_security_has_identity_theft_reversibility(self):
        """Verify security pack has irreversible identity theft harm."""
        self.assertIn("identity_theft", self.pack.reversibility_standards)
        self.assertFalse(self.pack.reversibility_standards["identity_theft"].is_reversible)

    def test_security_has_two_stakeholder_templates(self):
        """Verify security pack has platform user and infrastructure operator stakeholders."""
        self.assertEqual(len(self.pack.stakeholder_templates), 2)
        roles = [s.role for s in self.pack.stakeholder_templates]
        self.assertIn("platform user", roles)
        self.assertIn("critical infrastructure operator", roles)


class TestDataclassStructure(unittest.TestCase):
    """Test dataclass structures and validation."""

    def test_severity_threshold_dataclass(self):
        """Test SeverityThreshold dataclass can be instantiated."""
        threshold = SeverityThreshold(
            level=ImpactLevel.TRIVIAL,
            description="Test description",
            metric_example="Test example",
        )
        self.assertEqual(threshold.level, ImpactLevel.TRIVIAL)
        self.assertEqual(threshold.description, "Test description")
        self.assertEqual(threshold.metric_example, "Test example")

    def test_reversibility_definition_dataclass(self):
        """Test ReversibilityDefinition dataclass can be instantiated."""
        rev_def = ReversibilityDefinition(
            is_reversible=True,
            reversal_timeframe="days",
            reversal_mechanism="Test mechanism",
            reversal_cost_factor=1.5,
            downstream_irreversibility=False,
        )
        self.assertTrue(rev_def.is_reversible)
        self.assertEqual(rev_def.reversal_timeframe, "days")
        self.assertEqual(rev_def.reversal_cost_factor, 1.5)

    def test_stakeholder_template_dataclass(self):
        """Test StakeholderTemplate dataclass can be instantiated."""
        template = StakeholderTemplate(
            role="test role",
            power_relative_to_decision_maker="low",
            primary_harm_types=["harm1", "harm2"],
            vulnerability_flags=["flag1"],
            consent_capability="yes",
        )
        self.assertEqual(template.role, "test role")
        self.assertEqual(template.power_relative_to_decision_maker, "low")

    def test_metric_pack_dataclass(self):
        """Test MetricPack dataclass can be instantiated."""
        pack = MetricPack(domain="test")
        self.assertEqual(pack.domain, "test")
        self.assertEqual(pack.version, "1.0")
        self.assertEqual(len(pack.severity_thresholds), 0)


if __name__ == "__main__":
    unittest.main()
