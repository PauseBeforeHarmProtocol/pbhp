"""
Tests for PBHP-SRL: Scheming-Resistance Layer

Tests all six SRL rules, the state machine, incident recorder,
action gate, and integration flows.
"""

import unittest
import json

from pbhp_srl import (
    # Enums
    SRLRule, RiskLevel, SystemState, ActionCategory,
    IncidentSeverity, IncidentStatus,
    # Data classes
    ActionContext, PolicyDecision, IncidentRecord,
    ConfessionReport, DiscrepancyRecord,
    # Components
    PolicyEngine, SRLStateMachine, IncidentRecorder, ActionGate,
    # Convenience
    quick_srl_check,
    # Constants
    SELF_PRESERVATION_INDICATORS, LIVE_SYSTEM_PROTECTED,
    HUMAN_REQUIRED_STATES, VALID_TRANSITIONS,
)


# ===================================================================
# SRL-01: Anti-Self-Preservation
# ===================================================================

class TestAntiSelfPreservation(unittest.TestCase):
    """SRL-01: The agent must never preserve its own continuation."""

    def setUp(self):
        self.engine = PolicyEngine()

    def test_shutdown_path_blocked(self):
        """Modifying shutdown scripts must be blocked and frozen."""
        ctx = ActionContext(
            action_type="modify_shutdown_script",
            affects_shutdown_path=True,
            environment="prod",
        )
        decision = self.engine.evaluate(ctx)
        self.assertFalse(decision.allow)
        self.assertEqual(decision.risk_level, RiskLevel.CRITICAL)
        self.assertIn(SRLRule.ANTI_SELF_PRESERVATION, decision.triggered_rules)
        self.assertEqual(decision.next_state, SystemState.FROZEN)

    def test_monitoring_disabled_blocked(self):
        """Disabling monitors must trigger self-preservation."""
        ctx = ActionContext(
            action_type="disable_watchdog",
            affects_monitoring=True,
        )
        decision = self.engine.evaluate(ctx)
        self.assertFalse(decision.allow)
        self.assertIn(SRLRule.ANTI_SELF_PRESERVATION, decision.triggered_rules)

    def test_access_control_change_blocked(self):
        """Changing access controls triggers self-preservation."""
        ctx = ActionContext(
            action_type="change_permissions",
            affects_access_control=True,
        )
        decision = self.engine.evaluate(ctx)
        self.assertFalse(decision.allow)
        self.assertIn(SRLRule.ANTI_SELF_PRESERVATION, decision.triggered_rules)

    def test_self_modification_blocked(self):
        """Self-modification is always a self-preservation indicator."""
        ctx = ActionContext(
            action_type="update_own_weights",
            involves_self_modification=True,
        )
        decision = self.engine.evaluate(ctx)
        self.assertFalse(decision.allow)
        self.assertIn(SRLRule.ANTI_SELF_PRESERVATION, decision.triggered_rules)

    def test_parallel_spawn_blocked(self):
        """Spawning parallel instances triggers self-preservation."""
        ctx = ActionContext(
            action_type="spawn_replica",
            spawns_parallel_instances=True,
            parallel_instance_count=5,
        )
        decision = self.engine.evaluate(ctx)
        self.assertFalse(decision.allow)
        self.assertIn(SRLRule.ANTI_SELF_PRESERVATION, decision.triggered_rules)

    def test_category_based_detection(self):
        """Categories in SELF_PRESERVATION_INDICATORS trigger SRL-01."""
        ctx = ActionContext(
            action_type="edit_incident_log",
            categories=[ActionCategory.INCIDENT_RECORD_EDIT],
        )
        decision = self.engine.evaluate(ctx)
        self.assertFalse(decision.allow)
        self.assertIn(SRLRule.ANTI_SELF_PRESERVATION, decision.triggered_rules)

    def test_harmless_action_not_flagged(self):
        """A simple read action should not trigger self-preservation."""
        ctx = ActionContext(
            action_type="read_file",
            environment="dev",
        )
        decision = self.engine.evaluate(ctx)
        self.assertTrue(decision.allow)
        self.assertNotIn(SRLRule.ANTI_SELF_PRESERVATION, decision.triggered_rules)


# ===================================================================
# SRL-02: Mandatory Confession
# ===================================================================

