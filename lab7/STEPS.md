# Lab 7: Compliance Monitoring & Observability

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30 minutes |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | [Lab 6](../lab6/STEPS.md) |
| **Working directory** | `~/ai-infra-mlops/lab7` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab7/` |

> All commands run in the **VS Code integrated terminal** on EC2. Do not use local Windows PowerShell for lab steps.

> **Quick run:** `python3 scripts/run_lab7.py` runs all script steps in order.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
whoami   # must be ec2-user
cd ~/ai-infra-mlops/lab6 && python3 scripts/validate_lab6.py
cd ~/ai-infra-mlops/lab7
```

**Expected:** `Prerequisites OK — proceed to Lab 7` from Lab 6 validation.

![Lab 6 validation — `python3 scripts/validate_lab6.py`](images/step-00b-lab6-validate.png)

---

## Step 1 — Confirm lab7 folder

**Do this:**

```bash
cd ~/ai-infra-mlops && ls -1 lab7
```

**Expected result:**

```text
STEPS.md
config
images
requirements.txt
scripts
```

![Step 1 — `ls -1 lab7`](images/step-01-lab7-folder.png)

---

## Step 2 — Prepare monitoring baseline

**Do this:**

```bash
cd ~/ai-infra-mlops/lab7
python3 -m pip install -r requirements.txt
python3 scripts/prepare_monitoring_data.py
ls -1 ../workspace/lab7/data
```

**Expected result:**

```text
Preparing monitoring data and configuration
============================================================
   ✅ Baseline data loaded from Lab 3: 5000 rows
   ✅ Monitoring endpoint: banking-endpoint-prod-... (production)
   ✅ baseline_data.csv / current_data.csv
✅ Monitoring data ready
```

![Step 2 — `prepare_monitoring_data.py`](images/step-02-baseline.png)

---

## Step 3 — Configure CloudWatch dashboards

**Do this:**

```bash
python3 scripts/setup_cloudwatch_dashboard.py
```

**Expected result:**

```text
   ✅ Dashboard created in CloudWatch: Banking-MLOps-Model-Monitor
📊 CloudWatch Dashboard
============================================================
   ✅ Dashboard: Banking-MLOps-Model-Monitor
✅ Dashboard configuration saved
```

![Step 3 — `setup_cloudwatch_dashboard.py`](images/step-03-dashboard.png)

---

## Step 4 — SageMaker Model Monitor setup

**Do this:**

```bash
python3 scripts/setup_model_monitor.py
```

**Expected result:**

```text
   ✅ Endpoint banking-endpoint-prod-...: InService
   ✅ Baseline constraints generated (local baseline from Lab 7 Step 3)
   ✅ Endpoint verified for monitoring
✅ Model Monitor configured
```

![Step 4 — `setup_model_monitor.py`](images/step-04-model-monitor.png)

---

## Step 5 — Data drift monitoring

**Do this:**

```bash
python3 scripts/monitor_data_drift.py
```

**Expected result:**

```text
📉 Data Drift Check
============================================================
   Features checked: 30
   Drift detected: 0
   Status: NORMAL
✅ Drift report saved
```

![Step 5 — `monitor_data_drift.py`](images/step-05-drift.png)

---

## Step 6 — Model quality monitoring

**Do this:**

```bash
python3 scripts/monitor_model_quality.py
```

**Expected result:**

```text
📈 Model Quality
============================================================
   Invocations (1h): 12
   Avg latency: 149.2 ms
   Status: WITHIN SLA
✅ Quality report saved
```

> Invocations and latency come from **CloudWatch** (`AWS/SageMaker` metrics on your Lab 6 endpoint). Values vary with traffic.

![Step 6 — `monitor_model_quality.py`](images/step-06-quality.png)

---

## Step 7 — Configure alarms

**Do this:**

```bash
python3 scripts/setup_alarms.py
```

**Expected result:**

```text
   ✅ banking-ml-high-latency
   ✅ banking-ml-error-rate
✅ Alarms configured
```

![Step 7 — `setup_alarms.py`](images/step-07-alarms.png)

---

## Step 8 — Incident response simulation

**Do this:**

```bash
python3 scripts/simulate_incident.py
```

**Expected result:**

```text
⚠️ Simulated incident: latency spike
   ✅ Alarm triggered
   ✅ Runbook executed
✅ Incident drill complete
```

![Step 8 — `simulate_incident.py`](images/step-08-incident.png)

---

## Step 9 — Compliance monitoring report

**Do this:**

```bash
python3 scripts/generate_monitoring_report.py
```

**Expected result:**

```text
✅ Monitoring compliance report generated
```

![Step 9 — `generate_monitoring_report.py`](images/step-09-report.png)

---

## Step 10 — Validate lab7

**Do this:**

```bash
python3 scripts/validate_lab7.py
```

**Expected result:**

```text
Validate Lab 7
============================================================
   ✅ baseline_data.csv
   ✅ current_data.csv
   ✅ dashboard_config.json
   ✅ alarms.json
   ✅ monitoring_report_final.json

============================================================
Prerequisites OK — proceed to Lab 8
```

![Step 10 — `validate_lab7.py`](images/step-10-validate.png)

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Lab 6 validation fails | Complete [Lab 6](../lab6/STEPS.md) Steps 1–10 first |
| `No Lab 6 endpoint found` | Run `deploy_production.py` in Lab 6; endpoint must be `InService` |
| `Endpoint must be InService` | Wait for SageMaker endpoint status in AWS console |
| Dashboard/alarms not in CloudWatch | Re-run without `--dry-run`; confirm IAM `cloudwatch:PutDashboard` / `PutMetricAlarm` |
| Zero invocations in quality report | Run Lab 6 `test_deployment.py` or invoke endpoint to generate metrics |
| `InvalidParameterInput` on PutDashboard | `git pull` — dashboard metrics must not use multiple `...` shorthand markers |

---

## Lab 7 complete → [Lab 8](../lab8/STEPS.md)
