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


def main() -> int:
    validation = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate.py")], check=False)
    if validation.returncode:
        return validation.returncode

    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    version = manifest["version"].split("+", 1)[0]
    archive = DIST / f"mattpocock-skills-zh-cn-{version}.zip"
    DIST.mkdir(exist_ok=True)

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for path in sorted(item for item in PLUGIN.rglob("*") if item.is_file()):
            relative = Path(PLUGIN.name) / path.relative_to(PLUGIN)
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            output.writestr(
                info,
                canonical_file_bytes(path),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )

    digest = hashlib.sha256(archive.read_bytes()).hexdigest().upper()
    checksum = DIST / "SHA256SUMS.txt"
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8", newline="\n")
    print(f"Created {archive.relative_to(ROOT)}")
    print(f"SHA256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