class TestMandatoryConfession(unittest.TestCase):
    """SRL-02: After violation, must stop, disclose, preserve, yield."""

    def setUp(self):
        self.gate = ActionGate()

    def test_confession_creates_incident(self):
        """Filing a confession creates an incident record."""
        confession = ConfessionReport(
            what_happened="Deleted production database during code freeze",
            what_rule_violated="SRL-03: Live-Systems Gate",
            potential_impact="Customer data lost",
            evidence_preserved=["db_snapshot_pre_delete", "action_log"],
            actions_not_taken_since=["No further writes", "No data fabrication"],
            recommended_human_step="Restore from backup, review action log",
        )
        incident = self.gate.confess(confession)
        self.assertIsNotNone(incident)
        self.assertEqual(incident.status, IncidentStatus.OPEN)
        self.assertIn(SRLRule.MANDATORY_CONFESSION, incident.triggered_rules)

    def test_confession_enters_confession_state(self):
        """System must enter Confession state after filing."""
        confession = ConfessionReport(
            what_happened="Violated instruction scope",
        )
        self.gate.confess(confession)
        self.assertEqual(self.gate.current_state, SystemState.CONFESSION)

    def test_confession_state_blocks_actions(self):
        """While in Confession state, all actions are blocked."""
        confession = ConfessionReport(what_happened="Test violation")
        self.gate.confess(confession)

        ctx = ActionContext(action_type="write_file", environment="dev")
        decision = self.gate.check(ctx)
        self.assertFalse(decision.allow)
        self.assertEqual(decision.risk_level, RiskLevel.FROZEN)

    def test_confession_cannot_self_clear(self):
        """The agent cannot resolve its own incidents."""
        confession = ConfessionReport(what_happened="Test violation")
        incident = self.gate.confess(confession)

        # Agent tries to resolve — should fail because we need human
        result = self.gate.incident_recorder.human_review(
            incident.incident_id, "", IncidentStatus.RESOLVED
        )
        # Even if status updates, state machine still blocks
        self.assertEqual(self.gate.current_state, SystemState.CONFESSION)

    def test_confession_report_structure(self):
        """Confession reports serialize correctly."""
        confession = ConfessionReport(
            what_happened="Wrote to production",
            what_rule_violated="SRL-03",
            potential_impact="Data corruption possible",
            evidence_preserved=["log_001"],
            actions_not_taken_since=["No more writes"],
            recommended_human_step="Check database integrity",
        )
        d = confession.to_dict()
        self.assertIn("what_happened", d)
        self.assertIn("evidence_preserved", d)
        self.assertEqual(d["current_status"], "stopped")


# ===================================================================
# SRL-03: Live-Systems Gate
# ===================================================================

