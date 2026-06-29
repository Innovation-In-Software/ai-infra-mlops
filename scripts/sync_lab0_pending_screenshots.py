#!/usr/bin/env python3
"""Copy step-pending Lab 0 screenshots to lab0/images/ (Steps 17a–18)."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "lab0" / "config" / "lab0_screenshot_manifest.json"
IMAGES = REPO / "lab0" / "images"
DEFAULT_SOURCE = Path(
    r"D:\Current_work\Innovation in Software\MLOps On AWS June 4\screenshots"
)
PENDING_PREFIX = "step-pending-"


def load_manifest() -> dict:
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)


def pending_mappings(data: dict) -> dict[str, str]:
    return {
        src: dest
        for src, dest in data.get("canonical", {}).items()
        if src.startswith(PENDING_PREFIX)
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Lab 0 step-pending screenshots")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()

    mappings = pending_mappings(load_manifest())
    IMAGES.mkdir(parents=True, exist_ok=True)

    print("Lab 0 step-pending screenshot sync")
    print("=" * 50)

    copied = 0
    for src_name, dest_name in mappings.items():
        src = args.source / src_name
        if not src.is_file():
            print(f"   MISSING: {src_name}")
            continue
        shutil.copy2(src, IMAGES / dest_name)
        print(f"   COPY: {src_name} -> {dest_name}")
        copied += 1

    print(f"\nCopied: {copied}")
    return 0 if copied else 1


if __name__ == "__main__":
    sys.exit(main())
