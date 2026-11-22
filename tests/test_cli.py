"""Subprocess regressions against the real Rust CLI (not a simulated pass)."""
import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BINARY = ROOT / "target" / "debug" / "sybilwall-gate"


class OfflineObservationCLITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(["cargo", "build", "--offline", "--quiet"], cwd=ROOT, check=True)

    def invoke(self, *args):
        return subprocess.run(
            [str(BINARY), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_low_rejection_rate(self):
        result = self.invoke("inspect", "9", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("rejection_bps=1000 disposition=OBSERVE", result.stdout)

    def test_high_rejection_rate(self):
        result = self.invoke("inspect", "1", "9")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("rejection_bps=9000 disposition=REVIEW", result.stdout)

    def test_zero_observations_rejected(self):
        result = self.invoke("inspect", "0", "0")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NO_OBSERVATIONS", result.stderr)

    def test_negative_input_rejected(self):
        result = self.invoke("inspect", "-1", "1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("INVALID_ACCEPTED_COUNT", result.stderr)

    def test_non_numeric_input_rejected(self):
        result = self.invoke("inspect", "oops", "1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("INVALID_ACCEPTED_COUNT", result.stderr)

    def test_count_overflow_rejected(self):
        result = self.invoke("inspect", "18446744073709551615", "1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("COUNT_OVERFLOW", result.stderr)

    def test_missing_arguments_rejected(self):
        result = self.invoke("inspect", "1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("USAGE", result.stderr)

    def test_no_false_production_claims(self):
        result = self.invoke("inspect", "1", "0")
        self.assertEqual(result.returncode, 0)
        self.assertIn("OFFLINE_DIAGNOSTIC_ONLY", result.stdout)
        self.assertNotIn("FIPS", result.stdout)
        self.assertNotIn("100/100", result.stdout)


if __name__ == "__main__":
    unittest.main()
