from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.package_plugin import canonical_file_bytes


class CanonicalFileBytesTests(unittest.TestCase):
    def test_text_line_endings_produce_identical_archive_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lf_file = root / "lf.ps1"
            crlf_file = root / "crlf.ps1"
            lf_file.write_bytes(b"Write-Output 'ok'\nexit 0\n")
            crlf_file.write_bytes(b"Write-Output 'ok'\r\nexit 0\r\n")

            self.assertEqual(canonical_file_bytes(lf_file), canonical_file_bytes(crlf_file))
            self.assertEqual(canonical_file_bytes(lf_file), b"Write-Output 'ok'\nexit 0\n")

    def test_binary_bytes_are_not_normalized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            binary_file = Path(directory) / "asset.bin"
            payload = b"\x00\r\n\xff\n"
            binary_file.write_bytes(payload)

            self.assertEqual(canonical_file_bytes(binary_file), payload)


if __name__ == "__main__":
    unittest.main()
