"""Simulate a full pipeline run."""
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import write_json

from lab_paths import ARTIFACTS_DIR, ensure_workspace


def main():
    ensure_workspace()
    stages = ["Source", "Build", "Test", "Compliance", "ManualApproval", "Deploy"]
    print("   ✅ Source: PASS")
    print("   ✅ Build: PASS")
    print("   ✅ Test: PASS")
    print("   ✅ Compliance: PASS")
    print("   ⏸ Manual approval: simulated APPROVED")
    print("   ✅ Deploy: PASS (simulation)")
    write_json(
        ARTIFACTS_DIR / "pipeline_run_simulation.json",
        {"timestamp": datetime.now(timezone.utc).isoformat(), "stages": stages, "status": "SUCCEEDED"},
    )
    print("✅ Pipeline run complete (simulation)")


if __name__ == "__main__":
    main()
