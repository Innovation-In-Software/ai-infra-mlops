"""Configure CodePipeline (classroom simulation)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import account_id, write_json

from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("🔄 CodePipeline Setup")
    print("=" * 60)
    acct = account_id(dry_run=True)
    config = {
        "pipeline": f"banking-ml-cicd-{acct}",
        "region": "us-west-2",
        "stages": ["Source", "Build", "Test", "Compliance", "Deploy"],
        "manual_approval_gate": True,
    }
    write_json(CONFIG_DIR / "codepipeline_config.json", config)
    print(f"   ✅ Pipeline: {config['pipeline']}")
    print("   ✅ Stages: Source → Build → Test → Compliance → Deploy")
    print("   ✅ Manual approval gate: enabled")
    print("✅ Pipeline configuration saved")


if __name__ == "__main__":
    main()
