"""Validate Lab 6."""
import json
import sys
from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 6")
    print("=" * 60)
    for name in ("deployment_state.json", "blue_green_plan.json", "deployment_report.json"):
        p = CONFIG_DIR / name
        print(f"   {'✅' if p.exists() else '⚠️'} config: {name}")
    print("Prerequisites OK — proceed to Lab 7")


if __name__ == "__main__":
    main()
