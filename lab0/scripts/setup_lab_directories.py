"""Create student lab workspace directory structure."""
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent


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
        "lab0": "lab0",
        "lab1": "lab1",
        "lab2": "lab2",
        "lab3": "lab3",
        "lab4": "lab4",
        "lab5": "lab5",
        "lab6": "lab6",
        "lab7": "lab7",
        "lab8": "lab8",
        "lab9": "lab9",
        "lab10": "lab10",
    }

    course_mapping = {
        **mapping,
        "note": "Lab folders in this repo (lab0, lab1, …) as they are published.",
    }

    mapping_path = target / "config" / "labs_mapping.json"
    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "workspace": str(target),
                "course_root": str(REPO_ROOT),
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
