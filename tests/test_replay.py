from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import unittest

from window_kernel import run_cases, verify_saved_report


ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_SHA256 = "fc7ab07321c299d2f0adf921e07d8e3ecf0494b8da5e0f73ee14009bba8ae96b"


class ReplayTests(unittest.TestCase):
    def test_standalone_matches_colab_inputs_endpoints_and_decisions(self):
        raw = (ROOT / "window-results.json").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), HISTORICAL_SHA256)
        historical = json.loads(raw)
        current = run_cases()
        self.assertEqual(len(current), 10)
        self.assertEqual(current.keys(), historical.keys())
        for name, report in current.items():
            with self.subTest(name=name):
                for field in ("inputs", "details", "status", "claim_authority", "claim_status"):
                    self.assertEqual(report[field], historical[name][field])

    def test_current_report_replays(self):
        self.assertTrue(verify_saved_report((ROOT / "window-results-v2.json").read_bytes()))

    def test_lean_tail_caps_bind_to_replayed_input_and_endpoints(self):
        source = (ROOT / "tests/lean/E2ATailCapCertificate.lean").read_text(encoding="utf-8")
        reports = run_cases()
        model = {"component": "outside_window", "k": 3, "rate": "3", "a": "1", "b": "3",
                 "precision_bits": 128}
        for case, status, cap, lean_cap in (
            ("landau_tail_valid_cap", "PASS", "1/200", "acceptedCap"),
            ("landau_tail_violated_cap", "FAIL", "1/300", "rejectedCap"),
        ):
            with self.subTest(case=case):
                report = reports[case]
                raw = json.dumps({**model, "cap": cap}, sort_keys=True).encode("utf-8")
                self.assertEqual(report["inputs"]["window"]["sha256"], hashlib.sha256(raw).hexdigest())
                self.assertEqual(report["status"], status)
                self.assertEqual(report["details"]["fractional_bits"], model["precision_bits"])
                for name, expected in (("lower", report["details"]["lower"]),
                                       ("upper", report["details"]["upper"]),
                                       (lean_cap, cap)):
                    literals = re.findall(rf"^def {name} : Rat := (\d+) / ([1-9]\d*)$", source, re.M)
                    self.assertEqual(len(literals), 1, name)
                    numerator, denominator = map(int, literals[0])
                    self.assertEqual(Fraction(numerator, denominator), Fraction(expected), name)

    def test_report_with_missing_case_is_rejected(self):
        report = run_cases()
        del report["precision_exhausted"]
        self.assertFalse(verify_saved_report(json.dumps(report).encode()))

    def test_changed_interval_is_rejected(self):
        report = run_cases()
        report["landau_tail_valid_cap"]["details"]["lower"] = "0"
        self.assertFalse(verify_saved_report(json.dumps(report).encode()))

    def test_duplicate_key_report_is_rejected(self):
        self.assertFalse(verify_saved_report(b'{"case":0,"case":1}'))

    def test_changed_precision_type_is_rejected(self):
        report = run_cases()
        report["landau_tail_valid_cap"]["details"]["fractional_bits"] = 128.0
        self.assertFalse(verify_saved_report(json.dumps(report).encode()))

    def test_standalone_receipt_pins(self):
        receipt = json.loads((ROOT / "docs/standalone-replay.json").read_bytes())
        for filename, expected in receipt["sha256"].items():
            with self.subTest(file=filename):
                self.assertEqual(hashlib.sha256((ROOT / filename).read_bytes()).hexdigest(), expected)
