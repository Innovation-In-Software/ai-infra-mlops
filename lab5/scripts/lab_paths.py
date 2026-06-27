"""Paths for Lab 5 under workspace/lab5/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
WORKSPACE = REPO_ROOT / "workspace" / "lab5"
LAB3 = REPO_ROOT / "workspace" / "lab3"
CONFIG_DIR = WORKSPACE / "config"
MODELS_DIR = WORKSPACE / "models"
VALIDATION_DIR = WORKSPACE / "validation"
ARTIFACTS_DIR = WORKSPACE / "artifacts"


def ensure_workspace():
    for path in (CONFIG_DIR, MODELS_DIR, VALIDATION_DIR, ARTIFACTS_DIR):
        path.mkdir(parents=True, exist_ok=True)
