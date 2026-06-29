"""Generate deployment compliance report from real AWS configs."""
import json
from datetime import datetime, timezone

from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    ensure_workspace()
    staging = {}
    production = {}
    test = {}
    for name, var in [
        ("staging_deployment.json", "staging"),
        ("production_deployment.json", "production"),
        ("test_staging.json", "test"),
    ]:
        path = CONFIG_DIR / name
        if path.exists():
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if var == "staging":
                staging = data
            elif var == "production":
                production = data
            else:
                test = data

    zero_downtime = bool(
        production.get("endpoint_status") == "InService"
        and staging.get("endpoint_status") == "InService"
    )
    compliant = (
        staging.get("endpoint_status") == "InService"
        and production.get("endpoint_status") == "InService"
        and test.get("health") == "PASS"
        and not staging.get("dry_run")
        and not production.get("dry_run")
    )

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "COMPLIANT" if compliant else "REVIEW",
        "zero_downtime": zero_downtime,
        "staging_endpoint": staging.get("endpoint"),
        "production_endpoint": production.get("endpoint"),
        "staging_test_latency_ms": test.get("latency_ms"),
        "source": "aws",
    }
    with open(CONFIG_DIR / "deployment_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("✅ Deployment report: config/deployment_report.json")
    print(f"   Status: {report['status']}")
    print(f"   Zero-downtime staging+prod: {zero_downtime}")


if __name__ == "__main__":
    main()
