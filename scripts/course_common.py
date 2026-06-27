"""Shared helpers for course lab scripts."""
import argparse
import json
from pathlib import Path

import numpy as np


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
