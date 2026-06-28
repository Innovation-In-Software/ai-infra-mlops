#!/usr/bin/env python3
"""Tear down all course AWS resources and workspace (instructor / end of class)."""
import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def run(cmd, cwd=None, check=False):
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd or REPO, check=check)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Delete all MLOps lab AWS resources and workspace")
    parser.add_argument("--skip-aws", action="store_true", help="Only reset local workspace")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompt")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted (no AWS or workspace changes)",
    )
    parser.add_argument(
        "--terminate-ec2",
        action="store_true",
        help="Also terminate EC2 instances with 'mlops' in the Name tag",
    )
    parser.add_argument(
        "--kms-pending-days",
        type=int,
        default=7,
        choices=range(7, 31),
        metavar="N",
        help="KMS pending deletion window in days (7–30, default 7)",
    )
    args = parser.parse_args()

    if not args.yes and not args.dry_run:
        print(
            "This will delete Lab 1–10 AWS resources, IAM roles, KMS keys "
            "(scheduled), alarms, SageMaker experiments, and workspace folders."
        )
        if args.terminate_ec2:
            print("   --terminate-ec2: mlops-tagged EC2 instances will be terminated.")
        if input("Type yes to continue: ").strip().lower() != "yes":
            print("Aborted.")
            sys.exit(1)

    print("🧹 Full course teardown")
    print("=" * 60)

    if args.dry_run:
        print("   (dry-run mode — workspace reset skipped)")
    else:
        run(
            [
                sys.executable,
                "scripts/reset_course.py",
                "--labs",
                "lab1,lab2,lab3,lab4,lab5,lab6,lab7,lab8,lab9,lab10",
            ]
        )

    if args.skip_aws:
        print("\n✅ Workspace reset only (--skip-aws).")
        return

    if not args.dry_run:
        lab2 = REPO / "lab2" / "scripts" / "cleanup_lab2.py"
        if lab2.exists():
            run([sys.executable, str(lab2), "--aws"])

        lab1_scripts = REPO / "lab1" / "scripts"
        for script in (
            "delete_audit_logging.py",
            "delete_sagemaker_studio.py",
            "delete_banking_buckets.py",
        ):
            path = lab1_scripts / script
            if path.exists():
                run([sys.executable, str(path)])
    else:
        print("\n   would run lab2 cleanup_lab2.py --aws")
        print("   would run lab1 delete_audit_logging.py")
        print("   would run lab1 delete_sagemaker_studio.py")
        print("   would run lab1 delete_banking_buckets.py")

    sys.path.insert(0, str(REPO / "scripts"))
    from teardown_aws_extras import cleanup_aws_extras

    cleanup_aws_extras(
        dry_run=args.dry_run,
        terminate_ec2=args.terminate_ec2,
        kms_pending_days=args.kms_pending_days,
    )

    print("\n" + "=" * 60)
    if args.dry_run:
        print("✅ Dry run complete. Re-run with --yes to delete resources.")
    else:
        print("✅ Teardown complete.")
        print("   Re-run Lab 0 → Lab 1 to provision a fresh environment.")


if __name__ == "__main__":
    main()
