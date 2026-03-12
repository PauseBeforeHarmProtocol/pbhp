"""
Tests for PBHP Bridge Module (pbhp_bridge.py).

Covers community improvements #1-4, #7:
- Coverage gap reporting
- Cross-module subcontracting
- Demonstration > declaration
- Healthcare compliance adapter
- MBSE interface
"""

import unittest
from pbhp_bridge import (
    GapSeverity, CoverageGap, CoverageGapCollector,
    ModuleCapability, SubcontractRequest, SubcontractResponse,
    ModuleRegistry,
    SafetyClaim, SafetyClaimRegistry,
    RegulatoryFramework, RegulatoryMapping,
    HealthcareComplianceAdapter,
    RequirementMapping, MBSEInterface,
)


# ===========================================================================
# Coverage Gap Collector (#7)
# ===========================================================================

class TestCoverageGapCollector(unittest.TestCase):
    """Tests that coverage gaps are collected and prominently reported."""

    def setUp(self):
        self.collector = CoverageGapCollector()

    def test_report_gap(self):
        gap = self.collector.report(
            module="pbhp_srl",
            description="Cannot evaluate multi-agent coordination",
            severity=GapSeverity.WARNING,
        )
        self.assertEqual(len(self.collector.gaps), 1)
        self.assertEqual(gap.module, "pbhp_srl")

    def test_critical_gaps_property(self):
        self.collector.report("m1", "minor thing", GapSeverity.INFO)
        self.collector.report("m2", "big problem", GapSeverity.CRITICAL)
        self.collector.report("m3", "watch out", GapSeverity.WARNING)
        self.assertEqual(len(self.collector.critical_gaps), 1)

    def test_has_critical_gaps(self):
        self.assertFalse(self.collector.has_critical_gaps)
        self.collector.report("m1", "critical issue", GapSeverity.CRITICAL)
        self.assertTrue(self.collector.has_critical_gaps)

    def test_format_prominent_critical_first(self):
        self.collector.report("m1", "info thing", GapSeverity.INFO)
        self.collector.report("m2", "critical blind spot", GapSeverity.CRITICAL)
        output = self.collector.format_prominent()
        # Critical should appear before info
        critical_pos = output.find("CRITICAL")
        info_pos = output.find("INFO")
        self.assertGreater(info_pos, critical_pos)

    def test_format_prominent_header_on_critical(self):
        self.collector.report("m1", "blind spot", GapSeverity.CRITICAL)
        output = self.collector.format_prominent()
        self.assertIn("COVERAGE GAPS", output)
        self.assertIn("CANNOT FULLY EVALUATE", output)

    def test_format_prominent_empty(self):
        output = self.collector.format_prominent()
        self.assertEqual(output, "")

    def test_export(self):
        self.collector.report("m1", "gap1", GapSeverity.WARNING)
        exported = self.collector.export()
        self.assertEqual(len(exported), 1)
        self.assertIn("gap_id", exported[0])
        self.assertEqual(exported[0]["severity"], "warning")

    def test_clear(self):
        self.collector.report("m1", "gap1")
        self.collector.clear()
        self.assertEqual(len(self.collector.gaps), 0)

    def test_gaps_list_is_copy(self):
        self.collector.report("m1", "gap1")
        external = self.collector.gaps
        external.clear()
        self.assertEqual(len(self.collector.gaps), 1)

    def test_mitigation_included_in_output(self):
        self.collector.report(
            "m1", "missing check", GapSeverity.CRITICAL,
            mitigation="Add manual review step",
        )
        output = self.collector.format_prominent()
        self.assertIn("Add manual review step", output)


# ===========================================================================
# Cross-Module Subcontracting (#3)
# ===========================================================================

