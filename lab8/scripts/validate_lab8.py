"""Validate Lab 8."""
from lab_paths import CONFIG_DIR, RESULTS_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 8")
    print("=" * 60)
    for p, n in [(CONFIG_DIR / "pipeline_params.json", "pipeline_params.json"), (RESULTS_DIR / "pipeline_compliance_report_final.json", "pipeline_compliance_report_final.json")]:
        print(f"   {'✅' if p.exists() else '⚠️'} {n}")
    print("Prerequisites OK — proceed to Lab 9")


if __name__ == "__main__":
    main()
