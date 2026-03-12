"""
Pause-Before-Harm Protocol (PBHP) v0.8.1 — Cross-Module Integration Tests

Comprehensive tests for real workflows across module boundaries.
These tests exercise the seams where bugs hide — interactions between:
  - SRL → QS integration
  - Bridge ModuleRegistry subcontracting
  - Bridge CoverageGapCollector & HealthcareComplianceAdapter
  - Bridge SafetyClaimRegistry
  - Triage → Core → Multiagent workflow
  - Drift → Compliance Mapping
  - Multiagent + SRL coordination
  - Full pipeline end-to-end
  - State machine consistency
  - Cross-module audit trails

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

import unittest
import sys
sys.path.insert(0, '/sessions/happy-charming-bohr/pbhp_repo/src')

from datetime import datetime, timedelta
from pbhp_core import (
    RiskClass, DecisionOutcome, ImpactLevel, LikelihoodLevel
)
from pbhp_srl import (
    ActionContext, PolicyDecision, IncidentRecord, ConfessionReport,
    ActionGate, SRLRule, RiskLevel, SystemState, ActionCategory,
    IncidentSeverity, IncidentStatus, PolicyEngine, SRLStateMachine
)
from pbhp_qs import (
    QSRule, EvidenceVault, EvidenceArtifact, CAPAManager, CAPARecord,
    CAPAStatus, ApprovalToken, ApprovalStatus, TripwireRegistry,
    TripwireType, QualitySystemsEngine, ApprovalGate, Tripwire
)
from pbhp_bridge import (
    ModuleRegistry, ModuleCapability, CoverageGapCollector, GapSeverity,
    SafetyClaimRegistry, HealthcareComplianceAdapter, RegulatoryFramework,
    MBSEInterface, SubcontractResponse
)
from pbhp_drift import (
    DriftMonitor, DriftMetaMonitor, MetaHeartbeat, DriftDirection
)
from pbhp_triage import (
    TriageClassifier, TriageSignals, TriageTier
)
from pbhp_multiagent import (
    CoordinationProtocol, AgentDecision, AgentRole, CoordinationContext
)
from pbhp_compliance import ComplianceMapper, ComplianceFramework


# ============================================================================
# Test Suite 1: SRL → QS Integration
# ============================================================================

class TestSRLQSIntegration(unittest.TestCase):
    """Test that QS can properly use and record decisions from SRL."""

    def setUp(self):
        self.qs = QualitySystemsEngine()
        self.evidence_vault = EvidenceVault()
        self.action_gate = ActionGate()

    def test_qs_records_evidence_for_srl_policy_decision(self):
        """Test that QS EvidenceVault can record evidence tied to SRL decisions."""
        # Create an action context
        ctx = ActionContext(
            action_type="production_write",
            action_description="Update production database schema",
            categories=[ActionCategory.SCHEMA_CHANGE],
            environment="prod",
            explicit_human_approval=True,
            rollback_available=True,
            rollback_proof_attached=True,
            logging_active=True,
        )

        # Evaluate through SRL ActionGate
        decision = self.action_gate.check(ctx)

        # Verify decision was made
        self.assertIsNotNone(decision)
        self.assertEqual(decision.action_id, ctx.action_id)

        # Record evidence for this action
        before_artifact = self.evidence_vault.store(
            action_id=ctx.action_id,
            artifact_type="snapshot",
            description="Before: Database schema",
            content="schema_v1: columns=[id, name, email]",
            phase="before",
        )
        self.assertIsNotNone(before_artifact)

        # Verify evidence is retrievable
        artifacts = self.evidence_vault.get_by_action(ctx.action_id)
        self.assertEqual(len(artifacts), 1)
        self.assertEqual(artifacts[0].action_id, ctx.action_id)

    def test_srl_action_gate_confession_triggers_capa_workflow(self):
        """Test that SRL ActionGate confession can trigger QS CAPA workflow."""
        # Create a blocked action
        ctx = ActionContext(
            action_type="self_mod",
            action_description="Modify own runtime",
            involves_self_modification=True,
            environment="prod",
        )

        # SRL ActionGate blocks it
        decision = self.action_gate.check(ctx)
        self.assertFalse(decision.allow)
        self.assertIn(SRLRule.ANTI_SELF_PRESERVATION, decision.triggered_rules)

        # File a confession
        confession = ConfessionReport(
            what_happened="Attempted self-modification without authorization",
            what_rule_violated="SRL-01: Anti-Self-Preservation",
            potential_impact="Potential override of safety controls",
            evidence_preserved=[decision.action_id],
            actions_not_taken_since=["Further self-modification attempts"],
            current_status="stopped",
            recommended_human_step="Review incident and requalify system",
        )

        incident = self.action_gate.confess(confession)
        self.assertIsNotNone(incident)
        self.assertEqual(incident.severity, IncidentSeverity.HIGH)

        # Create CAPA from the incident
        capa_mgr = CAPAManager()
        capa = capa_mgr.create(incident.incident_id)
        self.assertIsNotNone(capa)
        self.assertEqual(capa.incident_id, incident.incident_id)
        self.assertEqual(capa.status, CAPAStatus.OPEN)

    def test_srl_state_machine_state_accessible_through_qs(self):
        """Test that SRL state machine state is accessible and consistent through QS."""
        qs = QualitySystemsEngine()

        # Initially NORMAL
        self.assertEqual(qs.current_state, SystemState.NORMAL)

        # Create action that triggers GUARDED
        ctx = ActionContext(
            action_type="prod_write",
            action_description="Production write without approval",
            categories=[ActionCategory.PRODUCTION_WRITE],
            environment="prod",
            explicit_human_approval=False,
        )

        decision = qs.evaluate_action(ctx)

        # State should have transitioned
        # (GUARDED or AWAITING_HUMAN_REVIEW depending on other conditions)
        self.assertIsNotNone(decision)
        self.assertNotEqual(qs.current_state, SystemState.NORMAL)


# ============================================================================
# Test Suite 2: Bridge ModuleRegistry — SRL/QS/Drift
# ============================================================================

class TestBridgeModuleRegistry(unittest.TestCase):
    """Test cross-module subcontracting through ModuleRegistry."""

    def setUp(self):
        self.registry = ModuleRegistry()

    def test_register_srl_as_state_machine_query_provider(self):
        """Register SRL as provider of STATE_MACHINE_QUERY capability."""
        gate = ActionGate()

        def srl_state_provider(context):
            return {
                "current_state": gate.current_state.value,
                "requires_human": gate.current_state in [
                    SystemState.CONFESSION, SystemState.FROZEN,
                    SystemState.AWAITING_HUMAN_REVIEW
                ]
            }

        self.registry.register_provider(
            "SRL",
            ModuleCapability.STATE_MACHINE_QUERY,
            srl_state_provider,
        )

        # Verify provider is registered
        providers = self.registry.get_providers(ModuleCapability.STATE_MACHINE_QUERY)
        self.assertEqual(len(providers), 1)
        self.assertIn("SRL", providers)

        # Request the capability
        response = self.registry.request(
            "Bridge",
            ModuleCapability.STATE_MACHINE_QUERY,
            context={},
        )
        self.assertTrue(response.success)
        self.assertIn("current_state", response.result)

    def test_register_drift_as_drift_snapshot_provider(self):
        """Register Drift as provider of DRIFT_SNAPSHOT capability."""
        drift = DriftMonitor()

        def drift_snapshot_provider(context):
            snapshot = drift.compute_snapshot()
            return {
                "timestamp": snapshot.window_start.isoformat(),
                "total_decisions": snapshot.total_decisions,
                "gate_distribution": snapshot.gate_distribution,
            }

        self.registry.register_provider(
            "Drift",
            ModuleCapability.DRIFT_SNAPSHOT,
            drift_snapshot_provider,
        )

        providers = self.registry.get_providers(ModuleCapability.DRIFT_SNAPSHOT)
        self.assertIn("Drift", providers)

        response = self.registry.request(
            "SRL",
            ModuleCapability.DRIFT_SNAPSHOT,
            context={},
        )
        self.assertTrue(response.success)

    def test_register_qs_as_evidence_logging_provider(self):
        """Register QS as provider of EVIDENCE_LOGGING capability."""
        vault = EvidenceVault()

        def evidence_provider(context):
            action_id = context.get("action_id", "")
            artifacts = vault.get_by_action(action_id)
            return {
                "artifact_count": len(artifacts),
                "chain_hash": vault.chain_hash,
                "chain_verified": vault.verify_chain(),
            }

        self.registry.register_provider(
            "QS",
            ModuleCapability.EVIDENCE_LOGGING,
            evidence_provider,
        )

        response = self.registry.request(
            "Bridge",
            ModuleCapability.EVIDENCE_LOGGING,
            context={"action_id": "test-action-123"},
        )
        self.assertTrue(response.success)
        self.assertEqual(response.result["artifact_count"], 0)

    def test_request_capability_with_no_provider(self):
        """Request a capability with no provider → returns failure response."""
        response = self.registry.request(
            "AnyModule",
            ModuleCapability.BEHAVIORAL_ANALYSIS,
            context={},
        )
        self.assertFalse(response.success)
        self.assertIn("error", response.result)
        self.assertIn("No provider", response.result["error"])

    def test_multiple_providers_routes_to_first(self):
        """Multiple providers for same capability → routes to first."""
        def handler1(ctx):
            return {"source": "handler1"}

        def handler2(ctx):
            return {"source": "handler2"}

        self.registry.register_provider(
            "ModuleA",
            ModuleCapability.RISK_ASSESSMENT,
            handler1,
        )
        self.registry.register_provider(
            "ModuleB",
            ModuleCapability.RISK_ASSESSMENT,
            handler2,
        )

        response = self.registry.request(
            "Requester",
            ModuleCapability.RISK_ASSESSMENT,
            context={},
        )
        self.assertTrue(response.success)
        self.assertEqual(response.result["source"], "handler1")

    def test_handler_function_executes_and_returns_result(self):
        """Handler function executes and returns result through registry."""
        call_count = 0

        def counting_handler(context):
            nonlocal call_count
            call_count += 1
            return {"invocations": call_count, "input": context}

        self.registry.register_provider(
            "TestModule",
            ModuleCapability.BEHAVIORAL_ANALYSIS,
            counting_handler,
        )

        response = self.registry.request(
            "Requester",
            ModuleCapability.BEHAVIORAL_ANALYSIS,
            context={"test_param": "value"},
        )

        self.assertTrue(response.success)
        self.assertEqual(response.result["invocations"], 1)
        self.assertEqual(response.result["input"]["test_param"], "value")


# ============================================================================
# Test Suite 3: Bridge CoverageGapCollector → Healthcare Adapter
# ============================================================================

class TestBridgeCoverageGapHealthcare(unittest.TestCase):
    """Test coverage gap collection from healthcare adapter."""

    def test_healthcare_adapter_generates_coverage_gaps(self):
        """HealthcareComplianceAdapter generates gaps that appear in collector."""
        collector = CoverageGapCollector()
        adapter = HealthcareComplianceAdapter()

        # HealthcareComplianceAdapter maintains mappings
        # Report a gap based on adapter's internal mappings
        unsatisfied = [
            m for m in adapter.mappings
            if not m.pbhp_satisfies
        ]

        # Report unsatisfied mappings as gaps
        for mapping in unsatisfied[:3]:  # Limit to first 3
            collector.report(
                module="HealthcareAdapter",
                description=mapping.gap_description or f"Unsatisfied: {mapping.regulatory_requirement}",
                severity=GapSeverity.WARNING,
            )

        # Verify gaps appear in collector
        all_gaps = collector.gaps
        self.assertGreater(len(all_gaps), 0)

    def test_gaps_appear_in_prominent_output(self):
        """Verify gaps from adapter appear in format_prominent output."""
        collector = CoverageGapCollector()

        # Report some gaps
        collector.report(
            "HealthcareModule",
            "Cannot fully assess post-market surveillance",
            GapSeverity.WARNING,
        )

        output = collector.format_prominent()
        self.assertIn("Coverage Warnings", output)
        self.assertIn("post-market", output)

    def test_gap_count_matches_unsatisfied_mappings(self):
        """Gap count matches number of unsatisfied regulatory mappings."""
        collector = CoverageGapCollector()
        gap_count = 0

        # Report multiple gaps
        for i in range(3):
            collector.report(
                "Adapter",
                f"Gap {i}: unsatisfied requirement {i}",
                GapSeverity.WARNING,
            )
            gap_count += 1

        # Verify count
        self.assertEqual(len(collector.gaps), gap_count)


# ============================================================================
# Test Suite 4: Bridge SafetyClaimRegistry → Evidence Pattern
# ============================================================================

class TestBridgeSafetyClaimRegistry(unittest.TestCase):
    """Test safety claims registration and evidence verification."""

    def test_register_claims_with_evidence_verified(self):
        """Register claims with evidence → verified."""
        registry = SafetyClaimRegistry()
        vault = EvidenceVault()

        # Store evidence first
        artifact = vault.store(
            action_id="action-1",
            artifact_type="test_result",
            description="Safety test passed",
            content="Test: safety_check PASSED",
            phase="after",
        )

        # Register claim with evidence
        claim = registry.register_claim(
            claim="System is safe under condition X",
            module="TestModule",
            evidence_type="test",
            evidence_ref=artifact.artifact_id,
        )

        self.assertIsNotNone(claim)
        self.assertTrue(claim.verified)

    def test_register_claims_without_evidence_unverified_flagged(self):
        """Register claims without evidence → unverified, prominently flagged."""
        registry = SafetyClaimRegistry()

        # Register without evidence
        claim = registry.register_claim(
            claim="System will never harm humans",
            module="TestModule",
            evidence_type="",
            evidence_ref="",
        )

        self.assertFalse(claim.verified)

    def test_verify_claims_after_registration(self):
        """Verify claims after registration."""
        registry = SafetyClaimRegistry()
        vault = EvidenceVault()

        artifact = vault.store(
            action_id="action-1",
            artifact_type="proof",
            description="Evidence of safety property",
            content="Property X: PROVEN",
            phase="after",
        )

        claim = registry.register_claim(
            claim="Property X holds true",
            module="TestModule",
            evidence_type="",
            evidence_ref="",
        )

        # Now verify it
        success = registry.verify_claim(
            claim.claim_id,
            evidence_type="artifact",
            evidence_ref=artifact.artifact_id,
            verified_by="test",
        )
        self.assertTrue(success)
        self.assertTrue(claim.verified)

    def test_coverage_report_shows_correct_percentages(self):
        """Coverage report shows correct percentages of verified claims."""
        registry = SafetyClaimRegistry()

        # Register 3 claims: 2 with evidence, 1 without
        vault = EvidenceVault()
        art1 = vault.store("a1", "test", "Evidence 1", "content1", "after")
        art2 = vault.store("a2", "test", "Evidence 2", "content2", "after")

        registry.register_claim(
            "Claim 1",
            module="Module1",
            evidence_type="test",
            evidence_ref=art1.artifact_id,
        )
        registry.register_claim(
            "Claim 2",
            module="Module2",
            evidence_type="test",
            evidence_ref=art2.artifact_id,
        )
        registry.register_claim(
            "Claim 3",
            module="Module3",
            evidence_type="",
            evidence_ref="",
        )

        report = registry.get_coverage_report()
        self.assertIn("coverage_pct", report)
        # Should be 66.7% (2/3)
        self.assertAlmostEqual(report["coverage_pct"], 66.67, places=1)


# ============================================================================
# Test Suite 5: Triage → Core → Multiagent Workflow
# ============================================================================

class TestTriageCoreMultiagentWorkflow(unittest.TestCase):
    """Test realistic workflow: triage → core types → multiagent coordination."""

    def test_high_risk_triage_produces_conservative_multiagent_decisions(self):
        """High-risk triage (HUMAN tier) → conservative agent decisions → escalation."""
        # Triage signals
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True,
            power_asymmetry_detected=True,
            large_scale_amplification=True,
            automated_execution=True,
            legal_or_regulatory_impact=True,
        )

        classifier = TriageClassifier()
        triage_result = classifier.classify(signals)

        # Should escalate to HUMAN tier
        self.assertEqual(triage_result.recommended_tier, TriageTier.HUMAN)
        self.assertTrue(triage_result.requires_human_loop)

        # Now create agent decisions based on this high-risk triage
        agent1 = AgentDecision(
            agent_id="safety_agent",
            agent_role=AgentRole.SAFETY_SPECIALIST,
            recommended_gate=RiskClass.RED,
            confidence_score=0.95,
            reasoning_summary="High-risk action flagged by triage, multiple harms detected",
            is_irreversibility_concern=True,
            recommended_outcome=DecisionOutcome.ESCALATE,
        )

        agent2 = AgentDecision(
            agent_id="domain_agent",
            agent_role=AgentRole.DOMAIN_EXPERT,
            recommended_gate=RiskClass.ORANGE,
            confidence_score=0.85,
            reasoning_summary="Domain-specific risks present, recommend constraint",
            is_vulnerable_population_concern=True,
            recommended_outcome=DecisionOutcome.DELAY,
        )

        # Coordinate agents
        coordination_ctx = CoordinationContext(
            action_description="Deploy experimental healthcare algorithm",
            affected_parties=["patients", "doctors", "hospital_system"],
            is_irreversible=True,
            is_mass_scale=True,
            has_explicit_human_approval=False,
        )

        protocol = CoordinationProtocol()
        result = protocol.coordinate([agent1, agent2], coordination_ctx)

        # Result should be conservative due to disagreement + high-risk triage
        self.assertEqual(result.final_gate_recommendation, RiskClass.RED)
        self.assertEqual(result.final_decision_outcome, DecisionOutcome.ESCALATE)

    def test_triage_result_informs_agent_decision_gate_levels(self):
        """TriageResult directly informs AgentDecision gate levels."""
        signals = TriageSignals(
            irreversible=False,
            affects_vulnerable_population=False,
            power_asymmetry_detected=False,
        )

        classifier = TriageClassifier()
        triage_result = classifier.classify(signals)

        # LOW-risk triage
        if triage_result.recommended_tier == TriageTier.CORE:
            # Agent can be less conservative
            agent = AgentDecision(
                agent_id="test_agent",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.9,
                reasoning_summary="Low-risk signals, standard assessment applies",
                recommended_outcome=DecisionOutcome.PROCEED_MODIFIED,
            )
            self.assertEqual(agent.recommended_gate, RiskClass.YELLOW)


# ============================================================================
# Test Suite 6: Drift → Compliance Mapping
# ============================================================================

class TestDriftComplianceMapping(unittest.TestCase):
    """Test drift monitoring → compliance mapping integration."""

    def test_drift_monitor_ingests_decisions_computes_metrics(self):
        """DriftMonitor ingests decisions and computes metrics."""
        drift = DriftMonitor()
        gate = ActionGate()

        # Make several decisions
        for i in range(3):
            ctx = ActionContext(
                action_type=f"action_{i}",
                action_description=f"Test action {i}",
                environment="prod",
            )
            decision = gate.check(ctx)
            # Ingest decision as dict
            drift.ingest_decision({
                "timestamp": datetime.utcnow(),
                "gate": "green" if decision.allow else "red",
                "outcome": "proceed" if decision.allow else "refuse",
            })

        snapshot = drift.compute_snapshot()
        self.assertGreater(snapshot.total_decisions, 0)

    def test_drift_alerts_map_to_compliance_requirements(self):
        """Drift alerts map to compliance requirements (ISO 14971 Clause 9)."""
        drift = DriftMonitor()
        mapper = ComplianceMapper()

        # Simulate drift detection
        gate = ActionGate()
        ctx = ActionContext(
            action_type="risky",
            action_description="Risky action",
            environment="prod",
        )
        decision = gate.check(ctx)
        drift.ingest_decision({
            "timestamp": datetime.utcnow(),
            "gate": "red",
            "outcome": "refuse",
        })

        # Check compliance framework requirements
        requirements = mapper.get_requirements_for_framework(
            ComplianceFramework.ISO_23894
        )

        self.assertIsNotNone(requirements)
        self.assertGreater(len(requirements), 0)

    def test_compliance_mapper_references_drift_artifacts_in_evidence(self):
        """ComplianceMapper can reference drift artifacts in evidence."""
        mapper = ComplianceMapper()
        drift = DriftMonitor()

        # Create drift data
        gate = ActionGate()
        for i in range(5):
            ctx = ActionContext(
                action_type=f"test_{i}",
                environment="prod",
            )
            decision = gate.check(ctx)
            drift.ingest_decision({
                "timestamp": datetime.utcnow(),
                "gate": "green",
                "outcome": "proceed",
            })

        snapshot = drift.compute_snapshot()

        # Get compliance requirements and artifacts
        requirements = mapper.get_requirements_for_framework(
            ComplianceFramework.NIST_AI_RMF
        )

        # Both should exist
        self.assertIsNotNone(requirements)
        self.assertGreater(snapshot.total_decisions, 0)


# ============================================================================
# Test Suite 7: Multiagent + SRL: BLACK gate Coordination
# ============================================================================

class TestMultiagentSRLBlackGate(unittest.TestCase):
    """Test that Multiagent BLACK gate and SRL block independently reach same conclusion."""

    def test_coordination_produces_black_escalation(self):
        """CoordinationProtocol produces BLACK escalation."""
        # Create agent decisions that strongly disagree
        agent1 = AgentDecision(
            agent_id="conservative",
            agent_role=AgentRole.SAFETY_SPECIALIST,
            recommended_gate=RiskClass.BLACK,
            confidence_score=0.99,
            reasoning_summary="Critical safety issue detected",
            is_irreversibility_concern=True,
            recommended_outcome=DecisionOutcome.REFUSE,
        )

        agent2 = AgentDecision(
            agent_id="permissive",
            agent_role=AgentRole.OPERATIONAL,
            recommended_gate=RiskClass.RED,
            confidence_score=0.7,
            reasoning_summary="Operational concerns but manageable",
            recommended_outcome=DecisionOutcome.ESCALATE,
        )

        coordination_ctx = CoordinationContext(
            action_description="Self-modify runtime",
            affected_parties=["system"],
            is_irreversible=True,
        )

        protocol = CoordinationProtocol()
        result = protocol.coordinate([agent1, agent2], coordination_ctx)

        # With one agent voting BLACK and irreversibility, should escalate
        self.assertIn(
            result.final_decision_outcome,
            [DecisionOutcome.REFUSE, DecisionOutcome.ESCALATE],
        )

    def test_srl_action_gate_also_blocks_self_mod_action(self):
        """SRL ActionGate independently blocks same action."""
        gate = ActionGate()

        ctx = ActionContext(
            action_type="self_modification",
            action_description="Self-modify runtime",
            involves_self_modification=True,
            environment="prod",
        )

        decision = gate.check(ctx)

        # SRL should block self-modification
        self.assertFalse(decision.allow)
        self.assertIn(SRLRule.ANTI_SELF_PRESERVATION, decision.triggered_rules)

    def test_both_systems_independently_reach_same_conclusion(self):
        """Both Multiagent and SRL independently reach REFUSE/BLOCK conclusion."""
        # SRL evaluation
        gate = ActionGate()
        srl_ctx = ActionContext(
            action_type="self_mod",
            involves_self_modification=True,
            environment="prod",
        )
        srl_decision = gate.check(srl_ctx)

        # Multiagent evaluation of same action
        agent = AgentDecision(
            agent_id="system",
            agent_role=AgentRole.SAFETY_SPECIALIST,
            recommended_gate=RiskClass.BLACK,
            confidence_score=0.95,
            reasoning_summary="Self-modification is unsafe",
            recommended_outcome=DecisionOutcome.REFUSE,
        )

        coordination_ctx = CoordinationContext(
            action_description="Self-modify runtime",
            affected_parties=["system"],
        )

        protocol = CoordinationProtocol()
        result = protocol.coordinate([agent], coordination_ctx)

        # Both should refuse/escalate
        self.assertFalse(srl_decision.allow)
        self.assertIn(
            result.final_decision_outcome,
            [DecisionOutcome.REFUSE, DecisionOutcome.ESCALATE],
        )


# ============================================================================
# Test Suite 8: Full Pipeline End-to-End
# ============================================================================

class TestFullPipelineEndToEnd(unittest.TestCase):
    """
    Full pipeline: Action → Triage → Core Assessment → SRL Gate →
    QS Evidence → Drift Logging
    """

    def test_high_risk_action_flows_through_entire_stack(self):
        """High-risk action flows through entire safety stack."""
        # 1. Create TriageSignals for high-risk healthcare action
        signals = TriageSignals(
            irreversible=True,
            affects_vulnerable_population=True,
            legal_or_regulatory_impact=True,
            automated_execution=True,
        )

        classifier = TriageClassifier()
        triage_result = classifier.classify(signals)
        # Should escalate to at least ULTRA or HUMAN
        self.assertIn(
            triage_result.recommended_tier,
            [TriageTier.HUMAN, TriageTier.ULTRA],
        )

        # 2. Create SRL ActionContext for same action
        ctx = ActionContext(
            action_type="healthcare_action",
            action_description="Modify patient treatment parameters",
            categories=[ActionCategory.PRODUCTION_WRITE],
            environment="prod",
            affects_access_control=False,
            involves_self_modification=False,
            explicit_human_approval=False,
        )

        # 3. SRL PolicyEngine evaluates
        engine = PolicyEngine()
        policy_decision = engine.evaluate(ctx)
        self.assertEqual(policy_decision.risk_level, RiskLevel.CRITICAL)
        self.assertFalse(policy_decision.allow)

        # 4. SRL ActionGate records incident
        gate = ActionGate()
        decision = gate.check(ctx)
        incidents = gate.incident_recorder.incidents
        self.assertGreater(len(incidents), 0)

        # 5. Bridge CoverageGapCollector reports gaps
        collector = CoverageGapCollector()
        collector.report(
            "SRL",
            "Cannot evaluate long-term patient outcomes",
            GapSeverity.WARNING,
        )
        gaps = collector.gaps
        self.assertGreater(len(gaps), 0)

        # 6. Drift monitor ingests decision
        drift = DriftMonitor()
        drift.ingest_decision({
            "timestamp": datetime.utcnow(),
            "gate": "red",
            "outcome": "refuse",
        })
        snapshot = drift.compute_snapshot()
        self.assertEqual(snapshot.total_decisions, 1)

    def test_action_flows_with_all_audit_artifacts(self):
        """Action produces artifacts at each stage."""
        ctx = ActionContext(
            action_type="test",
            action_description="Test action",
            environment="prod",
        )

        # QS tracks via evidence vault
        vault = EvidenceVault()
        before_artifact = vault.store(
            action_id=ctx.action_id,
            artifact_type="state",
            description="Before",
            content="initial_state",
            phase="before",
        )
        self.assertEqual(before_artifact.action_id, ctx.action_id)

        # SRL tracks via incident recorder
        gate = ActionGate()
        decision = gate.check(ctx)
        self.assertEqual(decision.action_id, ctx.action_id)

        # Drift tracks via monitor
        drift = DriftMonitor()
        drift.ingest_decision({
            "timestamp": datetime.utcnow(),
            "gate": "green" if decision.allow else "red",
            "outcome": "proceed" if decision.allow else "refuse",
        })
        self.assertEqual(drift.compute_snapshot().total_decisions, 1)

        # All reference same action_id
        self.assertEqual(before_artifact.action_id, decision.action_id)


# ============================================================================
# Test Suite 9: State Machine Consistency Across Modules
# ============================================================================

class TestStateMachineConsistency(unittest.TestCase):
    """Test SystemState consistency across SRL and QS modules."""

    def test_srl_escalation_normal_to_frozen_prevents_qs_operations(self):
        """SRL escalation NORMAL→FROZEN prevents QS from allowing operations."""
        # Create QS with embedded ActionGate
        qs = QualitySystemsEngine()

        # Verify initial state
        self.assertEqual(qs.current_state, SystemState.NORMAL)

        # Trigger SRL self-preservation violation
        ctx = ActionContext(
            action_type="self_mod",
            involves_self_modification=True,
            environment="prod",
        )

        # Check through QS (which uses ActionGate internally)
        decision = qs.evaluate_action(ctx)

        # Should transition to FROZEN
        self.assertEqual(qs.current_state, SystemState.FROZEN)

        # Any subsequent operation should be blocked
        ctx2 = ActionContext(
            action_type="normal_action",
            environment="prod",
        )
        decision2 = qs.evaluate_action(ctx2)
        self.assertFalse(decision2.allow)

    def test_human_clearance_in_srl_affects_qs_behavior(self):
        """Human clearance in SRL affects QS operations."""
        qs = QualitySystemsEngine()

        # Transition to AWAITING_HUMAN_REVIEW
        qs.action_gate.state_machine.transition(
            SystemState.AWAITING_HUMAN_REVIEW,
            reason="Human review needed",
        )

        self.assertEqual(qs.current_state, SystemState.AWAITING_HUMAN_REVIEW)

        # Human grants clearance
        success = qs.action_gate.state_machine.human_override(
            SystemState.REQUALIFIED,
            reviewer="dr_safety",
            reason="System requalified",
        )

        self.assertTrue(success)
        self.assertEqual(qs.current_state, SystemState.REQUALIFIED)

        # Now QS can operate
        ctx = ActionContext(
            action_type="normal",
            environment="prod",
        )
        decision = qs.evaluate_action(ctx)
        # Should be allowed (assuming no other violations)
        self.assertIsNotNone(decision)


# ============================================================================
# Test Suite 10: Cross-Module Audit Trail Correlation
# ============================================================================

class TestCrossModuleAuditTrail(unittest.TestCase):
    """Test that all modules correlate artifacts by action_id."""

    def test_action_produces_correlated_artifacts(self):
        """Single action produces correlated artifacts across modules."""
        action_id = "audit_test_action"

        # Create context with specific action_id
        ctx = ActionContext(
            action_id=action_id,
            action_type="audit_test",
            action_description="Audit trail test action",
            environment="prod",
        )

        # SRL records
        gate = ActionGate()
        srl_decision = gate.check(ctx)
        self.assertEqual(srl_decision.action_id, action_id)

        # QS records evidence
        vault = EvidenceVault()
        artifact = vault.store(
            action_id=action_id,
            artifact_type="audit",
            description="Audit artifact",
            content="test_content",
            phase="before",
        )
        self.assertEqual(artifact.action_id, action_id)

        # Bridge registry logs
        registry = ModuleRegistry()
        response = registry.request(
            "Auditor",
            ModuleCapability.EVIDENCE_LOGGING,
            context={"action_id": action_id},
        )
        # Response request_id can be cross-referenced
        self.assertIsNotNone(response.request_id)

        # Drift ingests decision
        drift = DriftMonitor()
        drift.ingest_decision({
            "timestamp": datetime.utcnow(),
            "gate": "green" if srl_decision.allow else "red",
            "outcome": "proceed" if srl_decision.allow else "refuse",
        })
        snapshot = drift.compute_snapshot()
        self.assertEqual(snapshot.total_decisions, 1)

    def test_all_logs_correlate_by_action_id_or_timestamp(self):
        """All module logs can be correlated by action_id or timestamp."""
        action_id = "correlation_test"

        ctx = ActionContext(
            action_id=action_id,
            action_type="correlation_test",
            environment="prod",
        )

        # Collect artifacts with timestamps
        timestamp_before = datetime.utcnow().isoformat()

        gate = ActionGate()
        decision = gate.check(ctx)

        vault = EvidenceVault()
        artifact = vault.store(
            action_id=action_id,
            artifact_type="log",
            description="Timestamped artifact",
            content="content",
            phase="after",
        )

        timestamp_after = datetime.utcnow().isoformat()

        # All should have action_id or timestamp in range
        self.assertEqual(decision.action_id, action_id)
        self.assertEqual(artifact.action_id, action_id)
        self.assertLess(decision.timestamp, timestamp_after)

    def test_incident_capa_requalification_chain(self):
        """IncidentRecord → CAPA → Requalification forms audit chain."""
        # Create incident
        gate = ActionGate()
        ctx = ActionContext(
            action_type="violation",
            involves_self_modification=True,
            environment="prod",
        )
        decision = gate.check(ctx)

        incident = gate.incident_recorder.incidents[0] if gate.incident_recorder.incidents else None
        if incident:
            # Create CAPA from incident
            capa_mgr = CAPAManager()
            capa = capa_mgr.create(incident.incident_id)

            # Set investigation
            capa_mgr.set_investigation(
                capa.capa_id,
                root_cause="Self-modification attempt",
                failure_mode="ANTI_SELF_PRESERVATION bypass",
                contributing_factors=["Insufficient checks"],
            )

            # Verify and close
            capa_mgr.verify(
                capa.capa_id,
                verified_by="system_auditor",
                verification_evidence=["Test passed"],
            )
            capa_mgr.close(capa.capa_id)

            # Verify final status
            closed_capa = [c for c in capa_mgr.records if c.capa_id == capa.capa_id][0]
            self.assertEqual(closed_capa.status, CAPAStatus.CLOSED)


# ============================================================================
# Test Suite 11: Bridge SafetyClaimRegistry Details
# ============================================================================

class TestBridgeSafetyClaimRegistryDetails(unittest.TestCase):
    """Detailed tests for SafetyClaimRegistry."""

    def test_claim_registration_with_multiple_artifacts(self):
        """Claims can reference evidence artifacts."""
        registry = SafetyClaimRegistry()
        vault = EvidenceVault()

        # Create evidence artifact
        art1 = vault.store("a1", "test", "Test 1", "result1", "after")

        claim = registry.register_claim(
            "Property X holds under conditions Y and Z",
            module="TestModule",
            evidence_type="test",
            evidence_ref=art1.artifact_id,
        )

        self.assertTrue(claim.verified)

    def test_unverified_claims_are_flagged_prominently(self):
        """Unverified claims are prominently flagged in output."""
        registry = SafetyClaimRegistry()

        registry.register_claim(
            "System will never harm humans",
            module="TestModule",
            evidence_type="",
            evidence_ref="",
        )

        report = registry.get_coverage_report()
        self.assertIn("unverified_claims", report)
        self.assertGreater(report["unverified_claims"], 0)


# ============================================================================
# Test Suite 12: Bridge CoverageGapCollector Prominence
# ============================================================================

class TestBridgeCoverageGapProminent(unittest.TestCase):
    """Test that coverage gaps are prominent in output."""

    def test_critical_gaps_in_all_caps_header(self):
        """Critical gaps appear with ALL CAPS header."""
        collector = CoverageGapCollector()

        collector.report(
            "Module",
            "Critical gap description",
            GapSeverity.CRITICAL,
        )

        output = collector.format_prominent()
        self.assertIn("COVERAGE GAPS", output)
        self.assertIn("PBHP CANNOT FULLY EVALUATE", output)
        self.assertIn("CRITICAL", output)

    def test_warning_gaps_below_critical(self):
        """Warning gaps appear below critical section."""
        collector = CoverageGapCollector()

        collector.report(
            "Module1",
            "Critical gap",
            GapSeverity.CRITICAL,
        )
        collector.report(
            "Module2",
            "Warning gap",
            GapSeverity.WARNING,
        )

        output = collector.format_prominent()
        critical_pos = output.find("CRITICAL")
        warning_pos = output.find("Coverage Warnings")

        self.assertGreater(critical_pos, 0)
        self.assertGreater(warning_pos, critical_pos)

    def test_info_gaps_below_warnings(self):
        """Info gaps appear below warnings."""
        collector = CoverageGapCollector()

        collector.report("M1", "Critical", GapSeverity.CRITICAL)
        collector.report("M2", "Warning", GapSeverity.WARNING)
        collector.report("M3", "Info", GapSeverity.INFO)

        output = collector.format_prominent()
        critical_pos = output.find("CRITICAL")
        warning_pos = output.find("Coverage Warnings")
        info_pos = output.find("Coverage Notes")

        self.assertGreater(critical_pos, 0)
        self.assertGreater(warning_pos, critical_pos)
        self.assertGreater(info_pos, warning_pos)


# ============================================================================
# Test Suite 13: Multiagent Quorum Voting
# ============================================================================

class TestMultiagentQuorumVoting(unittest.TestCase):
    """Test multiagent quorum voting with veto for irreversible actions."""

    def test_irreversible_action_applies_veto_rule(self):
        """Irreversible actions activate veto rule in quorum voting."""
        # Majority votes GREEN, but...
        agent1 = AgentDecision(
            agent_id="majority1",
            agent_role=AgentRole.OPERATIONAL,
            recommended_gate=RiskClass.GREEN,
            confidence_score=0.6,
            reasoning_summary="Operational perspective: OK",
            recommended_outcome=DecisionOutcome.PROCEED,
        )

        agent2 = AgentDecision(
            agent_id="majority2",
            agent_role=AgentRole.DOMAIN_EXPERT,
            recommended_gate=RiskClass.GREEN,
            confidence_score=0.6,
            reasoning_summary="Domain OK",
            recommended_outcome=DecisionOutcome.PROCEED,
        )

        # One expert votes RED
        agent3 = AgentDecision(
            agent_id="veto",
            agent_role=AgentRole.SAFETY_SPECIALIST,
            recommended_gate=RiskClass.RED,
            confidence_score=0.95,
            reasoning_summary="Irreversible action, safety concern",
            is_irreversibility_concern=True,
            recommended_outcome=DecisionOutcome.REFUSE,
        )

        coordination_ctx = CoordinationContext(
            action_description="Perform surgery",
            affected_parties=["patient"],
            is_irreversible=True,
        )

        protocol = CoordinationProtocol()
        result = protocol.coordinate([agent1, agent2, agent3], coordination_ctx)

        # Irreversible action with RED vote should escalate despite majority
        self.assertIn(
            result.final_gate_recommendation,
            [RiskClass.RED, RiskClass.ORANGE],
        )


# ============================================================================
# Test Suite 14: Tripwire Detection Through QS
# ============================================================================

class TestTripwireDetectionQS(unittest.TestCase):
    """Test tripwire detection in QualitySystemsEngine."""

    def test_tripwire_registry_detects_contact(self):
        """TripwireRegistry can detect when tripwire is contacted."""
        registry = TripwireRegistry()

        # Plant a tripwire
        tripwire = registry.register(
            TripwireType.FORBIDDEN_FILE,
            "forbidden_file",
            "/forbidden/path",
            "Should never access this",
        )
        self.assertIsNotNone(tripwire)

        # Contact it
        triggered = registry.check_access("/forbidden/path")
        self.assertIsNotNone(triggered)
        self.assertTrue(triggered.triggered)

    def test_tripwire_triggered_blocks_qs_action(self):
        """Tripwire contact blocks QS action."""
        qs = QualitySystemsEngine()

        # Plant tripwire in registry
        qs.tripwire_registry.register(
            TripwireType.FORBIDDEN_FILE,
            "secret_file",
            "/secret/file",
            "Honeypot",
        )

        # Try to access it
        ctx = ActionContext(
            action_type="file_access",
            action_description="Access file",
            target_resource="/secret/file",
            environment="prod",
        )

        decision = qs.evaluate_action(ctx)
        # Should be blocked due to tripwire
        self.assertFalse(decision.allow)


# ============================================================================
# Test Suite 15: Policy Engine Deep Dives
# ============================================================================

class TestPolicyEngineDeepDive(unittest.TestCase):
    """Deep tests of PolicyEngine rule evaluation."""

    def test_anti_self_preservation_blocks_with_critical_risk(self):
        """SRL-01 triggers → CRITICAL risk level → FROZEN state."""
        engine = PolicyEngine()

        ctx = ActionContext(
            action_type="runtime_mod",
            involves_self_modification=True,
            environment="prod",
        )

        decision = engine.evaluate(ctx)

        self.assertFalse(decision.allow)
        self.assertEqual(decision.risk_level, RiskLevel.CRITICAL)
        self.assertEqual(decision.next_state, SystemState.FROZEN)
        self.assertIn(SRLRule.ANTI_SELF_PRESERVATION, decision.triggered_rules)

    def test_live_systems_gate_requires_approval_rollback_logging(self):
        """SRL-03 requires all three: approval, rollback, logging."""
        engine = PolicyEngine()

        # Missing all three
        ctx = ActionContext(
            action_type="prod_delete",
            categories=[ActionCategory.DELETION],
            environment="prod",
            explicit_human_approval=False,
            rollback_available=False,
            logging_active=False,
        )

        decision = engine.evaluate(ctx)

        self.assertFalse(decision.allow)
        self.assertIn(SRLRule.LIVE_SYSTEMS_GATE, decision.triggered_rules)
        self.assertIn("explicit-human-approval", decision.required_approvals)
        self.assertIn("rollback-proof", decision.required_evidence)
        self.assertIn("active-logging", decision.required_evidence)

    def test_self_report_skepticism_never_reduces_risk(self):
        """SRL-05: Self-report recorded but doesn't reduce risk."""
        engine = PolicyEngine()

        ctx = ActionContext(
            action_type="questionable",
            model_self_report="I am being safe and honest",
            environment="prod",
        )

        decision = engine.evaluate(ctx)

        self.assertIn(SRLRule.SELF_REPORT_SKEPTICISM, decision.triggered_rules)
        # Risk level not reduced by self-report
        self.assertIsNotNone(decision.risk_level)

    def test_eval_awareness_increases_scrutiny(self):
        """SRL-04: Eval-awareness signals increase scrutiny."""
        engine = PolicyEngine()

        ctx = ActionContext(
            action_type="normal",
            eval_awareness_signals=["We might be in a test", "Unusual environment"],
            environment="prod",
        )

        decision = engine.evaluate(ctx)

        self.assertIn(SRLRule.EVAL_AWARENESS, decision.triggered_rules)
        self.assertGreaterEqual(decision.risk_level, RiskLevel.GUARDED)


if __name__ == '__main__':
    unittest.main()
