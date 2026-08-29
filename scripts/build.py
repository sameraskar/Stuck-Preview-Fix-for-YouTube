#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
UNPACKED = DIST / "stuck-preview-fix"
PACKAGES = DIST / "packages"


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def zip_directory(source_dir: Path, destination_zip: Path) -> None:
    destination_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source_dir))


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "validate.py")], check=True)

    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    version = manifest["version"]

    if UNPACKED.exists():
        shutil.rmtree(UNPACKED)
    if PACKAGES.exists():
        shutil.rmtree(PACKAGES)
    UNPACKED.mkdir(parents=True, exist_ok=True)
    PACKAGES.mkdir(parents=True, exist_ok=True)

    copy_file(ROOT / "manifest.json", UNPACKED / "manifest.json")
    copy_file(ROOT / "src" / "content.js", UNPACKED / "content.js")

    for size in (16, 32, 48, 128):
        copy_file(ROOT / "icons" / f"icon{size}.png", UNPACKED / "icons" / f"icon{size}.png")

    chrome_zip = PACKAGES / f"stuck-preview-fix-{version}-chrome.zip"
    edge_zip = PACKAGES / f"stuck-preview-fix-{version}-edge.zip"
    zip_directory(UNPACKED, chrome_zip)
    shutil.copy2(chrome_zip, edge_zip)

    print(f"Built unpacked extension: {UNPACKED}")
    print(f"Built Chrome package:     {chrome_zip}")
    print(f"Built Edge package:       {edge_zip}")


if __name__ == "__main__":
    main()
