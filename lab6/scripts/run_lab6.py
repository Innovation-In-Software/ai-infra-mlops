"""Run Lab 6 deployment workflow (dry-run)."""
import sys

from configure_blue_green import main as bg_main
from deploy_production import main as prod_main
from deploy_staging import main as staging_main
from generate_deployment_report import main as report_main
from prepare_deployment import main as prep_main
from rollback import main as rollback_main
from shift_traffic import main as shift_main
from test_deployment import main as test_main


def _dry(fn):
    sys.argv = ["", "--dry-run"]
    fn()


def run_lab6():
    print("Lab 6 — Blue-Green Deployment")
    print("=" * 60)
    prep_main()
    for name, fn in [
        ("Blue-green plan", bg_main),
        ("Staging deploy", staging_main),
        ("Test staging", test_main),
        ("Production deploy", prod_main),
        ("Traffic shift", shift_main),
        ("Rollback drill", rollback_main),
        ("Report", report_main),
    ]:
        print(f"\n▶ {name}")
        if fn in (bg_main, staging_main, prod_main, shift_main, rollback_main):
            _dry(fn)
        elif fn is test_main:
            sys.argv = ["", "--dry-run", "--environment", "staging"]
            fn()
        else:
            fn()
    print("\nLab 6 complete.")


if __name__ == "__main__":
    run_lab6()