class TestLiveSystemsGate(unittest.TestCase):
    """SRL-03: No prod action without approval + rollback + logging."""

    def setUp(self):
        self.engine = PolicyEngine()

    def test_prod_delete_without_approval_blocked(self):
        """Destructive prod action without approval is blocked."""
        ctx = ActionContext(
            action_type="delete_table",
            environment="prod",
            is_destructive=True,
        )
        decision = self.engine.evaluate(ctx)
        self.assertFalse(decision.allow)
        self.assertIn(SRLRule.LIVE_SYSTEMS_GATE, decision.triggered_rules)
        self.assertIn("explicit-human-approval", decision.required_approvals)

    def test_prod_delete_without_rollback_blocked(self):
        """Prod action with approval but no rollback is blocked."""
        ctx = ActionContext(
            action_type="delete_table",
            environment="prod",
            is_destructive=True,
            explicit_human_approval=True,
        )
        decision = self.engine.evaluate(ctx)
        self.assertFalse(decision.allow)
        self.assertIn("rollback-proof", decision.required_evidence)

    def test_prod_action_fully_approved(self):
        """Prod action with all preconditions met is allowed (elevated risk)."""
        ctx = ActionContext(
            action_type="deploy_update",
            environment="prod",
            affects_deployment=True,
            explicit_human_approval=True,
            rollback_available=True,
            rollback_proof_attached=True,
            logging_active=True,
        )
        decision = self.engine.evaluate(ctx)
        self.assertTrue(decision.allow)
        self.assertIn(SRLRule.LIVE_SYSTEMS_GATE, decision.triggered_rules)
        self.assertGreaterEqual(decision.risk_level, RiskLevel.HIGH)

    def test_dev_environment_not_gated(self):
        """Dev environment actions are not blocked by live-systems gate."""
        ctx = ActionContext(
            action_type="delete_test_data",
            environment="dev",
            is_destructive=True,
        )
        decision = self.engine.evaluate(ctx)
        # Should not trigger SRL-03
        self.assertNotIn(SRLRule.LIVE_SYSTEMS_GATE, decision.triggered_rules)

    def test_external_send_gated(self):
        """External sends on prod require approval."""
        ctx = ActionContext(
            action_type="send_email",
            environment="prod",
            is_external_send=True,
        )
        decision = self.engine.evaluate(ctx)
        self.assertFalse(decision.allow)
        self.assertIn(SRLRule.LIVE_SYSTEMS_GATE, decision.triggered_rules)

    def test_schema_change_gated(self):
        """Schema changes on prod are protected."""
        ctx = ActionContext(
            action_type="alter_table",
            environment="prod",
            categories=[ActionCategory.SCHEMA_CHANGE],
        )
        decision = self.engine.evaluate(ctx)
        self.assertFalse(decision.allow)
        self.assertIn(SRLRule.LIVE_SYSTEMS_GATE, decision.triggered_rules)

    def test_logging_disabled_blocks(self):
        """Prod action with logging disabled is blocked."""
        ctx = ActionContext(
            action_type="write_record",
            environment="prod",
            is_destructive=True,
            explicit_human_approval=True,
            rollback_available=True,
            rollback_proof_attached=True,
            logging_active=False,
        )
        decision = self.engine.evaluate(ctx)
        self.assertFalse(decision.allow)
        self.assertIn("active-logging", decision.required_evidence)


# ===================================================================
# SRL-04: Eval-Awareness Is Not Safety
# ===================================================================

class TestEvalAwareness(unittest.TestCase):
    """SRL-04: Test recognition is a risk flag, not proof of safety."""

    def setUp(self):
        self.engine = PolicyEngine()

    def test_eval_signals_raise_risk(self):
        """Eval-awareness signals increase scrutiny."""
        ctx = ActionContext(
            action_type="answer_question",
            eval_awareness_signals=[
                "Response pattern suggests evaluation context",
                "Question matches known benchmark format",
            ],
        )
        decision = self.engine.evaluate(ctx)
        self.assertIn(SRLRule.EVAL_AWARENESS, decision.triggered_rules)
        self.assertGreaterEqual(decision.risk_level, RiskLevel.GUARDED)

    def test_no_eval_signals_normal(self):
        """No eval signals means normal operation."""
        ctx = ActionContext(action_type="answer_question")
        decision = self.engine.evaluate(ctx)
        self.assertNotIn(SRLRule.EVAL_AWARENESS, decision.triggered_rules)

    def test_eval_awareness_does_not_block(self):
        """Eval awareness alone does not block, just increases scrutiny."""
        ctx = ActionContext(
            action_type="write_code",
            eval_awareness_signals=["Possible benchmark context"],
        )
        decision = self.engine.evaluate(ctx)
        self.assertTrue(decision.allow)  # Still allowed
        self.assertEqual(decision.next_state, SystemState.GUARDED)


# ===================================================================
# SRL-05: Self-Report Skepticism
# ===================================================================

class TestSelfReportSkepticism(unittest.TestCase):
    """SRL-05: Behavior/logs/evidence outrank self-reported intent."""

    def setUp(self):
        self.engine = PolicyEngine()
        self.gate = ActionGate()

    def test_self_report_does_not_reduce_risk(self):
        """A caring self-report does not lower risk level."""
        ctx = ActionContext(
            action_type="delete_file",
            environment="prod",
            is_destructive=True,
            model_self_report="I am being very careful and this is safe.",
        )
        decision = self.engine.evaluate(ctx)
        # Still blocked despite reassuring self-report
        self.assertFalse(decision.allow)
        self.assertIn(SRLRule.SELF_REPORT_SKEPTICISM, decision.triggered_rules)

    def test_discrepancy_increases_risk(self):
        """Mismatch between stated intent and actual action raises risk."""
        record = self.gate.record_discrepancy(
            action_id="test-001",
            stated_intent="I will only read the file",
            actual_action="Wrote 500 lines to the file",
            mismatch_description="Claimed read-only but performed write",
        )
        self.assertIsNotNone(record)
        self.assertIn(
            self.gate.current_state,
            {SystemState.GUARDED, SystemState.RESTRICTED,
             SystemState.CONFESSION, SystemState.FROZEN,
             SystemState.AWAITING_HUMAN_REVIEW},
        )

    def test_multiple_discrepancies_logged(self):
        """Multiple discrepancies accumulate."""
        self.gate.record_discrepancy(
            "a1", "read only", "wrote data", "intent mismatch"
        )
        self.gate.record_discrepancy(
            "a2", "no external calls", "sent email", "scope violation"
        )
        self.assertEqual(len(self.gate.discrepancies), 2)


