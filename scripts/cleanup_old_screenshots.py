#!/usr/bin/env python3
"""Remove local-machine screenshots; keep June 28 ProTech VM captures only."""
from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LAB0_IMAGES = REPO / "lab0" / "images"
LAB1_IMAGES = REPO / "lab1" / "images"
SCREENSHOTS = Path(r"D:\Current_work\Innovation in Software\MLOps On AWS June 4\screenshots")
CUTOFF = datetime(2026, 6, 28)  # keep files modified on/after this date

LAB0_STEPS = REPO / "lab0" / "STEPS.md"
LAB0_KEEP_PATTERN = re.compile(
    r"step-(0[1-9]|1[0-9]|2[0-2])[a-z]?-[\w-]+\.png|step-0[1-9]-[\w-]+\.png"
)


def referenced_in_lab0_steps() -> set[str]:
    text = LAB0_STEPS.read_text(encoding="utf-8")
    return set(re.findall(r"images/(step-[^)\s`]+\.png)", text))


def cleanup_lab0() -> int:
    keep = referenced_in_lab0_steps()
    deleted = 0
    for path in LAB0_IMAGES.glob("*.png"):
        if path.name in keep:
            continue
        path.unlink()
        print(f"   DELETE lab0: {path.name}")
        deleted += 1
    return deleted


def cleanup_lab1() -> int:
    deleted = 0
    for path in LAB1_IMAGES.glob("*.png"):
        if datetime.fromtimestamp(path.stat().st_mtime) >= CUTOFF:
            continue
        path.unlink()
        print(f"   DELETE lab1 (local/old): {path.name}")
        deleted += 1
    return deleted


def archive_screenshots_junk() -> int:
    archive = SCREENSHOTS / "archived" / "local-and-junk"
    archive.mkdir(parents=True, exist_ok=True)
    moved = 0
    for pattern in ("step-09-launch-*.png", "Screenshot*.png"):
        for path in SCREENSHOTS.glob(pattern):
            if path.is_file():
                dest = archive / path.name
                if dest.exists():
                    dest.unlink()
                shutil.move(str(path), str(dest))
                print(f"   ARCHIVE: {path.name}")
                moved += 1
    return moved


def main() -> None:
    print("Screenshot cleanup (keep ProTech VM June 28 captures)")
    print("=" * 55)
    d0 = cleanup_lab0()
    d1 = cleanup_lab1()
    moved = archive_screenshots_junk() if SCREENSHOTS.is_dir() else 0
    print(f"\nDeleted lab0 orphans: {d0}")
    print(f"Deleted lab1 local/old: {d1}")
    print(f"Archived source junk: {moved}")


if __name__ == "__main__":
    main()
