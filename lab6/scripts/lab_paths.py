"""Paths for Lab 6 under workspace/lab6/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
WORKSPACE = REPO_ROOT / "workspace" / "lab6"
LAB3 = REPO_ROOT / "workspace" / "lab3"
LAB5 = REPO_ROOT / "workspace" / "lab5"
CONFIG_DIR = WORKSPACE / "config"
ARTIFACTS_DIR = WORKSPACE / "artifacts"


def ensure_workspace():
    for path in (CONFIG_DIR, ARTIFACTS_DIR, CONFIG_DIR / "environments"):
        path.mkdir(parents=True, exist_ok=True)
