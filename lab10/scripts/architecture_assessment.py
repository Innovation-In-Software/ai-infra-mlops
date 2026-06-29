"""Enterprise architecture assessment."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION, write_json

from lab_paths import CONFIG_DIR, RESULTS_DIR, ensure_workspace, lab_workspace

# Course layer → lab workspace that proves the layer
LAYER_LABS = {
    "security": 1,
    "data": 2,
    "training": 3,
    "pipeline": 8,
    "deployment": 6,
    "monitoring": 7,
    "governance": 9,
}


def _layer_complete(lab_num: int) -> bool:
    ws = lab_workspace(lab_num)
    if not ws.exists():
        return False
    config = ws / "config"
    if not config.exists():
        return False
    # Minimum evidence per layer
    markers = {
        1: ["buckets.json", "iam_roles.json"],
        2: ["feature_store_config.json"],
        3: ["training_results.json"],
        6: ["staging_deployment.json", "production_deployment.json"],
        7: ["dashboard_config.json", "alarms.json"],
        8: ["pipeline_registration.json", "model_registry.json", "pipeline_execution.json"],
        9: ["iam_review.json", "encryption_audit.json"],
    }
    for fname in markers.get(lab_num, []):
        if not (config / fname).exists():
            return False
    return True


def _aws_resource_check():
    """Optional live checks for key resources."""
    try:
        import boto3

        sm = boto3.client("sagemaker", region_name=REGION)
        endpoints = sm.list_endpoints(MaxResults=5).get("Endpoints", [])
        banking = [e for e in endpoints if e["EndpointName"].startswith("banking-endpoint")]
        return {"banking_endpoints": len(banking), "checked": True}
    except Exception as exc:
        return {"checked": False, "error": str(exc)}


def main():
    ensure_workspace()
    scores = {}
    for layer, lab_num in LAYER_LABS.items():
        scores[layer] = "COMPLETE" if _layer_complete(lab_num) else "MISSING"

    complete = sum(1 for v in scores.values() if v == "COMPLETE")
    score = complete / len(scores) * 100
    aws_check = _aws_resource_check()

    report = {
        "layers": scores,
        "score": round(score, 1),
        "layer_labs": LAYER_LABS,
        "aws_check": aws_check,
    }
    write_json(RESULTS_DIR / "architecture_assessment.json", report)

    print("🏗️ Enterprise Architecture Assessment")
    print("=" * 60)
    for layer in LAYER_LABS:
        mark = "✅" if scores[layer] == "COMPLETE" else "❌"
        print(f"   {layer} layer (lab{LAYER_LABS[layer]}): {mark} {scores[layer]}")
    if aws_check.get("checked"):
        print(f"   AWS SageMaker banking endpoints: {aws_check.get('banking_endpoints', 0)}")
    print(f"   Score: {report['score']:.0f}/100")


if __name__ == "__main__":
    main()
