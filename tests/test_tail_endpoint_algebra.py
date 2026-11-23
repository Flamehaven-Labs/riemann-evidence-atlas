"""P3.1a exact rational endpoint propagation, NOT a Real.exp proof."""

from fractions import Fraction
import json
from pathlib import Path
import re
import unittest

from riemann_evidence.rational_intervals import exp_bounds

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "tests/lean/E2ATailEndpointAlgebra.lean"
BASELINE = ROOT / "window-results-v2.json"

def rational_def(source: str, name: str) -> Fraction:
    pattern = rf"(?m)^def {re.escape(name)} : Rat :=\s*(\d+)\s*/\s*(\d+)"
    match = re.search(pattern, source)
    if match is None or len(re.findall(rf"(?m)^def {re.escape(name)} : Rat :=", source)) != 1:
        raise AssertionError(f"missing or duplicate Lean constant: {name}")
    numerator, denominator = map(int, match.groups())
    return Fraction(numerator, denominator)

class EndpointAlgebraTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = LEAN.read_text(encoding="utf-8")
        cls.report = json.loads(BASELINE.read_text(encoding="utf-8"))
        cls.values = {
            name: rational_def(cls.source, name)
            for name in (
                "exp3Lower", "exp3Upper", "exp9Lower", "exp9Upper",
                "baselineLower", "baselineUpper"
            )
        }

    def test_dyadic_exp_endpoints_match_runtime(self):
        v = self.values
        self.assertEqual(
            (v["exp3Lower"], v["exp3Upper"]), exp_bounds(Fraction(-3), 128),
        )
        self.assertEqual(
            (v["exp9Lower"], v["exp9Upper"]), exp_bounds(Fraction(-9), 128),
        )

    def test_exact_tail_expression_propagates_to_baseline(self):
        v = self.values
        low = (1 - 13*v["exp3Upper"] + 172*v["exp9Lower"]) / 81
        high = (1 - 13*v["exp3Lower"] + 172*v["exp9Upper"]) / 81
        self.assertEqual((low, high), (v["baselineLower"], v["baselineUpper"]))
        self.assertLessEqual(low, high)

    def test_baseline_report_binds_both_caps(self):
        v = self.values
        for key, status in (
            ("landau_tail_valid_cap", "PASS"),
            ("landau_tail_violated_cap", "FAIL"),
        ):
            record = self.report[key]
            self.assertEqual(record["status"], status)
            self.assertEqual(record["details"]["fractional_bits"], 128)
            self.assertEqual(Fraction(record["details"]["lower"]), v["baselineLower"])
            self.assertEqual(Fraction(record["details"]["upper"]), v["baselineUpper"])
        self.assertLessEqual(v["baselineUpper"], Fraction(1, 200))
        self.assertGreater(v["baselineLower"], Fraction(1, 300))

    def test_negative_sign_or_endpoint_mutation_is_rejected(self):
        v = self.values
        correct = v["baselineLower"]
        wrong_sign = (1 + 13*v["exp3Upper"] + 172*v["exp9Lower"]) / 81
        wrong_endpoint = (1 - 13*v["exp3Lower"] + 172*v["exp9Lower"]) / 81
        self.assertNotEqual(wrong_sign, correct)
        self.assertNotEqual(wrong_endpoint, correct)
        self.assertGreater(wrong_endpoint, correct)

if __name__ == "__main__":
    unittest.main()
