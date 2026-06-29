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
cd ~/ai-infra-mlops/lab6 && python3 scripts/validate_lab6.py 2>/dev/null || true
cd ~/ai-infra-mlops/lab5 && python3 scripts/validate_lab5.py
cd ~/ai-infra-mlops/lab7
```

**Expected:** Lab 5 prerequisites OK (or prior lab7 outputs if re-running).

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

**Screenshot (optional):** `images/step-01-lab7-folder.png`

---

## Step 2 — Prepare monitoring baseline

**Do this:**

```bash
cd ~/ai-infra-mlops/lab7
pip install -r requirements.txt
python3 scripts/prepare_monitoring_data.py
ls -1 ../workspace/lab7/data
```

**Expected result:**

```text
✅ Baseline data loaded from Lab 2 engineered features
   ✅ Current production sample generated
baseline_data.csv
current_data.csv
```

**Screenshot (optional):** `images/step-02-baseline.png`

---

## Step 3 — Configure CloudWatch dashboards

**Do this:**

```bash
python3 scripts/setup_cloudwatch_dashboard.py
```

**Expected result:**

```text
📊 CloudWatch Dashboard
============================================================
   ✅ Dashboard: Banking-MLOps-Model-Monitor
   ✅ Widgets: invocations, latency, errors, drift
✅ Dashboard configuration saved
```

**Screenshot (optional):** `images/step-03-dashboard.png`

---

## Step 4 — SageMaker Model Monitor setup

**Do this:**

```bash
python3 scripts/setup_model_monitor.py
```

**Expected result:**

```text
✅ Baseline constraints generated
   ✅ Monitoring schedule: hourly (simulated)
✅ Model Monitor configured 
```

**Screenshot (optional):** `images/step-04-model-monitor.png`

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
   Features checked: 52
   Drift detected: 2
   Severity: LOW
   Status: NORMAL
✅ Drift report saved
```

**Screenshot (optional):** `images/step-05-drift.png`

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
   AUC (rolling): 0.86
   Precision@threshold: 0.78
   Status: WITHIN SLA
✅ Quality report saved
```

**Screenshot (optional):** `images/step-06-quality.png`

---

## Step 7 — Configure alarms

**Do this:**

```bash
python3 scripts/setup_alarms.py
```

**Expected result:**

```text
🚨 CloudWatch Alarms
============================================================
   ✅ banking-ml-high-latency
   ✅ banking-ml-error-rate
   ✅ banking-ml-drift-severity
✅ Alarms configured 
```

**Screenshot (optional):** `images/step-07-alarms.png`

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
   ✅ Notification sent (simulated)
✅ Incident drill complete
```

**Screenshot (optional):** `images/step-08-incident.png`

---

## Step 9 — Compliance monitoring report

**Do this:**

```bash
python3 scripts/generate_monitoring_report.py
```

**Expected result:**

```text
✅ Monitoring compliance report generated
   Overall status: COMPLIANT
   Audit trail: logs/monitoring_audit.json
```

**Screenshot (optional):** `images/step-09-report.png`

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
   ✅ monitoring_report_final.json
Prerequisites OK — proceed to Lab 8
```

**Screenshot (optional):** `images/step-10-validate.png`

---

## Lab 7 complete → [Lab 8](../lab8/STEPS.md)
