"""Delete Lab 4b CodePipeline and CodeBuild project."""
import json
import sys

import boto3

from lab_paths import CODEBUILD_PROJECT, CONFIG_DIR, REGION


def main():
    cfg_path = CONFIG_DIR / "codepipeline.json"
    if not cfg_path.exists():
        print("No codepipeline.json — nothing to delete.")
        return

    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)

    cp = boto3.client("codepipeline", region_name=REGION)
    cb = boto3.client("codebuild", region_name=REGION)
    iam = boto3.client("iam")

    name = cfg["pipeline_name"]
    try:
        cp.delete_pipeline(name=name)
        print(f"   ✅ Deleted pipeline: {name}")
    except Exception as exc:
        print(f"   ⚠️ Pipeline delete: {exc}")

    try:
        cb.delete_project(name=CODEBUILD_PROJECT)
        print(f"   ✅ Deleted CodeBuild: {CODEBUILD_PROJECT}")
    except Exception as exc:
        print(f"   ⚠️ CodeBuild delete: {exc}")

    for role, policy in (
        ("BankingLab4bPipelineRole", "Lab4bPipelinePolicy"),
        ("BankingLab4bCodeBuildRole", "Lab4bCodeBuildPolicy"),
    ):
        try:
            iam.delete_role_policy(RoleName=role, PolicyName=policy)
        except Exception:
            pass
        try:
            iam.delete_role(RoleName=role)
            print(f"   ✅ Deleted role: {role}")
        except Exception as exc:
            print(f"   ⚠️ Role {role}: {exc}")

    print("Done. S3 source.zip and build artifacts may remain in models bucket.")


if __name__ == "__main__":
    main()
