from fractions import Fraction
import json
from pathlib import Path
import unittest

from tools.prime_two_local_surface import compute, compute_character_comparison, local_terms, verify_report


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


class PrimeTwoCharacterTests(unittest.TestCase):
    def test_four_cases_and_conductor_change(self):
        cases = compute_character_comparison()["cases"]
        expected = [
            ("trivial_mod_1", 1, 1, 1, "4/3", "1/3", "4/3", "1", "0"),
            ("quadratic_mod_3", 3, 3, -1, "4/5", "-1/5", "4/5", "1", "0"),
            ("primitive_mod_4", 4, 4, 0, "1", "0", "1", "1", "0"),
            ("principal_mod_4", 4, 1, 0, "1", "0", "4/3", "3/4", "-1/3"),
        ]
        observed = [
            (c["character"], c["modulus"], c["conductor"], c["at_level"]["character_at_p"],
             c["at_level"]["L_p"], c["at_level"]["negative_log_derivative_over_log_p"],
             c["at_conductor"]["L_p"], c["finite_removal_factor"],
             c["finite_removal_log_derivative_coefficient"])
            for c in cases
        ]
        self.assertEqual(observed, expected)
        self.assertEqual([c["ramified_at_p"] for c in cases], [False, False, True, False])
        self.assertEqual([c["omitted_by_level"] for c in cases], [False, False, False, True])
        self.assertEqual(cases[3]["at_conductor"]["negative_log_derivative_over_log_p"], "1/3")

    def test_replay_fixed_character_record(self):
        report = Path(__file__).resolve().parents[1] / "docs/masullo/P2_CHARACTER_COMPARISON.json"
        verify_report(report.read_bytes(), characters=True)

    def test_reject_self_consistent_wrong_sign_and_added_ramified_factor(self):
        for index in (1, 2):
            with self.subTest(case=index):
                report = compute_character_comparison()
                row = report["cases"][index]
                for surface in ("at_level", "at_conductor"):
                    row[surface] = {"character_at_p": 1, **local_terms(Fraction(1, 4), 8)}
                with self.assertRaisesRegex(ValueError, "report mismatch"):
                    verify_report(json.dumps(report).encode("utf-8"), characters=True)

    def test_reject_conductor_swapped_for_modulus(self):
        report = compute_character_comparison()
        case = report["cases"][3]
        case["conductor"] = case["modulus"]
        with self.assertRaisesRegex(ValueError, "report mismatch"):
            verify_report(json.dumps(report).encode("utf-8"), characters=True)
