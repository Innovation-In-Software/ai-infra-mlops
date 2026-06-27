"""Delete Lab 1.1 banking S3 buckets so you can re-run create_banking_buckets.py."""
import argparse
import json
import sys

import boto3

from lab_paths import CONFIG_DIR, ensure_workspace

BUCKET_TYPES = ("raw", "processed", "models", "monitoring", "governance", "audit")


def load_bucket_names():
    config_path = CONFIG_DIR / "buckets.json"
    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            data = json.load(f)
        if data:
            return [info["name"] for info in data.values() if info.get("name")]

    account_id = boto3.client("sts").get_caller_identity()["Account"]
    return [f"bank-mlops-{account_id}-{t}" for t in BUCKET_TYPES]


def empty_bucket(s3, bucket_name):
    paginator = s3.get_paginator("list_object_versions")
    for page in paginator.paginate(Bucket=bucket_name):
        objects = []
        for item in page.get("Versions", []) + page.get("DeleteMarkers", []):
            objects.append({"Key": item["Key"], "VersionId": item["VersionId"]})
        if objects:
            s3.delete_objects(Bucket=bucket_name, Delete={"Objects": objects})

    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name):
        objects = [{"Key": obj["Key"]} for obj in page.get("Contents", [])]
        if objects:
            s3.delete_objects(Bucket=bucket_name, Delete={"Objects": objects})


def delete_banking_buckets(dry_run=False):
    ensure_workspace()
    s3 = boto3.client("s3", region_name="us-west-2")
    bucket_names = load_bucket_names()

    print("Delete Lab 1.1 S3 buckets")
    print("=" * 60)

    deleted = []
    for name in bucket_names:
        try:
            s3.head_bucket(Bucket=name)
        except s3.exceptions.ClientError:
            print(f"   skip (not found): {name}")
            continue

        if dry_run:
            print(f"   would delete: {name}")
            deleted.append(name)
            continue

        print(f"   emptying: {name}")
        empty_bucket(s3, name)
        s3.delete_bucket(Bucket=name)
        print(f"   deleted: {name}")
        deleted.append(name)

    config_path = CONFIG_DIR / "buckets.json"
    if not dry_run and config_path.exists():
        config_path.write_text("{}\n", encoding="utf-8")
        print(f"\n   cleared: {config_path}")

    print("\n" + "=" * 60)
    if dry_run:
        print(f"Dry run — {len(deleted)} bucket(s) would be deleted.")
    else:
        print(f"Done — deleted {len(deleted)} bucket(s).")
        print("Re-run: python scripts\\create_banking_buckets.py")

    return deleted


def main():
    parser = argparse.ArgumentParser(description="Delete Lab 1.1 banking S3 buckets")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted")
    args = parser.parse_args()
    delete_banking_buckets(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
