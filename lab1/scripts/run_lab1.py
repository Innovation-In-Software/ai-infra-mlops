"""Run all Lab 1.1 setup scripts in order."""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from create_banking_buckets import create_banking_buckets
from create_banking_iam_roles import create_banking_iam_roles
from create_kms_keys import create_banking_kms_keys
from create_sagemaker_studio import create_sagemaker_studio
from enable_audit_logging import enable_audit_logging
from lab_paths import WORKSPACE, ensure_workspace
from validate_environment import validate_environment


def main():
    print("Banking MLOps Lab 1.1 — Secure Environment Setup")
    print("=" * 60)
    ensure_workspace()
    print(f"Workspace: {WORKSPACE}\n")

    steps = [
        ("KMS keys", create_banking_kms_keys),
        ("S3 buckets", create_banking_buckets),
        ("IAM roles", create_banking_iam_roles),
        ("SageMaker Studio", create_sagemaker_studio),
        ("Audit logging", enable_audit_logging),
    ]

    for i, (label, fn) in enumerate(steps, 1):
        print(f"\n>>> Step {i}/5: {label}")
        fn()

    print("\n>>> Validation")
    results = validate_environment()
    failed = results["summary"]["failed"]
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
