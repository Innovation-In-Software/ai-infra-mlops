"""Create CodeBuild project and IAM role for Lab 4b."""
import json
import sys
import time
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from scripts.course_common import account_id, write_json

from lab_paths import CODEBUILD_PROJECT, CONFIG_DIR, LAB1_CONFIG, REGION, ensure_workspace

BUILD_ROLE = "BankingLab4bCodeBuildRole"


def _ensure_build_role(iam, account):
    trust = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "codebuild.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    }
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
                "Resource": "*",
            },
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:PutObject", "s3:GetBucketLocation", "s3:ListBucket"],
                "Resource": "*",
            },
        ],
    }
    try:
        iam.create_role(
            RoleName=BUILD_ROLE,
            AssumeRolePolicyDocument=json.dumps(trust),
            Description="CodeBuild role for Lab 4b optional pipeline",
        )
        print(f"   ✅ Created IAM role: {BUILD_ROLE}")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"   ✅ IAM role exists: {BUILD_ROLE}")
    iam.put_role_policy(
        RoleName=BUILD_ROLE,
        PolicyName="Lab4bCodeBuildPolicy",
        PolicyDocument=json.dumps(policy),
    )
    return f"arn:aws:iam::{account}:role/{BUILD_ROLE}"


def main():
    ensure_workspace()
    print("🔧 CodeBuild project (Lab 4b)")
    print("=" * 60)

    src_cfg = CONFIG_DIR / "pipeline_source.json"
    if not src_cfg.exists():
        print("   ❌ Run package_source.py first.")
        sys.exit(1)

    account = account_id()
    iam = boto3.client("iam")
    cb = boto3.client("codebuild", region_name=REGION)
    build_role_arn = _ensure_build_role(iam, account)
    time.sleep(10)  # IAM propagation

    with open(LAB1_CONFIG / "buckets.json", encoding="utf-8") as f:
        buckets = json.load(f)
    artifact_bucket = buckets["models"]["name"]

    project = {
        "name": CODEBUILD_PROJECT,
        "description": "Banking ML CI/CD build — optional Lab 4b",
        "source": {"type": "CODEPIPELINE", "buildspec": "buildspec.yml"},
        "artifacts": {"type": "CODEPIPELINE"},
        "environment": {
            "type": "LINUX_CONTAINER",
            "image": "aws/codebuild/standard:7.0",
            "computeType": "BUILD_GENERAL1_SMALL",
            "privilegedMode": False,
        },
        "serviceRole": build_role_arn,
    }

    try:
        cb.create_project(**project)
        print(f"   ✅ Created CodeBuild project: {CODEBUILD_PROJECT}")
    except cb.exceptions.ResourceAlreadyExistsException:
        cb.update_project(**project)
        print(f"   ✅ Updated CodeBuild project: {CODEBUILD_PROJECT}")

    write_json(
        CONFIG_DIR / "codebuild.json",
        {
            "project_name": CODEBUILD_PROJECT,
            "service_role_arn": build_role_arn,
            "artifact_bucket": artifact_bucket,
        },
    )
    print("✅ CodeBuild ready")


if __name__ == "__main__":
    main()
