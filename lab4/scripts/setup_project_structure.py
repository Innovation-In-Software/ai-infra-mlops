"""Create CI/CD project directories."""
from pathlib import Path

from lab_paths import ROOT, ensure_workspace


def main():
    ensure_workspace()
    for sub in ("src/compliance", "tests/unit", "tests/reports", "buildspecs"):
        (ROOT / sub).mkdir(parents=True, exist_ok=True)
    print("   ✅ Created: src/")
    print("   ✅ Created: tests/unit/")
    print("   ✅ Created: buildspecs/")
    print("✅ Banking ML CI/CD project structure ready")


if __name__ == "__main__":
    main()
