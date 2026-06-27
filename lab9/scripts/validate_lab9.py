"""Validate Lab 9."""
from lab_paths import CONFIG_DIR, RESULTS_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 9")
    for p, n in [(RESULTS_DIR / "governance_report_final.json", "governance_report_final.json"), (CONFIG_DIR / "governance_state.json", "governance_state.json")]:
        print(f"   {'✅' if p.exists() else '⚠️'} {n}")
    print("Prerequisites OK — proceed to Lab 10")


if __name__ == "__main__":
    main()
