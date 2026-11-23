import json
from pathlib import Path
import unittest

from tools.prime_two_local_surface import compute, verify_report


class PrimeTwoBaselineTests(unittest.TestCase):
    def test_exact_coefficients(self):
        cases = compute()["cases"]
        self.assertEqual([row["L_p"] for row in cases], ["4/3", "8/7", "16/15"])
        self.assertEqual(
            [row["negative_log_derivative_over_log_p"] for row in cases],
            ["1/3", "1/7", "1/15"],
        )

    def test_replay_fixed_record(self):
        report = Path(__file__).resolve().parents[1] / "docs/masullo/P2_LOCAL_SURFACE.json"
        verify_report(report.read_bytes())

    def test_reject_duplicate_fields(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            verify_report(b'{"cases": [], "cases": []}')

    def test_reject_type_mutation(self):
        report = compute()
        report["cases"][0]["identity_holds"] = 1
        with self.assertRaisesRegex(ValueError, "report mismatch"):
            verify_report(json.dumps(report).encode("utf-8"))

    def test_reject_invalid_inputs(self):
        for kwargs in ({"p": True}, {"p": 1}, {"m": 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                compute(**kwargs)
