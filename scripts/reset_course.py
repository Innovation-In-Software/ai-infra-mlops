#!/usr/bin/env python3
"""Reset local workspace for Labs 0–2 (instructor / fresh start)."""
import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = REPO_ROOT / "workspace"


def reset_workspace(labs):
    for lab in labs:
        lab_dir = WORKSPACE / lab
        if not lab_dir.exists():
            print(f"   ⚠️ Skip missing: {lab_dir}")
            continue
        for sub in lab_dir.iterdir():
            if sub.is_file():
                sub.unlink()
            elif sub.is_dir():
                shutil.rmtree(sub)
        print(f"   ✅ Cleared workspace/{lab}/")


def main():
    parser = argparse.ArgumentParser(description="Reset gitignored workspace folders")
    parser.add_argument(
        "--labs",
        default="lab1,lab2",
        help="Comma-separated lab folders under workspace/ (default: lab1,lab2)",
    )
    parser.add_argument(
        "--lab2-aws",
        action="store_true",
        help="Also delete Lab 2 SageMaker feature groups (runs cleanup_lab2 --aws)",
    )
    args = parser.parse_args()
    labs = [x.strip() for x in args.labs.split(",") if x.strip()]

    print("🧹 Reset course workspace")
    print("=" * 60)
    print(f"   Repo: {REPO_ROOT}")
    reset_workspace(labs)

    if args.lab2_aws and "lab2" in labs:
        sys.path.insert(0, str(REPO_ROOT / "lab2" / "scripts"))
        from cleanup_lab2 import delete_feature_groups

        print("\n📋 Deleting Lab 2 feature groups in AWS...")
        delete_feature_groups()

    print("\n✅ Done. Re-run labs from STEPS.md (Lab 0 verify → Lab 1 → Lab 2).")


if __name__ == "__main__":
    main()
