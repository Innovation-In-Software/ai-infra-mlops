"""Run Lab 5 container workflow (live ECR + Docker)."""
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


def run_lab5():
    print("Lab 5 — Secure Containerization (LIVE)")
    print("=" * 60)
    prep_main()
    sys.argv = [""]
    test_main()
    sys.argv = [""]  # live ECR
    ecr_main()
    build = ROOT / "scripts" / "build_container.sh"
    if build.exists():
        print("\n▶ Docker build")
        subprocess.run(["bash", str(build)], cwd=str(REPO), check=False)
    scan_main()
    report_main()
    print("\nLab 5 complete.")


if __name__ == "__main__":
    run_lab5()
