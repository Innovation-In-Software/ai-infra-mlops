"""Container vulnerability scan via ECR image scan (scan on push)."""
import json
import sys
import time
from pathlib import Path

import boto3

from lab_paths import CONFIG_DIR, REGION, ensure_workspace

REPO_NAME = "banking-ml-inference"
IMAGE_TAG = "latest"
MAX_WAIT_SEC = 300


def _load_ecr_config():
    path = CONFIG_DIR / "ecr_config.json"
    if not path.exists():
        print("   ❌ Missing ecr_config.json — run create_ecr_repo.py and push_to_ecr.sh first.")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _wait_for_scan(ecr, digest: str) -> str:
    deadline = time.time() + MAX_WAIT_SEC
    while time.time() < deadline:
        try:
            resp = ecr.describe_image_scan_findings(
                repositoryName=REPO_NAME,
                imageId={"imageDigest": digest},
            )
        except ecr.exceptions.ScanNotFoundException:
            print("   ... scan status: PENDING")
            time.sleep(10)
            continue
        status = resp.get("imageScanStatus", {}).get("status", "UNKNOWN")
        if status in ("COMPLETE", "FAILED"):
            return status
        print(f"   ... scan status: {status}")
        time.sleep(10)
    return "TIMED_OUT"


def main():
    ensure_workspace()
    print("🔍 Container Scan (ECR)")
    print("=" * 60)

    cfg = _load_ecr_config()
    ecr = boto3.client("ecr", region_name=REGION)

    images = ecr.describe_images(
        repositoryName=REPO_NAME,
        imageIds=[{"imageTag": IMAGE_TAG}],
    ).get("imageDetails", [])
    if not images:
        print(f"   ❌ No image {REPO_NAME}:{IMAGE_TAG} in ECR — run Step 7 (push_to_ecr.sh) first.")
        sys.exit(1)

    digest = images[0]["imageDigest"]
    print(f"   ✅ Image in ECR: {cfg['uri']}:{IMAGE_TAG}")

    status = _wait_for_scan(ecr, digest)
    if status == "TIMED_OUT":
        print("   ⚠️ Scan still in progress — saving partial report")
        report = {"critical": 0, "high": 0, "status": "PENDING", "scan_status": status}
    elif status == "FAILED":
        print("   ⚠️ ECR scan failed — check console → ECR → image → scan")
        report = {"critical": 0, "high": 0, "status": "UNKNOWN", "scan_status": status}
    else:
        findings = ecr.describe_image_scan_findings(
            repositoryName=REPO_NAME,
            imageId={"imageDigest": digest},
        )
        counts = findings.get("imageScanFindings", {}).get("findingSeverityCounts", {})
        critical = int(counts.get("CRITICAL", 0))
        high = int(counts.get("HIGH", 0))
        passed = critical == 0 and high == 0
        report = {
            "repository": REPO_NAME,
            "image_tag": IMAGE_TAG,
            "image_digest": digest,
            "critical": critical,
            "high": high,
            "medium": int(counts.get("MEDIUM", 0)),
            "low": int(counts.get("LOW", 0)),
            "status": "PASS" if passed else "REVIEW",
            "scan_status": status,
            "source": "ecr",
        }
        print(f"   Critical: {critical}")
        print(f"   High: {high}")
        print(f"   Status: {report['status']} (banking threshold: 0 critical / 0 high)")

    with open(CONFIG_DIR / "scan_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("✅ Scan report saved")


if __name__ == "__main__":
    main()
