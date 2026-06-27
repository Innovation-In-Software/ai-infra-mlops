"""Paths for Lab 1.2 outputs under workspace/lab2/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
WORKSPACE = REPO_ROOT / "workspace" / "lab2"
CONFIG_DIR = WORKSPACE / "config"
DATA_DIR = WORKSPACE / "data"
RESULTS_DIR = WORKSPACE / "results"
LOGS_DIR = WORKSPACE / "logs"
VALIDATION_DIR = WORKSPACE / "validation"
LAB1_CONFIG_DIR = REPO_ROOT / "workspace" / "lab1" / "config"


def ensure_workspace():
    for path in (
        CONFIG_DIR,
        DATA_DIR,
        RESULTS_DIR,
        LOGS_DIR,
        VALIDATION_DIR,
        WORKSPACE / "scripts",
    ):
        path.mkdir(parents=True, exist_ok=True)


def lab1_config_path(name: str) -> Path:
    """Lab 1.1 config files (buckets, IAM roles) required for Feature Store steps."""
    return LAB1_CONFIG_DIR / name