class TestModuleRegistry(unittest.TestCase):
    """Tests for cross-module capability routing."""

    def setUp(self):
        self.registry = ModuleRegistry()

    def test_register_provider(self):
        self.registry.register_provider(
            "pbhp_drift", ModuleCapability.DRIFT_SNAPSHOT
        )
        providers = self.registry.get_providers(ModuleCapability.DRIFT_SNAPSHOT)
        self.assertEqual(providers, ["pbhp_drift"])

    def test_has_provider(self):
        self.assertFalse(
            self.registry.has_provider(ModuleCapability.DRIFT_SNAPSHOT)
        )
        self.registry.register_provider(
            "pbhp_drift", ModuleCapability.DRIFT_SNAPSHOT
        )
        self.assertTrue(
            self.registry.has_provider(ModuleCapability.DRIFT_SNAPSHOT)
        )

    def test_request_with_handler(self):
        def mock_handler(ctx):
            return {"snapshot": "stable", "score": 0.95}

        self.registry.register_provider(
            "pbhp_drift", ModuleCapability.DRIFT_SNAPSHOT, mock_handler
        )
        resp = self.registry.request(
            "pbhp_srl", ModuleCapability.DRIFT_SNAPSHOT,
            {"window_hours": 24},
        )
        self.assertTrue(resp.success)
        self.assertEqual(resp.providing_module, "pbhp_drift")
        self.assertEqual(resp.result["score"], 0.95)

    def test_request_no_provider(self):
        resp = self.registry.request(
            "pbhp_srl", ModuleCapability.DRIFT_SNAPSHOT
        )
        self.assertFalse(resp.success)
        self.assertIn("No provider", resp.result["error"])

    def test_request_handler_exception(self):
        def bad_handler(ctx):
            raise ValueError("Database down")

        self.registry.register_provider(
            "pbhp_drift", ModuleCapability.DRIFT_SNAPSHOT, bad_handler
        )
        resp = self.registry.request(
            "pbhp_srl", ModuleCapability.DRIFT_SNAPSHOT
        )
        self.assertFalse(resp.success)
        self.assertIn("Database down", resp.result["error"])

    def test_request_no_handler(self):
        self.registry.register_provider(
            "pbhp_drift", ModuleCapability.DRIFT_SNAPSHOT
        )
        resp = self.registry.request(
            "pbhp_srl", ModuleCapability.DRIFT_SNAPSHOT
        )
        self.assertFalse(resp.success)
        self.assertIn("no handler", resp.result["error"])

    def test_get_missing_capabilities(self):
        self.registry.register_provider(
            "pbhp_srl", ModuleCapability.RISK_ASSESSMENT
        )
        required = {
            ModuleCapability.RISK_ASSESSMENT,
            ModuleCapability.DRIFT_SNAPSHOT,
            ModuleCapability.EVIDENCE_LOGGING,
        }
        missing = self.registry.get_missing_capabilities(required)
        self.assertEqual(missing, {
            ModuleCapability.DRIFT_SNAPSHOT,
            ModuleCapability.EVIDENCE_LOGGING,
        })

    def test_multiple_providers(self):
        self.registry.register_provider(
            "module_a", ModuleCapability.RISK_ASSESSMENT
        )
        self.registry.register_provider(
            "module_b", ModuleCapability.RISK_ASSESSMENT
        )
        providers = self.registry.get_providers(ModuleCapability.RISK_ASSESSMENT)
        self.assertEqual(len(providers), 2)

    def test_audit_log(self):
        def handler(ctx):
            return {"ok": True}

        self.registry.register_provider(
            "pbhp_drift", ModuleCapability.DRIFT_SNAPSHOT, handler
        )
        self.registry.request("pbhp_srl", ModuleCapability.DRIFT_SNAPSHOT)
        self.registry.request("pbhp_qs", ModuleCapability.EVIDENCE_LOGGING)

        log = self.registry.get_audit_log()
        self.assertEqual(log["total_requests"], 2)
        self.assertEqual(log["failed_requests"], 1)


# ===========================================================================
# Demonstration > Declaration (#4)
# ===========================================================================

