"""Build pipeline definition JSON."""
import json
from lab_paths import CONFIG_DIR, PIPELINE_DIR, ensure_workspace


def main():
    ensure_workspace()
    definition = {
        "steps": [
            {"name": "DataValidation", "type": "ProcessingStep"},
        ],
        "note": "Live pipeline is upserted by upsert_pipeline.py (SageMaker SDK).",
    }
    with open(PIPELINE_DIR / "pipeline_definition.json", "w", encoding="utf-8") as f:
        json.dump(definition, f, indent=2)
    with open(CONFIG_DIR / "pipeline_definition.json", "w", encoding="utf-8") as f:
        json.dump(definition, f, indent=2)
    print("🔧 SageMaker Pipeline")
    print("=" * 60)
    for step in definition["steps"]:
        print(f"   ✅ {step['type']}: {step['name']}")
    print("✅ Pipeline definition saved")


if __name__ == "__main__":
    main()
