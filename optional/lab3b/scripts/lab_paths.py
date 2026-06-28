"""Paths for optional Lab 3b outputs."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
WORKSPACE = REPO_ROOT / "workspace" / "optional-lab3b"
LAB1_CONFIG = REPO_ROOT / "workspace" / "lab1" / "config"
LAB3 = REPO_ROOT / "workspace" / "lab3"
CONFIG_DIR = WORKSPACE / "config"
LOGS_DIR = WORKSPACE / "logs"


def ensure_workspace():
    for path in (CONFIG_DIR, LOGS_DIR):
        path.mkdir(parents=True, exist_ok=True)
