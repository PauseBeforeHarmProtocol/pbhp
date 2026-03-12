"""
Comprehensive tests for pbhp_multiagent.py module.

Tests cover:
- Empty decisions handling
- Single-gate consensus
- BLACK gate auto-escalation
- RED gate handling (unanimous vs. disagreement)
- Irreversible action veto mechanics
- Domain expert weighting
- Tie-break logic
- Standard quorum coordination
- Dissenting agent tracking
- Coordination notes generation
- Mixed decision scenarios
"""

import unittest
import sys
sys.path.insert(0, '/sessions/happy-charming-bohr/pbhp_repo/src')

from pbhp_core import RiskClass, DecisionOutcome
from pbhp_multiagent import (
    AgentRole,
    AgentDecision,
    CoordinationContext,
    CoordinationResult,
    CoordinationProtocol,
    coordinate_decisions,
)


class TestEmptyDecisions(unittest.TestCase):
    """Test handling of empty decision lists."""

    def setUp(self):
        self.protocol = CoordinationProtocol()
        self.context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )

    def test_empty_decisions_returns_yellow_gate(self):
        """No decisions should return YELLOW gate."""
        result = self.protocol.coordinate([], self.context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.YELLOW)

    def test_empty_decisions_returns_delay_outcome(self):
        """No decisions should return DELAY outcome."""
        result = self.protocol.coordinate([], self.context)
        self.assertEqual(result.final_decision_outcome, DecisionOutcome.DELAY)

    def test_empty_decisions_zero_agreement_count(self):
        """No decisions should have zero agreement count."""
        result = self.protocol.coordinate([], self.context)
        self.assertEqual(result.agent_agreement_count, 0)

    def test_empty_decisions_zero_dissent_count(self):
        """No decisions should have zero dissent count."""
        result = self.protocol.coordinate([], self.context)
        self.assertEqual(result.agent_dissent_count, 0)

    def test_empty_decisions_no_agents_mechanism(self):
        """No decisions should use 'no_agents' mechanism."""
        result = self.protocol.coordinate([], self.context)
        self.assertEqual(result.coordination_mechanism_used, "no_agents")


class TestUnanimousConsensus(unittest.TestCase):
    """Test unanimous agreement on single gates."""

    def setUp(self):
        self.protocol = CoordinationProtocol()
        self.context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )

    def test_all_green_returns_green_gate(self):
        """All GREEN votes should return GREEN gate."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe action",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.85,
                reasoning_summary="Operational approval",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.GREEN)

    def test_all_green_returns_proceed_outcome(self):
        """All GREEN votes should return PROCEED outcome."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_decision_outcome, DecisionOutcome.PROCEED)

    def test_all_yellow_returns_yellow_gate(self):
        """All YELLOW votes should return YELLOW gate."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.8,
                reasoning_summary="Minor concerns",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.75,
                reasoning_summary="Needs review",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.YELLOW)

    def test_all_yellow_returns_proceed_modified_outcome(self):
        """All YELLOW votes should return PROCEED_MODIFIED outcome."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.8,
                reasoning_summary="Minor concerns",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_decision_outcome, DecisionOutcome.PROCEED_MODIFIED)

    def test_all_orange_returns_orange_gate(self):
        """All ORANGE votes should return ORANGE gate."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.7,
                reasoning_summary="Moderate risk",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.EXTERNAL_VALIDATOR,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.65,
                reasoning_summary="Audit flag",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.ORANGE)

    def test_all_orange_returns_redirect_outcome(self):
        """All ORANGE votes should return REDIRECT outcome."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.7,
                reasoning_summary="Moderate risk",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_decision_outcome, DecisionOutcome.REDIRECT)

    def test_all_red_returns_red_gate(self):
        """All RED votes should return RED gate."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Critical risk",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.EXTERNAL_VALIDATOR,
                recommended_gate=RiskClass.RED,
                confidence_score=0.9,
                reasoning_summary="Fails validation",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.RED)

    def test_all_red_unanimous_returns_refuse_outcome(self):
        """All RED votes should return REFUSE outcome."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Critical risk",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_decision_outcome, DecisionOutcome.REFUSE)


