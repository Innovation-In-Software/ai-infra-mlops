"""Run Lab 5 container workflow."""
from create_ecr_repo import main as ecr_main
from generate_container_report import main as report_main
from prepare_artifacts import main as prep_main
from scan_container import main as scan_main
from test_container import main as test_main
import sys


def run_lab5():
    print("Lab 5 — Secure Containerization")
    print("=" * 60)
    sys.argv = ["", "--dry-run"]
    for name, fn in [
        ("Prepare artifacts", prep_main),
        ("Test container", lambda: test_main()),
        ("ECR repo", ecr_main),
        ("Scan", scan_main),
        ("Report", report_main),
    ]:
        print(f"\n▶ {name}")
        fn()
    print("\nLab 5 complete. Run build_container.sh and push_to_ecr.sh on EC2 with Docker.")


if __name__ == "__main__":
    run_lab5()
