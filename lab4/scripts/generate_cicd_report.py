"""Generate CI/CD compliance report."""
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import write_json

from lab_paths import ARTIFACTS_DIR, CONFIG_DIR, ensure_workspace


def main():
    ensure_workspace()
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pipeline": "banking-ml-cicd",
        "compliance_gates": "PASS",
        "audit_trail": "simulated",
    }
    write_json(ARTIFACTS_DIR / "cicd_compliance_report_final.json", report)
    print("✅ CI/CD compliance report generated")


if __name__ == "__main__":
    main()
