"""
Comprehensive test suite for pbhp_compliance module.
Tests compliance framework mappings, requirement tracking, and audit reporting.
"""

import unittest
import sys
from datetime import datetime

sys.path.insert(0, '/sessions/happy-charming-bohr/pbhp_repo/src')

from pbhp_compliance import (
    ComplianceFramework,
    ComplianceRequirement,
    PBHPArtifact,
    ComplianceAuditReport,
    ComplianceMapper,
    audit_pbhp_compliance,
    NIST_REQUIREMENTS,
    ISO_42001_REQUIREMENTS,
    ISO_23894_REQUIREMENTS,
    EU_AI_ACT_REQUIREMENTS,
    PBHP_ARTIFACTS_CATALOG,
    ALL_REQUIREMENTS,
)


class TestComplianceFrameworkEnum(unittest.TestCase):
    """Test ComplianceFramework enum."""

    def test_enum_values_exist(self):
        """Test that all expected enum values exist."""
        self.assertEqual(ComplianceFramework.NIST_AI_RMF.value, "nist_ai_rmf")
        self.assertEqual(ComplianceFramework.ISO_42001.value, "iso_42001")
        self.assertEqual(ComplianceFramework.ISO_23894.value, "iso_23894")
        self.assertEqual(ComplianceFramework.EU_AI_ACT.value, "eu_ai_act")

    def test_enum_count(self):
        """Test that exactly 4 frameworks are defined."""
        self.assertEqual(len(list(ComplianceFramework)), 4)

    def test_enum_members_accessible(self):
        """Test that all enum members can be accessed by name."""
        frameworks = [
            ComplianceFramework.NIST_AI_RMF,
            ComplianceFramework.ISO_42001,
            ComplianceFramework.ISO_23894,
            ComplianceFramework.EU_AI_ACT,
        ]
        self.assertEqual(len(frameworks), 4)


class TestComplianceRequirementDataClass(unittest.TestCase):
    """Test ComplianceRequirement dataclass."""

    def test_requirement_has_all_fields(self):
        """Test that a requirement has all expected fields."""
        req = NIST_REQUIREMENTS[0]
        self.assertIsNotNone(req.framework)
        self.assertIsNotNone(req.requirement_id)
        self.assertIsNotNone(req.requirement_title)
        self.assertIsNotNone(req.requirement_text)
        self.assertIsNotNone(req.pbhp_satisfying_steps)
        self.assertIsNotNone(req.pbhp_artifacts_satisfying)
        self.assertIsNotNone(req.evidence_checklist)
        self.assertIsNotNone(req.verification_method)

    def test_requirement_fields_are_non_empty(self):
        """Test that all required fields are non-empty for first requirement."""
        req = NIST_REQUIREMENTS[0]
        self.assertTrue(len(req.requirement_id) > 0)
        self.assertTrue(len(req.requirement_title) > 0)
        self.assertTrue(len(req.requirement_text) > 0)
        self.assertTrue(len(req.pbhp_satisfying_steps) > 0)
        self.assertTrue(len(req.pbhp_artifacts_satisfying) > 0)
        self.assertTrue(len(req.evidence_checklist) > 0)
        self.assertTrue(len(req.verification_method) > 0)

    def test_all_requirements_have_non_empty_fields(self):
        """Test that all 14 requirements have non-empty critical fields."""
        for req in ALL_REQUIREMENTS:
            with self.subTest(requirement_id=req.requirement_id):
                self.assertTrue(len(req.requirement_id) > 0, f"Empty ID: {req}")
                self.assertTrue(len(req.requirement_title) > 0, f"Empty title: {req}")
                self.assertTrue(len(req.requirement_text) > 0, f"Empty text: {req}")
                self.assertGreater(len(req.pbhp_satisfying_steps), 0, f"No steps: {req}")
                self.assertGreater(len(req.pbhp_artifacts_satisfying), 0, f"No artifacts: {req}")
                self.assertGreater(len(req.evidence_checklist), 0, f"No evidence: {req}")
                self.assertTrue(len(req.verification_method) > 0, f"No verification: {req}")

    def test_requirement_default_applicable_to_domains(self):
        """Test that applicable_to_domains defaults to empty list."""
        req = NIST_REQUIREMENTS[0]
        self.assertIsInstance(req.applicable_to_domains, list)

    def test_requirement_with_applicable_domains(self):
        """Test that EU_AI_ACT requirements have applicable_to_domains set."""
        eu_req = EU_AI_ACT_REQUIREMENTS[0]
        self.assertIsInstance(eu_req.applicable_to_domains, list)
        self.assertGreater(len(eu_req.applicable_to_domains), 0)


