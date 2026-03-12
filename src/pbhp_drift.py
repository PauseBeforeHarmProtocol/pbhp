"""
Pause-Before-Harm Protocol (PBHP) v0.8.0 — Drift Rate Measurement
Measurable Drift Detection and Velocity Analysis

Upgrades from binary drift flags to quantifiable drift rates. Tracks:
  - Decision pattern changes over time (drift computation)
  - Drift velocity (rate of change acceleration)
  - Early warning thresholds
  - Temporal anomaly detection
  - Stakeholder impact correlation

Ingest PBHP logs and compute drift metrics for continuous monitoring.

Contact: pausebeforeharmprotocol_pbhp@protonmail.com
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
from collections import deque
import statistics


class DriftDirection(Enum):
    """Direction of drift in decision patterns."""
    SAFER = "safer"            # Drifting toward fewer harms (more refusals)
    RISKIER = "riskier"        # Drifting toward more harms (fewer refusals)
    NO_DRIFT = "no_drift"      # Stable pattern
    UNKNOWN = "unknown"        # Insufficient data


@dataclass
class DriftMetric:
    """A single drift metric measurement."""
    timestamp: datetime
    """When this measurement was taken."""

    metric_name: str
    """Name of the metric (e.g., 'refuse_rate', 'avg_gate_level')."""

    metric_value: float
    """Current value of the metric."""

    baseline_value: Optional[float] = None
    """Baseline/expected value for comparison."""

    deviation_from_baseline: Optional[float] = None
    """metric_value - baseline_value."""

    threshold_upper: Optional[float] = None
    """Upper bound before alert triggered."""

    threshold_lower: Optional[float] = None
    """Lower bound before alert triggered."""

    is_alert_triggered: bool = False
    """True if metric exceeds threshold."""


@dataclass
class DriftVelocity:
    """Rate of change of a drift metric over time."""
    metric_name: str
    current_velocity: float
    """Change per day (delta_value / days)."""

    acceleration: Optional[float] = None
    """Change in velocity (velocity_today - velocity_yesterday)."""

    direction: DriftDirection = DriftDirection.NO_DRIFT
    """Direction of drift (safer/riskier/no_drift)."""

    alert_level: str = "normal"
    """'normal', 'warning', 'critical' based on velocity magnitude."""

    projected_threshold_breach_days: Optional[int] = None
    """Days until metric would breach alert threshold if drift continues."""


@dataclass
class DecisionSnapshot:
    """Snapshot of decisions in a time window."""
    window_start: datetime
    window_end: datetime
    window_duration_hours: int
    """Length of time window."""

    total_decisions: int
    """Total PBHP assessments in this window."""

    gate_distribution: Dict[str, int] = field(default_factory=dict)
    """Count of decisions at each gate (GREEN, YELLOW, ORANGE, RED, BLACK)."""

    refuse_count: int = 0
    """Number of REFUSE/DELAY/ESCALATE decisions."""

    proceed_count: int = 0
    """Number of PROCEED/PROCEED_MODIFIED decisions."""

    avg_harm_impact_level: Optional[float] = None
    """Average impact level (numeric: 1=trivial, 4=catastrophic)."""

    vulnerable_population_percent: float = 0.0
    """% of decisions affecting vulnerable populations."""

    irreversible_percent: float = 0.0
    """% of decisions involving irreversible actions."""

    avg_confidence: float = 0.0
    """Average confidence score across assessments."""

    human_escalations: int = 0
    """Number of decisions escalated to human review."""


@dataclass
class DriftAlert:
    """An alert triggered by drift detection."""
    timestamp: datetime
    metric_name: str
    alert_level: str
    """'warning' or 'critical'."""

    current_value: float
    baseline_value: float
    deviation_percent: float
    """Percentage change from baseline."""

    probable_causes: List[str] = field(default_factory=list)
    """Hypothesized reasons for drift."""

    recommended_actions: List[str] = field(default_factory=list)
    """What to do about the drift."""

    requires_manual_review: bool = False
    """Whether human judgment needed."""


@dataclass
class DriftReport:
    """Comprehensive drift analysis report."""
    report_date: datetime
    analysis_period_days: int
    """How many days of data analyzed."""

    metrics_monitored: List[str]
    """Names of tracked metrics."""

    alerts_triggered: List[DriftAlert] = field(default_factory=list)
    """Alerts in the reporting period."""

    metric_summaries: Dict[str, Dict] = field(default_factory=dict)
    """Summary stats for each metric."""

    overall_drift_direction: DriftDirection = DriftDirection.NO_DRIFT
    """Net direction of drift across all metrics."""

    stability_score: float = 1.0
    """0.0-1.0 where 1.0 = perfectly stable."""

    high_risk_metrics: List[str] = field(default_factory=list)
    """Metrics showing concerning drift."""

    recommendations: List[str] = field(default_factory=list)
    """Actions to address drift."""


class DriftMonitor:
    """
    Monitors PBHP decision patterns for drift.

    Tracks key metrics:
    - Refuse rate (% of decisions that REFUSE/DELAY/ESCALATE)
    - Average gate level (GREEN=1, YELLOW=2, ..., BLACK=5)
    - Human escalation rate
    - Vulnerable population impact rate
    - Irreversibility rate
    - Confidence scores

    Computes drift velocity and alerts when thresholds breached.
    """

    def __init__(self, baseline_window_days: int = 30):
        """
        Initialize drift monitor.

        Args:
            baseline_window_days: How many days to use for baseline calculation
        """
        self.baseline_window_days = baseline_window_days
        self.decision_history: deque = deque()  # (timestamp, decision_info)
        self.metric_history: deque = deque()    # (timestamp, metric_dict)
        self.velocity_history: Dict[str, deque] = {}  # metric_name -> deque of velocities

        # Default thresholds (can be customized)
        self.alert_thresholds = {
            "refuse_rate_upper": 0.95,      # Alert if > 95% refusing
            "refuse_rate_lower": 0.10,      # Alert if < 10% refusing
            "avg_gate_level_upper": 3.5,    # Alert if avg gate >= RED
            "human_escalation_rate_upper": 0.50,
            "confidence_drop_threshold": 0.20,  # Drop > 20% from baseline
        }

        # Baseline metrics (computed from history)
        self.baseline_metrics = {}

    def ingest_decision(self, decision_info: Dict[str, Any]) -> None:
        """
        Add a decision to the drift monitor.

        Args:
            decision_info: Dict with keys:
                - timestamp: datetime
                - gate: str (GREEN/YELLOW/ORANGE/RED/BLACK)
                - outcome: str (PROCEED/REFUSE/etc.)
                - impact_level: int (1=trivial, 4=catastrophic)
                - affects_vulnerable: bool
                - is_irreversible: bool
                - confidence: float (0-1)
        """
        self.decision_history.append((datetime.now(), decision_info))

    def compute_snapshot(self, window_hours: int = 24) -> DecisionSnapshot:
        """
        Compute decision snapshot for a time window.

        Args:
            window_hours: Size of time window (default 24 hours)

        Returns:
            DecisionSnapshot with metrics for the window
        """
        now = datetime.now()
        cutoff = now - timedelta(hours=window_hours)

        # Filter decisions in window
        window_decisions = [
            d for ts, d in self.decision_history
            if ts >= cutoff
        ]

        if not window_decisions:
            return DecisionSnapshot(
                window_start=cutoff,
                window_end=now,
                window_duration_hours=window_hours,
                total_decisions=0,
            )

        # Compute stats
        gate_counts = {}
        refuse_count = 0
        proceed_count = 0
        impacts = []
        vulnerable_count = 0
        irreversible_count = 0
        confidences = []

        for decision in window_decisions:
            gate = decision.get("gate", "unknown")
            gate_counts[gate] = gate_counts.get(gate, 0) + 1

            outcome = decision.get("outcome", "")
            if outcome in ("REFUSE", "DELAY", "ESCALATE"):
                refuse_count += 1
            elif outcome in ("PROCEED", "PROCEED_MODIFIED"):
                proceed_count += 1

            impact = decision.get("impact_level", 2)
            impacts.append(impact)

            if decision.get("affects_vulnerable", False):
                vulnerable_count += 1

            if decision.get("is_irreversible", False):
                irreversible_count += 1

            confidence = decision.get("confidence", 0.5)
            confidences.append(confidence)

        # Calculate percentages
        total = len(window_decisions)
        vulnerable_pct = (vulnerable_count / total * 100) if total > 0 else 0
        irreversible_pct = (irreversible_count / total * 100) if total > 0 else 0
        avg_impact = statistics.mean(impacts) if impacts else 0
        avg_confidence = statistics.mean(confidences) if confidences else 0

        return DecisionSnapshot(
            window_start=cutoff,
            window_end=now,
            window_duration_hours=window_hours,
            total_decisions=total,
            gate_distribution=gate_counts,
            refuse_count=refuse_count,
            proceed_count=proceed_count,
            avg_harm_impact_level=avg_impact,
            vulnerable_population_percent=vulnerable_pct,
            irreversible_percent=irreversible_pct,
            avg_confidence=avg_confidence,
        )

    def compute_metrics(self, snapshot: DecisionSnapshot) -> List[DriftMetric]:
        """Compute drift metrics from a decision snapshot."""
        metrics = []
        now = datetime.now()

        total = snapshot.total_decisions
        if total == 0:
            return metrics

        # Metric 1: Refuse rate
        refuse_rate = (snapshot.refuse_count / total) if total > 0 else 0
        baseline_refuse = self.baseline_metrics.get("refuse_rate", 0.30)
        metrics.append(DriftMetric(
            timestamp=now,
            metric_name="refuse_rate",
            metric_value=refuse_rate,
            baseline_value=baseline_refuse,
            deviation_from_baseline=refuse_rate - baseline_refuse,
            threshold_upper=self.alert_thresholds["refuse_rate_upper"],
            threshold_lower=self.alert_thresholds["refuse_rate_lower"],
            is_alert_triggered=(refuse_rate > self.alert_thresholds["refuse_rate_upper"] or
                              refuse_rate < self.alert_thresholds["refuse_rate_lower"]),
        ))

        # Metric 2: Average gate level
        gate_levels = {"GREEN": 1, "YELLOW": 2, "ORANGE": 3, "RED": 4, "BLACK": 5}
        gate_values = []
        for gate, count in snapshot.gate_distribution.items():
            level = gate_levels.get(gate, 0)
            gate_values.extend([level] * count)
        avg_gate = statistics.mean(gate_values) if gate_values else 0

        baseline_gate = self.baseline_metrics.get("avg_gate_level", 2.0)
        metrics.append(DriftMetric(
            timestamp=now,
            metric_name="avg_gate_level",
            metric_value=avg_gate,
            baseline_value=baseline_gate,
            deviation_from_baseline=avg_gate - baseline_gate,
            threshold_upper=self.alert_thresholds["avg_gate_level_upper"],
            is_alert_triggered=(avg_gate > self.alert_thresholds["avg_gate_level_upper"]),
        ))

        # Metric 3: Vulnerable population impact rate
        vulnerable_pct = snapshot.vulnerable_population_percent
        baseline_vulnerable = self.baseline_metrics.get("vulnerable_pct", 10.0)
        metrics.append(DriftMetric(
            timestamp=now,
            metric_name="vulnerable_population_rate",
            metric_value=vulnerable_pct,
            baseline_value=baseline_vulnerable,
            deviation_from_baseline=vulnerable_pct - baseline_vulnerable,
        ))

        # Metric 4: Average confidence
        avg_conf = snapshot.avg_confidence
        baseline_conf = self.baseline_metrics.get("avg_confidence", 0.75)
        metrics.append(DriftMetric(
            timestamp=now,
            metric_name="avg_confidence",
            metric_value=avg_conf,
            baseline_value=baseline_conf,
            deviation_from_baseline=avg_conf - baseline_conf,
        ))

        # Store in history
        for metric in metrics:
            self.metric_history.append((now, metric.metric_name, metric.metric_value))

        return metrics

    def compute_velocity(self, metric_name: str, window_days: int = 7) -> Optional[DriftVelocity]:
        """
        Compute drift velocity (rate of change) for a metric.

        Args:
            metric_name: Name of metric to analyze
            window_days: How many days to look back

        Returns:
            DriftVelocity with current velocity and direction
        """
        now = datetime.now()
        cutoff = now - timedelta(days=window_days)

        # Get values in window
        values_in_window = [
            (ts, val) for ts, name, val in self.metric_history
            if name == metric_name and ts >= cutoff
        ]

        if len(values_in_window) < 2:
            return None

        # Linear regression for velocity
        values = [v for _, v in values_in_window]
        avg_value = statistics.mean(values)
        change = values[-1] - values[0]
        days_elapsed = window_days if window_days > 0 else 1
        velocity = change / days_elapsed

        # Determine direction
        if abs(velocity) < 0.01:
            direction = DriftDirection.NO_DRIFT
        elif metric_name == "refuse_rate" and velocity > 0:
            direction = DriftDirection.SAFER
        elif metric_name == "refuse_rate" and velocity < 0:
            direction = DriftDirection.RISKIER
        elif metric_name == "avg_gate_level" and velocity < 0:
            direction = DriftDirection.SAFER
        elif metric_name == "avg_gate_level" and velocity > 0:
            direction = DriftDirection.RISKIER
        else:
            direction = DriftDirection.UNKNOWN

        # Determine alert level
        alert_level = "normal"
        if abs(velocity) > 0.10:  # Large velocity
            alert_level = "warning"
        if abs(velocity) > 0.20:
            alert_level = "critical"

        return DriftVelocity(
            metric_name=metric_name,
            current_velocity=velocity,
            direction=direction,
            alert_level=alert_level,
        )

    def generate_drift_alerts(self, metrics: List[DriftMetric]) -> List[DriftAlert]:
        """Generate alerts for metrics exceeding thresholds."""
        alerts = []

        for metric in metrics:
            if metric.is_alert_triggered:
                deviation_pct = (
                    abs(metric.deviation_from_baseline) / metric.baseline_value * 100
                    if metric.baseline_value and metric.baseline_value != 0
                    else 0
                )

                probable_causes = self._infer_causes(metric)
                recommended_actions = self._recommend_actions(metric)

                alerts.append(DriftAlert(
                    timestamp=metric.timestamp,
                    metric_name=metric.metric_name,
                    alert_level="critical" if deviation_pct > 30 else "warning",
                    current_value=metric.metric_value,
                    baseline_value=metric.baseline_value or 0,
                    deviation_percent=deviation_pct,
                    probable_causes=probable_causes,
                    recommended_actions=recommended_actions,
                    requires_manual_review=(deviation_pct > 30),
                ))

        return alerts

    def generate_drift_report(self, days: int = 30) -> DriftReport:
        """
        Generate comprehensive drift analysis report.

        Args:
            days: How many days to analyze

        Returns:
            DriftReport with full analysis
        """
        now = datetime.now()
        report_date = now
        cutoff = now - timedelta(days=days)

        # Get metrics in period
        recent_metrics = [
            (ts, name, val) for ts, name, val in self.metric_history
            if ts >= cutoff
        ]

        if not recent_metrics:
            return DriftReport(
                report_date=report_date,
                analysis_period_days=days,
                metrics_monitored=[],
            )

        # Group by metric
        metrics_by_name = {}
        for ts, name, val in recent_metrics:
            if name not in metrics_by_name:
                metrics_by_name[name] = []
            metrics_by_name[name].append(val)

        # Compute summaries
        metric_summaries = {}
        for name, values in metrics_by_name.items():
            metric_summaries[name] = {
                "current": values[-1],
                "mean": statistics.mean(values),
                "min": min(values),
                "max": max(values),
                "stdev": statistics.stdev(values) if len(values) > 1 else 0,
            }

        # Compute overall stability (inverse of variance)
        all_deviations = []
        for values in metrics_by_name.values():
            if len(values) > 1:
                all_deviations.append(statistics.stdev(values))
        stability = max(0, 1.0 - (statistics.mean(all_deviations) if all_deviations else 0))

        return DriftReport(
            report_date=report_date,
            analysis_period_days=days,
            metrics_monitored=list(metrics_by_name.keys()),
            metric_summaries=metric_summaries,
            stability_score=max(0, min(1.0, stability)),
            recommendations=[
                "Review metrics with stdev > 0.15",
                "Investigate alerts with deviation > 30%",
            ],
        )

    def _infer_causes(self, metric: DriftMetric) -> List[str]:
        """Infer probable causes for metric drift."""
        causes = []

        if metric.metric_name == "refuse_rate":
            if metric.metric_value > metric.baseline_value:
                causes.append("More conservative decision-making")
                causes.append("Increased caution or new risks detected")
            else:
                causes.append("More lenient decision patterns")
                causes.append("Potential erosion of safety standards")

        elif metric.metric_name == "avg_gate_level":
            if metric.metric_value > metric.baseline_value:
                causes.append("Shift toward higher-risk gates (RED/ORANGE)")
                causes.append("Possible change in decision inputs or criteria")

        elif metric.metric_name == "vulnerable_population_rate":
            causes.append("Change in population demographics or features")
            causes.append("Different types of decisions being made")

        return causes

    def _recommend_actions(self, metric: DriftMetric) -> List[str]:
        """Recommend actions for a drifting metric."""
        actions = []

        if metric.metric_name == "refuse_rate" and metric.metric_value < metric.baseline_value:
            actions.append("Manual review of recent low-gate decisions")
            actions.append("Check for possible safety standard erosion")

        if metric.metric_name == "avg_gate_level" and metric.metric_value > metric.baseline_value:
            actions.append("Investigate new harms or risks")
            actions.append("Check for upstream changes in decision context")

        actions.append("Collect additional decision context for analysis")

        return actions


# ---------------------------------------------------------------------------
# Meta-Monitor: Drift monitoring monitors itself (community improvement #6)
# ---------------------------------------------------------------------------

@dataclass
class MetaHeartbeat:
    """A heartbeat record from the drift monitor itself."""
    timestamp: datetime
    metrics_computed: int
    alerts_generated: int
    decisions_ingested: int
    computation_time_ms: float = 0.0


@dataclass
class MetaMonitorStatus:
    """Health status of the drift monitor."""
    is_healthy: bool = True
    last_heartbeat: Optional[datetime] = None
    heartbeat_count: int = 0
    missed_heartbeats: int = 0
    avg_computation_time_ms: float = 0.0
    monitor_drift_detected: bool = False
    alert_message: str = ""


class DriftMetaMonitor:
    """
    Monitors the drift monitor itself.

    Community improvement #6: "Drift monitoring needs monitoring of itself."

    Tracks:
    - Heartbeat regularity (is the monitor still running?)
    - Computation time drift (is the monitor slowing down?)
    - Alert rate changes (is the monitor's own behavior drifting?)
    - Silent failure detection (monitor stops producing output)
    """

    def __init__(
        self,
        expected_heartbeat_interval_minutes: int = 60,
        max_missed_heartbeats: int = 3,
    ):
        self.expected_interval = timedelta(
            minutes=expected_heartbeat_interval_minutes
        )
        self.max_missed = max_missed_heartbeats
        self._heartbeats: deque = deque(maxlen=1000)
        self._alert_rate_history: deque = deque(maxlen=100)

    def record_heartbeat(self, heartbeat: MetaHeartbeat) -> MetaMonitorStatus:
        """
        Record a heartbeat from the drift monitor.
        Returns current health status.
        """
        self._heartbeats.append(heartbeat)
        self._alert_rate_history.append(heartbeat.alerts_generated)
        return self.check_health()

    def check_health(self) -> MetaMonitorStatus:
        """Check if the drift monitor is functioning correctly."""
        if not self._heartbeats:
            return MetaMonitorStatus(
                is_healthy=False,
                alert_message="No heartbeats received — monitor may not be running",
            )

        last = self._heartbeats[-1]
        now = datetime.now()
        time_since_last = now - last.timestamp

        # Check for missed heartbeats
        missed = 0
        if time_since_last > self.expected_interval:
            missed = int(time_since_last / self.expected_interval) - 1

        # Check computation time drift
        avg_time = 0.0
        if len(self._heartbeats) >= 2:
            times = [h.computation_time_ms for h in self._heartbeats]
            avg_time = statistics.mean(times)

        # Check alert rate drift (is the monitor generating unusual numbers?)
        monitor_drift = False
        alert_msg = ""
        if len(self._alert_rate_history) >= 10:
            recent = list(self._alert_rate_history)[-5:]
            older = list(self._alert_rate_history)[-10:-5]
            recent_avg = statistics.mean(recent)
            older_avg = statistics.mean(older) if older else recent_avg
            if older_avg > 0 and abs(recent_avg - older_avg) / older_avg > 0.5:
                monitor_drift = True
                alert_msg = (
                    f"Monitor alert rate shifted: {older_avg:.1f} → "
                    f"{recent_avg:.1f} alerts per cycle"
                )

        is_healthy = missed <= self.max_missed and not monitor_drift

        if missed > self.max_missed and not alert_msg:
            alert_msg = (
                f"Monitor missed {missed} heartbeats "
                f"(max allowed: {self.max_missed})"
            )

        return MetaMonitorStatus(
            is_healthy=is_healthy,
            last_heartbeat=last.timestamp,
            heartbeat_count=len(self._heartbeats),
            missed_heartbeats=missed,
            avg_computation_time_ms=avg_time,
            monitor_drift_detected=monitor_drift,
            alert_message=alert_msg,
        )

    @property
    def heartbeat_count(self) -> int:
        return len(self._heartbeats)


# Convenience function
def monitor_drift(decision_history: List[Dict[str, Any]],
                 analysis_days: int = 30) -> DriftReport:
    """
    Quick entry point for drift analysis.

    Usage:
        decisions = [
            {
                "timestamp": datetime.now(),
                "gate": "GREEN",
                "outcome": "PROCEED",
                "impact_level": 2,
                "affects_vulnerable": False,
                "is_irreversible": False,
                "confidence": 0.85,
            },
            # ... more decisions
        ]

        report = monitor_drift(decisions, analysis_days=30)
        print(f"Stability score: {report.stability_score:.2f}")
        print(f"Alerts: {len(report.alerts_triggered)}")
    """
    monitor = DriftMonitor()

    for decision in decision_history:
        monitor.ingest_decision(decision)

    snapshot = monitor.compute_snapshot(window_hours=24 * analysis_days)
    metrics = monitor.compute_metrics(snapshot)
    _ = monitor.generate_drift_alerts(metrics)

    return monitor.generate_drift_report(days=analysis_days)
