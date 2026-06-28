"""Paths for optional Lab 4b outputs."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
WORKSPACE = REPO_ROOT / "workspace" / "optional-lab4b"
LAB1_CONFIG = REPO_ROOT / "workspace" / "lab1" / "config"
CONFIG_DIR = WORKSPACE / "config"
LOGS_DIR = WORKSPACE / "logs"

REGION = "us-west-2"
PIPELINE_NAME_PREFIX = "banking-ml-cicd-lab4b"
CODEBUILD_PROJECT = "banking-ml-cicd-build-lab4b"


def ensure_workspace():
    for path in (CONFIG_DIR, LOGS_DIR):
        path.mkdir(parents=True, exist_ok=True)
