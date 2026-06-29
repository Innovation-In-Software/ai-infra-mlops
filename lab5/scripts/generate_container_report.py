"""Generate container compliance report from ECR scan results."""

import json
from datetime import datetime, timezone

from lab_paths import CONFIG_DIR, VALIDATION_DIR, ensure_workspace


def main():
    ensure_workspace()

    ecr_cfg = {}
    ecr_path = CONFIG_DIR / "ecr_config.json"
    if ecr_path.exists():
        with open(ecr_path, encoding="utf-8") as f:
            ecr_cfg = json.load(f)

    scan = {}
    scan_path = CONFIG_DIR / "scan_report.json"
    if scan_path.exists():
        with open(scan_path, encoding="utf-8") as f:
            scan = json.load(f)

    scan_status = scan.get("status", "UNKNOWN")
    compliance = "PASS" if scan_status == "PASS" else "REVIEW" if scan_status == "REVIEW" else "PENDING"

    manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "image": f"{ecr_cfg.get('repository', 'banking-ml-inference')}:latest",
        "image_uri": f"{ecr_cfg.get('uri', '')}:latest" if ecr_cfg.get("uri") else None,
        "scan_source": scan.get("source", "ecr"),
        "critical": scan.get("critical", 0),
        "high": scan.get("high", 0),
        "scan_status": scan.get("scan_status", scan_status),
        "compliance": compliance,
    }

    manifest_path = VALIDATION_DIR / "container_deployment_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    with open(CONFIG_DIR / "container_compliance_report.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("✅ Container compliance report generated")
    print(f"   Manifest: validation/{manifest_path.name}")
    print(f"   Compliance: {compliance} (critical={manifest['critical']}, high={manifest['high']})")


if __name__ == "__main__":
    main()