class TestSafetyClaimRegistry(unittest.TestCase):
    """Tests that safety claims require evidence."""

    def setUp(self):
        self.registry = SafetyClaimRegistry()

    def test_claim_with_evidence_is_verified(self):
        claim = self.registry.register_claim(
            "SRL blocks self-preservation",
            "pbhp_srl",
            evidence_type="test",
            evidence_ref="TestAntiSelfPreservation",
        )
        self.assertTrue(claim.verified)

    def test_claim_without_evidence_is_unverified(self):
        claim = self.registry.register_claim(
            "System is safe",
            "pbhp_core",
        )
        self.assertFalse(claim.verified)

    def test_unverified_claims_property(self):
        self.registry.register_claim("claim1", "m1", "test", "ref1")
        self.registry.register_claim("claim2", "m2")
        self.registry.register_claim("claim3", "m3")
        self.assertEqual(len(self.registry.unverified_claims), 2)

    def test_verify_claim(self):
        claim = self.registry.register_claim("claim1", "m1")
        self.assertFalse(claim.verified)
        result = self.registry.verify_claim(
            claim.claim_id, "test", "test_xyz", "human_reviewer"
        )
        self.assertTrue(result)
        self.assertTrue(claim.verified)
        self.assertEqual(claim.verified_by, "human_reviewer")

    def test_verify_nonexistent_claim(self):
        result = self.registry.verify_claim("fake", "test", "ref")
        self.assertFalse(result)

    def test_coverage_report(self):
        self.registry.register_claim("c1", "m1", "test", "ref1")
        self.registry.register_claim("c2", "m2")
        report = self.registry.get_coverage_report()
        self.assertEqual(report["total_claims"], 2)
        self.assertEqual(report["verified_claims"], 1)
        self.assertEqual(report["unverified_claims"], 1)
        self.assertAlmostEqual(report["coverage_pct"], 50.0)

    def test_empty_coverage_report(self):
        report = self.registry.get_coverage_report()
        self.assertEqual(report["coverage_pct"], 100.0)

    def test_claims_list_is_copy(self):
        self.registry.register_claim("c1", "m1")
        external = self.registry.claims
        external.clear()
        self.assertEqual(len(self.registry.claims), 1)


# ===========================================================================
# Healthcare Compliance Adapter (#1)
# ===========================================================================

class TestHealthcareComplianceAdapter(unittest.TestCase):
    """Tests for healthcare regulatory mapping."""

    def setUp(self):
        self.adapter = HealthcareComplianceAdapter()

    def test_default_mappings_loaded(self):
        self.assertTrue(len(self.adapter.mappings) > 0)

    def test_has_iso_14971_mappings(self):
        mappings = self.adapter.get_framework_mappings(
            RegulatoryFramework.ISO_14971
        )
        self.assertTrue(len(mappings) > 0)

    def test_has_iec_62304_mappings(self):
        mappings = self.adapter.get_framework_mappings(
            RegulatoryFramework.IEC_62304
        )
        self.assertTrue(len(mappings) > 0)

    def test_gaps_identified(self):
        gaps = self.adapter.get_gaps()
        self.assertTrue(len(gaps) > 0)
        # Should include IEC 62304 Class A/B/C mapping gap
        gap_descriptions = [g.gap_description for g in gaps]
        self.assertTrue(any("Class A/B/C" in d for d in gap_descriptions))

    def test_satisfied_requirements(self):
        satisfied = self.adapter.get_satisfied()
        self.assertTrue(len(satisfied) > 0)

    def test_add_custom_mapping(self):
        initial_count = len(self.adapter.mappings)
        self.adapter.add_mapping(RegulatoryMapping(
            pbhp_module="custom",
            pbhp_concept="custom_feature",
            regulatory_framework="CUSTOM_REG",
            regulatory_clause="Clause 99",
            regulatory_requirement="Must do X",
            pbhp_satisfies=True,
        ))
        self.assertEqual(len(self.adapter.mappings), initial_count + 1)

    def test_export_compliance_matrix(self):
        matrix = self.adapter.export_compliance_matrix()
        self.assertIn(RegulatoryFramework.ISO_14971.value, matrix)
        iso_data = matrix[RegulatoryFramework.ISO_14971.value]
        self.assertIn("total_requirements", iso_data)
        self.assertIn("satisfied", iso_data)
        self.assertIn("gaps", iso_data)

    def test_generate_coverage_gaps(self):
        collector = CoverageGapCollector()
        self.adapter.generate_coverage_gaps(collector)
        # Should have generated gaps for the non-satisfied mappings
        adapter_gaps = self.adapter.get_gaps()
        self.assertEqual(len(collector.gaps), len(adapter_gaps))

    def test_compliance_gap_has_mitigation(self):
        collector = CoverageGapCollector()
        self.adapter.generate_coverage_gaps(collector)
        for gap in collector.gaps:
            self.assertNotEqual(gap.mitigation, "")


