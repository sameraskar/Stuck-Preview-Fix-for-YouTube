#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
SOURCE = ROOT / "src" / "content.js"
REQUIRED_ICONS = [16, 32, 48, 128]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not MANIFEST.exists():
        fail("manifest.json is missing")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if manifest.get("manifest_version") != 3:
        fail("manifest_version must be 3")
    if manifest.get("version") != "1.0.0":
        fail("unexpected release version")
    if manifest.get("permissions"):
        fail("this release should not request extension API permissions")
    if manifest.get("host_permissions"):
        fail("this release does not need separate host_permissions")

    scripts = manifest.get("content_scripts", [])
    if len(scripts) != 1:
        fail("expected exactly one static content script")
    if scripts[0].get("matches") != ["https://www.youtube.com/*"]:
        fail("content script must stay scoped to www.youtube.com")

    if not SOURCE.exists():
        fail("src/content.js is missing")

    source_text = SOURCE.read_text(encoding="utf-8")
    if "const DEBUG = false;" not in source_text:
        fail("release source must keep DEBUG disabled")
    if "fetch(" in source_text or "XMLHttpRequest" in source_text:
        fail("unexpected network request code found")

    for size in REQUIRED_ICONS:
        path = ROOT / "icons" / f"icon{size}.png"
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}")

    print("Validation passed.")


if __name__ == "__main__":
    main()
