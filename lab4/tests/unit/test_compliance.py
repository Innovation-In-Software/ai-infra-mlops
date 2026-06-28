"""Prerequisite and compliance checks for the CI/CD pipeline lab."""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
LAB1_CONFIG = REPO / "workspace" / "lab1" / "config"
LAB2_CONFIG = REPO / "workspace" / "lab2" / "config"
LAB3 = REPO / "workspace" / "lab3"


def test_lab1_buckets_config():
    assert (LAB1_CONFIG / "buckets.json").exists()


def test_lab1_iam_roles_config():
    assert (LAB1_CONFIG / "iam_roles.json").exists()


def test_lab2_pii_report():
    assert (LAB2_CONFIG / "pii_report.json").exists()


def test_lab3_best_model():
    assert (LAB3 / "models" / "best_model.pkl").exists()


def test_lab3_fairness_pass():
    report_path = LAB3 / "results" / "fairness_report.json"
    assert report_path.exists()
    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data.get("status") == "PASS"
