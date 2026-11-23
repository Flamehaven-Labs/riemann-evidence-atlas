"""Verify the original Lean distribution and compare selected source files."""

from hashlib import sha256
import io
import json
from pathlib import Path
import tarfile


ROOT = Path(__file__).resolve().parent
MIT_JOINED_SHA256 = "9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc"
MIRROR_FILES = {
    "src/Main.lean": "rh-Main.lean",
    "src/Statements.lean": "rh-Statements.lean",
    "lean-toolchain": "rh-lean-toolchain",
    "lake-manifest.json": "rh-lake-manifest.json",
}


class ConcatenatedParts(io.RawIOBase):
    def __init__(self, paths):
        self.remaining = iter(paths)
        self.current = None

    def readable(self):
        return True

    def readinto(self, buffer):
        while True:
            if self.current is None:
                path = next(self.remaining, None)
                if path is None:
                    return 0
                self.current = path.open("rb")
            count = self.current.readinto(buffer)
            if count:
                return count
            self.current.close()
            self.current = None

    def close(self):
        if self.current is not None:
            self.current.close()
        super().close()


def verify():
    parts = [ROOT / "sources" / "lean-parts" / f"lean.tar.gz.part{i:02}" for i in range(1, 15)]
    joined = sha256()
    rows = []
    for path in parts:
        if not path.is_file():
            raise FileNotFoundError(path)
        data = path.read_bytes()
        joined.update(data)
        rows.append({"file": path.relative_to(ROOT).as_posix(), "url": f"https://alpo.ge/{path.name}",
                     "bytes": len(data), "sha256": sha256(data).hexdigest()})
    total = sum(row["bytes"] for row in rows)
    if total != 239_275_554 or joined.hexdigest() != MIT_JOINED_SHA256:
        raise ValueError(f"Source archive differs from MIT reference ({total}, {joined.hexdigest()})")

    members = {}
    with io.BufferedReader(ConcatenatedParts(parts)) as stream, tarfile.open(fileobj=stream, mode="r|gz") as tar:
        first = tar.next()
        if first is None:
            raise ValueError("Empty archive")
        root_dir = first.name.split("/")[0]
        targets = {f"{root_dir}/{key}": name for key, name in MIRROR_FILES.items()}
        for item in tar:
            if item.name not in targets or not item.isfile():
                continue
            if item.name in members:
                raise ValueError(f"Duplicate archive member: {item.name}")
            with tar.extractfile(item) as member:
                data = member.read()
            members[item.name] = {
                "sha256": sha256(data).hexdigest(),
                "matches_pinned_mirror": data == (ROOT / "sources" / targets[item.name]).read_bytes(),
            }
            if members.keys() == targets.keys():
                break
    if members.keys() != targets.keys():
        raise ValueError(f"Missing expected archive entries: {targets.keys() - members.keys()}")
    result = {"joined_bytes": total, "joined_sha256": joined.hexdigest(),
              "matches_mit_manifest": True, "parts": rows, "selected_members": members}
    (ROOT / "lean-archive-manifest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "parts"}, indent=2))


if __name__ == "__main__":
    verify()
