"""Executive summary markdown."""
from datetime import datetime, timezone
from lab_paths import RESULTS_DIR, ensure_workspace


def main():
    ensure_workspace()
    text = f"""# Banking MLOps — Executive Summary
## Course: ai-mlops-2026-jun30
Generated: {datetime.now(timezone.utc).isoformat()}

All core MLOps layers implemented across Labs 1-9 on AWS (us-west-2).
"""
    path = RESULTS_DIR / "executive_summary.md"
    path.write_text(text, encoding="utf-8")
    print("✅ Executive summary generated")


if __name__ == "__main__":
    main()
