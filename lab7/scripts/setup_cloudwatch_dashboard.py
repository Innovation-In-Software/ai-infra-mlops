"""CloudWatch dashboard config."""
import argparse
import json
from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()
    cfg = {"dashboard": "Banking-MLOps-Model-Monitor", "widgets": ["invocations", "latency", "errors", "drift"]}
    with open(CONFIG_DIR / "dashboard_config.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print("📊 CloudWatch Dashboard")
    print("=" * 60)
    print(f"   ✅ Dashboard: {cfg['dashboard']}")
    print("✅ Dashboard configuration saved")


if __name__ == "__main__":
    main()