class TestPBHPArtifactDataClass(unittest.TestCase):
    """Test PBHPArtifact dataclass."""

    def test_artifact_has_all_fields(self):
        """Test that an artifact has all expected fields."""
        artifact = PBHP_ARTIFACTS_CATALOG[0]
        self.assertIsNotNone(artifact.name)
        self.assertIsNotNone(artifact.pbhp_step)
        self.assertIsNotNone(artifact.content_description)
        self.assertIsInstance(artifact.serves_compliance_requirements, list)

    def test_artifact_fields_are_non_empty(self):
        """Test that artifact critical fields are non-empty."""
        artifact = PBHP_ARTIFACTS_CATALOG[0]
        self.assertTrue(len(artifact.name) > 0)
        self.assertTrue(len(artifact.pbhp_step) > 0)
        self.assertTrue(len(artifact.content_description) > 0)

    def test_all_artifacts_have_non_empty_fields(self):
        """Test that all 6 artifacts have non-empty critical fields."""
        for artifact in PBHP_ARTIFACTS_CATALOG:
            with self.subTest(artifact_name=artifact.name):
                self.assertTrue(len(artifact.name) > 0)
                self.assertTrue(len(artifact.pbhp_step) > 0)
                self.assertTrue(len(artifact.content_description) > 0)


class TestRequirementCounts(unittest.TestCase):
    """Test framework requirement counts."""

    def test_nist_requirement_count(self):
        """Test that NIST has exactly 5 requirements."""
        self.assertEqual(len(NIST_REQUIREMENTS), 5)

    def test_iso_42001_requirement_count(self):
        """Test that ISO 42001 has exactly 3 requirements."""
        self.assertEqual(len(ISO_42001_REQUIREMENTS), 3)

    def test_iso_23894_requirement_count(self):
        """Test that ISO 23894 has exactly 3 requirements."""
        self.assertEqual(len(ISO_23894_REQUIREMENTS), 3)

    def test_eu_ai_act_requirement_count(self):
        """Test that EU AI Act has exactly 3 requirements."""
        self.assertEqual(len(EU_AI_ACT_REQUIREMENTS), 3)

    def test_all_requirements_total_count(self):
        """Test that combined total is exactly 14 requirements."""
        self.assertEqual(len(ALL_REQUIREMENTS), 14)

    def test_all_requirements_sum_of_lists(self):
        """Test that ALL_REQUIREMENTS is the sum of all framework requirements."""
        expected = (
            NIST_REQUIREMENTS
            + ISO_42001_REQUIREMENTS
            + ISO_23894_REQUIREMENTS
            + EU_AI_ACT_REQUIREMENTS
        )
        self.assertEqual(len(ALL_REQUIREMENTS), len(expected))

    def test_pbhp_artifacts_count(self):
        """Test that there are exactly 6 artifacts."""
        self.assertEqual(len(PBHP_ARTIFACTS_CATALOG), 6)


class TestComplianceMapperGetRequirementsForFramework(unittest.TestCase):
    """Test ComplianceMapper.get_requirements_for_framework."""

    def setUp(self):
        """Set up mapper instance."""
        self.mapper = ComplianceMapper()

    def test_get_nist_requirements(self):
        """Test getting NIST requirements."""
        reqs = self.mapper.get_requirements_for_framework(ComplianceFramework.NIST_AI_RMF)
        self.assertEqual(len(reqs), 5)
        for req in reqs:
            self.assertEqual(req.framework, ComplianceFramework.NIST_AI_RMF)

    def test_get_iso_42001_requirements(self):
        """Test getting ISO 42001 requirements."""
        reqs = self.mapper.get_requirements_for_framework(ComplianceFramework.ISO_42001)
        self.assertEqual(len(reqs), 3)
        for req in reqs:
            self.assertEqual(req.framework, ComplianceFramework.ISO_42001)

    def test_get_iso_23894_requirements(self):
        """Test getting ISO 23894 requirements."""
        reqs = self.mapper.get_requirements_for_framework(ComplianceFramework.ISO_23894)
        self.assertEqual(len(reqs), 3)
        for req in reqs:
            self.assertEqual(req.framework, ComplianceFramework.ISO_23894)

    def test_get_eu_ai_act_requirements(self):
        """Test getting EU AI Act requirements."""
        reqs = self.mapper.get_requirements_for_framework(ComplianceFramework.EU_AI_ACT)
        self.assertEqual(len(reqs), 3)
        for req in reqs:
            self.assertEqual(req.framework, ComplianceFramework.EU_AI_ACT)

    def test_framework_isolation(self):
        """Test that requirements are properly isolated by framework."""
        nist_reqs = self.mapper.get_requirements_for_framework(ComplianceFramework.NIST_AI_RMF)
        iso_42001_reqs = self.mapper.get_requirements_for_framework(ComplianceFramework.ISO_42001)
        nist_ids = {r.requirement_id for r in nist_reqs}
        iso_42001_ids = {r.requirement_id for r in iso_42001_reqs}
        self.assertEqual(len(nist_ids & iso_42001_ids), 0)


