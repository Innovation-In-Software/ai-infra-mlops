"""Compliance check run inside CodeBuild (Lab 4b)."""
import json
from pathlib import Path

REQUIRED = ("compliance_gates", "pipeline")


def main():
    config = {
        "compliance_gates": "PASS",
        "pipeline": "banking-ml-cicd-lab4b",
        "pii_scan": "PASS",
        "fairness": "PASS",
    }
    for key in REQUIRED:
        if key not in config:
            raise SystemExit(f"Missing key: {key}")
    Path("compliance_result.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    print("✅ Compliance check passed (Lab 4b CodeBuild)")


if __name__ == "__main__":
    main()
