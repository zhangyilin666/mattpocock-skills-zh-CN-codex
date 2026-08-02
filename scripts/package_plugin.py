#!/usr/bin/env python3
"""Create a deterministic plugin ZIP and SHA-256 checksum."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "mattpocock-skills-zh-cn"
DIST = ROOT / "dist"


def canonical_file_bytes(path: Path) -> bytes:
    """Return platform-independent bytes for an archive member."""
    data = path.read_bytes()
    if b"\x00" in data:
        return data

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data

    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def create_archive(plugin: Path, archive: Path) -> None:
    """Create a ZIP with canonical member order, metadata, and file contents."""
    paths = sorted(
        (item for item in plugin.rglob("*") if item.is_file()),
        key=lambda item: item.relative_to(plugin).as_posix(),
    )

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for path in paths:
            relative = Path(plugin.name) / path.relative_to(plugin)
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            output.writestr(
                info,
                canonical_file_bytes(path),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )


def main() -> int:
    validation = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate.py")], check=False)
    if validation.returncode:
        return validation.returncode

    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    version = manifest["version"].split("+", 1)[0]
    archive = DIST / f"mattpocock-skills-zh-cn-{version}.zip"
    DIST.mkdir(exist_ok=True)

    create_archive(PLUGIN, archive)

    digest = hashlib.sha256(archive.read_bytes()).hexdigest().upper()
    checksum = DIST / "SHA256SUMS.txt"
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8", newline="\n")
    print(f"Created {archive.relative_to(ROOT)}")
    print(f"SHA256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