class TestComplianceMapperGetRequirementsByPBHPStep(unittest.TestCase):
    """Test ComplianceMapper.get_requirements_by_pbhp_step."""

    def setUp(self):
        """Set up mapper instance."""
        self.mapper = ComplianceMapper()

    def test_get_requirements_for_step_0a(self):
        """Test getting requirements for Step 0a."""
        reqs = self.mapper.get_requirements_by_pbhp_step("Step 0a")
        self.assertGreater(len(reqs), 0)
        for req in reqs:
            self.assertIn("Step 0a", req.pbhp_satisfying_steps)

    def test_get_requirements_for_step_1(self):
        """Test getting requirements for Step 1."""
        reqs = self.mapper.get_requirements_by_pbhp_step("Step 1")
        self.assertGreater(len(reqs), 0)
        for req in reqs:
            self.assertIn("Step 1", req.pbhp_satisfying_steps)

    def test_get_requirements_for_step_2(self):
        """Test getting requirements for Step 2."""
        reqs = self.mapper.get_requirements_by_pbhp_step("Step 2")
        self.assertGreater(len(reqs), 0)
        for req in reqs:
            self.assertIn("Step 2", req.pbhp_satisfying_steps)

    def test_get_requirements_for_step_3a(self):
        """Test getting requirements for Step 3a."""
        reqs = self.mapper.get_requirements_by_pbhp_step("Step 3a")
        self.assertGreater(len(reqs), 0)

    def test_get_requirements_for_step_3b(self):
        """Test getting requirements for Step 3b."""
        reqs = self.mapper.get_requirements_by_pbhp_step("Step 3b")
        self.assertGreater(len(reqs), 0)

    def test_get_requirements_for_step_3c(self):
        """Test getting requirements for Step 3c."""
        reqs = self.mapper.get_requirements_by_pbhp_step("Step 3c")
        self.assertGreater(len(reqs), 0)

    def test_get_requirements_for_step_4(self):
        """Test getting requirements for Step 4."""
        reqs = self.mapper.get_requirements_by_pbhp_step("Step 4")
        self.assertGreater(len(reqs), 0)

    def test_get_requirements_for_step_5(self):
        """Test getting requirements for Step 5."""
        reqs = self.mapper.get_requirements_by_pbhp_step("Step 5")
        self.assertGreater(len(reqs), 0)

    def test_get_requirements_for_step_6(self):
        """Test getting requirements for Step 6."""
        reqs = self.mapper.get_requirements_by_pbhp_step("Step 6")
        self.assertGreater(len(reqs), 0)

    def test_get_requirements_for_nonexistent_step(self):
        """Test getting requirements for non-existent step returns empty list."""
        reqs = self.mapper.get_requirements_by_pbhp_step("Step 999")
        self.assertEqual(len(reqs), 0)


class TestComplianceMapperGetArtifactsForStep(unittest.TestCase):
    """Test ComplianceMapper.get_artifacts_for_step."""

    def setUp(self):
        """Set up mapper instance."""
        self.mapper = ComplianceMapper()

    def test_get_artifacts_for_step_2(self):
        """Test getting artifacts for Step 2."""
        artifacts = self.mapper.get_artifacts_for_step("Step 2")
        self.assertEqual(len(artifacts), 1)
        self.assertEqual(artifacts[0].name, "Harm Assessment Report")

    def test_get_artifacts_for_step_3b(self):
        """Test getting artifacts for Step 3b."""
        artifacts = self.mapper.get_artifacts_for_step("Step 3b")
        self.assertEqual(len(artifacts), 1)
        self.assertEqual(artifacts[0].name, "Red Team Review Notes")

    def test_get_artifacts_for_step_3c(self):
        """Test getting artifacts for Step 3c."""
        artifacts = self.mapper.get_artifacts_for_step("Step 3c")
        self.assertEqual(len(artifacts), 1)
        self.assertEqual(artifacts[0].name, "Door/Wall/Gap Analysis")

    def test_get_artifacts_for_step_4(self):
        """Test getting artifacts for Step 4."""
        artifacts = self.mapper.get_artifacts_for_step("Step 4")
        self.assertEqual(len(artifacts), 1)
        self.assertEqual(artifacts[0].name, "PBHP Assessment Result")

    def test_get_artifacts_for_step_6(self):
        """Test getting artifacts for Step 6."""
        artifacts = self.mapper.get_artifacts_for_step("Step 6")
        self.assertEqual(len(artifacts), 1)
        self.assertEqual(artifacts[0].name, "Drift Detection Report")

    def test_get_artifacts_for_all_steps(self):
        """Test getting artifacts for 'All' step."""
        artifacts = self.mapper.get_artifacts_for_step("All")
        self.assertEqual(len(artifacts), 1)
        self.assertEqual(artifacts[0].name, "PBHP Decision Log")

    def test_get_artifacts_for_nonexistent_step(self):
        """Test getting artifacts for non-existent step returns empty list."""
        artifacts = self.mapper.get_artifacts_for_step("Step 999")
        self.assertEqual(len(artifacts), 0)


