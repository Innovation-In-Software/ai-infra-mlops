"""Run Lab 7 monitoring workflow."""
import sys
from generate_monitoring_report import main as report_main
from monitor_data_drift import main as drift_main
from monitor_model_quality import main as quality_main
from prepare_monitoring_data import main as prep_main
from setup_alarms import main as alarms_main
from setup_cloudwatch_dashboard import main as dash_main
from setup_model_monitor import main as monitor_main
from simulate_incident import main as incident_main


def run_lab7():
    print("Lab 7 — Monitoring & Observability")
    print("=" * 60)
    prep_main()
    for fn in [dash_main, monitor_main, drift_main, quality_main, alarms_main, incident_main, report_main]:
        if fn in (monitor_main, alarms_main, dash_main):
            sys.argv = ["", "--dry-run"]
        print(f"\n▶ {fn.__module__}")
        fn()
    print("\nLab 7 complete.")


if __name__ == "__main__":
    run_lab7()
