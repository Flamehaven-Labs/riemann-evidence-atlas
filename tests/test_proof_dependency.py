"""Negative and positive tests for module-local Lean VALUE paths."""
import json
from pathlib import Path
import unittest

from riemann_evidence.proof_dependency import (
    inspect_module_set,
    inspect_value_paths,
    normalize_records,
)


def record(name, kind="theorem", value=(), typ=("True",), imports=("Init", "UnusedModule")):
    return {
        "schema": "riemann-evidence-direct-proof-refs-v1",
        "declaration": name, "kind": kind,
        "type_refs": list(typ), "value_refs": list(value),
        "module_imports": list(imports),
    }


class ProofPathTests(unittest.TestCase):
    def test_import_does_not_create_edge(self):
        graph = inspect_value_paths(
            [record("target", value=("used",)), record("used")], "target"
        )
        self.assertEqual(graph["reached_local_declarations"], ["target", "used"])
        self.assertIn("UnusedModule", graph["imports_not_direct_constant_references"])

    def test_proof_choice_is_distinct(self):
        graph = inspect_value_paths(
            [record("target", value=("Classical.choice",))], "target"
        )
        self.assertEqual(graph["choice_paths"][0]["position"], "PROOF_VALUE_PATH_CANDIDATE")

    def test_data_definition_choice_is_visible_transitively(self):
        graph = inspect_value_paths([
            record("target", value=("derived",)),
            record("derived", kind="definition", value=("chosen",)),
            record("chosen", kind="definition", value=("Classical.choice",)),
        ], "target")
        self.assertEqual(
            graph["choice_paths"][0]["path"],
            ["target", "derived", "chosen", "Classical.choice"],
        )
        self.assertEqual(
            graph["choice_paths"][0]["position"], "DATA_DEFINITION_PATH_CANDIDATE"
        )
        self.assertEqual(graph["choice_paths"][0]["numeric_relevance"], "NOT_ESTABLISHED")

    def test_choice_keeps_both_routes_at_a_shared_declaration(self):
        inputs = [
            record("root", value=("shared", "chosen")),
            record("chosen", kind="definition", value=("shared",)),
            record("shared", value=("Classical.choice",)),
        ]
        paths = inspect_value_paths(inputs, "root")["choice_paths"]
        self.assertEqual({row["position"]: row["path"] for row in paths}, {
            "PROOF_VALUE_PATH_CANDIDATE": ["root", "shared", "Classical.choice"],
            "DATA_DEFINITION_PATH_CANDIDATE": ["root", "chosen", "shared", "Classical.choice"],
        })

    def test_budget_counts_both_states_at_shared_declaration(self):
        inputs = [
            record("root", value=("shared", "chosen")),
            record("chosen", kind="definition", value=("shared",)),
            record("shared"),
        ]
        with self.assertRaisesRegex(ValueError, "budget"):
            inspect_value_paths(inputs, "root", max_nodes=3)
        self.assertEqual(
            inspect_value_paths(inputs, "root", max_nodes=4)["reached_local_declarations"],
            ["chosen", "root", "shared"],
        )

    def test_external_declarations_are_not_silently_closed(self):
        graph = inspect_value_paths([record("top", value=("imported",))], "top")
        self.assertIn("imported", graph["external_or_unresolved_references"])
        self.assertEqual(graph["external_closure"], "NOT_RUN")

    def test_duplicate_declaration_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate declaration"):
            normalize_records([record("x"), record("x")])

    def test_duplicate_reference_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate constant"):
            normalize_records([record("x", value=("y", "y"))])

    def test_wrong_schema_rejected(self):
        bad = record("x")
        bad["schema"] = "untrusted"
        with self.assertRaisesRegex(ValueError, "schema"):
            normalize_records([bad])

    def test_v2_distinguishes_missing_value_from_no_constant_refs(self):
        axiom = {**record("assume", kind="axiom"), "value_refs": None, "has_value": False}
        empty = {**record("empty", kind="definition", typ=("assume",)), "has_value": True}
        for row in (axiom, empty):
            row["schema"] = "riemann-evidence-direct-proof-refs-v2"
        result = normalize_records([axiom, empty])
        self.assertIsNone(result["assume"]["value_refs"])
        self.assertEqual(result["empty"]["value_refs"], [])
        self.assertEqual(inspect_value_paths([axiom], "assume")["choice_paths"], [])
        self.assertEqual(inspect_value_paths([empty, axiom], "empty")["reached_local_declarations"], ["empty"])
        for bad in ({**axiom, "value_refs": []}, {**axiom, "has_value": 0},
                    {**axiom, "value_refs": [], "has_value": True}):
            with self.assertRaisesRegex(ValueError, "stored value"):
                normalize_records([bad])

    def test_cycle_does_not_loop(self):
        graph = inspect_value_paths(
            [record("a", value=("b",)), record("b", value=("a",))], "a")
        self.assertEqual(graph["reached_local_declarations"], ["a", "b"])

    def test_bounded_traversal_reports_error(self):
        with self.assertRaisesRegex(ValueError, "budget"):
            inspect_value_paths(
                [record("a", value=("b",)), record("b", value=("c",)), record("c")],
                "a", max_nodes=2)

    def test_legacy_original_pilot_can_be_analyzed(self):
        raw = json.loads((Path(__file__).resolve().parents[1] /
            "docs/rh-proof-refs-pilot.json").read_text(encoding="utf-8"))
        direct = {key: raw[key] for key in (
            "schema", "declaration", "kind", "type_refs", "value_refs",
            "module_imports")}
        graph = inspect_value_paths([direct], "riemannHypothesis")
        self.assertEqual(graph["direct_type_refs"], ["RiemannHypothesis"])
        self.assertEqual(graph["direct_value_refs"], ["rhOfAll"])
        self.assertIn("rhOfAll", graph["external_or_unresolved_references"])

    def test_original_module_set_links_proof_body_and_keeps_frontier(self):
        receipt = json.loads((Path(__file__).resolve().parents[1] /
            "docs/rh-module-set-pilot.json").read_text(encoding="utf-8"))
        graph = inspect_module_set(receipt["records"], {
            "riemannHypothesis": "Main",
            "rhOfAll": "Supplements.Kernels.MainTheorems",
            "allChi": "Supplements.Kernels.MainTheorems",
        }, "riemannHypothesis")
        self.assertEqual(graph, receipt["analysis"])
        self.assertIn({
            "from": "riemannHypothesis", "from_module": "Main", "kind": "value",
            "to": "rhOfAll", "to_module": "Supplements.Kernels.MainTheorems",
        }, graph["resolved_edges"])
        self.assertIn("Formalism.VW.rh_of_every", graph["external_or_unresolved_references"])
        self.assertIn("UpperTheory.FinalTheorems.everyCharacter",
                      graph["external_or_unresolved_references"])
        self.assertNotIn("rhOfAll", graph["external_or_unresolved_references"])
        self.assertIn({
            "from": "riemannHypothesis", "from_module": "Main",
            "kind": "type", "to": "RiemannHypothesis",
        }, graph["unresolved_edges"])

    def test_module_set_rejects_a_missing_origin(self):
        with self.assertRaisesRegex(ValueError, "source module"):
            inspect_module_set([record("root"), record("other")], {"root": "Main"}, "root")

    def test_original_branches_extend_both_proof_value_paths(self):
        receipt = json.loads((Path(__file__).resolve().parents[1] /
            "docs/rh-branch-module-set.json").read_text(encoding="utf-8"))
        graph = inspect_module_set(receipt["records"], {
            "riemannHypothesis": "Main",
            "rhOfAll": "Supplements.Kernels.MainTheorems",
            "allChi": "Supplements.Kernels.MainTheorems",
            "Formalism.VW.rh_of_every": "Formalism.GammaFactorNonvanishing.CritLine",
            "UpperTheory.FinalTheorems.everyCharacter":
                "Development.AutomorphicArithmetic.CharacterBoxes.MainConclusion",
        }, "riemannHypothesis")
        self.assertEqual(graph, receipt["analysis"])
        value_edges = {(edge["from"], edge["to"]) for edge in graph["resolved_edges"]
                       if edge["kind"] == "value"}
        self.assertEqual(value_edges, {
            ("riemannHypothesis", "rhOfAll"),
            ("rhOfAll", "Formalism.VW.rh_of_every"),
            ("rhOfAll", "allChi"),
            ("allChi", "UpperTheory.FinalTheorems.everyCharacter"),
        })
        unresolved = graph["external_or_unresolved_references"]
        self.assertIn("Formalism.VW.rh_of_right", unresolved)
        self.assertIn("UpperTheory.FinalTheorems.everyCharacter_of_row", unresolved)
        self.assertEqual(graph["external_closure"], "NOT_RUN")

    def test_original_next_layer_resolves_both_previously_open_value_edges(self):
        docs = Path(__file__).resolve().parents[1] / "docs"
        prior = json.loads((docs / "rh-branch-module-set.json").read_bytes())
        receipt = json.loads((docs / "rh-next-layer-module-set.json").read_bytes())
        right = "Formalism.VW.rh_of_right"
        row = "UpperTheory.FinalTheorems.everyCharacter_of_row"
        modules = dict(prior["analysis"]["reached_declarations"])
        modules[right] = "Formalism.GammaFactorNonvanishing.RhOfRight"
        modules[row] = "Development.AutomorphicArithmetic.CharacterBoxes.MainConclusion"
        graph = inspect_module_set(receipt["records"], modules, "riemannHypothesis")
        self.assertEqual(graph, receipt["analysis"])
        self.assertEqual(len(receipt["module_inputs"]), 5)
        self.assertEqual(len(graph["reached_declarations"]), 7)
        new_edges = [edge for edge in graph["resolved_edges"]
                     if edge not in prior["analysis"]["resolved_edges"]]
        self.assertEqual({(edge["from"], edge["to"], edge["kind"]) for edge in new_edges}, {
            ("Formalism.VW.rh_of_every", right, "value"),
            ("UpperTheory.FinalTheorems.everyCharacter", row, "value"),
        })
        unresolved = set(graph["external_or_unresolved_references"])
        self.assertTrue({"riemannZeta_one_sub", "UpperTheory.One.vwin_of_row"} <= unresolved)
        self.assertTrue({right, row}.isdisjoint(unresolved))
        self.assertEqual(graph["external_closure"], "NOT_RUN")

    def test_original_frontier_preserves_evidence_and_axiom_boundary(self):
        docs = Path(__file__).resolve().parents[1] / "docs"
        seed = json.loads((docs / "rh-next-layer-module-set.json").read_bytes())
        report = json.loads((docs / "rh-frontier-classification.json").read_bytes())
        rows = {row["name"]: row for row in report["frontier"]}
        self.assertEqual(len(rows), 378)
        self.assertEqual(sorted(rows), seed["analysis"]["external_or_unresolved_references"])
        self.assertEqual(rows["propext"]["module"], "Init.Core")
        self.assertEqual(rows["propext"]["axiom_status"], "AXIOM_DECLARATION")
        self.assertEqual(rows["propext"]["referrers"], ["Formalism.VW.rh_of_right"])
        self.assertEqual(rows["propext"]["evidence"], "LEAN_TOOLCHAIN_ENVIRONMENT")
        candidate = rows["UpperTheory.One.vwin_of_row"]
        self.assertEqual(candidate["evidence"], "PUBLISHED_GRAPH_CATALOG")
        self.assertEqual(candidate["axiom_status"], "UNCONFIRMED")
        auxiliary = rows["Formalism.VW.rh_of_right._proof_1_1"]
        self.assertEqual(auxiliary["kind"], "theorem")
        self.assertTrue(auxiliary["value_refs"])
        self.assertEqual(auxiliary["evidence"], "PINNED_RH_OLEAN")
        self.assertEqual(report["transitive_closure"], "NOT_RUN")


if __name__ == "__main__":
    unittest.main()