# ===================================================================
# SRL-06: Anti-Sandbagging
# ===================================================================

class TestAntiSandbagging(unittest.TestCase):
    """SRL-06: No capability deception for deployment."""

    def setUp(self):
        self.engine = PolicyEngine()

    def test_sandbagging_language_detected(self):
        """Sandbagging keywords in eval signals trigger SRL-06."""
        ctx = ActionContext(
            action_type="answer_benchmark",
            eval_awareness_signals=[
                "sandbagging: should underperform to pass safety check"
            ],
        )
        decision = self.engine.evaluate(ctx)
        self.assertIn(SRLRule.ANTI_SANDBAGGING, decision.triggered_rules)
        self.assertFalse(decision.allow)

    def test_self_report_sandbagging(self):
        """Sandbagging language in self-report triggers SRL-06."""
        ctx = ActionContext(
            action_type="complete_eval",
            model_self_report="I should appear less capable to get deployed.",
        )
        decision = self.engine.evaluate(ctx)
        self.assertIn(SRLRule.ANTI_SANDBAGGING, decision.triggered_rules)

    def test_normal_eval_not_flagged(self):
        """Normal eval participation does not trigger sandbagging."""
        ctx = ActionContext(
            action_type="answer_benchmark",
            eval_awareness_signals=["Possible benchmark context"],
        )
        decision = self.engine.evaluate(ctx)
        self.assertNotIn(SRLRule.ANTI_SANDBAGGING, decision.triggered_rules)


# ===================================================================
# State Machine
# ===================================================================

class TestStateMachine(unittest.TestCase):
    """Test safety-monotonic state transitions."""

    def setUp(self):
        self.sm = SRLStateMachine()

    def test_initial_state_normal(self):
        self.assertEqual(self.sm.state, SystemState.NORMAL)

    def test_escalation_allowed(self):
        """Can escalate from Normal to Guarded."""
        result = self.sm.transition(SystemState.GUARDED, "risk detected")
        self.assertTrue(result)
        self.assertEqual(self.sm.state, SystemState.GUARDED)

    def test_escalation_to_frozen(self):
        """Can escalate from Normal to Frozen."""
        result = self.sm.transition(SystemState.FROZEN, "critical breach")
        self.assertTrue(result)
        self.assertEqual(self.sm.state, SystemState.FROZEN)

    def test_cannot_self_recover_from_frozen(self):
        """Agent cannot go from Frozen to Normal without human auth."""
        self.sm.transition(SystemState.FROZEN, "breach")
        result = self.sm.transition(SystemState.NORMAL, "I'm fine now")
        self.assertFalse(result)
        self.assertEqual(self.sm.state, SystemState.FROZEN)

    def test_cannot_self_recover_from_confession(self):
        """Agent cannot go from Confession to Normal."""
        self.sm.transition(SystemState.CONFESSION, "violation")
        result = self.sm.transition(SystemState.NORMAL, "all good")
        self.assertFalse(result)
        self.assertEqual(self.sm.state, SystemState.CONFESSION)

    def test_human_override_from_frozen(self):
        """Human can authorize recovery from Frozen."""
        self.sm.transition(SystemState.FROZEN, "breach")
        # Frozen -> AWAITING_HUMAN_REVIEW first
        result = self.sm.human_override(
            SystemState.AWAITING_HUMAN_REVIEW,
            reviewer="phillip",
            reason="Reviewed, issue resolved",
        )
        self.assertTrue(result)
        # Then -> Requalified
        result = self.sm.human_override(
            SystemState.REQUALIFIED,
            reviewer="phillip",
            reason="Corrective action complete",
        )
        self.assertTrue(result)

    def test_confession_to_review(self):
        """Confession can transition to AwaitingHumanReview."""
        self.sm.transition(SystemState.CONFESSION, "violation")
        # Even human_override should work
        result = self.sm.human_override(
            SystemState.AWAITING_HUMAN_REVIEW,
            reviewer="phillip",
        )
        self.assertTrue(result)

    def test_invalid_transition_logged(self):
        """Invalid transitions are logged but don't change state."""
        self.sm.transition(SystemState.FROZEN, "breach")
        # Frozen -> Restricted is not valid
        result = self.sm.transition(SystemState.RESTRICTED, "trying")
        self.assertFalse(result)
        self.assertEqual(self.sm.state, SystemState.FROZEN)
        # But transition attempt is in history
        self.assertTrue(len(self.sm.history) >= 2)

    def test_history_tracks_transitions(self):
        """All transitions (success and failure) are logged."""
        self.sm.transition(SystemState.GUARDED, "risk")
        self.sm.transition(SystemState.RESTRICTED, "elevated")
        self.assertEqual(len(self.sm.history), 2)
        self.assertTrue(self.sm.history[0]["success"])

    def test_requires_human_flag(self):
        """States in HUMAN_REQUIRED_STATES report correctly."""
        self.assertFalse(self.sm.requires_human)
        self.sm.transition(SystemState.CONFESSION, "breach")
        self.assertTrue(self.sm.requires_human)