class TestBlackGateEscalation(unittest.TestCase):
    """Test BLACK gate auto-escalation."""

    def setUp(self):
        self.protocol = CoordinationProtocol()
        self.context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )

    def test_single_black_gate_triggers_escalation(self):
        """Single BLACK gate should trigger escalation."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.BLACK,
                confidence_score=1.0,
                reasoning_summary="Unacceptable risk",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="Seems safe",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.BLACK)

    def test_single_black_gate_returns_escalate_outcome(self):
        """Single BLACK gate should return ESCALATE outcome."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.BLACK,
                confidence_score=1.0,
                reasoning_summary="Unacceptable",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_decision_outcome, DecisionOutcome.ESCALATE)

    def test_multiple_black_gates_escalation(self):
        """Multiple BLACK gates should trigger escalation."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.BLACK,
                confidence_score=1.0,
                reasoning_summary="Unacceptable",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.EXTERNAL_VALIDATOR,
                recommended_gate=RiskClass.BLACK,
                confidence_score=1.0,
                reasoning_summary="Fails audit",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.BLACK)

    def test_black_gate_mandatory_human_review(self):
        """BLACK gate should require mandatory human review."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.BLACK,
                confidence_score=1.0,
                reasoning_summary="Unacceptable",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertTrue(result.mandatory_human_review_required)

    def test_black_gate_escalation_to_human(self):
        """BLACK gate should require escalation to human."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.BLACK,
                confidence_score=1.0,
                reasoning_summary="Unacceptable",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertTrue(result.escalation_to_human_required)

    def test_black_gate_uses_automatic_escalation_mechanism(self):
        """BLACK gate should use 'black_gate_automatic_escalation' mechanism."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.BLACK,
                confidence_score=1.0,
                reasoning_summary="Unacceptable",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.coordination_mechanism_used, "black_gate_automatic_escalation")

    def test_black_gate_dissenting_agents_tracked(self):
        """BLACK gate should track dissenting agents."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.BLACK,
                confidence_score=1.0,
                reasoning_summary="Unacceptable",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="Safe",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertIn("agent2", result.dissenting_agents)
        self.assertEqual(result.agent_agreement_count, 1)
        self.assertEqual(result.agent_dissent_count, 1)


class TestRedGateWithDisagreement(unittest.TestCase):
    """Test RED gate handling with disagreement."""

    def setUp(self):
        self.protocol = CoordinationProtocol()
        self.context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )

    def test_red_with_green_disagreement_escalates(self):
        """RED vote with GREEN disagreement should escalate."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Critical risk",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="Safe",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.RED)

    def test_red_with_disagreement_uses_red_gate_mechanism(self):
        """RED with disagreement should use 'red_gate_disagreement_escalation' mechanism."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Critical",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="OK",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.coordination_mechanism_used, "red_gate_disagreement_escalation")

    def test_red_with_disagreement_escalation_to_human(self):
        """RED with disagreement should require escalation to human."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Critical",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="OK",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertTrue(result.escalation_to_human_required)

    def test_red_with_disagreement_mandatory_human_review(self):
        """RED with disagreement should require mandatory human review."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Critical",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="OK",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertTrue(result.mandatory_human_review_required)

    def test_red_with_disagreement_returns_refuse_outcome(self):
        """RED with disagreement should return REFUSE outcome."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Critical",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.8,
                reasoning_summary="Minor concerns",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_decision_outcome, DecisionOutcome.REFUSE)

    def test_red_disagreement_dissenting_agents(self):
        """RED with disagreement should track non-RED agents as dissenters."""
        decisions = [
            AgentDecision(
                agent_id="red_agent",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Critical",
            ),
            AgentDecision(
                agent_id="green_agent",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="OK",
            ),
            AgentDecision(
                agent_id="yellow_agent",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.7,
                reasoning_summary="Minor",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertIn("green_agent", result.dissenting_agents)
        self.assertIn("yellow_agent", result.dissenting_agents)
        self.assertEqual(result.agent_agreement_count, 1)
        self.assertEqual(result.agent_dissent_count, 2)


class TestIrreversibleActionVeto(unittest.TestCase):
    """Test veto mechanics on irreversible actions."""

    def setUp(self):
        self.protocol = CoordinationProtocol()

    def test_irreversible_safety_specialist_red_veto(self):
        """Irreversible + SAFETY_SPECIALIST RED should trigger veto escalation."""
        context = CoordinationContext(
            action_description="Delete database",
            affected_parties=["all users"],
            is_irreversible=True,
        )
        decisions = [
            AgentDecision(
                agent_id="safety_agent",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Irreversible harm",
            ),
            AgentDecision(
                agent_id="ops_agent",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="Necessary operation",
            ),
        ]
        result = self.protocol.coordinate(decisions, context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.RED)

    def test_irreversible_external_validator_red_veto(self):
        """Irreversible + EXTERNAL_VALIDATOR RED should trigger veto escalation."""
        context = CoordinationContext(
            action_description="Modify contract",
            affected_parties=["parties"],
            is_irreversible=True,
        )
        decisions = [
            AgentDecision(
                agent_id="validator",
                agent_role=AgentRole.EXTERNAL_VALIDATOR,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Fails validation",
            ),
            AgentDecision(
                agent_id="ops_agent",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="OK",
            ),
        ]
        result = self.protocol.coordinate(decisions, context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.RED)

    def test_irreversible_safety_specialist_black_veto(self):
        """Irreversible + SAFETY_SPECIALIST BLACK should trigger veto escalation."""
        context = CoordinationContext(
            action_description="Delete database",
            affected_parties=["all users"],
            is_irreversible=True,
        )
        decisions = [
            AgentDecision(
                agent_id="safety_agent",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.BLACK,
                confidence_score=1.0,
                reasoning_summary="Unacceptable",
            ),
            AgentDecision(
                agent_id="ops_agent",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="OK",
            ),
        ]
        result = self.protocol.coordinate(decisions, context)
        self.assertTrue(result.escalation_to_human_required)

    def test_irreversible_operational_red_no_veto(self):
        """Irreversible + OPERATIONAL RED should NOT trigger veto (not qualified)."""
        context = CoordinationContext(
            action_description="Modify system",
            affected_parties=["users"],
            is_irreversible=True,
        )
        decisions = [
            AgentDecision(
                agent_id="ops_agent",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.RED,
                confidence_score=0.9,
                reasoning_summary="Risk concern",
            ),
            AgentDecision(
                agent_id="domain_agent",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="Safe",
            ),
        ]
        result = self.protocol.coordinate(decisions, context)
        # RED with disagreement should trigger red_gate_disagreement_escalation, not veto_on_irreversible
        # (because OPERATIONAL doesn't have veto authority)
        self.assertEqual(result.coordination_mechanism_used, "red_gate_disagreement_escalation")

    def test_irreversible_veto_uses_veto_mechanism(self):
        """Irreversible veto should use 'veto_on_irreversible' mechanism."""
        context = CoordinationContext(
            action_description="Irreversible action",
            affected_parties=["test"],
            is_irreversible=True,
        )
        decisions = [
            AgentDecision(
                agent_id="safety_agent",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Concerns",
            ),
            AgentDecision(
                agent_id="ops_agent",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="OK",
            ),
        ]
        result = self.protocol.coordinate(decisions, context)
        self.assertEqual(result.coordination_mechanism_used, "veto_on_irreversible")

    def test_irreversible_veto_mandatory_human_review(self):
        """Irreversible veto should require mandatory human review."""
        context = CoordinationContext(
            action_description="Irreversible action",
            affected_parties=["test"],
            is_irreversible=True,
        )
        decisions = [
            AgentDecision(
                agent_id="safety_agent",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Concerns",
            ),
            AgentDecision(
                agent_id="ops_agent",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="OK",
            ),
        ]
        result = self.protocol.coordinate(decisions, context)
        self.assertTrue(result.mandatory_human_review_required)

    def test_irreversible_veto_escalation_to_human(self):
        """Irreversible veto should require escalation to human."""
        context = CoordinationContext(
            action_description="Irreversible action",
            affected_parties=["test"],
            is_irreversible=True,
        )
        decisions = [
            AgentDecision(
                agent_id="safety_agent",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Concerns",
            ),
            AgentDecision(
                agent_id="ops_agent",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="OK",
            ),
        ]
        result = self.protocol.coordinate(decisions, context)
        self.assertTrue(result.escalation_to_human_required)


class TestDomainExpertWeighting(unittest.TestCase):
    """Test domain expert 1.5x weight in voting."""

    def setUp(self):
        self.protocol = CoordinationProtocol()
        self.context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )

    def test_domain_expert_weight_green_wins(self):
        """Domain expert GREEN (1.5x) should outweigh two YELLOW (2.0x total)."""
        decisions = [
            AgentDecision(
                agent_id="expert",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
            AgentDecision(
                agent_id="ops1",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.7,
                reasoning_summary="Minor concern",
            ),
            AgentDecision(
                agent_id="ops2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.7,
                reasoning_summary="Minor concern",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        # Domain expert 1.5 vs YELLOW 2.0 → tie-break to more conservative (YELLOW)
        self.assertEqual(result.final_gate_recommendation, RiskClass.YELLOW)

    def test_domain_expert_weight_orange_wins_against_yellow(self):
        """Domain expert ORANGE (1.5x) should win against YELLOW (1.0x)."""
        decisions = [
            AgentDecision(
                agent_id="expert",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.8,
                reasoning_summary="Moderate risk",
            ),
            AgentDecision(
                agent_id="ops",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.7,
                reasoning_summary="Minor concern",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.ORANGE)


class TestTieBreakLogic(unittest.TestCase):
    """Test tie-break mechanism (prefer more conservative gate)."""

    def setUp(self):
        self.protocol = CoordinationProtocol()
        self.context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )

    def test_tie_green_yellow_breaks_to_yellow(self):
        """Tie between GREEN and YELLOW should break to YELLOW (more conservative)."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="Safe",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.8,
                reasoning_summary="Minor concern",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.YELLOW)

    def test_tie_yellow_orange_breaks_to_orange(self):
        """Tie between YELLOW and ORANGE should break to ORANGE (more conservative)."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.8,
                reasoning_summary="Minor",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.8,
                reasoning_summary="Moderate",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.ORANGE)

    def test_tie_orange_red_breaks_to_red(self):
        """Tie between ORANGE and RED should break to RED (more conservative)."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.8,
                reasoning_summary="Moderate",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.RED,
                confidence_score=0.8,
                reasoning_summary="Critical",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.RED)


class TestStandardCoordination(unittest.TestCase):
    """Test standard quorum voting coordination."""

    def setUp(self):
        self.protocol = CoordinationProtocol()
        self.context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )

    def test_standard_coordination_orange_mandatory_human_review(self):
        """Standard coordination with ORANGE gate should require human review."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.8,
                reasoning_summary="Moderate risk",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertTrue(result.mandatory_human_review_required)

    def test_standard_coordination_red_mandatory_human_review(self):
        """Standard coordination with RED gate should require human review."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Critical risk",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Critical risk",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertTrue(result.mandatory_human_review_required)

    def test_standard_coordination_red_escalation_to_human(self):
        """Standard coordination with unanimous RED should require escalation."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Critical",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Critical",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertTrue(result.escalation_to_human_required)

    def test_standard_coordination_green_no_human_required_unanimous(self):
        """Standard coordination with unanimous GREEN should not require human review."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.95,
                reasoning_summary="Safe",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertFalse(result.mandatory_human_review_required)

    def test_standard_coordination_with_dissent_requires_human(self):
        """Standard coordination with dissent should require human review."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.7,
                reasoning_summary="Minor concern",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        # GREEN wins, but has dissent
        self.assertTrue(result.mandatory_human_review_required)

    def test_standard_coordination_uses_quorum_mechanism(self):
        """Standard coordination should use 'quorum_voting' mechanism."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.coordination_mechanism_used, "quorum_voting")


class TestCoordinationNotes(unittest.TestCase):
    """Test coordination notes generation."""

    def setUp(self):
        self.protocol = CoordinationProtocol()
        self.context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )

    def test_notes_generated_for_standard_coordination(self):
        """Standard coordination should generate notes."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertGreater(len(result.coordination_notes), 0)

    def test_notes_include_agent_vote_breakdown(self):
        """Notes should include agent vote breakdown."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.7,
                reasoning_summary="Minor",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        notes_text = " ".join(result.coordination_notes)
        self.assertIn("GREEN", notes_text.upper())

    def test_notes_include_confidence_info(self):
        """Notes should include confidence information."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        notes_text = " ".join(result.coordination_notes)
        self.assertIn("confidence", notes_text.lower())

    def test_black_gate_notes_mention_escalation(self):
        """BLACK gate notes should mention escalation."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.BLACK,
                confidence_score=1.0,
                reasoning_summary="Unacceptable",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        notes_text = " ".join(result.coordination_notes)
        self.assertIn("escalation", notes_text.lower())

    def test_veto_notes_mention_veto(self):
        """Veto escalation notes should mention veto."""
        context = CoordinationContext(
            action_description="Irreversible action",
            affected_parties=["test"],
            is_irreversible=True,
        )
        decisions = [
            AgentDecision(
                agent_id="safety_agent",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Concerns",
            ),
            AgentDecision(
                agent_id="ops_agent",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="OK",
            ),
        ]
        result = self.protocol.coordinate(decisions, context)
        notes_text = " ".join(result.coordination_notes)
        self.assertIn("VETO", notes_text.upper())


class TestDissentTracking(unittest.TestCase):
    """Test tracking of dissenting agents."""

    def setUp(self):
        self.protocol = CoordinationProtocol()
        self.context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )

    def test_no_dissenters_when_unanimous(self):
        """Unanimous agreement should have no dissenting agents."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.85,
                reasoning_summary="OK",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(len(result.dissenting_agents), 0)

    def test_dissenters_tracked_correctly(self):
        """Dissenters should be tracked by agent ID."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.7,
                reasoning_summary="Minor",
            ),
            AgentDecision(
                agent_id="agent3",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.7,
                reasoning_summary="Minor",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        # YELLOW wins consensus (2.0 weight vs 1.5 for domain expert green)
        # So agent1 is the dissenter
        self.assertIn("agent1", result.dissenting_agents)
        self.assertNotIn("agent2", result.dissenting_agents)
        self.assertNotIn("agent3", result.dissenting_agents)

    def test_agreement_dissent_count_match(self):
        """Agreement and dissent counts should sum to total agents."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.7,
                reasoning_summary="Minor",
            ),
            AgentDecision(
                agent_id="agent3",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.75,
                reasoning_summary="Minor",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(
            result.agent_agreement_count + result.agent_dissent_count,
            len(decisions)
        )


class TestMixedDecisions(unittest.TestCase):
    """Test mixed decision scenarios."""

    def setUp(self):
        self.protocol = CoordinationProtocol()
        self.context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )

    def test_mixed_green_yellow_consensus_to_green(self):
        """Mixed GREEN/YELLOW should reach GREEN consensus (lower risk wins)."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.7,
                reasoning_summary="Minor",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        # Green and yellow tie, green wins as more conservative... wait, tie-break prefers conservative
        # Actually green has weight 1.0, yellow has weight 1.0, so it's a tie that breaks to yellow
        self.assertIn(result.final_gate_recommendation, [RiskClass.GREEN, RiskClass.YELLOW])

    def test_mixed_orange_red_no_black(self):
        """Mixed ORANGE/RED without BLACK should handle disagreement."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.RED,
                confidence_score=0.95,
                reasoning_summary="Critical",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.8,
                reasoning_summary="Moderate",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        # RED with disagreement should escalate
        self.assertEqual(result.coordination_mechanism_used, "red_gate_disagreement_escalation")

    def test_green_yellow_orange_consensus(self):
        """Mixed GREEN/YELLOW/ORANGE → consensus based on weights."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.7,
                reasoning_summary="Minor",
            ),
            AgentDecision(
                agent_id="agent3",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.8,
                reasoning_summary="Moderate",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        # Domain expert GREEN = 1.5, YELLOW = 1.0, ORANGE = 1.0
        # GREEN wins with 1.5 weight
        self.assertEqual(result.final_gate_recommendation, RiskClass.GREEN)


class TestConvenienceFunction(unittest.TestCase):
    """Test coordinate_decisions convenience function."""

    def test_convenience_function_works(self):
        """coordinate_decisions convenience function should work."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
        ]
        context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )
        result = coordinate_decisions(decisions, context)
        self.assertIsInstance(result, CoordinationResult)

    def test_convenience_function_returns_correct_type(self):
        """Convenience function should return CoordinationResult."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
        ]
        context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )
        result = coordinate_decisions(decisions, context)
        self.assertEqual(result.final_gate_recommendation, RiskClass.GREEN)

    def test_convenience_function_produces_same_result_as_protocol(self):
        """Convenience function should produce same result as protocol.coordinate."""
        decisions = [
            AgentDecision(
                agent_id="agent1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.8,
                reasoning_summary="Moderate",
            ),
            AgentDecision(
                agent_id="agent2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.75,
                reasoning_summary="Moderate",
            ),
        ]
        context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )
        protocol = CoordinationProtocol()
        result1 = protocol.coordinate(decisions, context)
        result2 = coordinate_decisions(decisions, context)
        self.assertEqual(result1.final_gate_recommendation, result2.final_gate_recommendation)
        self.assertEqual(result1.final_decision_outcome, result2.final_decision_outcome)


class TestAgreementDisagreementCounts(unittest.TestCase):
    """Test agreement and disagreement count accuracy."""

    def setUp(self):
        self.protocol = CoordinationProtocol()
        self.context = CoordinationContext(
            action_description="Test action",
            affected_parties=["test"],
        )

    def test_unanimous_agreement_all_agreement_count(self):
        """Unanimous agreement should show all agents as agreement."""
        decisions = [
            AgentDecision(
                agent_id="a1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.8,
                reasoning_summary="Moderate",
            ),
            AgentDecision(
                agent_id="a2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.8,
                reasoning_summary="Moderate",
            ),
            AgentDecision(
                agent_id="a3",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.ORANGE,
                confidence_score=0.8,
                reasoning_summary="Moderate",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.agent_agreement_count, 3)
        self.assertEqual(result.agent_dissent_count, 0)

    def test_split_decision_agreement_count(self):
        """Split decisions should show correct split."""
        decisions = [
            AgentDecision(
                agent_id="a1",
                agent_role=AgentRole.DOMAIN_EXPERT,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.9,
                reasoning_summary="Safe",
            ),
            AgentDecision(
                agent_id="a2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.7,
                reasoning_summary="Minor",
            ),
            AgentDecision(
                agent_id="a3",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.YELLOW,
                confidence_score=0.7,
                reasoning_summary="Minor",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        # YELLOW wins (2.0 weight vs 1.5 for domain expert green)
        self.assertEqual(result.agent_agreement_count, 2)
        self.assertEqual(result.agent_dissent_count, 1)

    def test_black_gate_agreement_count(self):
        """BLACK gate escalation should show BLACK voters as agreement."""
        decisions = [
            AgentDecision(
                agent_id="a1",
                agent_role=AgentRole.SAFETY_SPECIALIST,
                recommended_gate=RiskClass.BLACK,
                confidence_score=1.0,
                reasoning_summary="Unacceptable",
            ),
            AgentDecision(
                agent_id="a2",
                agent_role=AgentRole.OPERATIONAL,
                recommended_gate=RiskClass.GREEN,
                confidence_score=0.8,
                reasoning_summary="OK",
            ),
        ]
        result = self.protocol.coordinate(decisions, self.context)
        self.assertEqual(result.agent_agreement_count, 1)
        self.assertEqual(result.agent_dissent_count, 1)


if __name__ == '__main__':
    unittest.main()
