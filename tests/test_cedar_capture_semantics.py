from __future__ import annotations

import subprocess
import unittest

from scripts.capture_cedar_observation import classify_authorize_result


class CedarCaptureExitSemanticsTests(unittest.TestCase):
    def test_allow_exit_zero_is_valid_observation(self) -> None:
        result = subprocess.CompletedProcess(["cedar"], 0, stdout="\nALLOW\n", stderr="")
        decision, valid, semantics = classify_authorize_result(result)
        self.assertEqual(decision, "ALLOW")
        self.assertTrue(valid)
        self.assertEqual(semantics, "cedar_success_exit_0")

    def test_deny_exit_two_is_valid_observation(self) -> None:
        result = subprocess.CompletedProcess(["cedar"], 2, stdout="\nDENY\n", stderr="")
        decision, valid, semantics = classify_authorize_result(result)
        self.assertEqual(decision, "DENY")
        self.assertTrue(valid)
        self.assertEqual(semantics, "cedar_authorize_deny_exit_2")

    def test_failure_exit_one_remains_fail_closed(self) -> None:
        result = subprocess.CompletedProcess(["cedar"], 1, stdout="DENY\n", stderr="failure")
        decision, valid, semantics = classify_authorize_result(result)
        self.assertIsNone(decision)
        self.assertFalse(valid)
        self.assertEqual(semantics, "unexpected_or_failed_cedar_authorize_result")

    def test_mismatched_decision_and_exit_remains_fail_closed(self) -> None:
        result = subprocess.CompletedProcess(["cedar"], 2, stdout="ALLOW\n", stderr="")
        decision, valid, semantics = classify_authorize_result(result)
        self.assertIsNone(decision)
        self.assertFalse(valid)
        self.assertEqual(semantics, "unexpected_or_failed_cedar_authorize_result")


if __name__ == "__main__":
    unittest.main()
