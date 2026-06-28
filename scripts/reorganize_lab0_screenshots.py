#!/usr/bin/env python3
"""Copy canonical Lab 0 screenshots and remove step-09-launch-* junk from lab0/images/."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path(
    r"D:\Current_work\Innovation in Software\MLOps On AWS June 4\screenshots"
)
MANIFEST = REPO / "lab0" / "config" / "lab0_screenshot_manifest.json"
IMAGES = REPO / "lab0" / "images"
ARCHIVE = DEFAULT_SOURCE / "archived" / "step-09-launch-junk"


def load_manifest() -> dict:
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)


def resolve_source(source_dir: Path, name: str) -> Path | None:
    for candidate in (source_dir / name, IMAGES / name):
        if candidate.is_file():
            return candidate
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Reorganize Lab 0 screenshots to canonical names")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()

    if not MANIFEST.is_file():
        print(f"Manifest missing: {MANIFEST}", file=sys.stderr)
        return 1

    data = load_manifest()
    canonical: dict[str, str] = data.get("canonical", {})
    IMAGES.mkdir(parents=True, exist_ok=True)

    print("Lab 0 screenshot reorganize")
    print("=" * 50)

    copied = 0
    for src_name, dest_name in canonical.items():
        src = resolve_source(args.source, src_name)
        if not src:
            print(f"   MISSING source: {src_name}")
            continue
        dest = IMAGES / dest_name
        shutil.copy2(src, dest)
        print(f"   COPY: {src_name} -> {dest_name}")
        copied += 1

    deleted = 0
    for pattern in data.get("delete_from_repo_images", []):
        for path in IMAGES.glob(pattern):
            path.unlink()
            print(f"   DELETE: {path.name}")
            deleted += 1

    if args.source.is_dir():
        ARCHIVE.mkdir(parents=True, exist_ok=True)
        for path in args.source.glob("step-09-launch-*.png"):
            if path.name in canonical:
                continue
            target = ARCHIVE / path.name
            if target.exists():
                target.unlink()
            shutil.move(str(path), str(target))
            print(f"   ARCHIVE: {path.name}")

    print(f"\nCopied: {copied} | Deleted from repo: {deleted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
