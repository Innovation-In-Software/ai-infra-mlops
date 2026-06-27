"""Build compliance bundle zip manifest."""
import json
import zipfile
from datetime import datetime, timezone
from lab_paths import RESULTS_DIR, ensure_workspace


def main():
    ensure_workspace()
    bundle = RESULTS_DIR / "course_compliance_bundle.zip"
    with zipfile.ZipFile(bundle, "w") as zf:
        for name in ("architecture_assessment.json", "implementation_roadmap.json", "executive_summary.md"):
            p = RESULTS_DIR / name
            if p.exists():
                zf.write(p, arcname=name)
    manifest = {"bundle": str(bundle.name), "timestamp": datetime.now(timezone.utc).isoformat()}
    with open(RESULTS_DIR / "bundle_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("✅ Compliance bundle created")


if __name__ == "__main__":
    main()
