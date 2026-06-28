#!/usr/bin/env python3
"""Rename Lab 0 screenshots in the course folder and sync to lab0/images/."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path(
    r"D:\Current_work\Innovation in Software\MLOps On AWS June 4\screenshots"
)
MAP_PATH = REPO / "lab0" / "config" / "screenshot_map.json"
DEST = REPO / "lab0" / "images"
ARCHIVE = DEFAULT_SOURCE / "archived"


def load_map() -> dict:
    with open(MAP_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_map(data: dict) -> None:
    with open(MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def next_auto_name(prefix: str, dest_dir: Path, source_dir: Path) -> str:
    existing = set()
    for folder in (dest_dir, source_dir):
        if not folder.exists():
            continue
        for path in folder.glob(f"{prefix}-*.png"):
            existing.add(path.name)
    for n in range(1, 1000):
        name = f"{prefix}-{n:02d}.png"
        if name not in existing:
            return name
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{stamp}.png"


def rename_in_source(source_dir: Path, data: dict) -> list[tuple[str, str]]:
    """Rename Screenshot*.png in source using map or auto prefix."""
    mappings: dict[str, str] = data.setdefault("mappings", {})
    skip = set(data.get("skip_sources", []))
    prefix = data.get("auto_prefix_unmapped", "step-pending")
    renamed: list[tuple[str, str]] = []

    shots = sorted(source_dir.glob("Screenshot*.png"), key=lambda p: p.stat().st_mtime)
    for path in shots:
        if path.name in skip:
            print(f"   SKIP (passwords/sensitive): {path.name}")
            continue
        if path.name in mappings:
            target_name = mappings[path.name]
        else:
            target_name = next_auto_name(prefix, DEST, source_dir)
            mappings[path.name] = target_name
            print(f"   AUTO-MAP: {path.name} -> {target_name}")
            save_map(data)

        target = source_dir / target_name
        old_name = path.name
        if target.exists() and target.resolve() != path.resolve():
            ARCHIVE.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
            backup = ARCHIVE / f"{target.stem}-{stamp}{target.suffix}"
            shutil.move(str(target), str(backup))
            print(f"   ARCHIVE prior: {target.name} -> archived/{backup.name}")

        if old_name != target_name:
            path.rename(target)
            print(f"   RENAME: {old_name} -> {target_name}")
            renamed.append((old_name, target_name))

    return renamed


def sync_to_repo(source_dir: Path, skip_names: set[str] | None = None) -> list[str]:
    """Copy step-*.png from source (and subdirs) into lab0/images/."""
    DEST.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    patterns = [source_dir.glob("step-*.png")]
    lab0_sub = source_dir / "lab0"
    if lab0_sub.is_dir():
        patterns.append(lab0_sub.glob("step-*.png"))

    skip = skip_names or set()
    seen: set[str] = set()
    for gen in patterns:
        for path in sorted(gen, key=lambda p: p.name):
            if path.name in seen or path.name in skip:
                continue
            seen.add(path.name)
            dest = DEST / path.name
            shutil.copy2(path, dest)
            copied.append(path.name)
            print(f"   COPY: {path.name}")
    return copied


def git_push(repo: Path, message: str) -> bool:
    def run(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            args,
            cwd=repo,
            capture_output=True,
            text=True,
            check=False,
        )

    status = run("git", "status", "--porcelain", "lab0/images", "lab0/config/screenshot_map.json")
    if not status.stdout.strip():
        print("   Git: no screenshot changes to push")
        return False

    run("git", "add", "lab0/images", "lab0/config/screenshot_map.json")
    commit = run("git", "commit", "-m", message)
    if commit.returncode != 0:
        print(f"   Git commit failed: {commit.stderr.strip()}")
        return False
    push = run("git", "push", "origin", "main")
    if push.returncode != 0:
        print(f"   Git push failed: {push.stderr.strip()}")
        return False
    print(f"   Git: pushed ({message})")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Rename and sync Lab 0 screenshots")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--push", action="store_true", help="Commit and push if images changed")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    if not args.source.is_dir():
        print(f"Source folder missing: {args.source}", file=sys.stderr)
        return 1
    if not MAP_PATH.exists():
        print(f"Map file missing: {MAP_PATH}", file=sys.stderr)
        return 1

    if not args.quiet:
        print("Lab 0 screenshot sync")
        print("=" * 50)

    data = load_map()
    skip = set(data.get("skip_sources", []))
    renamed = rename_in_source(args.source, data)
    copied = sync_to_repo(args.source, skip)

    if not args.quiet:
        print(f"\nRenamed: {len(renamed)} | Copied: {len(copied)}")

    if args.push:
        msg = "Lab 0: sync screenshots (auto rename + push)."
        if renamed:
            names = ", ".join(t for _, t in renamed[:3])
            if len(renamed) > 3:
                names += ", ..."
            msg = f"Lab 0: add/update screenshots ({names})."
        git_push(REPO, msg)

    return 0


if __name__ == "__main__":
    sys.exit(main())
