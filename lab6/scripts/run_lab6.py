"""Run Lab 6 deployment workflow (live AWS config — no dry-run)."""
import sys

from configure_blue_green import main as bg_main
from deploy_production import main as prod_main
from deploy_staging import main as staging_main
from generate_deployment_report import main as report_main
from prepare_deployment import main as prep_main
from rollback import main as rollback_main
from shift_traffic import main as shift_main
from test_deployment import main as test_main


def _live(fn, extra=None):
    sys.argv = [""] + (extra or [])
    fn()


def run_lab6():
    print("Lab 6 — Blue-Green Deployment (LIVE)")
    print("=" * 60)
    prep_main()
    for name, fn, extra in [
        ("Blue-green plan", bg_main, None),
        ("Staging deploy", staging_main, None),
        ("Test staging", test_main, ["--environment", "staging"]),
        ("Production deploy", prod_main, None),
        ("Traffic shift", shift_main, ["--steps", "90,50,0"]),
        ("Rollback drill", rollback_main, ["--endpoint-name", "banking-endpoint-prod-demo"]),
        ("Report", report_main, None),
    ]:
        print(f"\n▶ {name}")
        if fn is report_main:
            fn()
        else:
            _live(fn, extra)
    print("\nLab 6 complete.")


if __name__ == "__main__":
    run_lab6()
