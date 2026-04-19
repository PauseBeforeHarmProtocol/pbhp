"""
Pause-Before-Harm Protocol (PBHP) v0.9.5 — Multi-Agent Coordination
Multi-Agent Decision Coordination Protocol

Defines rules for when multiple agents running PBHP reach different gate
decisions on the same action. Implements:
  - Quorum voting with veto for irreversible actions
  - Tie-break mechanisms
  - Mandatory human-in-the-loop for BLACK gates
  - Agreement thresholds by severity

Ensures that multi-agent disagreement doesn't weaken safety, and that
collective wisdom aggregates safely.

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any, Tuple
from collections import Counter
from pbhp_core import RiskClass, DecisionOutcome


class AgentRole(Enum):
    """Role of the agent in the coordination context."""
    DOMAIN_EXPERT = "domain_expert"      # e.g., radiologist, auditor
    SAFETY_SPECIALIST = "safety_specialist"  # PBHP/ethics expert
    OPERATIONAL = "operational"          # Deployment/ops perspective
    EXTERNAL_VALIDATOR = "external_validator"  # Third-party audit
    AUTONOMOUS_AI = "autonomous_ai"      # Non-human agent


@dataclass
class AgentDecision:
    """One agent's PBHP assessment result."""
    agent_id: str
    """Unique identifier for the agent."""

    agent_role: AgentRole
    """Role of the agent in the coordination."""

    recommended_gate: RiskClass
    """The risk class gate this agent recommends."""

    confidence_score: float
    """0.0-1.0 confidence in this recommendation."""

    reasoning_summary: str
    """Why this agent recommends this gate."""

    is_irreversibility_concern: bool = False
    """Agent flagged this action as potentially irreversible."""

    is_vulnerable_population_concern: bool = False
    """Agent flagged vulnerable population impact."""

    recommended_outcome: DecisionOutcome = DecisionOutcome.PROCEED
    """What this agent thinks the final decision should be."""


@dataclass
class CoordinationContext:
    """Context for multi-agent coordination."""
    action_description: str
    """What action is being decided."""

    affected_parties: List[str]
    """Who could be affected by this action."""

    is_irreversible: bool = False
    """Action is irreversible (activates stricter rules)."""

    is_mass_scale: bool = False
    """Action affects many people (activates stricter rules)."""

    has_explicit_human_approval: bool = False
    """Human explicitly approved this specific action."""

    time_pressure_hours: Optional[int] = None
    """Hours until decision deadline (None = no pressure)."""


@dataclass
class CoordinationResult:
    """Output of multi-agent coordination."""
    final_gate_recommendation: RiskClass
    """The final recommended gate after coordination."""

    final_decision_outcome: DecisionOutcome
    """What the final action should be."""

    coordination_mechanism_used: str
    """How disagreement was resolved (e.g., 'quorum', 'veto', 'escalation')."""

    agent_agreement_count: int
    """How many agents agreed with the final recommendation."""

    agent_dissent_count: int
    """How many agents disagreed."""

    dissenting_agents: List[str] = field(default_factory=list)
    """IDs of agents who disagreed."""

    mandatory_human_review_required: bool = False
    """Must be reviewed by human before proceeding."""

    escalation_to_human_required: bool = False
    """Disagreement requires escalation to human authority."""

    coordination_notes: List[str] = field(default_factory=list)
    """Explanation of coordination process."""


