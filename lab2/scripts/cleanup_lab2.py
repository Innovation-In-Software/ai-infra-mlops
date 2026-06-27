"""Reset Lab 2 local workspace and optional SageMaker Feature Groups."""
import shutil
import sys
import time

import boto3
from lab_paths import CONFIG_DIR, DATA_DIR, LOGS_DIR, RESULTS_DIR, VALIDATION_DIR, ensure_workspace

FEATURE_GROUPS = (
    "banking-transaction-features",
    "banking-customer-features",
)


def cleanup_workspace():
    ensure_workspace()
    removed = []
    for folder in (DATA_DIR, CONFIG_DIR, LOGS_DIR, RESULTS_DIR, VALIDATION_DIR):
        if not folder.exists():
            continue
        for path in folder.iterdir():
            if path.is_file():
                path.unlink()
                removed.append(str(path))
            elif path.is_dir():
                shutil.rmtree(path)
                removed.append(str(path))
    print(f"   ✅ Cleared {len(removed)} files under workspace/lab2/")
    return removed


def delete_feature_groups(region="us-west-2"):
    sm = boto3.client("sagemaker", region_name=region)
    for name in FEATURE_GROUPS:
        try:
            sm.describe_feature_group(FeatureGroupName=name)
        except sm.exceptions.ResourceNotFound:
            print(f"   ⚠️ Feature group not found: {name}")
            continue
        print(f"   🗑️ Deleting feature group: {name}")
        sm.delete_feature_group(FeatureGroupName=name)
        deadline = time.time() + 600
        while time.time() < deadline:
            try:
                sm.describe_feature_group(FeatureGroupName=name)
                print(f"   ... waiting for delete: {name}")
                time.sleep(15)
            except sm.exceptions.ResourceNotFound:
                print(f"   ✅ Deleted: {name}")
                break
        else:
            print(f"   ⚠️ Timed out waiting for delete: {name}")


def cleanup_lab2(delete_aws_feature_groups=False):
    print("🧹 Lab 2 cleanup — start from scratch")
    print("=" * 60)
    cleanup_workspace()
    if delete_aws_feature_groups:
        print("\n📋 Deleting SageMaker Feature Groups...")
        delete_feature_groups()
    else:
        print("\n   Skipping AWS feature group delete (pass --aws to remove them)")
    print("\n" + "=" * 60)
    print("✅ Lab 2 workspace reset. Re-run STEPS.md from Step 4.")


if __name__ == "__main__":
    delete_aws = "--aws" in sys.argv
    cleanup_lab2(delete_aws_feature_groups=delete_aws)
