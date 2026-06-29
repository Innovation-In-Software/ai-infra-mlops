"""Shared KMS + S3 helpers for Lab 4b IAM policies."""
import json
from pathlib import Path

LAB1_CONFIG = Path(__file__).resolve().parents[3] / "workspace" / "lab1" / "config"


def kms_key_arn():
    path = LAB1_CONFIG / "kms_keys.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f).get("s3_key_arn")
    return None


def kms_statement():
    arn = kms_key_arn()
    if not arn:
        return None
    return {
        "Effect": "Allow",
        "Action": [
            "kms:Decrypt",
            "kms:Encrypt",
            "kms:ReEncrypt*",
            "kms:GenerateDataKey",
            "kms:GenerateDataKey*",
            "kms:DescribeKey",
        ],
        "Resource": arn,
    }
