"""Run Lab 8 pipeline workflow."""
import sys
from build_pipeline import main as build_main
from define_pipeline_params import main as params_main
from generate_pipeline_report import main as report_main
from monitor_pipeline import main as monitor_main
from register_model import main as register_main
from start_pipeline import main as start_main
from upsert_pipeline import main as upsert_main


def run_lab8():
    print("Lab 8 — SageMaker Pipelines")
    print("=" * 60)
    params_main()
    build_main()
    for fn in [upsert_main, start_main, monitor_main, register_main]:
        sys.argv = ["", "--dry-run"]
        print(f"\n▶ {fn.__module__}")
        fn()
    report_main()
    print("\nLab 8 complete.")


if __name__ == "__main__":
    run_lab8()