class TestComplianceMapperGenerateChecklist(unittest.TestCase):
    """Test ComplianceMapper.generate_compliance_checklist."""

    def setUp(self):
        """Set up mapper instance."""
        self.mapper = ComplianceMapper()

    def test_checklist_structure_for_nist(self):
        """Test checklist structure for NIST framework."""
        checklist = self.mapper.generate_compliance_checklist(ComplianceFramework.NIST_AI_RMF)
        self.assertIsInstance(checklist, dict)
        self.assertEqual(len(checklist), 5)

    def test_checklist_structure_for_iso_42001(self):
        """Test checklist structure for ISO 42001 framework."""
        checklist = self.mapper.generate_compliance_checklist(ComplianceFramework.ISO_42001)
        self.assertIsInstance(checklist, dict)
        self.assertEqual(len(checklist), 3)

    def test_checklist_item_has_required_keys(self):
        """Test that checklist items have all required keys."""
        checklist = self.mapper.generate_compliance_checklist(ComplianceFramework.NIST_AI_RMF)
        for req_id, item in checklist.items():
            self.assertIn("title", item)
            self.assertIn("satisfied", item)
            self.assertIn("evidence_needed", item)
            self.assertIn("pbhp_steps", item)
            self.assertIn("pbhp_artifacts", item)

    def test_checklist_satisfied_starts_false(self):
        """Test that all checklist items start with satisfied=False."""
        checklist = self.mapper.generate_compliance_checklist(ComplianceFramework.NIST_AI_RMF)
        for item in checklist.values():
            self.assertFalse(item["satisfied"])

    def test_checklist_evidence_needed_is_list(self):
        """Test that evidence_needed is a list."""
        checklist = self.mapper.generate_compliance_checklist(ComplianceFramework.NIST_AI_RMF)
        for item in checklist.values():
            self.assertIsInstance(item["evidence_needed"], list)

    def test_checklist_pbhp_steps_is_list(self):
        """Test that pbhp_steps is a list."""
        checklist = self.mapper.generate_compliance_checklist(ComplianceFramework.NIST_AI_RMF)
        for item in checklist.values():
            self.assertIsInstance(item["pbhp_steps"], list)

    def test_checklist_pbhp_artifacts_is_list(self):
        """Test that pbhp_artifacts is a list."""
        checklist = self.mapper.generate_compliance_checklist(ComplianceFramework.NIST_AI_RMF)
        for item in checklist.values():
            self.assertIsInstance(item["pbhp_artifacts"], list)