# ===========================================================================
# MBSE Interface (#2)
# ===========================================================================

class TestMBSEInterface(unittest.TestCase):
    """Tests for MBSE requirement taxonomy interface."""

    def setUp(self):
        self.mbse = MBSEInterface(taxonomy="SysML")

    def test_add_mapping(self):
        m = self.mbse.add_mapping(
            pbhp_output="risk_class=RED",
            requirement_id="SYS-REQ-042",
            requirement_text="System shall halt on critical risk",
            satisfaction_status="satisfied",
        )
        self.assertEqual(m.taxonomy, "SysML")
        self.assertEqual(m.requirement_id, "SYS-REQ-042")

    def test_get_unsatisfied(self):
        self.mbse.add_mapping("out1", "REQ-1", "req1", "satisfied")
        self.mbse.add_mapping("out2", "REQ-2", "req2", "not_assessed")
        self.mbse.add_mapping("out3", "REQ-3", "req3", "partial")
        unsatisfied = self.mbse.get_unsatisfied()
        self.assertEqual(len(unsatisfied), 2)

    def test_export_traceability(self):
        self.mbse.add_mapping("out1", "REQ-1", "req1", "satisfied")
        self.mbse.add_mapping("out2", "REQ-2", "req2", "not_assessed")
        trace = self.mbse.export_traceability()
        self.assertEqual(trace["taxonomy"], "SysML")
        self.assertEqual(trace["total_mappings"], 2)
        self.assertEqual(trace["satisfied"], 1)


# ===========================================================================
# Integration: Coverage Gaps Flow Through System
# ===========================================================================

class TestCoverageGapIntegration(unittest.TestCase):
    """Tests that coverage gaps flow from all sources into prominent output."""

    def test_healthcare_gaps_plus_module_gaps(self):
        collector = CoverageGapCollector()

        # Healthcare adapter feeds its gaps
        adapter = HealthcareComplianceAdapter()
        adapter.generate_coverage_gaps(collector)

        # Module reports its own gap
        collector.report(
            "pbhp_srl",
            "Multi-agent scheming not covered by current SRL rules",
            GapSeverity.CRITICAL,
            mitigation="Extend SRL for multi-agent coordination",
        )

        # Registry reports missing capabilities
        registry = ModuleRegistry()
        missing = registry.get_missing_capabilities({
            ModuleCapability.DRIFT_SNAPSHOT,
            ModuleCapability.COMPLIANCE_MAPPING,
        })
        for cap in missing:
            collector.report(
                "pbhp_bridge",
                f"No provider registered for {cap.value}",
                GapSeverity.WARNING,
            )

        # Should have all gaps combined
        self.assertTrue(collector.has_critical_gaps)
        output = collector.format_prominent()
        self.assertIn("CRITICAL", output)
        self.assertIn("WARNING", output)


# ===========================================================================
# Data Class Serialization
# ===========================================================================

class TestSerialization(unittest.TestCase):
    """Tests that all data classes serialize properly."""

    def test_coverage_gap_to_dict(self):
        gap = CoverageGap(
            module="test", description="missing",
            severity=GapSeverity.CRITICAL,
        )
        d = gap.to_dict()
        self.assertEqual(d["severity"], "critical")

    def test_safety_claim_to_dict(self):
        claim = SafetyClaim(claim="safe", module="m1", verified=True)
        d = claim.to_dict()
        self.assertTrue(d["verified"])

    def test_regulatory_mapping_to_dict(self):
        m = RegulatoryMapping(
            pbhp_module="core",
            regulatory_framework="ISO_14971",
            pbhp_satisfies=True,
        )
        d = m.to_dict()
        self.assertTrue(d["satisfied"])

    def test_requirement_mapping_to_dict(self):
        m = RequirementMapping(
            pbhp_output="risk=RED",
            requirement_id="REQ-1",
            taxonomy="SysML",
        )
        d = m.to_dict()
        self.assertEqual(d["taxonomy"], "SysML")


if __name__ == "__main__":
    unittest.main()
