"""Trace RH declaration starts and the archive's static module graph."""

from collections import deque
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import tarfile

from verify_lean_archive import ConcatenatedParts, MIT_JOINED_SHA256


ROOT = Path(__file__).resolve().parent
PREFIX = "lean/src/"
LANDAU = "Development.AutomorphicArithmetic.DedekindLFunctions.LandauTheorems."
CORE = "Development.AutomorphicArithmetic.CharacterBoxes."
KERNEL = "Supplements.Kernels."
DECLARATIONS = (
    ("Main", "riemannHypothesis", ("rhOfAll",)),
    ("Main", "riemannZeta_eq_zero_re", ("rhOfAll",)),
    ("Main", "LFunction_ne_zero_of_half_lt_re", ("allChi",)),
    ("Main", "LFunction_eq_zero_re", ("claimAll",)),
    ("Main", "LFunction_eq_zero_re_of_isPrimitive", ("critAll",)),
    (KERNEL+"MainTheorems", "rhOfAll", ("Formalism.VW.rh_of_every", "allChi")),
    (KERNEL+"MainTheorems", "allChi", ("UpperTheory.FinalTheorems.everyCharacter",)),
    (KERNEL+"MainTheorems", "critAll", ("Formalism.VW.critLine", "allChi")),
    (KERNEL+"MainTheorems", "claimAll", ("allChi", "Claim.strip", "Claim.zeta")),
    (CORE+"MainConclusion", "UpperTheory.FinalTheorems.everyCharacter",
     ("UpperTheory.FinalTheorems.everyCharacter_of_row", "UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter")),
    (CORE+"MainConclusion", "UpperTheory.FinalTheorems.everyCharacter_of_row",
     ("UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin", "UpperTheory.One.vwin_of_row")),
    (LANDAU+"landauWindow", "landau_window", ("landau_window_key",)),
    (LANDAU+"landauWindow", "landau_window_key", ("landau_coeff", "landau_window_ineq", "landau_tails")),
)
DECL = re.compile(r"(?m)^(?:private\s+)?(?:theorem|lemma|def|abbrev)\s+([^\s:{(]+)")
IMPORT = re.compile(rb"(?m)^[ \t]*(?:(?:public|private|meta)[ \t]+)*import[ \t]+([^\r\n]+)")


def read_graph(paths):
    modules = {}
    snippets = {}
    selected = {module for module, _, _ in DECLARATIONS} | {
        LANDAU+"LandauCoeff", LANDAU+"landauWindowIneq"
    }
    with io.BufferedReader(ConcatenatedParts(paths)) as stream, tarfile.open(fileobj=stream, mode="r|gz") as tar:
        for member in tar:
            if not (member.isfile() and member.name.startswith(PREFIX) and member.name.endswith(".lean")):
                continue
            name = member.name[len(PREFIX):-5].replace("/", ".")
            with tar.extractfile(member) as src:
                head = src.read()
            # This source snapshot uses leading import blocks. Record an import scan,
            # with exact targeted declaration sightings stored separately.
            matches = IMPORT.findall(head)
            modules[name] = tuple(
                item.decode("utf-8")
                for line in matches
                for item in line.split(b"--", 1)[0].split()
            )
            if name in selected:
                snippets[name] = head
    return modules, snippets


def shortest_import_path(graph, start, finish):
    back = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == finish:
            route = []
            while node is not None:
                route.append(node)
                node = back[node]
            return route[::-1]
        for child in graph.get(node, ()):
            if child not in back:
                back[child] = node
                queue.append(child)
    raise ValueError(f"no source import path to {finish}")


def locate(snippets, module, name, expected):
    source = snippets[module].decode("utf-8")
    matches = list(DECL.finditer(source))
    for index, item in enumerate(matches):
        if item[1] != name:
            continue
        end = matches[index+1].start() if index+1 < len(matches) else len(source)
        block = source[item.start():end]
        edges = []
        for reference in expected:
            token = re.search(r"(?<![\w.])" + re.escape(reference) + r"(?![\w])", block[len(item[0]):])
            if token is None:
                raise ValueError(f"reference missing: {name} -> {reference}")
            edges.append({
                "target_token": reference,
                "line": source.count("\n", 0, item.end()+token.start())+1,
            })
        return {
            "declaration": name, "module": module,
            "source_path": "src/" + module.replace(".", "/") + ".lean",
            "source_sha256": sha256(snippets[module]).hexdigest(),
            "line": source.count("\n", 0, item.start())+1, "references": edges,
        }
    raise ValueError(f"declaration missing: {module}.{name}")


def run():
    manifest = json.loads((ROOT/"lean-archive-manifest.json").read_bytes())
    if manifest["joined_sha256"] != MIT_JOINED_SHA256:
        raise ValueError("archive manifest is not the selected RH snapshot")
    paths = []
    joined = sha256()
    for item in manifest["parts"]:
        path = ROOT/item["file"]
        data = path.read_bytes()
        if sha256(data).hexdigest() != item["sha256"]:
            raise ValueError(f"archive part hash mismatch: {path.name}")
        paths.append(path)
        joined.update(data)
    if len(paths) != 14 or joined.hexdigest() != MIT_JOINED_SHA256:
        raise ValueError("archive snapshot mismatch")
    graph, snippets = read_graph(paths)
    if len(graph) != 175187:
        raise ValueError(f"unexpected module count: {len(graph)}")
    lexical = [locate(snippets, *entry) for entry in DECLARATIONS]
    route = shortest_import_path(graph, "Main", LANDAU+"landauWindowIneq")
    for module in (LANDAU+"LandauCoeff", LANDAU+"landauWindowIneq"):
        name = module.split(".")[-1]
        (ROOT/"sources"/f"rh-{name}.lean").write_bytes(snippets[module])
    (ROOT/"rh-import-graph.json").write_text(json.dumps(graph, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "archive_sha256": MIT_JOINED_SHA256,
        "module_count": len(graph),
        "internal_import_edges": sum(child in graph for children in graph.values() for child in children),
        "import_path_to_window_inequality": route,
        "selected_declarations": lexical,
        "method": "static source import scan and checked source tokens",
        "kernel_dependency_closure": "NOT_RUN",
    }
    (ROOT/"rh-proof-trace.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(len(graph), "modules;", len(lexical), "declarations;", len(route)-1, "import edges to the window inequality")
    print("\n".join(route))


if __name__ == "__main__":
    run()