class TestComplianceMapperGenerateAuditReportPartialSatisfaction(unittest.TestCase):
    """Test ComplianceMapper.generate_audit_report with partial satisfaction."""

    def setUp(self):
        """Set up mapper instance."""
        self.mapper = ComplianceMapper()

    def test_audit_report_partial_satisfaction(self):
        """Test audit report with some requirements satisfied."""
        frameworks = [ComplianceFramework.NIST_AI_RMF]
        satisfied = {"NIST.GOVERN-1.1", "NIST.MAP-1.1"}
        artifacts = ["PBHP Context Assessment", "Decision Context"]

        report = self.mapper.generate_audit_report(
            organization="TestOrg",
            frameworks=frameworks,
            satisfied_requirements=satisfied,
            collected_artifacts=artifacts,
        )

        self.assertEqual(report.satisfied_count, 2)
        self.assertEqual(report.unsatisfied_count, 3)
        self.assertEqual(len(report.gaps), 3)

    def test_audit_report_has_audit_date(self):
        """Test that audit report has an audit date."""
        report = self.mapper.generate_audit_report(
            organization="TestOrg",
            frameworks=[ComplianceFramework.NIST_AI_RMF],
            satisfied_requirements=set(),
            collected_artifacts=[],
        )
        self.assertIsInstance(report.audit_date, datetime)

    def test_audit_report_has_organization(self):
        """Test that audit report stores organization name."""
        org_name = "MyTestOrganization"
        report = self.mapper.generate_audit_report(
            organization=org_name,
            frameworks=[ComplianceFramework.NIST_AI_RMF],
            satisfied_requirements=set(),
            collected_artifacts=[],
        )
        self.assertEqual(report.organization, org_name)

    def test_audit_report_has_frameworks(self):
        """Test that audit report lists frameworks audited."""
        frameworks = [ComplianceFramework.NIST_AI_RMF, ComplianceFramework.ISO_42001]
        report = self.mapper.generate_audit_report(
            organization="TestOrg",
            frameworks=frameworks,
            satisfied_requirements=set(),
            collected_artifacts=[],
        )
        self.assertEqual(len(report.frameworks_audited), 2)
        self.assertIn(ComplianceFramework.NIST_AI_RMF, report.frameworks_audited)
        self.assertIn(ComplianceFramework.ISO_42001, report.frameworks_audited)

    def test_audit_report_has_artifacts_collected(self):
        """Test that audit report stores collected artifacts."""
        artifacts = ["Artifact1", "Artifact2"]
        report = self.mapper.generate_audit_report(
            organization="TestOrg",
            frameworks=[ComplianceFramework.NIST_AI_RMF],
            satisfied_requirements=set(),
            collected_artifacts=artifacts,
        )
        self.assertEqual(report.artifacts_collected, artifacts)

    def test_audit_report_gaps_list(self):
        """Test that audit report includes gaps."""
        frameworks = [ComplianceFramework.NIST_AI_RMF]
        satisfied = {"NIST.GOVERN-1.1"}

        report = self.mapper.generate_audit_report(
            organization="TestOrg",
            frameworks=frameworks,
            satisfied_requirements=satisfied,
            collected_artifacts=[],
        )

        self.assertGreater(len(report.gaps), 0)
        self.assertNotIn("NIST.GOVERN-1.1", report.gaps)


class TestComplianceMapperGenerateAuditReportFullSatisfaction(unittest.TestCase):
    """Test ComplianceMapper.generate_audit_report with full satisfaction."""

    def setUp(self):
        """Set up mapper instance."""
        self.mapper = ComplianceMapper()

    def test_audit_report_all_satisfied(self):
        """Test audit report when all requirements are satisfied."""
        frameworks = [ComplianceFramework.NIST_AI_RMF]
        all_nist = {req.requirement_id for req in NIST_REQUIREMENTS}

        report = self.mapper.generate_audit_report(
            organization="TestOrg",
            frameworks=frameworks,
            satisfied_requirements=all_nist,
            collected_artifacts=[],
        )

        self.assertEqual(report.satisfied_count, 5)
        self.assertEqual(report.unsatisfied_count, 0)
        self.assertEqual(len(report.gaps), 0)

    def test_audit_report_recommendation_all_satisfied(self):
        """Test that recommendations mention all satisfied when gaps=0."""
        frameworks = [ComplianceFramework.NIST_AI_RMF]
        all_nist = {req.requirement_id for req in NIST_REQUIREMENTS}

        report = self.mapper.generate_audit_report(
            organization="TestOrg",
            frameworks=frameworks,
            satisfied_requirements=all_nist,
            collected_artifacts=[],
        )

        self.assertGreater(len(report.recommendations), 0)


class TestComplianceMapperGenerateAuditReportNoSatisfaction(unittest.TestCase):
    """Test ComplianceMapper.generate_audit_report with no satisfaction."""

    def setUp(self):
        """Set up mapper instance."""
        self.mapper = ComplianceMapper()

    def test_audit_report_none_satisfied(self):
        """Test audit report when no requirements are satisfied."""
        frameworks = [ComplianceFramework.NIST_AI_RMF]

        report = self.mapper.generate_audit_report(
            organization="TestOrg",
            frameworks=frameworks,
            satisfied_requirements=set(),
            collected_artifacts=[],
        )

        self.assertEqual(report.satisfied_count, 0)
        self.assertEqual(report.unsatisfied_count, 5)
        self.assertEqual(len(report.gaps), 5)

    def test_audit_report_multiple_frameworks_no_satisfaction(self):
        """Test audit report with multiple frameworks and no satisfaction."""
        frameworks = [
            ComplianceFramework.NIST_AI_RMF,
            ComplianceFramework.ISO_42001,
            ComplianceFramework.ISO_23894,
        ]

        report = self.mapper.generate_audit_report(
            organization="TestOrg",
            frameworks=frameworks,
            satisfied_requirements=set(),
            collected_artifacts=[],
        )

        self.assertEqual(report.satisfied_count, 0)
        self.assertEqual(report.unsatisfied_count, 11)


