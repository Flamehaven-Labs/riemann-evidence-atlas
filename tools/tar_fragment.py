"""Look up a hash-pinned regular file in a partial, decompressed tar stream."""

from __future__ import annotations

from hashlib import sha256
from io import BytesIO
import tarfile

MAX_BYTES = 10 * 1024 * 1024


def pinned_member(raw: bytes, member: str, expected_sha256: str) -> bytes | None:
    """Accept complete payloads only; a fragment may start or end mid-member."""
    search_from = 0
    with BytesIO(raw) as stream:
        while (magic := raw.find(b"ustar", search_from)) != -1:
            search_from = magic + 5
            offset = magic - 257
            if offset < 0 or offset + tarfile.BLOCKSIZE > len(raw):
                continue
            try:
                header = tarfile.TarInfo.frombuf(
                    raw[offset:offset + tarfile.BLOCKSIZE], "utf-8", "surrogateescape",
                )
            except (tarfile.HeaderError, ValueError, OverflowError):
                continue
            if header.type in (tarfile.XHDTYPE, tarfile.XGLTYPE, tarfile.GNUTYPE_LONGNAME):
                if not 0 < header.size <= MAX_BYTES or offset + tarfile.BLOCKSIZE + header.size > len(raw):
                    continue
                stream.seek(offset)
                try:
                    # Let tarfile resolve the GNU or PAX name and the payload offset.
                    with tarfile.open(fileobj=stream, mode="r:") as archive:
                        info = archive.next()
                except (tarfile.TarError, ValueError, OverflowError, RecursionError):
                    continue
                if info is None:
                    continue
                search_from = max(search_from, info.offset_data)
            else:
                info = header
                info.offset_data = offset + tarfile.BLOCKSIZE
            if info.name != member or not info.isfile() or not 0 < info.size <= MAX_BYTES:
                continue
            end = info.offset_data + info.size
            if end > len(raw):
                continue
            payload = raw[info.offset_data:end]
            if sha256(payload).hexdigest() == expected_sha256:
                return payload
    return None
