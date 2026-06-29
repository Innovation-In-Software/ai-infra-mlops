#!/usr/bin/env python3
"""Copy canonical Lab 7 screenshots from instructor captures to lab7/images/."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "lab7" / "config" / "lab7_screenshot_manifest.json"
IMAGES = REPO / "lab7" / "images"
DEFAULT_SOURCE = Path(
    r"D:\Current_work\Innovation in Software\MLOps On AWS June 4\screenshots"
)


def load_manifest() -> dict:
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)


def resolve_source(source_dir: Path, name: str) -> Path | None:
    path = source_dir / name
    return path if path.is_file() and path.stat().st_size > 0 else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Lab 7 screenshots to lab7/images/")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()

    data = load_manifest()
    source = args.source
    IMAGES.mkdir(parents=True, exist_ok=True)

    print("Lab 7 screenshot sync")
    print("=" * 50)
    print(f"   Source: {source}")
    print(f"   Dest:   {IMAGES}")

    copied = 0
    for src_name, dest_name in data.get("canonical", {}).items():
        src = resolve_source(source, src_name)
        if not src:
            print(f"   MISSING: {src_name}")
            continue
        shutil.copy2(src, IMAGES / dest_name)
        print(f"   COPY: {src_name} -> {dest_name}")
        copied += 1

    for dest_name, src_name in data.get("aliases", {}).items():
        src = IMAGES / src_name
        if src.is_file():
            shutil.copy2(src, IMAGES / dest_name)
            print(f"   ALIAS: {src_name} -> {dest_name}")
            copied += 1

    for dest_name, rel_src in data.get("reuse_from_lab6", {}).items():
        src = REPO / rel_src
        if src.is_file():
            shutil.copy2(src, IMAGES / dest_name)
            print(f"   REUSE lab6: {rel_src} -> {dest_name}")
            copied += 1

    allowed = (
        set(data.get("canonical", {}).values())
        | set(data.get("aliases", {}).keys())
        | set(data.get("reuse_from_lab6", {}).keys())
    )
    for path in IMAGES.glob("*.png"):
        if path.name not in allowed and path.name != ".gitkeep":
            path.unlink()
            print(f"   DELETE unmapped: {path.name}")

    print(f"\nCopied: {copied}")
    return 0 if copied else 1


if __name__ == "__main__":
    sys.exit(main())
