"""Paths for Lab 8."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
WORKSPACE = REPO_ROOT / "workspace" / "lab8"
LAB2 = REPO_ROOT / "workspace" / "lab2"
CONFIG_DIR = WORKSPACE / "config"
DATA_DIR = WORKSPACE / "data"
RESULTS_DIR = WORKSPACE / "results"
PIPELINE_DIR = ROOT / "pipeline"


def ensure_workspace():
    for path in (CONFIG_DIR, DATA_DIR, RESULTS_DIR, PIPELINE_DIR):
        path.mkdir(parents=True, exist_ok=True)
