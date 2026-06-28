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
    args = parser.parse_args()

    if not args.yes:
        print("This will delete Lab 1 AWS resources, Lab 2 feature groups, and all workspace/lab* folders.")
        if input("Type yes to continue: ").strip().lower() != "yes":
            print("Aborted.")
            sys.exit(1)

    print("🧹 Full course teardown")
    print("=" * 60)

    run([sys.executable, "scripts/reset_course.py", "--labs",
         "lab1,lab2,lab3,lab4,lab5,lab6,lab7,lab8,lab9,lab10"])

    if args.skip_aws:
        print("\n✅ Workspace reset only (--skip-aws).")
        return

    lab2 = REPO / "lab2" / "scripts" / "cleanup_lab2.py"
    if lab2.exists():
        run([sys.executable, str(lab2), "--aws"])

    lab1_scripts = REPO / "lab1" / "scripts"
    for script in ("delete_audit_logging.py", "delete_sagemaker_studio.py", "delete_banking_buckets.py"):
        path = lab1_scripts / script
        if path.exists():
            run([sys.executable, str(path)])

    # Optional: ECR repository created in Lab 5
    try:
        import boto3
        ecr = boto3.client("ecr", region_name="us-west-2")
        repo = "banking-ml-inference"
        try:
            ecr.delete_repository(repositoryName=repo, force=True)
            print(f"   ✅ Deleted ECR repository: {repo}")
        except ecr.exceptions.RepositoryNotFoundException:
            print(f"   ⚠️ ECR repo not found: {repo}")
    except Exception as exc:
        print(f"   ⚠️ ECR cleanup skipped: {exc}")

    print("\n" + "=" * 60)
    print("✅ Teardown complete.")
    print("   Manual (if re-running Lab 1 from scratch):")
    print("   - IAM Console: delete BankingDataScientistRole, BankingMLEngineerRole, BankingComplianceOfficerRole")
    print("   - KMS Console: disable/delete keys from workspace/lab1/config/kms_keys.json")
    print("   - CloudWatch: delete Banking-MLOps-Audit-Dashboard and BankingDataDriftAlarm if desired")
    print("   - SageMaker Experiments: banking-risk-experiments (optional)")


if __name__ == "__main__":
    main()
