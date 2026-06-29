"""Run Lab 8 pipeline workflow (live account IDs — no dry-run)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import refresh_banking_iam

from build_pipeline import main as build_main
from define_pipeline_params import main as params_main
from generate_pipeline_report import main as report_main
from monitor_pipeline import main as monitor_main
from register_model import main as register_main
from start_pipeline import main as start_main
from upsert_pipeline import main as upsert_main


def run_lab8():
    print("Lab 8 — SageMaker Pipelines (LIVE)")
    print("=" * 60)
    refresh_banking_iam()
    params_main()
    build_main()
    for fn in [upsert_main, start_main, monitor_main, register_main]:
        sys.argv = [""]
        print(f"\n▶ {fn.__module__}")
        fn()
    report_main()
    print("\nLab 8 complete.")


if __name__ == "__main__":
    run_lab8()
