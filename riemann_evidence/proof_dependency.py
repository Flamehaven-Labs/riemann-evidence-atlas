"""Inspect declaration-level VALUE references exported from a pinned Lean .olean.

Only value edges between supplied declaration records are traversed.
References beyond the supplied records stay unresolved.
"""
from __future__ import annotations

from collections import deque
from collections.abc import Mapping, Sequence

KIND = frozenset({"theorem", "definition", "opaque"})
MAX_DEFAULT = 4096


def _names(value: object, label: str, *, allow_duplicates: bool = False) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value):
        raise ValueError(f"{label}: expected a list of nonempty constant names")
    if not allow_duplicates and len(value) != len(set(value)):
        raise ValueError(f"{label}: duplicate constant reference")
    return value


def normalize_records(raw: object) -> dict[str, dict]:
    """Admit only Lean-extracted records with well-formed named edges."""
    if not isinstance(raw, list) or not raw:
        raise ValueError("expected nonempty list of Lean direct-reference records")
    indexed: dict[str, dict] = {}
    for record in raw:
        if not isinstance(record, dict):
            raise ValueError("expected declaration record object")
        if record.get("schema") != "riemann-evidence-direct-proof-refs-v1":
            raise ValueError("unexpected Lean direct-reference schema")
        name, kind = record.get("declaration"), record.get("kind")
        if not isinstance(name, str) or not name or not isinstance(kind, str) or kind not in KIND:
            raise ValueError("invalid declaration name or kind")
        if name in indexed:
            raise ValueError(f"duplicate declaration {name}")
        _names(record.get("type_refs"), f"{name}.type_refs")
        _names(record.get("value_refs"), f"{name}.value_refs")
        # A source .olean can contain duplicate Init header imports.
        _names(record.get("module_imports"), f"{name}.module_imports", allow_duplicates=True)
        indexed[name] = record
    return indexed


def inspect_value_paths(raw: object, root: str, *, max_nodes: int = MAX_DEFAULT) -> dict:
    """Report shortest module-local value paths; imports are never value edges.

    Classical.choice encountered in a theorem's value is a proof-position use.
    A path through a definition is a possible data-selection dependency, not a
    proof of numerical noncomputability or relevance to a particular observable.
    """
    index = normalize_records(raw)
    if root not in index:
        raise ValueError(f"missing root declaration: {root}")
    if type(max_nodes) is not int or not 1 <= max_nodes <= 100000:
        raise ValueError("max_nodes must be 1..100000")
    pending = deque([(root, (root,))])
    seen: set[str] = set()
    external: set[str] = set()
    choices: list[dict] = []
    while pending:
        node, path = pending.popleft()
        if node in seen:
            continue
        if len(seen) >= max_nodes:
            raise ValueError("module-local dependency budget exhausted")
        seen.add(node)
        for referenced in index[node]["value_refs"]:
            next_path = (*path, referenced)
            if referenced == "Classical.choice":
                # A numeric dependency needs separate proof that the chosen
                # object actually enters the target computation.
                data_nodes = [
                    n for n in path
                    if index.get(n, {}).get("kind") == "definition"
                ]
                choices.append({
                    "path": list(next_path),
                    "position": (
                        "DATA_DEFINITION_PATH_CANDIDATE" if data_nodes
                        else "PROOF_VALUE_PATH_CANDIDATE"
                    ),
                    "data_definitions": data_nodes,
                    "numeric_relevance": "NOT_ESTABLISHED",
                })
            if referenced in index:
                if referenced not in seen:
                    pending.append((referenced, next_path))
            else:
                external.add(referenced)
    initial = index[root]
    actual_refs = set(initial["type_refs"]) | set(initial["value_refs"])
    return {
        "schema": "riemann-evidence-module-local-value-paths-v1",
        "root": root,
        "scope": "MODULE_LOCAL_VALUE_REFS_ONLY",
        "kind": initial["kind"],
        "direct_type_refs": sorted(initial["type_refs"]),
        "direct_value_refs": sorted(initial["value_refs"]),
        "imports_not_direct_constant_references": sorted(
            set(initial["module_imports"]) - actual_refs
        ),
        "reached_local_declarations": sorted(seen),
        "external_or_unresolved_references": sorted(external),
        "external_closure": "NOT_RUN",
        "choice_paths": sorted(choices, key=lambda x: x["path"]),
        "original_proof_kernel_replay": "NOT_RUN",
    }


def inspect_module_set(raw: object, modules: Mapping[str, str], root: str) -> dict:
    """Attribute each reached declaration and retain every unresolved edge."""
    index = normalize_records(raw)
    if set(modules) != set(index) or any(
        not isinstance(module, str) or not module for module in modules.values()
    ):
        raise ValueError("each declaration needs exactly one source module")

    analysis = inspect_value_paths(raw, root)
    reached = analysis.pop("reached_local_declarations")
    resolved = []
    unresolved = []
    for name in reached:
        for kind in ("type", "value"):
            for target in sorted(index[name][f"{kind}_refs"]):
                edge = {"from": name, "from_module": modules[name], "kind": kind,
                        "to": target}
                if target in modules:
                    resolved.append({**edge, "to_module": modules[target]})
                else:
                    unresolved.append(edge)
    return {
        **analysis,
        "schema": "riemann-evidence-module-set-value-paths-v1",
        "scope": "SUPPLIED_MODULE_DECLARATION_RECORDS",
        "reached_declarations": {name: modules[name] for name in reached},
        "resolved_edges": resolved,
        "unresolved_edges": unresolved,
    }