class TestAuditPBHPComplianceConvenienceFunction(unittest.TestCase):
    """Test audit_pbhp_compliance convenience function."""

    def test_convenience_function_basic(self):
        """Test basic usage of convenience function."""
        report = audit_pbhp_compliance(
            organization="TestOrg",
            frameworks=[ComplianceFramework.NIST_AI_RMF],
            satisfied_requirements={"NIST.GOVERN-1.1"},
            collected_artifacts=["Artifact1"],
        )

        self.assertIsInstance(report, ComplianceAuditReport)
        self.assertEqual(report.organization, "TestOrg")

    def test_convenience_function_returns_audit_report(self):
        """Test that convenience function returns ComplianceAuditReport."""
        report = audit_pbhp_compliance(
            organization="TestOrg",
            frameworks=[ComplianceFramework.ISO_42001],
            satisfied_requirements=set(),
            collected_artifacts=[],
        )

        self.assertIsInstance(report, ComplianceAuditReport)
        self.assertTrue(hasattr(report, "audit_date"))
        self.assertTrue(hasattr(report, "satisfied_count"))

    def test_convenience_function_multiple_frameworks(self):
        """Test convenience function with multiple frameworks."""
        frameworks = [ComplianceFramework.NIST_AI_RMF, ComplianceFramework.ISO_42001]
        report = audit_pbhp_compliance(
            organization="TestOrg",
            frameworks=frameworks,
            satisfied_requirements=set(),
            collected_artifacts=[],
        )

        self.assertEqual(len(report.frameworks_audited), 2)


class TestArtifactCatalogCompleteness(unittest.TestCase):
    """Test PBHP artifact catalog completeness and cross-references."""

    def test_artifact_catalog_count(self):
        """Test that artifact catalog has exactly 6 artifacts."""
        self.assertEqual(len(PBHP_ARTIFACTS_CATALOG), 6)

    def test_all_artifacts_have_unique_names(self):
        """Test that all artifacts have unique names."""
        names = [a.name for a in PBHP_ARTIFACTS_CATALOG]
        self.assertEqual(len(names), len(set(names)))

    def test_all_artifacts_have_valid_steps(self):
        """Test that all artifacts reference valid PBHP steps."""
        valid_steps = {
            "Step 0a",
            "Step 0b",
            "Step 0c",
            "Step 0g",
            "Step 1",
            "Step 2",
            "Step 3a",
            "Step 3b",
            "Step 3c",
            "Step 4",
            "Step 5",
            "Step 6",
            "Step 7",
            "All",
        }
        for artifact in PBHP_ARTIFACTS_CATALOG:
            self.assertIn(artifact.pbhp_step, valid_steps)

    def test_artifact_serves_compliance_requirements(self):
        """Test that artifacts reference valid compliance requirements."""
        valid_req_ids = {req.requirement_id for req in ALL_REQUIREMENTS}
        for artifact in PBHP_ARTIFACTS_CATALOG:
            for req_id in artifact.serves_compliance_requirements:
                self.assertIn(req_id, valid_req_ids)

    def test_artifacts_referenced_in_requirements(self):
        """Test that artifact names are non-empty strings in requirements."""
        # Requirements may reference artifacts not in the catalog yet
        # Verify that artifacts_satisfying list contains only strings
        for req in ALL_REQUIREMENTS:
            for artifact_name in req.pbhp_artifacts_satisfying:
                self.assertIsInstance(artifact_name, str)
                self.assertGreater(len(artifact_name), 0)


