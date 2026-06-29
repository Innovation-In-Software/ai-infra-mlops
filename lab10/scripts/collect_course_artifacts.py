"""Collect artifacts from Labs 1-9 workspaces and verify key AWS resources."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION

from lab_paths import CONFIG_DIR, ensure_workspace, lab_workspace


def main():
    ensure_workspace()
    print("📦 Course Artifact Collection")
    print("=" * 60)
    manifest = {"timestamp": datetime.now(timezone.utc).isoformat(), "labs": {}, "aws": {}}

    for n in range(1, 10):
        ws = lab_workspace(n)
        manifest["labs"][f"lab{n}"] = {
            "exists": ws.exists(),
            "has_config": (ws / "config").exists(),
            "has_results": (ws / "results").exists() or (ws / "artifacts").exists(),
        }
        if ws.exists():
            print(f"   ✅ Lab {n}: workspace present")

    try:
        ecr = boto3.client("ecr", region_name=REGION)
        repos = ecr.describe_repositories(repositoryNames=["banking-ml-inference"])
        manifest["aws"]["ecr"] = {"repository": "banking-ml-inference", "exists": bool(repos.get("repositories"))}
        print("   ✅ AWS: ECR repository banking-ml-inference")
    except Exception as exc:
        manifest["aws"]["ecr"] = {"exists": False, "error": str(exc)}
        print(f"   ⚠️ AWS ECR check: {exc}")

    try:
        sm = boto3.client("sagemaker", region_name=REGION)
        endpoints = [e["EndpointName"] for e in sm.list_endpoints(MaxResults=20).get("Endpoints", [])]
        banking = [e for e in endpoints if e.startswith("banking-endpoint")]
        manifest["aws"]["sagemaker_endpoints"] = banking
        print(f"   ✅ AWS: {len(banking)} banking endpoint(s)")
    except Exception as exc:
        manifest["aws"]["sagemaker_endpoints"] = []
        print(f"   ⚠️ AWS SageMaker check: {exc}")

    with open(CONFIG_DIR / "artifact_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("✅ Artifact manifest saved")


if __name__ == "__main__":
    main()
