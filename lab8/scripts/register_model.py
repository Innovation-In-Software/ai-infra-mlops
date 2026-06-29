"""Register model in SageMaker Model Registry."""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION, load_iam_role, write_json

from lab_paths import CONFIG_DIR, LAB5, LAB6, ensure_workspace

GROUP_NAME = "banking-risk-models"


def _image_uri():
    path = LAB5 / "config" / "ecr_config.json"
    if not path.exists():
        print("   ❌ Missing Lab 5 ecr_config.json")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        base = json.load(f).get("uri", "")
    return base if base.endswith(":latest") else f"{base}:latest"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()

    image_uri = _image_uri()
    load_iam_role("ml_engineer")

    staging_note = ""
    staging_path = LAB6 / "config" / "staging_deployment.json"
    if staging_path.exists():
        with open(staging_path, encoding="utf-8") as f:
            staging_note = json.load(f).get("model", "")

    if args.dry_run:
        reg = {
            "model_package_group": GROUP_NAME,
            "approval_status": "PendingManualApproval",
            "dry_run": True,
        }
        write_json(CONFIG_DIR / "model_registry.json", reg)
        print(f"   ✅ Model package group: {GROUP_NAME}")
        print("✅ Model registered (dry-run)")
        return

    sm = boto3.client("sagemaker", region_name=REGION)
    try:
        sm.create_model_package_group(
            ModelPackageGroupName=GROUP_NAME,
            ModelPackageGroupDescription="Banking risk models — course lab registry",
        )
        print(f"   ✅ Created model package group: {GROUP_NAME}")
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "ValidationException":
            raise
        print(f"   ✅ Model package group exists: {GROUP_NAME}")

    description = f"Banking inference image registered {datetime.now(timezone.utc).isoformat()}"
    if staging_note:
        description += f" (staging model: {staging_note})"

    try:
        resp = sm.create_model_package(
            ModelPackageGroupName=GROUP_NAME,
            ModelPackageDescription=description,
            InferenceSpecification={
                "Containers": [{"Image": image_uri}],
                "SupportedContentTypes": ["application/json"],
                "SupportedResponseMIMETypes": ["application/json"],
            },
            ModelApprovalStatus="PendingManualApproval",
            CertifyForMarketplace=False,
        )
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"   ❌ Model registry failed: {code} — {exc.response['Error'].get('Message', '')}")
        if code in ("AccessDenied", "AccessDeniedException"):
            print("   Re-run: cd ~/ai-infra-mlops/lab1 && python3 scripts/create_banking_iam_roles.py")
        sys.exit(1)
    package_arn = resp["ModelPackageArn"]
    reg = {
        "model_package_group": GROUP_NAME,
        "model_package_arn": package_arn,
        "approval_status": "PendingManualApproval",
        "image_uri": image_uri,
        "source": "sagemaker",
    }
    write_json(CONFIG_DIR / "model_registry.json", reg)
    print("📋 Model Registry")
    print("=" * 60)
    print(f"   ✅ Model package group: {GROUP_NAME}")
    print(f"   ✅ Model package ARN: {package_arn}")
    print("✅ Model registered")


if __name__ == "__main__":
    main()
