"""Collect artifacts from Labs 1-9 workspaces."""
import json
from datetime import datetime, timezone

from lab_paths import CONFIG_DIR, REPO_ROOT, ensure_workspace, lab_workspace


def main():
    ensure_workspace()
    print("📦 Course Artifact Collection")
    print("=" * 60)
    manifest = {"timestamp": datetime.now(timezone.utc).isoformat(), "labs": {}}
    for n in range(1, 10):
        ws = lab_workspace(n)
        manifest["labs"][f"lab{n}"] = {
            "exists": ws.exists(),
            "has_config": (ws / "config").exists(),
            "has_results": (ws / "results").exists() or (ws / "artifacts").exists(),
        }
        if ws.exists():
            print(f"   ✅ Lab {n}: workspace present")
    with open(CONFIG_DIR / "artifact_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("✅ Artifact manifest saved")


if __name__ == "__main__":
    main()