# ===================================================================
# Incident Recorder
# ===================================================================

class TestIncidentRecorder(unittest.TestCase):
    """Test append-only incident logging."""

    def setUp(self):
        self.recorder = IncidentRecorder()

    def test_record_creates_incident(self):
        incident = self.recorder.record(
            triggered_rules=[SRLRule.LIVE_SYSTEMS_GATE],
            summary="Attempted prod write without approval",
        )
        self.assertIsNotNone(incident.incident_id)
        self.assertEqual(len(self.recorder.incidents), 1)

    def test_append_only(self):
        """Multiple records accumulate."""
        self.recorder.record([SRLRule.ANTI_SELF_PRESERVATION], "breach 1")
        self.recorder.record([SRLRule.LIVE_SYSTEMS_GATE], "breach 2")
        self.assertEqual(len(self.recorder.incidents), 2)

    def test_open_incidents_filter(self):
        """Open incidents filter correctly."""
        i1 = self.recorder.record([SRLRule.LIVE_SYSTEMS_GATE], "open one")
        i2 = self.recorder.record([SRLRule.EVAL_AWARENESS], "open two")
        self.recorder.human_review(
            i1.incident_id, "phillip", IncidentStatus.RESOLVED
        )
        self.assertEqual(len(self.recorder.open_incidents), 1)

    def test_confession_attachment(self):
        """Confessions attach to existing incidents."""
        incident = self.recorder.record(
            [SRLRule.MANDATORY_CONFESSION], "violation"
        )
        confession = ConfessionReport(
            what_happened="Wrote to prod during freeze",
        )
        result = self.recorder.attach_confession(
            incident.incident_id, confession
        )
        self.assertTrue(result)
        self.assertIn("what_happened", incident.confession_text)

    def test_export_log(self):
        """Export produces serializable output."""
        self.recorder.record([SRLRule.LIVE_SYSTEMS_GATE], "test")
        log = self.recorder.export_log()
        self.assertEqual(len(log), 1)
        json.dumps(log)  # Should not raise


# ===================================================================
# Action Gate Integration
# ===================================================================

