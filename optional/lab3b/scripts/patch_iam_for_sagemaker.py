"""Patch BankingDataScientistRole S3 permissions for Lab 3b SageMaker jobs."""
import json
import sys
from pathlib import Path

import boto3

REPO = Path(__file__).resolve().parents[3]
BUCKETS = REPO / "workspace" / "lab1" / "config" / "buckets.json"
ROLE = "BankingDataScientistRole"
POLICY = "DataScientistBankingPolicy"


def _ensure_statement(doc, resources, actions):
    """Add or merge an allow statement for the given resources."""
    for stmt in doc["Statement"]:
        if stmt.get("Effect") != "Allow":
            continue
        stmt_actions = stmt.get("Action", [])
        if isinstance(stmt_actions, str):
            stmt_actions = [stmt_actions]
        if set(actions).issubset(set(stmt_actions)) and set(resources).issubset(set(stmt.get("Resource", []))):
            return False
    doc["Statement"].append({"Effect": "Allow", "Action": actions, "Resource": resources})
    return True


def main():
    if not BUCKETS.exists():
        print(f"   ❌ Missing {BUCKETS} — complete Lab 1 first.")
        sys.exit(1)

    with open(BUCKETS, encoding="utf-8") as f:
        buckets = json.load(f)
    account_id = boto3.client("sts").get_caller_identity()["Account"]
    models = buckets["models"]["name"]
    sm_bucket = f"sagemaker-us-west-2-{account_id}"

    iam = boto3.client("iam")
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    if isinstance(doc, str):
        doc = json.loads(doc)

    s3_actions = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket",
        "s3:GetBucketLocation",
    ]
    resources = [
        f"arn:aws:s3:::{models}",
        f"arn:aws:s3:::{models}/*",
        f"arn:aws:s3:::{sm_bucket}",
        f"arn:aws:s3:::{sm_bucket}/*",
    ]
    log_actions = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
    ]

    changed = _ensure_statement(doc, resources, s3_actions)
    changed = _ensure_statement(doc, ["*"], log_actions) or changed

    iam.put_role_policy(RoleName=ROLE, PolicyName=POLICY, PolicyDocument=json.dumps(doc))
    print("🔧 Lab 3b IAM patch")
    print("=" * 60)
    print(f"   ✅ Updated {ROLE}")
    print(f"   ✅ S3 access: {models}, {sm_bucket}")
    print("   ✅ CloudWatch Logs for SageMaker jobs")
    print("\nWait ~10 seconds for IAM propagation, then re-run run_training_job.py")


if __name__ == "__main__":
    main()
