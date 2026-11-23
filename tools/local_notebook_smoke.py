"""Execute RH_Window.ipynb's two source cells in an offline scratch directory.

This is a LOCAL notebook-cell replay. It does not connect to a Colab VM.
The source notebook writes its report only inside this temporary directory.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "window_kernel.py",
    "riemann_evidence/__init__.py",
    "riemann_evidence/rational_intervals.py",
    "riemann_evidence/verification.py",
)

def main():
    notebook = json.loads((ROOT / "RH_Window.ipynb").read_text(encoding="utf-8"))
    cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    if len(cells) != 2:
        raise AssertionError("Expected exactly two source code cells")
    previous = Path.cwd()
    with TemporaryDirectory(prefix="riemann-notebook-offline-") as directory:
        scratch = Path(directory)
        for relative in FILES:
            target = scratch / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        try:
            os.chdir(scratch)
            namespace = {"__name__": "__main__"}
            for index, cell in enumerate(cells):
                exec(compile("".join(cell["source"]), f"notebook-cell-{index}", "exec"), namespace)
            generated = (scratch / "window-results-v2.json").read_bytes()
        finally:
            os.chdir(previous)
    saved = (ROOT / "window-results-v2.json").read_bytes()
    if json.loads(generated) != json.loads(saved):
        raise AssertionError("Notebook report differs from pinned report")
    print(json.dumps({
        "schema": "riemann-evidence-local-notebook-smoke-v1",
        "environment": "LOCAL_OFFLINE_PYTHON_NOT_COLAB",
        "cases": len(json.loads(generated)),
        "notebook_sha256": hashlib.sha256((ROOT / "RH_Window.ipynb").read_bytes()).hexdigest(),
        "generated_report_sha256": hashlib.sha256(generated).hexdigest(),
        "saved_report_sha256": hashlib.sha256(saved).hexdigest(),
        "matches_saved_parsed_report": True,
        "colab_execution": "NOT_RUN",
        "lean_kernel_replay": "NOT_RUN",
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