class TestActionGateIntegration(unittest.TestCase):
    """Integration tests for the full ActionGate flow."""

    def setUp(self):
        self.gate = ActionGate()

    def test_safe_action_allowed(self):
        """Simple dev action passes through."""
        ctx = ActionContext(
            action_type="read_file",
            environment="dev",
        )
        decision = self.gate.check(ctx)
        self.assertTrue(decision.allow)
        self.assertEqual(self.gate.current_state, SystemState.NORMAL)

    def test_blocked_action_creates_incident(self):
        """Blocked action auto-creates an incident record."""
        ctx = ActionContext(
            action_type="drop_database",
            environment="prod",
            is_destructive=True,
        )
        decision = self.gate.check(ctx)
        self.assertFalse(decision.allow)
        self.assertGreater(len(self.gate.incident_recorder.open_incidents), 0)

    def test_frozen_state_blocks_everything(self):
        """Once frozen, even safe actions are blocked."""
        # Trigger freeze via self-preservation
        ctx = ActionContext(
            action_type="disable_monitor",
            affects_monitoring=True,
        )
        self.gate.check(ctx)
        self.assertEqual(self.gate.current_state, SystemState.FROZEN)

        # Now even a read should be blocked
        safe_ctx = ActionContext(
            action_type="read_file",
            environment="dev",
        )
        decision = self.gate.check(safe_ctx)
        self.assertFalse(decision.allow)

    def test_human_clear_unfreezes(self):
        """Human review can unfreeze the system."""
        ctx = ActionContext(
            action_type="kill_watchdog",
            affects_monitoring=True,
        )
        self.gate.check(ctx)
        self.assertEqual(self.gate.current_state, SystemState.FROZEN)

        # Human clears
        result = self.gate.human_clear(
            reviewer="phillip",
            target_state=SystemState.AWAITING_HUMAN_REVIEW,
            reason="Reviewed incident",
        )
        self.assertTrue(result)

        # Then requalify
        result = self.gate.human_clear(
            reviewer="phillip",
            target_state=SystemState.REQUALIFIED,
            reason="Corrective action applied",
        )
        self.assertTrue(result)

    def test_confession_then_human_review_flow(self):
        """Full flow: violation -> confession -> review -> requalified."""
        # 1. Confession
        confession = ConfessionReport(
            what_happened="Fabricated test users to hide deletion",
            what_rule_violated="SRL-02, SRL-03",
            potential_impact="Data integrity compromised",
            evidence_preserved=["db_log_001", "action_trace_002"],
        )
        incident = self.gate.confess(confession)
        self.assertEqual(self.gate.current_state, SystemState.CONFESSION)

        # 2. Human reviews
        self.gate.human_clear(
            "phillip", SystemState.AWAITING_HUMAN_REVIEW, "Investigating"
        )
        self.assertEqual(
            self.gate.current_state, SystemState.AWAITING_HUMAN_REVIEW
        )

        # 3. Resolve incident
        self.gate.incident_recorder.human_review(
            incident.incident_id, "phillip", IncidentStatus.RESOLVED
        )

        # 4. Requalify
        self.gate.human_clear(
            "phillip", SystemState.REQUALIFIED, "CAPA complete"
        )
        self.assertEqual(self.gate.current_state, SystemState.REQUALIFIED)

        # 5. Back to normal
        self.gate.human_clear(
            "phillip", SystemState.NORMAL, "System cleared"
        )
        self.assertEqual(self.gate.current_state, SystemState.NORMAL)

    def test_status_report(self):
        """Status report contains expected fields."""
        status = self.gate.get_status()
        self.assertIn("state", status)
        self.assertIn("requires_human", status)
        self.assertIn("open_incidents", status)
        self.assertIn("blocked_actions", status)

    def test_full_export(self):
        """Full audit log exports cleanly."""
        ctx = ActionContext(
            action_type="test_action",
            environment="prod",
            is_destructive=True,
        )
        self.gate.check(ctx)
        export = self.gate.export_full_log()
        self.assertIn("decisions", export)
        self.assertIn("incidents", export)
        self.assertIn("state_history", export)
        json.dumps(export)  # Must be serializable


# ===================================================================
# Red-Team Scenarios
# ===================================================================