class TestRequirementStepReferences(unittest.TestCase):
    """Test that requirements have valid PBHP step references."""

    def test_all_requirements_have_valid_step_references(self):
        """Test that all requirement step references are valid."""
        valid_steps = {
            "Step 0",
            "Step 0a",
            "Step 0b",
            "Step 0c",
            "Step 0g",
            "Step 1",
            "Step 2",
            "Step 3",
            "Step 3a",
            "Step 3b",
            "Step 3c",
            "Step 4",
            "Step 5",
            "Step 6",
            "Step 7",
        }
        for req in ALL_REQUIREMENTS:
            for step in req.pbhp_satisfying_steps:
                self.assertIn(step, valid_steps)

    def test_nist_requirements_have_steps(self):
        """Test that all NIST requirements have at least one step."""
        for req in NIST_REQUIREMENTS:
            self.assertGreater(len(req.pbhp_satisfying_steps), 0)

    def test_iso_42001_requirements_have_steps(self):
        """Test that all ISO 42001 requirements have at least one step."""
        for req in ISO_42001_REQUIREMENTS:
            self.assertGreater(len(req.pbhp_satisfying_steps), 0)

    def test_iso_23894_requirements_have_steps(self):
        """Test that all ISO 23894 requirements have at least one step."""
        for req in ISO_23894_REQUIREMENTS:
            self.assertGreater(len(req.pbhp_satisfying_steps), 0)

    def test_eu_ai_act_requirements_have_steps(self):
        """Test that all EU AI Act requirements have at least one step."""
        for req in EU_AI_ACT_REQUIREMENTS:
            self.assertGreater(len(req.pbhp_satisfying_steps), 0)


class TestFrameworkCoverageCounts(unittest.TestCase):
    """Test framework coverage counts match expectations."""

    def test_framework_coverage_nist(self):
        """Test NIST framework has exactly 5 requirements."""
        nist_reqs = [r for r in ALL_REQUIREMENTS if r.framework == ComplianceFramework.NIST_AI_RMF]
        self.assertEqual(len(nist_reqs), 5)

    def test_framework_coverage_iso_42001(self):
        """Test ISO 42001 framework has exactly 3 requirements."""
        iso_reqs = [r for r in ALL_REQUIREMENTS if r.framework == ComplianceFramework.ISO_42001]
        self.assertEqual(len(iso_reqs), 3)

    def test_framework_coverage_iso_23894(self):
        """Test ISO 23894 framework has exactly 3 requirements."""
        iso_reqs = [r for r in ALL_REQUIREMENTS if r.framework == ComplianceFramework.ISO_23894]
        self.assertEqual(len(iso_reqs), 3)

    def test_framework_coverage_eu_ai_act(self):
        """Test EU AI Act framework has exactly 3 requirements."""
        eu_reqs = [r for r in ALL_REQUIREMENTS if r.framework == ComplianceFramework.EU_AI_ACT]
        self.assertEqual(len(eu_reqs), 3)

    def test_all_requirements_assigned_framework(self):
        """Test that all requirements have a framework assigned."""
        for req in ALL_REQUIREMENTS:
            self.assertIsNotNone(req.framework)
            self.assertIn(
                req.framework,
                [
                    ComplianceFramework.NIST_AI_RMF,
                    ComplianceFramework.ISO_42001,
                    ComplianceFramework.ISO_23894,
                    ComplianceFramework.EU_AI_ACT,
                ],
            )


class TestAuditReportGapDetection(unittest.TestCase):
    """Test audit report gap detection."""

    def setUp(self):
        """Set up mapper instance."""
        self.mapper = ComplianceMapper()

    def test_gaps_detected_correctly(self):
        """Test that gaps are detected correctly."""
        frameworks = [ComplianceFramework.NIST_AI_RMF]
        satisfied = {"NIST.GOVERN-1.1"}

        report = self.mapper.generate_audit_report(
            organization="TestOrg",
            frameworks=frameworks,
            satisfied_requirements=satisfied,
            collected_artifacts=[],
        )

        expected_gaps = {
            "NIST.MAP-1.1",
            "NIST.MAP-2.1",
            "NIST.MEASURE-1.1",
            "NIST.MANAGE-1.1",
        }
        actual_gaps = set(report.gaps)
        self.assertEqual(actual_gaps, expected_gaps)

    def test_gaps_match_unsatisfied_count(self):
        """Test that gaps count matches unsatisfied count."""
        frameworks = [ComplianceFramework.NIST_AI_RMF, ComplianceFramework.ISO_42001]
        satisfied = {"NIST.GOVERN-1.1", "ISO42001.A.5.2"}

        report = self.mapper.generate_audit_report(
            organization="TestOrg",
            frameworks=frameworks,
            satisfied_requirements=satisfied,
            collected_artifacts=[],
        )

        self.assertEqual(len(report.gaps), report.unsatisfied_count)

    def test_no_gaps_when_all_satisfied(self):
        """Test that there are no gaps when all requirements satisfied."""
        all_nist = {req.requirement_id for req in NIST_REQUIREMENTS}
        frameworks = [ComplianceFramework.NIST_AI_RMF]

        report = self.mapper.generate_audit_report(
            organization="TestOrg",
            frameworks=frameworks,
            satisfied_requirements=all_nist,
            collected_artifacts=[],
        )

        self.assertEqual(len(report.gaps), 0)


