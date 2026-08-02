from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.package_plugin import canonical_file_bytes, create_archive


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


class CreateArchiveTests(unittest.TestCase):
    def test_member_order_and_platform_metadata_are_canonical(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin = root / "demo-plugin"
            (plugin / "agents").mkdir(parents=True)
            (plugin / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (plugin / "agents" / "openai.yaml").write_text("agent\n", encoding="utf-8")
            archive = root / "plugin.zip"

            create_archive(plugin, archive)

            with zipfile.ZipFile(archive) as package:
                self.assertEqual(
                    package.namelist(),
                    ["demo-plugin/SKILL.md", "demo-plugin/agents/openai.yaml"],
                )
                self.assertTrue(all(item.create_system == 3 for item in package.infolist()))


if __name__ == "__main__":
    unittest.main()
