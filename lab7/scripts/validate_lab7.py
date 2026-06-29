"""Validate Lab 7."""
import json
import sys

from lab_paths import CONFIG_DIR, DATA_DIR, RESULTS_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 7")
    print("=" * 60)
    ok = True
    for p, label in [
        (DATA_DIR / "baseline_data.csv", "baseline_data.csv"),
        (DATA_DIR / "current_data.csv", "current_data.csv"),
        (CONFIG_DIR / "dashboard_config.json", "dashboard_config.json"),
        (CONFIG_DIR / "alarms.json", "alarms.json"),
        (RESULTS_DIR / "monitoring_report_final.json", "monitoring_report_final.json"),
    ]:
        if p.exists():
            print(f"   ✅ {label}")
        else:
            print(f"   ❌ Missing: {label}")
            ok = False

    dash = CONFIG_DIR / "dashboard_config.json"
    if dash.exists():
        data = json.loads(dash.read_text(encoding="utf-8"))
        if data.get("source") != "cloudwatch" and not data.get("dry_run"):
            print("   ❌ Dashboard was not created in CloudWatch")
            ok = False

    alarms = CONFIG_DIR / "alarms.json"
    if alarms.exists():
        data = json.loads(alarms.read_text(encoding="utf-8"))
        if data.get("source") != "cloudwatch" and not data.get("dry_run"):
            print("   ❌ Alarms were not created in CloudWatch")
            ok = False

    print("\n" + "=" * 60)
    if ok:
        print("Prerequisites OK — proceed to Lab 8")
    else:
        print("Complete Lab 7 steps (lab7/STEPS.md).")
        sys.exit(1)


if __name__ == "__main__":
    main()
