"""Paths for Lab 10."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
WORKSPACE = REPO_ROOT / "workspace" / "lab10"
CONFIG_DIR = WORKSPACE / "config"
RESULTS_DIR = WORKSPACE / "results"


def ensure_workspace():
    for path in (CONFIG_DIR, RESULTS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def lab_workspace(n: int) -> Path:
    return REPO_ROOT / "workspace" / f"lab{n}"
