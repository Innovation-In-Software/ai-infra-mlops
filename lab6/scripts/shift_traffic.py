"""Simulate traffic shift between blue and green."""
import argparse
import json

from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--steps", default="90,50,0")
    args = parser.parse_args()
    ensure_workspace()
    steps = [f"Blue {s}% / Green {100-int(s)}%" for s in args.steps.split(",")]
    for i, step in enumerate(steps, 1):
        print(f"   Step {i}: {step}")
    with open(CONFIG_DIR / "traffic_shift.json", "w", encoding="utf-8") as f:
        json.dump({"steps": steps, "dry_run": args.dry_run}, f, indent=2)
    print("✅ Traffic shift complete (simulated)")


if __name__ == "__main__":
    main()
