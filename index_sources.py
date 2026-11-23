"""Build a page-level index and record source checksums for the research intake."""

from hashlib import sha256
from pathlib import Path
import json
import re

import pypdfium2 as pdfium


ROOT = Path(__file__).resolve().parent
SOURCES = {
    "alpoge-remark.pdf": "https://alpo.ge/remark.pdf",
    "rubinstein-zeta-guide.pdf": "https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/zeta-paper.pdf",
    "pei-proof-roadmap.pdf": "https://peabrane.github.io/files/pei-2026-claimed-lean-proof-rh-roadmap.pdf",
    "alpoge-buckmaster-navier-stokes.pdf": "https://raw.githubusercontent.com/tristanbuckmaster/navier-stokes/ad53419de079eb8f95f60313473374624a348546/paper/finite-time-blow-up-navier-stokes.pdf",
    "rh-Main.lean": "https://raw.githubusercontent.com/leanprover-community/riemann-hypothesis/40e56bab026552e089d7afcfeff08d2defb9c005/src/Main.lean",
    "rh-Statements.lean": "https://raw.githubusercontent.com/leanprover-community/riemann-hypothesis/40e56bab026552e089d7afcfeff08d2defb9c005/src/Statements.lean",
    "rh-lean-toolchain": "https://raw.githubusercontent.com/leanprover-community/riemann-hypothesis/40e56bab026552e089d7afcfeff08d2defb9c005/lean-toolchain",
    "rh-lake-manifest.json": "https://raw.githubusercontent.com/leanprover-community/riemann-hypothesis/40e56bab026552e089d7afcfeff08d2defb9c005/lake-manifest.json",
    "ns-lean-README.md": "https://raw.githubusercontent.com/tristanbuckmaster/navier-stokes/ad53419de079eb8f95f60313473374624a348546/lean/README.md",
    "mit-audit.log": "https://math.mit.edu/~drew/grh/audit.log",
}
EXPECTED_PAGES = {
    "alpoge-remark.pdf": 4,
    "rubinstein-zeta-guide.pdf": 164,
    "pei-proof-roadmap.pdf": 23,
    "alpoge-buckmaster-navier-stokes.pdf": 79,
}
TOPICS = {
    "verification": r"\b(?:kernel|comparator|axioms?|Lean)\b",
    "analytic-reduction": r"\b(?:Landau|Riesz|von Mangoldt)\b",
    "arithmetic-method": r"\b(?:Stepanov|theta lifts?|divisibility)\b",
    "numerical-certificate": r"\b(?:certificates?|interval arithmetic|Arb|FLINT)\b",
    "navier-stokes-profile": r"\b(?:self.simi(?:lar|larity)|Navier.Stokes|tail data)\b",
}


def build_index():
    sources = []
    pages = []
    for name, url in SOURCES.items():
        path = ROOT / "sources" / name
        data = path.read_bytes()
        source = {"file": path.relative_to(ROOT).as_posix(), "url": url,
                  "bytes": len(data), "sha256": sha256(data).hexdigest()}
        sources.append(source)
        if name not in EXPECTED_PAGES:
            continue
        if not data.startswith(b"%PDF-"):
            raise ValueError(f"Invalid PDF signature in {path.name}")
        with pdfium.PdfDocument(data) as document:
            if len(document) != EXPECTED_PAGES[name]:
                raise ValueError(f"Unexpected page count in {path.name}")
            source["pages"] = len(document)
            for i, page in enumerate(document, 1):
                text_page = page.get_textpage()
                extracted = text_page.get_text_range().replace("\r\n", "\n")
                location = f"{url}#page={i}"
                hits = [topic for topic, pattern in TOPICS.items()
                        if re.search(pattern, extracted, re.IGNORECASE)]
                pages.append({
                    "file": source["file"], "pdf_sha256": source["sha256"],
                    "pdf_page": i, "location": location, "topic_hits": hits,
                    "extracted_text_characters": len(extracted),
                    "extracted_text_sha256": sha256(extracted.encode()).hexdigest(),
                    "requires_visual_check": len(extracted.strip()) < 40,
                })
                text_page.close()
                page.close()

    (ROOT / "sources.json").write_text(
        json.dumps(sources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (ROOT / "pdf-pages.jsonl").open("w", encoding="utf-8", newline="\n") as out:
        for row in pages:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Indexed {len(pages)} pages in {len(EXPECTED_PAGES)} PDFs.")


if __name__ == "__main__":
    build_index()
