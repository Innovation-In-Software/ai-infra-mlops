"""Paths for Lab 9."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
WORKSPACE = REPO_ROOT / "workspace" / "lab9"
LAB3 = REPO_ROOT / "workspace" / "lab3"
LAB5 = REPO_ROOT / "workspace" / "lab5"
CONFIG_DIR = WORKSPACE / "config"
DATA_DIR = WORKSPACE / "data"
MODELS_DIR = WORKSPACE / "models"
RESULTS_DIR = WORKSPACE / "results"
LOGS_DIR = WORKSPACE / "logs"


def ensure_workspace():
    for path in (CONFIG_DIR, DATA_DIR, MODELS_DIR, RESULTS_DIR, LOGS_DIR):
        path.mkdir(parents=True, exist_ok=True)
