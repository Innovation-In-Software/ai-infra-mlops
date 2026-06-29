"""IAM least-privilege review (live AWS)."""
import json
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import write_json

from lab_paths import CONFIG_DIR, ensure_workspace

ROLE_NAMES = [
    "BankingDataScientistRole",
    "BankingMLEngineerRole",
    "BankingComplianceOfficerRole",
]


def main():
    ensure_workspace()
    iam = boto3.client("iam")
    reviewed = []
    over_privileged = 0

    for role_name in ROLE_NAMES:
        entry = {"role_name": role_name, "inline_policies": [], "status": "OK"}
        try:
            iam.get_role(RoleName=role_name)
        except ClientError:
            entry["status"] = "MISSING"
            over_privileged += 1
            reviewed.append(entry)
            continue

        inline = iam.list_role_policies(RoleName=role_name).get("PolicyNames", [])
        entry["inline_policies"] = inline
        for policy_name in inline:
            doc = iam.get_role_policy(RoleName=role_name, PolicyName=policy_name)
            statements = doc.get("PolicyDocument", {}).get("Statement", [])
            for stmt in statements:
                actions = stmt.get("Action", [])
                if isinstance(actions, str):
                    actions = [actions]
                if any(a in ("*", "iam:*", "s3:*") or a.endswith(":*") for a in actions):
                    entry["status"] = "REVIEW"
                    over_privileged += 1
        reviewed.append(entry)

    status = "COMPLIANT" if over_privileged == 0 else "REVIEW"
    report = {
        "roles_reviewed": len(reviewed),
        "over_privileged": over_privileged,
        "roles": reviewed,
        "status": status,
        "source": "aws-iam",
    }
    write_json(CONFIG_DIR / "iam_review.json", report)
    print("🔑 IAM Review")
    print("=" * 60)
    print(f"   Roles reviewed: {len(reviewed)}")
    print(f"   Status: {status}")
    print("✅ IAM review report saved")


if __name__ == "__main__":
    main()
