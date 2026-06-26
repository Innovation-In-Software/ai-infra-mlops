"""Create student lab workspace directory structure."""
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANKING = ROOT.parent


def default_workspace() -> Path:
    return Path.home() / "Documents" / "banking-mlops-labs"


def load_config():
    config_path = ROOT / "config" / "environment_config.json"
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def create_workspace(target: Path, per_lab_subdirs: bool = True):
    config = load_config()
    target.mkdir(parents=True, exist_ok=True)

    created = []
    for name in config["student_workspace_dirs"]:
        path = target / name
        path.mkdir(exist_ok=True)
        created.append(name)
        if per_lab_subdirs and name.startswith("lab") and name[3:].isdigit():
            for sub in ("scripts", "config", "data", "results", "logs"):
                (path / sub).mkdir(exist_ok=True)

    mapping = {
        "lab0": "Lab_0_Environment_Setup_and_Prerequisites",
        "lab1": "Lab_1.1_Secure_MLOps_Environment_Setup",
        "lab2": "Lab_1.2_Banking_Data_Management_and_PII_Protection",
        "lab3": "Lab_2.1_Model_Training_and_Fairness_Testing",
        "lab4": "Lab_3.1_CICD_Pipeline_with_Compliance_Gates",
        "lab5": "Lab_4.1_Secure_Containerization_for_Banking",
        "lab6": "Lab_5.1_Model_Deployment_with_Blue_Green",
        "lab7": "Lab_6.1_Compliance_Monitoring_and_Observability",
        "lab8": "Lab_7.1_End_to_End_SageMaker_Pipeline",
        "lab9": "Lab_8.1_Banking_Security_and_Governance_Framework",
        "lab10": "Lab_9.1_Enterprise_MLOps_Architecture",
    }

    course_mapping = {
        **mapping,
        "note": "Use labs/ folders in the ai-infra-mlops repo for course content.",
    }

    mapping_path = target / "config" / "labs_mapping.json"
    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "workspace": str(target),
                "course_root": str(BANKING),
                "mapping": course_mapping,
            },
            f,
            indent=2,
        )

    setup_info = target / "config" / "setup_info.txt"
    setup_info.write_text(
        f"Banking MLOps workspace created at {datetime.now(timezone.utc).isoformat()}\n"
        f"Region: {config['default_region']}\n",
        encoding="utf-8",
    )

    log_path = target / "lab0" / "logs" / "setup.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        f"Lab 0 - Started at {datetime.now(timezone.utc).isoformat()}\n",
        encoding="utf-8",
    )

    return created, mapping_path


def main():
    parser = argparse.ArgumentParser(description="Create banking MLOps student workspace")
    parser.add_argument("--target", type=Path, default=None, help="Workspace root path")
    args = parser.parse_args()

    target = args.target or default_workspace()
    print("Creating Banking MLOps Lab Directory Structure")
    print("=" * 60)
    print(f"   Target: {target}")

    created, mapping_path = create_workspace(target)
    print(f"   Directories created: {len(created)}")
    print(f"   Mapping file: {mapping_path}")
    print("\nDirectory structure ready.")


if __name__ == "__main__":
    main()
