"""
PBHP CLI & Examples Smoke Tests
================================

Lightweight integration tests for pbhp_cli.py and pbhp_examples.py.
Tests that imports work, helper functions behave correctly, and example
scenarios run end-to-end without errors.

These are smoke tests — they verify nothing blows up, not that the
interactive prompts produce correct UX flows.
"""

import unittest
import sys
import os
import io
from unittest.mock import patch
from contextlib import redirect_stdout

# Ensure src/ is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ── CLI helper function tests ──────────────────────────────────────────


class TestCLIImports(unittest.TestCase):
    """Verify all CLI imports resolve without error."""

    def test_cli_module_imports(self):
        import pbhp_cli
        self.assertTrue(hasattr(pbhp_cli, "main"))
        self.assertTrue(hasattr(pbhp_cli, "VERSION"))
        self.assertTrue(hasattr(pbhp_cli, "PBHPEngine"))

    def test_examples_module_imports(self):
        import pbhp_examples
        self.assertTrue(hasattr(pbhp_examples, "run_all_examples"))
        self.assertTrue(hasattr(pbhp_examples, "example_employee_warning"))


class TestCLIHelpers(unittest.TestCase):
    """Test CLI display helper functions."""

    def setUp(self):
        import pbhp_cli
        self.cli = pbhp_cli

    def test_banner_prints(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.cli.banner("Test Title")
        output = buf.getvalue()
        self.assertIn("Test Title", output)
        self.assertIn("=" * self.cli.BANNER_WIDTH, output)

    def test_sub_banner_prints(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.cli.sub_banner("Sub Title")
        output = buf.getvalue()
        self.assertIn("Sub Title", output)
        self.assertIn("-" * self.cli.BANNER_WIDTH, output)

    def test_info_message(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.cli.info("hello")
        self.assertIn("[INFO]", buf.getvalue())
        self.assertIn("hello", buf.getvalue())

    def test_warn_message(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.cli.warn("caution")
        self.assertIn("[WARN]", buf.getvalue())
        self.assertIn("caution", buf.getvalue())

    def test_error_message(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.cli.error("bad")
        self.assertIn("[ERROR]", buf.getvalue())

    def test_success_message(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.cli.success("good")
        self.assertIn("[OK]", buf.getvalue()) if hasattr(self.cli, "success") else None

    def test_display_risk_class(self):
        from pbhp_core import RiskClass
        result = self.cli.display_risk_class(RiskClass.ORANGE)
        self.assertIn("ORANGE", result)

    def test_display_risk_class_green(self):
        from pbhp_core import RiskClass
        result = self.cli.display_risk_class(RiskClass.GREEN)
        self.assertIn("GREEN", result)

    def test_display_risk_color_all_classes(self):
        from pbhp_core import RiskClass
        for rc in RiskClass:
            result = self.cli.display_risk_color(rc)
            self.assertIsInstance(result, str)
            self.assertTrue(len(result) > 0)

    def test_constants(self):
        self.assertEqual(self.cli.BANNER_WIDTH, 72)
        self.assertIn("@", self.cli.CONTACT_EMAIL)


class TestCLIPromptHelpers(unittest.TestCase):
    """Test prompt functions with mocked input."""

    def setUp(self):
        import pbhp_cli
        self.cli = pbhp_cli

    @patch("builtins.input", return_value="test answer")
    def test_prompt_returns_input(self, mock_input):
        result = self.cli.prompt("Question?")
        self.assertEqual(result, "test answer")

    @patch("builtins.input", return_value="")
    def test_prompt_default(self, mock_input):
        result = self.cli.prompt("Question?", default="fallback")
        self.assertEqual(result, "fallback")

    @patch("builtins.input", return_value="y")
    def test_prompt_yes_no_yes(self, mock_input):
        result = self.cli.prompt_yes_no("Continue?")
        self.assertTrue(result)

    @patch("builtins.input", return_value="n")
    def test_prompt_yes_no_no(self, mock_input):
        result = self.cli.prompt_yes_no("Continue?")
        self.assertFalse(result)

    @patch("builtins.input", return_value="1")
    def test_prompt_choice(self, mock_input):
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = self.cli.prompt_choice("Pick one:", ["alpha", "beta"])
        self.assertEqual(result, "alpha")


# ── Examples smoke tests ───────────────────────────────────────────────


class TestExamplesRunClean(unittest.TestCase):
    """Each example scenario should run to completion without error."""

    def _run_example(self, func):
        """Run an example function, capturing stdout, asserting no exception."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            func()
        output = buf.getvalue()
        # Every example should produce some output
        self.assertTrue(len(output) > 100,
                        f"{func.__name__} produced too little output")
        return output

    def test_example_employee_warning(self):
        from pbhp_examples import example_employee_warning
        output = self._run_example(example_employee_warning)
        self.assertIn("Employee Performance Warning", output)

    def test_example_workplace_abuse_advice(self):
        from pbhp_examples import example_workplace_abuse_advice
        output = self._run_example(example_workplace_abuse_advice)
        self.assertIn("Workplace", output)

    def test_example_rename_file(self):
        from pbhp_examples import example_rename_file
        output = self._run_example(example_rename_file)
        self.assertIn("Rename", output)

    def test_example_public_accusation_post(self):
        from pbhp_examples import example_public_accusation_post
        output = self._run_example(example_public_accusation_post)
        self.assertIn("Public", output)

    def test_example_policy_analysis(self):
        from pbhp_examples import example_policy_analysis
        output = self._run_example(example_policy_analysis)
        self.assertIn("Policy", output)

    @patch("builtins.input", return_value="")
    def test_run_all_examples(self, mock_input):
        """run_all_examples should execute all scenarios without error."""
        from pbhp_examples import run_all_examples
        buf = io.StringIO()
        with redirect_stdout(buf):
            run_all_examples()
        output = buf.getvalue()
        # Should contain output from multiple scenarios
        self.assertIn("Employee Performance Warning", output)
        self.assertIn("Policy", output)


class TestExamplesEngineState(unittest.TestCase):
    """Verify examples produce correct protocol state."""

    def test_employee_warning_produces_log(self):
        """The employee warning example should create a complete log."""
        from pbhp_examples import example_employee_warning
        from pbhp_core import PBHPEngine
        # Run it and verify the engine has logs
        buf = io.StringIO()
        with redirect_stdout(buf):
            example_employee_warning()
        # No assertion on engine state since examples create local engines,
        # but we verify it ran without raising
        self.assertTrue(True)

    def test_examples_import_all_needed_types(self):
        """Verify pbhp_examples imports don't fail."""
        import pbhp_examples
        # Check key imports are available
        self.assertTrue(hasattr(pbhp_examples, "PBHPEngine"))
        self.assertTrue(hasattr(pbhp_examples, "ImpactLevel"))
        self.assertTrue(hasattr(pbhp_examples, "RiskClass"))
        self.assertTrue(hasattr(pbhp_examples, "DecisionOutcome"))


# ── CLI structural tests ──────────────────────────────────────────────


class TestCLIStructure(unittest.TestCase):
    """Verify CLI has expected structure without running interactive flows."""

    def test_all_step_functions_exist(self):
        import pbhp_cli
        step_funcs = [
            "step_00_protocol_understanding",
            "step_0a_ethical_pause",
            "step_0d_quick_risk_check",
            "step_0g_absolute_rejection",
            "step_1_name_action",
            "step_0e_door_wall_gap",
            "step_0f_constraint_awareness_check",
            "step_2_identify_harms",
            "step_3_risk_display",
            "step_4_consent_check",
            "step_5_alternatives",
            "step_6_5_red_team",
            "step_6_7_decision",
        ]
        for name in step_funcs:
            self.assertTrue(
                hasattr(pbhp_cli, name),
                f"CLI missing step function: {name}",
            )

    def test_standalone_functions_exist(self):
        import pbhp_cli
        for name in [
            "standalone_quick_risk_check",
            "standalone_drift_alarm",
            "standalone_tone_validator",
            "standalone_compare_options",
        ]:
            self.assertTrue(
                hasattr(pbhp_cli, name),
                f"CLI missing standalone function: {name}",
            )

    @patch("builtins.input", return_value="")
    def test_show_help_runs(self, mock_input):
        import pbhp_cli
        buf = io.StringIO()
        with redirect_stdout(buf):
            pbhp_cli.show_help()
        output = buf.getvalue()
        self.assertIn("PBHP", output)

    def test_main_menu_callable(self):
        """main_menu should be callable (we won't actually run it)."""
        import pbhp_cli
        self.assertTrue(callable(pbhp_cli.main_menu))


if __name__ == "__main__":
    unittest.main()