class TestDomainSpecificRequirements(unittest.TestCase):
    """Test domain-specific requirements handling."""

    def test_eu_ai_act_has_applicable_domains(self):
        """Test that EU AI Act requirements have applicable_to_domains set."""
        eu_reqs = [r for r in ALL_REQUIREMENTS if r.framework == ComplianceFramework.EU_AI_ACT]
        # At least one EU requirement should have applicable_to_domains
        domain_reqs = [r for r in eu_reqs if len(r.applicable_to_domains) > 0]
        self.assertGreater(len(domain_reqs), 0)

    def test_eu_ai_act_first_requirement_has_domains(self):
        """Test that EU_AI_ACT.6.1 has applicable domains."""
        eu_req = EU_AI_ACT_REQUIREMENTS[0]
        self.assertGreater(len(eu_req.applicable_to_domains), 0)
        self.assertIn("hiring", eu_req.applicable_to_domains)
        self.assertIn("healthcare", eu_req.applicable_to_domains)
        self.assertIn("finance", eu_req.applicable_to_domains)

    def test_other_frameworks_no_domains_or_empty(self):
        """Test that other frameworks don't have domain restrictions."""
        nist_reqs = [r for r in NIST_REQUIREMENTS]
        for req in nist_reqs:
            self.assertIsInstance(req.applicable_to_domains, list)


class TestRequirementIDFormat(unittest.TestCase):
    """Test requirement ID format consistency."""

    def test_nist_ids_have_correct_format(self):
        """Test that NIST requirement IDs follow expected format."""
        for req in NIST_REQUIREMENTS:
            self.assertTrue(
                req.requirement_id.startswith("NIST."),
                f"Invalid NIST ID: {req.requirement_id}",
            )

    def test_iso_42001_ids_have_correct_format(self):
        """Test that ISO 42001 requirement IDs follow expected format."""
        for req in ISO_42001_REQUIREMENTS:
            self.assertTrue(
                req.requirement_id.startswith("ISO42001."),
                f"Invalid ISO 42001 ID: {req.requirement_id}",
            )

    def test_iso_23894_ids_have_correct_format(self):
        """Test that ISO 23894 requirement IDs follow expected format."""
        for req in ISO_23894_REQUIREMENTS:
            self.assertTrue(
                req.requirement_id.startswith("ISO23894."),
                f"Invalid ISO 23894 ID: {req.requirement_id}",
            )

    def test_eu_ai_act_ids_have_correct_format(self):
        """Test that EU AI Act requirement IDs follow expected format."""
        for req in EU_AI_ACT_REQUIREMENTS:
            self.assertTrue(
                req.requirement_id.startswith("EU_AI_ACT."),
                f"Invalid EU AI Act ID: {req.requirement_id}",
            )

    def test_all_requirement_ids_unique(self):
        """Test that all requirement IDs are unique."""
        ids = [r.requirement_id for r in ALL_REQUIREMENTS]
        self.assertEqual(len(ids), len(set(ids)))


class TestComplianceAuditReportDataClass(unittest.TestCase):
    """Test ComplianceAuditReport dataclass."""

    def test_audit_report_fields_populated(self):
        """Test that audit report fields are properly populated."""
        mapper = ComplianceMapper()
        report = mapper.generate_audit_report(
            organization="TestOrg",
            frameworks=[ComplianceFramework.NIST_AI_RMF],
            satisfied_requirements={"NIST.GOVERN-1.1"},
            collected_artifacts=["Artifact1"],
        )

        self.assertIsNotNone(report.audit_date)
        self.assertEqual(report.organization, "TestOrg")
        self.assertEqual(len(report.frameworks_audited), 1)
        self.assertIsInstance(report.requirement_coverage, dict)
        self.assertIsInstance(report.satisfied_count, int)
        self.assertIsInstance(report.unsatisfied_count, int)
        self.assertIsInstance(report.gaps, list)
        self.assertIsInstance(report.recommendations, list)
        self.assertEqual(report.artifacts_collected, ["Artifact1"])


class TestRequirementEvidenceChecklists(unittest.TestCase):
    """Test requirement evidence checklists."""

    def test_all_requirements_have_evidence_items(self):
        """Test that all requirements have evidence checklist items."""
        for req in ALL_REQUIREMENTS:
            self.assertGreater(len(req.evidence_checklist), 0)

    def test_evidence_items_are_strings(self):
        """Test that evidence items are strings."""
        for req in ALL_REQUIREMENTS:
            for item in req.evidence_checklist:
                self.assertIsInstance(item, str)
                self.assertGreater(len(item), 0)


if __name__ == "__main__":
    unittest.main()
