"""
Tests for community-identified improvements applied to existing modules.

- #5: UncertaintyAssessment.update_threshold
- #6: DriftMetaMonitor (drift monitors itself)
"""

import unittest
from datetime import datetime, timedelta

# Import from core (UncertaintyAssessment needs the Confidence enum)
import sys
sys.path.insert(0, ".")
from pbhp_core import UncertaintyAssessment, Confidence
from pbhp_drift import DriftMetaMonitor, MetaHeartbeat, MetaMonitorStatus


# ===========================================================================
# #5: Uncertainty Threshold
# ===========================================================================

class TestUpdateThreshold(unittest.TestCase):
    """Tests for adaptive uncertainty thresholds."""

    def test_default_threshold(self):
        ua = UncertaintyAssessment()
        self.assertEqual(ua.update_threshold, 0.5)

    def test_effective_threshold_prod(self):
        ua = UncertaintyAssessment(
            update_threshold=0.5,
            threshold_context="prod",
        )
        # Prod applies 0.7x multiplier
        self.assertAlmostEqual(ua.effective_threshold(), 0.35)

    def test_effective_threshold_dev(self):
        ua = UncertaintyAssessment(
            update_threshold=0.5,
            threshold_context="dev",
        )
        # Dev applies 1.5x multiplier
        self.assertAlmostEqual(ua.effective_threshold(), 0.75)

    def test_effective_threshold_emergency(self):
        ua = UncertaintyAssessment(
            update_threshold=0.5,
            threshold_context="emergency",
        )
        # Emergency applies 1.3x
        self.assertAlmostEqual(ua.effective_threshold(), 0.65)

    def test_effective_threshold_capped_at_1(self):
        ua = UncertaintyAssessment(
            update_threshold=0.9,
            threshold_context="dev",
        )
        # 0.9 * 1.5 = 1.35, should cap at 1.0
        self.assertAlmostEqual(ua.effective_threshold(), 1.0)

    def test_effective_threshold_floor_at_0(self):
        ua = UncertaintyAssessment(update_threshold=0.0)
        self.assertAlmostEqual(ua.effective_threshold(), 0.0)

    def test_passes_threshold_high_confidence(self):
        ua = UncertaintyAssessment(
            confidence=Confidence.HIGH,
            update_threshold=0.5,
        )
        # HIGH maps to 0.9, threshold is 0.5
        self.assertTrue(ua.passes_threshold())

    def test_fails_threshold_low_confidence(self):
        ua = UncertaintyAssessment(
            confidence=Confidence.LOW,
            update_threshold=0.5,
        )
        # LOW maps to 0.2, threshold is 0.5
        self.assertFalse(ua.passes_threshold())

    def test_passes_threshold_prod_strict(self):
        ua = UncertaintyAssessment(
            confidence=Confidence.MEDIUM,
            update_threshold=0.5,
            threshold_context="prod",
        )
        # MEDIUM=0.5, effective threshold=0.35 → passes
        self.assertTrue(ua.passes_threshold())

    def test_fails_threshold_dev_loose(self):
        ua = UncertaintyAssessment(
            confidence=Confidence.MEDIUM,
            update_threshold=0.5,
            threshold_context="dev",
        )
        # MEDIUM=0.5, effective threshold=0.75 → fails
        self.assertFalse(ua.passes_threshold())

    def test_to_dict_includes_threshold(self):
        ua = UncertaintyAssessment(
            update_threshold=0.6,
            threshold_context="prod",
        )
        d = ua.to_dict()
        self.assertIn("threshold", d)
        self.assertEqual(d["threshold"]["update_threshold"], 0.6)
        self.assertEqual(d["threshold"]["threshold_context"], "prod")
        self.assertAlmostEqual(d["threshold"]["effective_threshold"], 0.42)


# ===========================================================================
# #6: Drift Self-Monitoring (Meta-Monitor)
# ===========================================================================

class TestDriftMetaMonitor(unittest.TestCase):
    """Tests that the drift monitor monitors itself."""

    def setUp(self):
        self.meta = DriftMetaMonitor(
            expected_heartbeat_interval_minutes=60,
            max_missed_heartbeats=3,
        )

    def test_no_heartbeats_unhealthy(self):
        status = self.meta.check_health()
        self.assertFalse(status.is_healthy)
        self.assertIn("No heartbeats", status.alert_message)

    def test_record_heartbeat(self):
        hb = MetaHeartbeat(
            timestamp=datetime.now(),
            metrics_computed=5,
            alerts_generated=1,
            decisions_ingested=100,
            computation_time_ms=42.0,
        )
        status = self.meta.record_heartbeat(hb)
        self.assertTrue(status.is_healthy)
        self.assertEqual(status.heartbeat_count, 1)

    def test_missed_heartbeats_detected(self):
        # Record a heartbeat from 5 hours ago
        old = MetaHeartbeat(
            timestamp=datetime.now() - timedelta(hours=5),
            metrics_computed=5,
            alerts_generated=1,
            decisions_ingested=50,
        )
        self.meta.record_heartbeat(old)
        status = self.meta.check_health()
        # 5 hours / 1 hour interval = 4 missed, exceeds max of 3
        self.assertFalse(status.is_healthy)
        self.assertTrue(status.missed_heartbeats > self.meta.max_missed)

    def test_recent_heartbeat_healthy(self):
        hb = MetaHeartbeat(
            timestamp=datetime.now(),
            metrics_computed=5,
            alerts_generated=0,
            decisions_ingested=100,
        )
        status = self.meta.record_heartbeat(hb)
        self.assertTrue(status.is_healthy)
        self.assertEqual(status.missed_heartbeats, 0)

    def test_alert_rate_drift_detection(self):
        # Generate 10 heartbeats with stable alert rate
        for i in range(10):
            hb = MetaHeartbeat(
                timestamp=datetime.now() - timedelta(minutes=60 * (10 - i)),
                metrics_computed=5,
                alerts_generated=2,  # stable rate
                decisions_ingested=100,
            )
            self.meta.record_heartbeat(hb)

        # Then 5 heartbeats with very different alert rate
        for i in range(5):
            hb = MetaHeartbeat(
                timestamp=datetime.now() - timedelta(minutes=5 * (5 - i)),
                metrics_computed=5,
                alerts_generated=10,  # 5x spike
                decisions_ingested=100,
            )
            status = self.meta.record_heartbeat(hb)

        # The monitor should detect its own drift
        self.assertTrue(status.monitor_drift_detected)

    def test_computation_time_tracked(self):
        for ms in [10.0, 20.0, 30.0]:
            hb = MetaHeartbeat(
                timestamp=datetime.now(),
                metrics_computed=5,
                alerts_generated=0,
                decisions_ingested=50,
                computation_time_ms=ms,
            )
            status = self.meta.record_heartbeat(hb)
        self.assertAlmostEqual(status.avg_computation_time_ms, 20.0)

    def test_heartbeat_count(self):
        for _ in range(5):
            self.meta.record_heartbeat(MetaHeartbeat(
                timestamp=datetime.now(),
                metrics_computed=1,
                alerts_generated=0,
                decisions_ingested=10,
            ))
        self.assertEqual(self.meta.heartbeat_count, 5)


if __name__ == "__main__":
    unittest.main()
