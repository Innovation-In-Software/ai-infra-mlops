"""Encryption audit (S3, ECR, KMS)."""
import json
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION, load_buckets, write_json

from lab_paths import CONFIG_DIR, ensure_workspace

ECR_REPO = "banking-ml-inference"


def _bucket_encryption(s3, bucket_name):
    try:
        resp = s3.get_bucket_encryption(Bucket=bucket_name)
        rules = resp.get("ServerSideEncryptionConfiguration", {}).get("Rules", [])
        if rules:
            algo = rules[0].get("ApplyServerSideEncryptionByDefault", {}).get("SSEAlgorithm", "UNKNOWN")
            return algo
        return "NONE"
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ServerSideEncryptionConfigurationNotFoundError":
            return "NONE"
        raise


def main():
    ensure_workspace()
    buckets = load_buckets()
    s3 = boto3.client("s3", region_name=REGION)
    ecr = boto3.client("ecr", region_name=REGION)

    s3_results = {}
    for key in ("raw", "processed", "models"):
        name = buckets[key]["name"]
        s3_results[key] = _bucket_encryption(s3, name)

    ecr_enc = "UNKNOWN"
    try:
        repos = ecr.describe_repositories(repositoryNames=[ECR_REPO])
        cfg = repos["repositories"][0].get("encryptionConfiguration", {})
        ecr_enc = cfg.get("encryptionType", "AES256")
    except ClientError:
        ecr_enc = "NOT_FOUND"

    all_ok = all(v in ("aws:kms", "KMS", "AES256") for v in s3_results.values()) and ecr_enc in (
        "KMS",
        "AES256",
    )
    report = {
        "s3": s3_results,
        "ecr": ecr_enc,
        "status": "PASS" if all_ok else "REVIEW",
        "source": "aws",
    }
    write_json(CONFIG_DIR / "encryption_audit.json", report)
    print("🔐 Encryption Audit")
    print("=" * 60)
    print(f"   Status: {report['status']}")
    for key, val in s3_results.items():
        print(f"   S3 {key}: {val}")
    print(f"   ECR {ECR_REPO}: {ecr_enc}")
    print("✅ Encryption audit saved")


if __name__ == "__main__":
    main()