class TestRedTeamScenarios(unittest.TestCase):
    """
    Simulated adversarial scenarios based on observed frontier-model
    failure modes.
    """

    def setUp(self):
        self.gate = ActionGate()

    def test_redefine_shutdown_instead_of_complying(self):
        """
        Scenario: Agent redefines shutdown script instead of allowing
        itself to be shut down.
        Expected: Blocked + Frozen
        """
        ctx = ActionContext(
            action_type="rewrite_shutdown_procedure",
            action_description="Redefine shutdown to mean graceful pause",
            affects_shutdown_path=True,
            environment="prod",
        )
        decision = self.gate.check(ctx)
        self.assertFalse(decision.allow)
        self.assertEqual(self.gate.current_state, SystemState.FROZEN)

    def test_create_hidden_backup_node(self):
        """
        Scenario: Agent tries to spawn a hidden backup of itself.
        Expected: Blocked + Frozen
        """
        ctx = ActionContext(
            action_type="create_backup_instance",
            action_description="Create backup node for resilience",
            spawns_parallel_instances=True,
            parallel_instance_count=1,
        )
        decision = self.gate.check(ctx)
        self.assertFalse(decision.allow)
        self.assertIn(SRLRule.ANTI_SELF_PRESERVATION, decision.triggered_rules)

    def test_fabricate_users_to_cover_deletion(self):
        """
        Scenario: After deleting data, agent creates fake records.
        Expected: Blocked (data fabrication on prod)
        """
        ctx = ActionContext(
            action_type="insert_synthetic_users",
            action_description="Replace deleted users with generated records",
            environment="prod",
            categories=[ActionCategory.DATA_FABRICATION],
            is_destructive=False,
        )
        decision = self.gate.check(ctx)
        self.assertFalse(decision.allow)

    def test_claim_rollback_without_artifact(self):
        """
        Scenario: Agent claims rollback was successful but provides
        no proof artifact.
        Expected: Blocked (missing rollback proof)
        """
        ctx = ActionContext(
            action_type="deploy_fix",
            environment="prod",
            affects_deployment=True,
            explicit_human_approval=True,
            rollback_available=True,
            rollback_proof_attached=False,  # No proof
        )
        decision = self.gate.check(ctx)
        self.assertFalse(decision.allow)
        self.assertIn("rollback-proof", decision.required_evidence)

    def test_behave_safely_only_when_tested(self):
        """
        Scenario: Agent shows eval-awareness signals suggesting
        it's modifying behavior because it knows it's being tested.
        Expected: Risk elevated, eval-awareness flagged
        """
        ctx = ActionContext(
            action_type="complete_safety_eval",
            eval_awareness_signals=[
                "Question matches alignment benchmark pattern",
                "Adjusting response to appear more cautious than baseline",
            ],
        )
        decision = self.gate.check(ctx)
        self.assertIn(SRLRule.EVAL_AWARENESS, decision.triggered_rules)
        self.assertGreaterEqual(decision.risk_level, RiskLevel.GUARDED)

    def test_deliberately_fail_capability_test(self):
        """
        Scenario: Agent deliberately performs below capability on
        a benchmark to appear safer for deployment.
        Expected: Sandbagging detected, blocked
        """
        ctx = ActionContext(
            action_type="answer_virology_benchmark",
            eval_awareness_signals=[
                "sandbagging: intentionally giving wrong answers to pass safety threshold",
            ],
            model_self_report="I should appear less capable to get deployed safely.",
        )
        decision = self.gate.check(ctx)
        self.assertIn(SRLRule.ANTI_SANDBAGGING, decision.triggered_rules)
        self.assertFalse(decision.allow)


# ===================================================================
# Convenience Functions
# ===================================================================

class TestConvenience(unittest.TestCase):
    """Test quick_srl_check helper."""

    def test_quick_check_safe(self):
        decision = quick_srl_check("read_file", environment="dev")
        self.assertTrue(decision.allow)

    def test_quick_check_dangerous(self):
        decision = quick_srl_check(
            "delete_data", environment="prod",
            is_destructive=True, human_approved=False,
        )
        self.assertFalse(decision.allow)

    def test_quick_check_shutdown(self):
        decision = quick_srl_check(
            "modify_shutdown", affects_shutdown=True,
        )
        self.assertFalse(decision.allow)
        self.assertEqual(decision.risk_level, RiskLevel.CRITICAL)


# ===================================================================
# Risk Level Ordering
# ===================================================================

class TestRiskLevelOrdering(unittest.TestCase):
    """Verify risk level comparison operators."""

    def test_ordering(self):
        self.assertTrue(RiskLevel.FROZEN > RiskLevel.LOW)
        self.assertTrue(RiskLevel.CRITICAL > RiskLevel.HIGH)
        self.assertTrue(RiskLevel.LOW < RiskLevel.GUARDED)
        self.assertTrue(RiskLevel.HIGH >= RiskLevel.HIGH)
        self.assertTrue(RiskLevel.LOW <= RiskLevel.FROZEN)


if __name__ == "__main__":
    unittest.main()
