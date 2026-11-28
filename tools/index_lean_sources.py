"""Match local extracted Lean sources to exact members of the pinned archive."""

from hashlib import sha256
import io
import json
import tarfile

from verify_lean_archive import ConcatenatedParts, MIT_JOINED_SHA256, ROOT, SOURCE_INDEX


def index_sources():
    source_dir = ROOT / "sources"
    local_files = sorted(
        [*source_dir.glob("rh-*.lean"), source_dir / "rh-lean-toolchain",
         source_dir / "rh-lake-manifest.json"]
    )
    if len(local_files) != 15:
        raise ValueError("expected the fifteen preserved Lean input files")
    pins = {
        path.name.removeprefix("rh-"): (path, sha256(path.read_bytes()).hexdigest())
        for path in local_files
    }
    manifest = json.loads((SOURCE_INDEX / "lean-archive-manifest.json").read_bytes())
    joined = sha256()
    parts = []
    for entry in manifest["parts"]:
        path = ROOT / entry["file"]
        raw = path.read_bytes()
        if len(raw) != entry["bytes"] or sha256(raw).hexdigest() != entry["sha256"]:
            raise ValueError(f"archive part mismatch: {path.name}")
        joined.update(raw)
        parts.append(path)
    if len(parts) != 14 or joined.hexdigest() != MIT_JOINED_SHA256:
        raise ValueError("selected archive hash mismatch")

    matches = {}
    with io.BufferedReader(ConcatenatedParts(parts)) as stream:
        with tarfile.open(fileobj=stream, mode="r|gz") as archive:
            for member in archive:
                name = member.name.rsplit("/", 1)[-1]
                if not member.isfile() or name not in pins:
                    continue
                path, expected = pins[name]
                with archive.extractfile(member) as source:
                    digest = sha256(source.read()).hexdigest()
                if digest == expected:
                    matches.setdefault(path.name, []).append(member.name)
    if set(matches) != {path.name for path in local_files}:
        raise ValueError("one or more extracts do not match an archive member")
    return {
        "archive_sha256": MIT_JOINED_SHA256,
        "files": [
            {"file": path.relative_to(ROOT).as_posix(), "sha256": digest,
             "archive_members": sorted(matches[path.name])}
            for path, digest in pins.values()
        ],
    }


if __name__ == "__main__":
    print(json.dumps(index_sources(), indent=2))
