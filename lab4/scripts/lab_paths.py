"""Paths for Lab 4 under workspace/lab4/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
WORKSPACE = REPO_ROOT / "workspace" / "lab4"
LAB1 = REPO_ROOT / "workspace" / "lab1" / "config"
LAB3 = REPO_ROOT / "workspace" / "lab3"
CONFIG_DIR = WORKSPACE / "config"
MODELS_DIR = WORKSPACE / "models"
RESULTS_DIR = WORKSPACE / "results"
ARTIFACTS_DIR = WORKSPACE / "artifacts"
LOGS_DIR = WORKSPACE / "logs"


def ensure_workspace():
    for path in (CONFIG_DIR, MODELS_DIR, RESULTS_DIR, ARTIFACTS_DIR, LOGS_DIR):
        path.mkdir(parents=True, exist_ok=True)
