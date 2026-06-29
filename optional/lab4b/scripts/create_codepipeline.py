"""Create real CodePipeline for Lab 4b (S3 → CodeBuild)."""
import json
import sys
import time
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from scripts.course_common import account_id, write_json

from lab_paths import CODEBUILD_PROJECT, CONFIG_DIR, LAB1_CONFIG, PIPELINE_NAME_PREFIX, REGION, ensure_workspace
from iam_helpers import kms_statement

PIPELINE_ROLE = "BankingLab4bPipelineRole"


def _ensure_pipeline_role(iam, account, artifact_bucket, build_role_arn):
    trust = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "codepipeline.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    }
    statements = [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectVersion",
                    "s3:PutObject",
                    "s3:GetBucketLocation",
                    "s3:GetBucketVersioning",
                    "s3:ListBucket",
                ],
                "Resource": [
                    f"arn:aws:s3:::{artifact_bucket}",
                    f"arn:aws:s3:::{artifact_bucket}/*",
                ],
            },
            {
                "Effect": "Allow",
                "Action": ["codebuild:BatchGetBuilds", "codebuild:StartBuild"],
                "Resource": "*",
            },
            {
                "Effect": "Allow",
                "Action": "iam:PassRole",
                "Resource": build_role_arn,
            },
    ]
    kms = kms_statement()
    if kms:
        statements.append(kms)
    policy = {"Version": "2012-10-17", "Statement": statements}
    try:
        iam.create_role(
            RoleName=PIPELINE_ROLE,
            AssumeRolePolicyDocument=json.dumps(trust),
            Description="CodePipeline role for Lab 4b optional module",
        )
        print(f"   ✅ Created IAM role: {PIPELINE_ROLE}")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"   ✅ IAM role exists: {PIPELINE_ROLE}")
    iam.put_role_policy(
        RoleName=PIPELINE_ROLE,
        PolicyName="Lab4bPipelinePolicy",
        PolicyDocument=json.dumps(policy),
    )
    return f"arn:aws:iam::{account}:role/{PIPELINE_ROLE}"


def main():
    ensure_workspace()
    print("🔄 CodePipeline (Lab 4b — LIVE AWS)")
    print("=" * 60)

    for path, label in [
        (CONFIG_DIR / "pipeline_source.json", "pipeline_source.json"),
        (CONFIG_DIR / "codebuild.json", "codebuild.json"),
    ]:
        if not path.exists():
            print(f"   ❌ Missing {label} — run prior steps first.")
            sys.exit(1)

    with open(CONFIG_DIR / "pipeline_source.json", encoding="utf-8") as f:
        source = json.load(f)
    with open(CONFIG_DIR / "codebuild.json", encoding="utf-8") as f:
        build_cfg = json.load(f)
    with open(LAB1_CONFIG / "buckets.json", encoding="utf-8") as f:
        buckets = json.load(f)
    kms_path = LAB1_CONFIG / "kms_keys.json"
    if not kms_path.exists():
        print("   ❌ Missing kms_keys.json — complete Lab 1 Step 4 first.")
        sys.exit(1)
    with open(kms_path, encoding="utf-8") as f:
        kms = json.load(f)
    kms_key_arn = kms.get("s3_key_arn")
    if not kms_key_arn:
        print("   ❌ kms_keys.json missing s3_key_arn.")
        sys.exit(1)

    account = account_id()
    pipeline_name = f"{PIPELINE_NAME_PREFIX}-{account}"
    artifact_bucket = buckets["models"]["name"]
    iam = boto3.client("iam")
    cp = boto3.client("codepipeline", region_name=REGION)

    pipeline_role_arn = _ensure_pipeline_role(
        iam, account, artifact_bucket, build_cfg["service_role_arn"]
    )
    time.sleep(10)

    pipeline = {
        "name": pipeline_name,
        "roleArn": pipeline_role_arn,
        "artifactStore": {
            "type": "S3",
            "location": artifact_bucket,
            "encryptionKey": {"id": kms_key_arn, "type": "KMS"},
        },
        "stages": [
            {
                "name": "Source",
                "actions": [
                    {
                        "name": "S3Source",
                        "actionTypeId": {
                            "category": "Source",
                            "owner": "AWS",
                            "provider": "S3",
                            "version": "1",
                        },
                        "outputArtifacts": [{"name": "SourceOutput"}],
                        "configuration": {
                            "S3Bucket": source["bucket"],
                            "S3ObjectKey": source["key"],
                            "PollForSourceChanges": "false",
                        },
                    }
                ],
            },
            {
                "name": "Build",
                "actions": [
                    {
                        "name": "ComplianceBuild",
                        "actionTypeId": {
                            "category": "Build",
                            "owner": "AWS",
                            "provider": "CodeBuild",
                            "version": "1",
                        },
                        "inputArtifacts": [{"name": "SourceOutput"}],
                        "outputArtifacts": [{"name": "BuildOutput"}],
                        "configuration": {"ProjectName": CODEBUILD_PROJECT},
                    }
                ],
            },
        ],
    }

    try:
        cp.create_pipeline(pipeline=pipeline)
        print(f"   ✅ Created pipeline: {pipeline_name}")
    except cp.exceptions.PipelineNameInUseException:
        cp.update_pipeline(pipeline=pipeline)
        print(f"   ✅ Updated pipeline: {pipeline_name}")

    write_json(
        CONFIG_DIR / "codepipeline.json",
        {
            "pipeline_name": pipeline_name,
            "role_arn": pipeline_role_arn,
            "artifact_bucket": artifact_bucket,
            "stages": ["Source", "Build"],
        },
    )
    print("✅ CodePipeline visible in AWS console")


if __name__ == "__main__":
    main()
