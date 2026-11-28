from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import unittest

from tools.verify_landau_tail import ReceiptMismatch, require_receipt_match
from tools.verify_lean_match import semantic_digest
from window_kernel import run_cases, verify_saved_report


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "docs" / "evidence" / "baseline"
HISTORICAL_SHA256 = "fc7ab07321c299d2f0adf921e07d8e3ecf0494b8da5e0f73ee14009bba8ae96b"


class ReplayTests(unittest.TestCase):
    def test_standalone_matches_colab_inputs_endpoints_and_decisions(self):
        raw = (BASELINE / "window-results.json").read_bytes()
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
        self.assertTrue(verify_saved_report((BASELINE / "window-results-v2.json").read_bytes()))

    def test_lean_tail_caps_bind_to_replayed_input_and_endpoints(self):
        source = (ROOT / "tests/lean/E2ATailCapCertificate.lean").read_text(encoding="utf-8")
        p3 = (ROOT / "tests/lean/E2ALandauTailRational.lean").read_text(encoding="utf-8")
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
                    if name in ("lower", "upper"):
                        checks = re.findall(
                            rf"^\s+tail{name.title()} = (\d+) / ([1-9]\d*)", p3, re.M,
                        )
                        self.assertEqual(len(checks), 1, name)
                        self.assertEqual(Fraction(*map(int, checks[0])), Fraction(expected), name)

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

    def test_lean_receipts_bind_to_tracked_sources(self):
        def load(path):
            return json.loads((ROOT / path).read_bytes())

        def check(path, expected):
            with self.subTest(path=path):
                self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), expected)

        helper = "docs/rh-lean-helper-match-v2.json"
        for path in ("docs/rh-lean-fixture-match-v2.json", helper):
            receipt = load(path)
            semantic = receipt["semantic"]
            self.assertEqual(semantic_digest(semantic), receipt["semantic_sha256"])
            check("tests/lean/ChoiceDependenceFixture.lean", semantic["fixture_source_sha256"])
            check("tools/ProofCatalog.lean", semantic["catalog_sha256"])

        frontier = load("docs/rh-mathlib-frontier-match.json")
        check("tools/ProofCatalog.lean", frontier["extractor_sha256"])
        check(helper, frontier["seed_report_sha256"])

        landau = load("docs/landau-tail-lean-replay.json")
        for section, module in (("endpoints", "E2ATailEndpointAlgebra"),
                                ("rational", "E2ALandauTailRational"),
                                ("real", "E2ALandauTailReal")):
            check(f"tests/lean/{module}.lean", landau[section]["sha256"])
        lock = "formal/landau/lake-manifest.json"
        check(lock, landau["real"]["dependency_lock_sha256"])
        self.assertEqual((ROOT / "formal/landau/lean-toolchain").read_bytes(),
                         (ROOT / "lean-toolchain").read_bytes())
        mathlib = next(row["rev"] for row in load(lock)["packages"] if row["name"] == "mathlib")
        self.assertEqual(mathlib, frontier["mathlib_commit"])
        self.assertEqual(mathlib, landau["real"]["mathlib_commit"])
        colab = "docs/landau-tail-colab-replay.json"
        check(colab, "45fb8d94c5969278472f0c9b828d21dd7f97db81edf7ab898e989fed8cbd975e")
        require_receipt_match(load(colab), landau)

    def test_landau_receipt_replay_allows_host_variance_only(self):
        raw = (ROOT / "docs/landau-tail-lean-replay.json").read_bytes()
        expected = json.loads(raw)
        actual = json.loads(raw)
        actual["lean_version"] = actual["lean_version"].replace("x86_64-w64-windows-gnu", "x86_64-unknown-linux-gnu")
        self.assertNotEqual(actual["lean_version"], expected["lean_version"])
        require_receipt_match(actual, expected)
        actual["real"]["axioms"]["tail_mass_caps"].append("sorryAx")
        with self.assertRaisesRegex(ReceiptMismatch, "proof evidence"):
            require_receipt_match(actual, expected)
        actual = json.loads(raw)
        actual["real"] = {"status": "NOT_RUN"}
        with self.assertRaisesRegex(ReceiptMismatch, "proof evidence"):
            require_receipt_match(actual, expected)
        actual["lean_version"] = actual["lean_version"].replace("4.33.1", "4.33.0")
        with self.assertRaisesRegex(ReceiptMismatch, "toolchain"):
            require_receipt_match(actual, expected)

    def test_standalone_receipt_pins(self):
        receipt = json.loads((ROOT / "docs/standalone-replay.json").read_bytes())
        # The original receipt keeps the paths recorded at the time of execution.
        relocated = {
            "RH_Window.ipynb": ROOT / "colab/RH_Window.ipynb",
            "window-results.json": BASELINE / "window-results.json",
            "window-results-v2.json": BASELINE / "window-results-v2.json",
            "lean-archive-manifest.json": ROOT / "docs/evidence/source-index/lean-archive-manifest.json",
            "rh-proof-trace.json": ROOT / "docs/evidence/source-index/rh-proof-trace.json",
        }
        for filename, expected in receipt["sha256"].items():
            with self.subTest(file=filename):
                path = relocated.get(filename, ROOT / filename)
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
