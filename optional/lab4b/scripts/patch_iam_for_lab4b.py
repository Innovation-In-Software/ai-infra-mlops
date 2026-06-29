"""Patch Lab 4b IAM roles and CodePipeline artifact store for SSE-KMS buckets."""
import json
import sys
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from iam_helpers import kms_key_arn, kms_statement
from lab_paths import CONFIG_DIR, LAB1_CONFIG, REGION, ensure_workspace

PIPELINE_ROLE = "BankingLab4bPipelineRole"
BUILD_ROLE = "BankingLab4bCodeBuildRole"


def _merge_s3_actions(doc, extra_actions):
    changed = False
    for stmt in doc.get("Statement", []):
        if stmt.get("Effect") != "Allow":
            continue
        actions = stmt.get("Action", [])
        if isinstance(actions, str):
            actions = [actions]
        if not any(a.startswith("s3:") for a in actions):
            continue
        for action in extra_actions:
            if action not in actions:
                actions.append(action)
                changed = True
        stmt["Action"] = actions
    return changed


def _patch_role(iam, role, policy_name):
    kms = kms_statement()
    if not kms:
        print("   ❌ Missing workspace/lab1/config/kms_keys.json — complete Lab 1 first.")
        sys.exit(1)

    doc = iam.get_role_policy(RoleName=role, PolicyName=policy_name)["PolicyDocument"]
    if isinstance(doc, str):
        doc = json.loads(doc)

    changed = _merge_s3_actions(doc, ["s3:GetBucketVersioning"])
    has_kms = any(
        "kms:Decrypt" in (s.get("Action") if isinstance(s.get("Action"), list) else [s.get("Action")])
        for s in doc.get("Statement", [])
    )
    if not has_kms:
        doc["Statement"].append(kms)
        changed = True

    if changed:
        iam.put_role_policy(RoleName=role, PolicyName=policy_name, PolicyDocument=json.dumps(doc))
        print(f"   ✅ Updated {role}")
    else:
        print(f"   ✅ {role} already patched")


def _patch_pipeline_encryption(cp, pipeline_name, kms_arn):
    pipeline = cp.get_pipeline(name=pipeline_name)["pipeline"]
    store = pipeline.get("artifactStore", {})
    key = store.get("encryptionKey", {})
    if key.get("id") == kms_arn and key.get("type") == "KMS":
        print(f"   ✅ Pipeline artifact store already uses KMS key")
        return
    store["encryptionKey"] = {"id": kms_arn, "type": "KMS"}
    pipeline["artifactStore"] = store
    cp.update_pipeline(pipeline=pipeline)
    print(f"   ✅ Pipeline artifact store updated with KMS key")


def main():
    ensure_workspace()
    kms_arn = kms_key_arn()
    if not kms_arn:
        print("   ❌ Missing workspace/lab1/config/kms_keys.json — complete Lab 1 first.")
        sys.exit(1)

    cfg_path = CONFIG_DIR / "codepipeline.json"
    if not cfg_path.exists():
        print("   ❌ Run create_codepipeline.py first.")
        sys.exit(1)

    with open(cfg_path, encoding="utf-8") as f:
        pipeline_name = json.load(f)["pipeline_name"]

    print("🔧 Lab 4b IAM + pipeline patch")
    print("=" * 60)

    iam = boto3.client("iam")
    _patch_role(iam, PIPELINE_ROLE, "Lab4bPipelinePolicy")
    _patch_role(iam, BUILD_ROLE, "Lab4bCodeBuildPolicy")

    cp = boto3.client("codepipeline", region_name=REGION)
    _patch_pipeline_encryption(cp, pipeline_name, kms_arn)

    print("\nWait ~30 seconds for IAM propagation, then re-run:")
    print("   python3 scripts/start_pipeline.py")


if __name__ == "__main__":
    main()
