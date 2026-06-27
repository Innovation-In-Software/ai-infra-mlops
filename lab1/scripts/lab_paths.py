"""Paths for Lab 1 outputs under workspace/lab1/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
WORKSPACE = REPO_ROOT / "workspace" / "lab1"
CONFIG_DIR = WORKSPACE / "config"
DATA_DIR = WORKSPACE / "data"
RESULTS_DIR = WORKSPACE / "results"
LOGS_DIR = WORKSPACE / "logs"


def ensure_workspace():
    for path in (CONFIG_DIR, DATA_DIR, RESULTS_DIR, LOGS_DIR, WORKSPACE / "scripts"):
        path.mkdir(parents=True, exist_ok=True)
