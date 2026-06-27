"""Banking data drift detection and monitoring setup."""
import json
from datetime import datetime, timezone

import boto3
import numpy as np
import pandas as pd
from scipy import stats
from lab_paths import CONFIG_DIR, DATA_DIR, LAB1_CONFIG_DIR, RESULTS_DIR, ensure_workspace


def _json_safe(value):
    """Convert numpy/pandas scalars to native Python types for json.dump."""
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value


class BankingDataDriftDetector:
    """Banking-specific data drift detection."""

    def __init__(self):
        self.region = "us-west-2"
        self.account_id = boto3.client("sts").get_caller_identity()["Account"]
        self.cloudwatch = boto3.client("cloudwatch", region_name=self.region)
        self.s3 = boto3.client("s3", region_name=self.region)

        self.drift_thresholds = {
            "numerical_ks": 0.1,
            "categorical_chi2": 0.1,
            "p_value_threshold": 0.05,
        }

    def calculate_numerical_drift(self, baseline, current, feature):
        baseline_clean = baseline[feature].dropna()
        current_clean = current[feature].dropna()

        if len(baseline_clean) == 0 or len(current_clean) == 0:
            return None

        ks_statistic, p_value = stats.ks_2samp(baseline_clean, current_clean)

        stats_comparison = {
            "baseline_mean": float(baseline_clean.mean()),
            "current_mean": float(current_clean.mean()),
            "baseline_std": float(baseline_clean.std()),
            "current_std": float(current_clean.std()),
            "baseline_median": float(baseline_clean.median()),
            "current_median": float(current_clean.median()),
            "baseline_min": float(baseline_clean.min()),
            "current_min": float(current_clean.min()),
            "baseline_max": float(baseline_clean.max()),
            "current_max": float(current_clean.max()),
        }

        return {
            "feature": feature,
            "type": "numerical",
            "ks_statistic": float(ks_statistic),
            "p_value": float(p_value),
            "drift_detected": bool(p_value < self.drift_thresholds["p_value_threshold"]),
            "drift_severity": "HIGH"
            if ks_statistic > 0.2
            else "MEDIUM"
            if ks_statistic > 0.1
            else "LOW",
            "statistics": stats_comparison,
        }

    def calculate_categorical_drift(self, baseline, current, feature):
        baseline_counts = baseline[feature].value_counts(normalize=True)
        current_counts = current[feature].value_counts(normalize=True)
        categories = set(baseline_counts.index) | set(current_counts.index)

        baseline_probs = [baseline_counts.get(cat, 0) for cat in categories]
        current_probs = [current_counts.get(cat, 0) for cat in categories]
        max_diff = max(abs(b - c) for b, c in zip(baseline_probs, current_probs))

        return {
            "feature": feature,
            "type": "categorical",
            "max_probability_diff": float(max_diff),
            "drift_detected": bool(max_diff > 0.1),
            "drift_severity": "HIGH"
            if max_diff > 0.2
            else "MEDIUM"
            if max_diff > 0.1
            else "LOW",
            "baseline_distribution": {str(k): float(v) for k, v in baseline_counts.items()},
            "current_distribution": {str(k): float(v) for k, v in current_counts.items()},
        }

    def detect_drift(self, baseline_data, current_data):
        print("\n🔍 Detecting Data Drift...")
        print("=" * 60)

        drift_report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_features": 0,
            "features_with_drift": 0,
            "drift_details": {},
        }

        common_columns = set(baseline_data.columns) & set(current_data.columns)

        for feature in common_columns:
            if feature in ["transaction_id", "customer_id"]:
                continue

            drift_result = None
            if baseline_data[feature].dtype in ["float64", "int64"]:
                drift_result = self.calculate_numerical_drift(baseline_data, current_data, feature)
            else:
                drift_result = self.calculate_categorical_drift(baseline_data, current_data, feature)

            if drift_result:
                drift_report["drift_details"][feature] = drift_result
                drift_report["total_features"] += 1

                if drift_result["drift_detected"]:
                    drift_report["features_with_drift"] += 1
                    print(f"   ⚠️ {feature}: {drift_result['drift_severity']} drift detected")
                else:
                    print(f"   ✅ {feature}: No significant drift")

        drift_report["summary"] = {
            "total_features_analyzed": drift_report["total_features"],
            "features_with_drift": drift_report["features_with_drift"],
            "drift_percentage": (
                drift_report["features_with_drift"]
                / max(1, drift_report["total_features"])
                * 100
            ),
            "status": "WARNING" if drift_report["features_with_drift"] > 0 else "NORMAL",
        }

        with open(CONFIG_DIR / "drift_report.json", "w", encoding="utf-8") as f:
            json.dump(_json_safe(drift_report), f, indent=2)
        print("\n" + "=" * 60)
        print("📊 Drift Detection Summary:")
        print(f"   Total Features: {drift_report['summary']['total_features_analyzed']}")
        print(f"   Features with Drift: {drift_report['summary']['features_with_drift']}")
        print(f"   Drift Percentage: {drift_report['summary']['drift_percentage']:.1f}%")
        print(f"   Status: {drift_report['summary']['status']}")

        return drift_report

    def create_drift_alarms(self):
        print("\n📋 Creating Drift Alarms...")
        try:
            self.cloudwatch.put_metric_alarm(
                AlarmName="BankingDataDriftAlarm",
                AlarmDescription="Alert when data drift exceeds 10%",
                MetricName="DriftPercentage",
                Namespace="Banking/MLOps",
                Statistic="Average",
                Period=3600,
                EvaluationPeriods=3,
                Threshold=10.0,
                ComparisonOperator="GreaterThanThreshold",
                TreatMissingData="missing",
                AlarmActions=[f"arn:aws:sns:us-west-2:{self.account_id}:banking-drift-alerts"],
            )
            print("   ✅ Drift alarm created")
        except Exception as e:
            print(f"   ⚠️ Could not create alarm (SNS topic may not exist): {str(e)}")

    def setup_drift_monitoring(self, baseline_data):
        print("\n📋 Setting Up Drift Monitoring")
        print("=" * 60)

        baseline_path = DATA_DIR / f"baseline_data_{datetime.now(timezone.utc).strftime('%Y%m%d')}.csv"
        baseline_data.to_csv(baseline_path, index=False)
        print(f"   ✅ Baseline saved: {baseline_path}")

        s3_key = f"baselines/baseline_{datetime.now(timezone.utc).strftime('%Y%m%d')}.csv"
        self.s3.upload_file(
            str(baseline_path),
            f"bank-mlops-{self.account_id}-monitoring",
            s3_key,
        )
        print(f"   ✅ Baseline uploaded to S3: {s3_key}")

        self.create_drift_alarms()

        print("\n" + "=" * 60)
        print("✅ Drift Monitoring Setup Complete!")
        print(f"   Baseline: {baseline_path}")
        print(f"   Config: {CONFIG_DIR / 'drift_report.json'}")


def main_drift_detection():
    ensure_workspace()
    print("🔍 Banking Data Drift Detection")
    print("=" * 60)

    print("\n📂 Loading datasets...")
    baseline_data = pd.read_csv(DATA_DIR / "engineered_banking_data.csv")
    print(f"   Baseline: {len(baseline_data)} records")

    current_data = baseline_data.copy()

    for col in ["amount", "risk_score"]:
        if col in current_data.columns:
            current_data[col] = current_data[col] * (
                1 + np.random.normal(0.05, 0.02, len(current_data))
            )

    for col in ["merchant", "location"]:
        if col in current_data.columns:
            current_data[col] = (
                current_data[col].sample(frac=1, replace=False).reset_index(drop=True)
            )

    print(f"   Current: {len(current_data)} records")

    detector = BankingDataDriftDetector()
    detector.detect_drift(baseline_data, current_data)
    detector.setup_drift_monitoring(baseline_data)

    print("\n" + "=" * 60)
    print("✅ Drift Detection Complete!")
    print(f"   Report: {CONFIG_DIR / 'drift_report.json'}")


if __name__ == "__main__":
    main_drift_detection()
