"""Remove --dry-run from participant STEPS.md (live training default)."""
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def main():
    for path in sorted(REPO.glob("lab*/STEPS.md")):
        text = path.read_text(encoding="utf-8")
        orig = text
        text = text.replace(" --dry-run", "")
        text = text.replace("(dry-run)", "")
        text = text.replace("[dry-run] ", "")
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print(f"Updated {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
