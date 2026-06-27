"""Model approval workflow."""
import argparse
import json
from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()
    wf = {"model": "banking-risk-xgboost-v1", "fairness": "APPROVED", "security": "APPROVED", "status": "PendingComplianceOfficer", "dry_run": args.dry_run}
    with open(CONFIG_DIR / "approval_workflow.json", "w", encoding="utf-8") as f:
        json.dump(wf, f, indent=2)
    print("📋 Model Approval — workflow state saved")


if __name__ == "__main__":
    main()
