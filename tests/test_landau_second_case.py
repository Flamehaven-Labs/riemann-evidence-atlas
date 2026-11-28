"""Bounded second RH case, distinct from the released Landau certificate."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import unittest

import landau_second_case as second
from riemann_evidence.rational_intervals import exp_bounds, expm1_bounds
from riemann_evidence.verification import Status
from window_kernel import decide_upper_cap

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs/landau-second-case.json"


def alternating_exp_neg(x: F) -> tuple[F, F]:
    """Independent direct alternating Taylor enclosure for x in [0, 4].

    Beyond n=180 the positive term magnitudes decrease to zero, so adjacent
    partial sums bound exp(-x). No range reduction, squaring or outward
    rounding from the production evaluator is reused.
    """
    if not F(0) <= x <= F(4):
        raise ValueError("test oracle requires 0 <= x <= 4")
    term = total = F(1)
    for n in range(1, 181):
        term *= -x / n
        total += term
    return total - term*x/181, total


class SecondLandauTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved = RECEIPT.read_bytes()
        cls.report = second.run_cases()
        cls.cases = cls.report["cases"]

    def test_pinned_second_case_and_original_report(self):
        self.assertTrue(second.verify_saved_report(self.saved))
        baseline = ROOT / "docs/evidence/baseline/window-results-v2.json"
        self.assertEqual(hashlib.sha256(baseline.read_bytes()).hexdigest(),
                         "ad3d31ceaf5a9a78e5f17f5c25ac087394eb57ebfb3cfdd977aa57c61ac66bf1")
        self.assertEqual(self.report["formal_real_proof"], "NOT_RUN")

    def test_independent_alternating_series_encloses_real_tail(self):
        # J=(1-2 exp(-1)+5 exp(-4))/4.
        l1, u1 = alternating_exp_neg(F(1))
        l4, u4 = alternating_exp_neg(F(4))
        oracle_lo, oracle_hi = (1-2*u1+5*l4)/4, (1-2*l1+5*u4)/4
        for name, entry in self.cases.items():
            with self.subTest(case=name):
                d = entry["report"]["details"]
                lo, hi = F(d["lower"]), F(d["upper"])
                self.assertLessEqual(lo, oracle_lo)
                self.assertLessEqual(oracle_lo, oracle_hi)
                self.assertLessEqual(oracle_hi, hi)

    def test_pass_fail_unresolved_and_refined(self):
        expected = {"valid_cap": "PASS", "violated_cap": "FAIL",
                    "precision_exhausted": "UNRESOLVED", "refined_cap": "PASS"}
        for name, status in expected.items():
            self.assertEqual(self.cases[name]["report"]["status"], status)
        d = self.cases["precision_exhausted"]["report"]["details"]
        cap = F(second.NEAR_CAP)
        self.assertEqual(F(d["cap"]), cap)
        self.assertEqual(d["fractional_bits"], 128)
        self.assertLessEqual(F(d["lower"]), cap)
        self.assertLess(cap, F(d["upper"]))
        r = self.cases["refined_cap"]["report"]["details"]
        self.assertEqual(r["fractional_bits"], 256)
        self.assertLessEqual(F(r["upper"]), cap)
        self.assertLess(F(r["upper"]) - F(r["lower"]), F(d["upper"]) - F(d["lower"]))

    def test_reject_ordered_mutations_and_precision_status_drift(self):
        for key, value in (("lower", "0"), ("upper", "1/10"),
                           ("fractional_bits", 128.0), ("cap", "1/9")):
            with self.subTest(key=key):
                altered = json.loads(self.saved)
                altered["cases"]["valid_cap"]["report"]["details"][key] = value
                self.assertFalse(second.verify_saved_report(json.dumps(altered).encode()))
        altered = json.loads(self.saved)
        altered["cases"]["precision_exhausted"]["report"]["status"] = "PASS"
        self.assertFalse(second.verify_saved_report(json.dumps(altered).encode()))
        self.assertFalse(second.verify_saved_report(b'{"cases":{},"cases":{}}'))

    def test_threshold_boundary_semantics(self):
        enclose = lambda bits: (F(1, 3), F(1, 2))
        for cap, expected in ((F(1, 2), Status.PASS), (F(1, 3), Status.UNRESOLVED),
                              (F(1, 4), Status.FAIL)):
            with self.subTest(cap=cap):
                self.assertEqual(decide_upper_cap(enclose, cap, 128).status, expected)
        exact = lambda bits: (F(1, 2), F(1, 2))
        self.assertEqual(decide_upper_cap(exact, F(1, 2), 128).status, Status.PASS)
        with self.assertRaises(ArithmeticError):
            decide_upper_cap(lambda bits: (F(2), F(1)), F(1), 128)
        with self.assertRaises(ArithmeticError):
            decide_upper_cap(lambda bits: (0.1, 0.2), F(1), 128)

    def test_interval_api_exact_input_and_supported_precision(self):
        for x in (F(-16), F(0), F(16)):
            for bits in (128, 256, 512):
                lo, hi = exp_bounds(x, bits)
                self.assertIsInstance(lo, F)
                self.assertIsInstance(hi, F)
                self.assertLessEqual(lo, hi)
                self.assertGreaterEqual(lo, 0)
        self.assertEqual(exp_bounds(F(0), 128), (F(1), F(1)))
        self.assertEqual(expm1_bounds(F(0), 512), (F(0), F(0)))
        for func in (exp_bounds, expm1_bounds):
            with self.assertRaises(ValueError):
                func(0.25, 128)
            with self.assertRaises(ValueError):
                func(F(1, 4), 128.0)
            with self.assertRaises(ValueError):
                func(F(1, 4), 64)
        with self.assertRaises(ValueError):
            exp_bounds(F(17), 128)
        with self.assertRaises(ValueError):
            expm1_bounds(F(3, 4), 128)
