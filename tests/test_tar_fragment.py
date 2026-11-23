from hashlib import sha256
from io import BytesIO
import tarfile
import unittest
import zlib

from tools.recover_pinned_member import recover
from tools.tar_fragment import pinned_member


MEMBER = ("alp-oleans/lib/Development/AutomorphicArithmetic/AutomorphicVarieties/"
          "ModularityArgument/ThresholdArguments/DenseThresholdCases/VwinOfRow.olean")
BODY = b"pinned artifact fixture"
SHA256 = sha256(BODY).hexdigest()


def archive(format):
    info = tarfile.TarInfo(MEMBER)
    info.size = len(BODY)
    with BytesIO() as raw:
        with tarfile.open(fileobj=raw, mode="w:", format=format) as tar:
            tar.addfile(info, BytesIO(BODY))
        return raw.getvalue()


class TarFragmentTests(unittest.TestCase):
    def test_pinned_member_survives_long_name_variants_and_unaligned_start(self):
        for format in (tarfile.USTAR_FORMAT, tarfile.PAX_FORMAT, tarfile.GNU_FORMAT):
            with self.subTest(format=format):
                self.assertEqual(pinned_member(b"unrelated prefix" + archive(format), MEMBER, SHA256), BODY)

    def test_bad_digest_and_truncated_payload_are_not_recovered(self):
        raw = archive(tarfile.PAX_FORMAT)
        self.assertIsNone(pinned_member(raw, MEMBER, "0" * 64))
        self.assertIsNone(pinned_member(raw[:raw.index(BODY) + len(BODY) - 1], MEMBER, SHA256))

    def test_recover_after_deflate_restart_marker(self):
        compressor = zlib.compressobj(wbits=-15)
        compressor.compress(b"short unrelated prefix")
        start = compressor.flush(zlib.Z_FULL_FLUSH)[-4:]
        chunk = start + compressor.compress(archive(tarfile.PAX_FORMAT)) + compressor.flush()
        self.assertEqual(recover(chunk, MEMBER, SHA256), BODY)

    def test_short_header_name_is_not_a_pax_member_alias(self):
        raw = archive(tarfile.PAX_FORMAT)
        self.assertIsNone(pinned_member(raw, MEMBER[:100], SHA256))
