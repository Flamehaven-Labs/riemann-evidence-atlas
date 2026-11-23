"""Recover one hash-pinned tar member from local pigz cache fragments."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import zlib

if __package__:
    from .tar_fragment import pinned_member
else:
    from tar_fragment import pinned_member

MIB = 1024 * 1024
SYNC_MARKER = b"\x00\x00\xff\xff"


def recover(chunk: bytes, member: str, digest: str) -> bytes | None:
    payload = memoryview(chunk)
    candidates = [(0, 31)] if chunk.startswith(b"\x1f\x8b") else []
    search = 0
    while len(candidates) < 8 and (marker := chunk.find(SYNC_MARKER, search)) != -1:
        search = marker + len(SYNC_MARKER)
        candidates.append((search, -15))
    for offset, window_bits in candidates:
        try:
            if window_bits == 31:
                decoder = zlib.decompressobj(window_bits)
            else:
                # A restart may initially depend on an unavailable previous window.
                decoder = zlib.decompressobj(window_bits, zdict=bytes(32768))
            raw = decoder.decompress(payload[offset:], max_length=64 * MIB)
        except zlib.error:
            continue
        if (found := pinned_member(raw, member, digest)) is not None:
            return found
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--member", required=True)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("fragments", nargs="+", type=Path)
    args = parser.parse_args()
    if re.fullmatch(r"[0-9a-f]{64}", args.sha256) is None:
        parser.error("expected lowercase SHA-256")
    try:
        for fragment in args.fragments:
            if fragment.stat().st_size > 16 * MIB:
                parser.error(f"cache fragment exceeds 16 MiB: {fragment.name}")
            if (body := recover(fragment.read_bytes(), args.member, args.sha256)) is not None:
                with args.output.open("xb") as output:
                    output.write(body)
                print(f"PINNED_MEMBER_RECOVERED {args.sha256} {fragment.name}")
                return 0
    except FileNotFoundError as error:
        print(f"ENV_BLOCKED: {error}", file=sys.stderr)
        return 2
    print(f"NOT_RECOVERED_IN_BOUNDED_CACHE_SCAN {len(args.fragments)} fragments")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
