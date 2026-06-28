"""Run Lab 5 container workflow (Docker + ECR)."""
import subprocess
import sys
from pathlib import Path

from create_ecr_repo import main as ecr_main
from generate_container_report import main as report_main
from prepare_artifacts import main as prep_main
from scan_container import main as scan_main
from test_container import main as test_main

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent


def _bash(script_name: str) -> None:
    script = ROOT / "scripts" / script_name
    print(f"\n▶ {script_name}")
    subprocess.run(["bash", str(script)], cwd=str(REPO), check=True)


def run_lab5():
    print("Lab 5 — Secure Containerization")
    print("=" * 60)
    prep_main()
    _bash("build_container.sh")
    test_main()
    sys.argv = [""]
    ecr_main()
    _bash("push_to_ecr.sh")
    scan_main()
    report_main()
    print("\nLab 5 complete — run validate_lab5.py to confirm.")


if __name__ == "__main__":
    run_lab5()