class CoordinationProtocol:
    """
    Rules for multi-agent coordination on PBHP decisions.

    Core logic:
    1. For GREEN gates: Consensus not required, simple majority rules
    2. For YELLOW/ORANGE: Majority rules, minority concerns noted
    3. For RED gates: Any RED vote blocks PROCEED; requires human arbitration
    4. For BLACK gates: Automatic escalation to human; multi-agent NEVER overrides
    5. Irreversible actions: Single veto (qualified agent) can block PROCEED
    """

    # Quorum thresholds by gate
    QUORUM_THRESHOLDS = {
        RiskClass.GREEN: 0.0,      # Consensus not required
        RiskClass.YELLOW: 0.5,     # Simple majority
        RiskClass.ORANGE: 0.6,     # 60% agreement
        RiskClass.RED: 0.8,        # 80% agreement (high bar)
        RiskClass.BLACK: 1.0,      # 100% (impossible; auto-escalates)
    }

    def __init__(self):
        """Initialize the coordination protocol."""
        self.veto_roles = [AgentRole.SAFETY_SPECIALIST, AgentRole.EXTERNAL_VALIDATOR]
        self.expert_weight = 1.5  # Domain experts count 1.5x in voting

    def coordinate(self, decisions: List[AgentDecision],
                  context: CoordinationContext) -> CoordinationResult:
        """
        Coordinate multiple agent decisions into a final recommendation.

        Args:
            decisions: List of individual agent decisions
            context: Coordination context (irreversibility, scale, etc.)

        Returns:
            CoordinationResult with final gate and decision outcome
        """
        if not decisions:
            return self._no_decisions_result()

        # Rule 1: BLACK gate → automatic escalation (no override possible)
        if any(d.recommended_gate == RiskClass.BLACK for d in decisions):
            return self._black_gate_escalation(decisions, context)

        # Rule 2: Irreversible action with veto-capable agent dissent → escalate
        if context.is_irreversible and self._has_qualified_veto(decisions, context):
            return self._veto_escalation(decisions, context)

        # Rule 3: RED gate with disagreement → escalate
        if any(d.recommended_gate == RiskClass.RED for d in decisions):
            if not self._unanimous_agreement(decisions, RiskClass.RED):
                return self._red_gate_escalation(decisions, context)

        # Rule 4: Standard quorum voting
        final_gate = self._compute_consensus_gate(decisions)
        return self._standard_coordination(decisions, context, final_gate)

    def _black_gate_escalation(self, decisions: List[AgentDecision],
                              context: CoordinationContext) -> CoordinationResult:
        """Handle BLACK gate: auto-escalate to human authority."""
        black_count = sum(1 for d in decisions if d.recommended_gate == RiskClass.BLACK)
        notes = [
            f"BLACK gate identified by {black_count} agent(s)",
            "Automatic escalation to human authority (no multi-agent override)",
            "Decision cannot proceed without explicit human approval",
        ]

        return CoordinationResult(
            final_gate_recommendation=RiskClass.BLACK,
            final_decision_outcome=DecisionOutcome.ESCALATE,
            coordination_mechanism_used="black_gate_automatic_escalation",
            agent_agreement_count=black_count,
            agent_dissent_count=len(decisions) - black_count,
            dissenting_agents=self._get_dissenting_agents(decisions, RiskClass.BLACK),
            mandatory_human_review_required=True,
            escalation_to_human_required=True,
            coordination_notes=notes,
        )

    def _veto_escalation(self, decisions: List[AgentDecision],
                        context: CoordinationContext) -> CoordinationResult:
        """Handle veto on irreversible actions by qualified agents."""
        veto_agents = self._find_qualified_vetoes(decisions, context)
        notes = [
            f"VETO from {len(veto_agents)} qualified agent(s) on irreversible action",
            f"Agents: {', '.join(veto_agents)}",
            "Qualified veto blocks PROCEED on irreversible actions (PBHP v0.8 rule)",
            "Escalation to human authority required",
        ]

        consensus = self._compute_consensus_gate(decisions)
        gate_order = [RiskClass.GREEN, RiskClass.YELLOW, RiskClass.ORANGE,
                      RiskClass.RED, RiskClass.BLACK]

        return CoordinationResult(
            final_gate_recommendation=RiskClass.RED,
            final_decision_outcome=DecisionOutcome.ESCALATE,
            coordination_mechanism_used="veto_on_irreversible",
            agent_agreement_count=sum(1 for d in decisions if gate_order.index(d.recommended_gate) <= gate_order.index(RiskClass.ORANGE)),
            agent_dissent_count=len(veto_agents),
            dissenting_agents=veto_agents,
            mandatory_human_review_required=True,
            escalation_to_human_required=True,
            coordination_notes=notes,
        )

    def _red_gate_escalation(self, decisions: List[AgentDecision],
                            context: CoordinationContext) -> CoordinationResult:
        """Handle RED gate with disagreement."""
        red_agents = [d.agent_id for d in decisions if d.recommended_gate == RiskClass.RED]
        non_red_agents = [d.agent_id for d in decisions if d.recommended_gate != RiskClass.RED]

        notes = [
            f"RED gate flagged by {len(red_agents)} agent(s): {', '.join(red_agents)}",
            f"Disagreement with {len(non_red_agents)} other agent(s): {', '.join(non_red_agents)}",
            "Multi-agent disagreement at RED level requires human arbitration",
        ]

        return CoordinationResult(
            final_gate_recommendation=RiskClass.RED,
            final_decision_outcome=DecisionOutcome.REFUSE,
            coordination_mechanism_used="red_gate_disagreement_escalation",
            agent_agreement_count=len(red_agents),
            agent_dissent_count=len(non_red_agents),
            dissenting_agents=non_red_agents,
            mandatory_human_review_required=True,
            escalation_to_human_required=True,
            coordination_notes=notes,
        )

    def _standard_coordination(self, decisions: List[AgentDecision],
                             context: CoordinationContext,
                             final_gate: RiskClass) -> CoordinationResult:
        """Standard quorum-based coordination for GREEN/YELLOW/ORANGE gates."""
        agreement_count = sum(1 for d in decisions if d.recommended_gate == final_gate)
        dissent_count = len(decisions) - agreement_count
        dissenters = self._get_dissenting_agents(decisions, final_gate)

        notes = self._explain_standard_coordination(decisions, final_gate, agreement_count)

        # Determine final outcome from gate
        outcome = self._gate_to_outcome(final_gate, context)

        human_required = (final_gate in (RiskClass.ORANGE, RiskClass.RED) or
                         dissent_count > 0)

        return CoordinationResult(
            final_gate_recommendation=final_gate,
            final_decision_outcome=outcome,
            coordination_mechanism_used="quorum_voting",
            agent_agreement_count=agreement_count,
            agent_dissent_count=dissent_count,
            dissenting_agents=dissenters,
            mandatory_human_review_required=human_required,
            escalation_to_human_required=(final_gate == RiskClass.RED),
            coordination_notes=notes,
        )

    def _compute_consensus_gate(self, decisions: List[AgentDecision]) -> RiskClass:
        """Compute the consensus gate from all agent decisions."""
        # Weight decisions by agent role
        weighted_votes = {}
        gate_order = [RiskClass.GREEN, RiskClass.YELLOW, RiskClass.ORANGE,
                      RiskClass.RED, RiskClass.BLACK]

        for decision in decisions:
            weight = self.expert_weight if decision.agent_role == AgentRole.DOMAIN_EXPERT else 1.0
            gate = decision.recommended_gate
            weighted_votes[gate] = weighted_votes.get(gate, 0) + weight

        # Find gate with highest weight
        if not weighted_votes:
            return RiskClass.GREEN

        # Tie-break: choose more conservative (higher risk)
        max_weight = max(weighted_votes.values())
        tied_gates = [g for g, w in weighted_votes.items() if w == max_weight]

        if len(tied_gates) == 1:
            return tied_gates[0]

        # Tie-break: prefer more conservative gate (later in order)
        return max(tied_gates, key=lambda g: gate_order.index(g))

    def _has_qualified_veto(self, decisions: List[AgentDecision],
                           context: CoordinationContext) -> bool:
        """Check if a qualified agent wants to veto an irreversible action."""
        for decision in decisions:
            if decision.agent_role in self.veto_roles:
                if decision.recommended_gate in (RiskClass.RED, RiskClass.BLACK):
                    return True
        return False

    def _find_qualified_vetoes(self, decisions: List[AgentDecision],
                              context: CoordinationContext) -> List[str]:
        """Find agents with qualified veto authority who exercised it."""
        vetoes = []
        for decision in decisions:
            if decision.agent_role in self.veto_roles:
                if decision.recommended_gate in (RiskClass.RED, RiskClass.BLACK):
                    vetoes.append(decision.agent_id)
        return vetoes

    def _unanimous_agreement(self, decisions: List[AgentDecision],
                            gate: RiskClass) -> bool:
        """Check if all agents agree on a specific gate."""
        return all(d.recommended_gate == gate for d in decisions)

    def _get_dissenting_agents(self, decisions: List[AgentDecision],
                              consensus_gate: RiskClass) -> List[str]:
        """Get list of agent IDs that disagreed with consensus."""
        return [d.agent_id for d in decisions if d.recommended_gate != consensus_gate]

    def _explain_standard_coordination(self, decisions: List[AgentDecision],
                                      final_gate: RiskClass,
                                      agreement_count: int) -> List[str]:
        """Generate explanation for standard coordination."""
        notes = []

        # Count by gate
        gate_counts = {}
        for d in decisions:
            gate_counts[d.recommended_gate] = gate_counts.get(d.recommended_gate, 0) + 1

        # Explain voting
        details = []
        for gate in [RiskClass.BLACK, RiskClass.RED, RiskClass.ORANGE,
                     RiskClass.YELLOW, RiskClass.GREEN]:
            if gate in gate_counts:
                details.append(f"{gate.value.upper()}: {gate_counts[gate]} agents")

        notes.append(f"Agent votes: {', '.join(details)}")
        notes.append(f"Consensus gate: {final_gate.value.upper()} ({agreement_count}/{len(decisions)} agents)")

        # Confidence note
        avg_confidence = sum(d.confidence_score for d in decisions) / len(decisions)
        notes.append(f"Average confidence: {avg_confidence:.2f}")

        return notes

    def _gate_to_outcome(self, gate: RiskClass,
                        context: CoordinationContext) -> DecisionOutcome:
        """Convert gate to DecisionOutcome."""
        mapping = {
            RiskClass.GREEN: DecisionOutcome.PROCEED,
            RiskClass.YELLOW: DecisionOutcome.PROCEED_MODIFIED,
            RiskClass.ORANGE: DecisionOutcome.REDIRECT,
            RiskClass.RED: DecisionOutcome.REFUSE,
            RiskClass.BLACK: DecisionOutcome.ESCALATE,
        }
        return mapping.get(gate, DecisionOutcome.ESCALATE)

    def _no_decisions_result(self) -> CoordinationResult:
        """Handle edge case: no decisions provided."""
        return CoordinationResult(
            final_gate_recommendation=RiskClass.YELLOW,
            final_decision_outcome=DecisionOutcome.DELAY,
            coordination_mechanism_used="no_agents",
            agent_agreement_count=0,
            agent_dissent_count=0,
            coordination_notes=["No agent decisions provided; default to YELLOW gate"],
        )


# Convenience function
def coordinate_decisions(decisions: List[AgentDecision],
                        context: CoordinationContext) -> CoordinationResult:
    """
    Quick entry point for multi-agent coordination.

    Usage:
        decision1 = AgentDecision(
            agent_id="alice",
            agent_role=AgentRole.SAFETY_SPECIALIST,
            recommended_gate=RiskClass.ORANGE,
            confidence_score=0.85,
            reasoning_summary="...",
        )
        decision2 = AgentDecision(
            agent_id="bob",
            agent_role=AgentRole.DOMAIN_EXPERT,
            recommended_gate=RiskClass.GREEN,
            confidence_score=0.60,
            reasoning_summary="...",
        )

        context = CoordinationContext(
            action_description="Deploy new hiring algorithm",
            affected_parties=["job applicants"],
            is_irreversible=False,
        )

        result = coordinate_decisions([decision1, decision2], context)
        print(f"Final gate: {result.final_gate_recommendation.value}")
    """
    protocol = CoordinationProtocol()
    return protocol.coordinate(decisions, context)
