"""Paths for Lab 3 outputs under workspace/lab3/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
WORKSPACE = REPO_ROOT / "workspace" / "lab3"
LAB2 = REPO_ROOT / "workspace" / "lab2"
LAB1_CONFIG = REPO_ROOT / "workspace" / "lab1" / "config"
CONFIG_DIR = WORKSPACE / "config"
DATA_DIR = WORKSPACE / "data"
MODELS_DIR = WORKSPACE / "models"
RESULTS_DIR = WORKSPACE / "results"
LOGS_DIR = WORKSPACE / "logs"
VALIDATION_DIR = WORKSPACE / "validation"


def ensure_workspace():
    for path in (CONFIG_DIR, DATA_DIR, MODELS_DIR, RESULTS_DIR, LOGS_DIR, VALIDATION_DIR):
        path.mkdir(parents=True, exist_ok=True)
