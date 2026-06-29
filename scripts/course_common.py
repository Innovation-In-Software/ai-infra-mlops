"""Shared helpers for course lab scripts."""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

REGION = "us-west-2"
REPO_ROOT = Path(__file__).resolve().parents[1]
LAB1_CONFIG = REPO_ROOT / "workspace" / "lab1" / "config"


def add_dry_run_arg(parser=None):
    p = parser or argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true", help="Simulate AWS calls; write local configs only")
    return p


def account_id(dry_run=False):
    if dry_run:
        return "000000000000"
    import boto3

    return boto3.client("sts").get_caller_identity()["Account"]


def json_safe(value):
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(json_safe(data), f, indent=2)


def load_json(path: Path, label=None):
    if not path.exists():
        print(f"   ❌ Missing {label or path.name} — {path}")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_iam_role(role_key="ml_engineer"):
    roles = load_json(LAB1_CONFIG / "iam_roles.json", "iam_roles.json (Lab 1 Step 6)")
    if role_key not in roles:
        print(f"   ❌ iam_roles.json missing key: {role_key}")
        sys.exit(1)
    return roles[role_key]["arn"]


def load_buckets():
    return load_json(LAB1_CONFIG / "buckets.json", "buckets.json (Lab 1)")


def wait_for_status(describe_fn, status_key, ready_values, timeout_sec=900, poll_sec=30, label="resource"):
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        resp = describe_fn()
        status = resp.get(status_key, "UNKNOWN")
        if status in ready_values:
            return resp
        if status in ("Failed", "Stopped", "Deleted"):
            reason = resp.get("FailureReason", resp.get("StatusMessage", status))
            print(f"   ❌ {label} entered {status}: {reason}")
            sys.exit(1)
        print(f"   ... {label} status: {status}")
        time.sleep(poll_sec)
    print(f"   ❌ Timed out waiting for {label} ({timeout_sec}s)")
    sys.exit(1)


def sample_features_for_model(model_path, fill=0.1):
    """Return a feature vector matching the trained sklearn model width."""
    import joblib

    model = joblib.load(model_path)
    n = int(getattr(model, "n_features_in_", 0) or 0)
    if n <= 0:
        print(f"   ❌ Cannot determine feature count from {model_path}")
        sys.exit(1)
    return [fill] * n
