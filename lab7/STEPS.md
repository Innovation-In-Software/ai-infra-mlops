# Lab 7: Compliance Monitoring & Observability

## Class · `ai-mlops-2026-jun30` · **30 min** · **us-west-2**
## Platform · **EC2** + [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) + **bash**
## Prerequisite · [Lab 6](../lab6/STEPS.md) complete
## Working directory · `~/ai-infra-mlops/lab7`
## Outputs · `~/ai-infra-mlops/workspace/lab7/`
## Run all · `python3 scripts/run_lab7.py`

---

# Step 1 — Confirm lab7 folder

```bash
clear
cd ~/ai-infra-mlops && ls -1 lab7
```

**Expected output:** `STEPS.md`, `config`, `images`, `requirements.txt`, `scripts`

**Optional screenshot:** `images/step-01-lab7-folder.png`

---

# Step 2 — Prepare monitoring baseline

```bash
clear
cd ~/ai-infra-mlops/lab7
pip install -r requirements.txt
python3 scripts/prepare_monitoring_data.py
ls -1 ../workspace/lab7/data
```

**Expected output:**

```text
   ✅ Baseline data loaded from Lab 2 engineered features
   ✅ Current production sample generated
baseline_data.csv
current_data.csv
```

**Optional screenshot:** `images/step-02-baseline.png`

---

# Step 3 — Configure CloudWatch dashboards

```bash
clear
python3 scripts/setup_cloudwatch_dashboard.py
```

**Expected output:**

```text
📊 CloudWatch Dashboard
============================================================
   ✅ Dashboard: Banking-MLOps-Model-Monitor
   ✅ Widgets: invocations, latency, errors, drift
✅ Dashboard configuration saved
```

**Optional screenshot:** `images/step-03-dashboard.png`

---

# Step 4 — SageMaker Model Monitor setup

```bash
clear
python3 scripts/setup_model_monitor.py --dry-run
```

**Expected output:**

```text
   ✅ Baseline constraints generated
   ✅ Monitoring schedule: hourly (simulated)
✅ Model Monitor configured (dry-run)
```

**Optional screenshot:** `images/step-04-model-monitor.png`

---

# Step 5 — Data drift monitoring

```bash
clear
python3 scripts/monitor_data_drift.py
```

**Expected output:**

```text
📉 Data Drift Check
============================================================
   Features checked: 52
   Drift detected: 2
   Severity: LOW
   Status: NORMAL
✅ Drift report saved
```

**Optional screenshot:** `images/step-05-drift.png`

---

# Step 6 — Model quality monitoring

```bash
clear
python3 scripts/monitor_model_quality.py
```

**Expected output:**

```text
📈 Model Quality
============================================================
   AUC (rolling): 0.86
   Precision@threshold: 0.78
   Status: WITHIN SLA
✅ Quality report saved
```

**Optional screenshot:** `images/step-06-quality.png`

---

# Step 7 — Configure alarms

```bash
clear
python3 scripts/setup_alarms.py --dry-run
```

**Expected output:**

```text
🚨 CloudWatch Alarms
============================================================
   ✅ banking-ml-high-latency
   ✅ banking-ml-error-rate
   ✅ banking-ml-drift-severity
✅ Alarms configured (dry-run)
```

**Optional screenshot:** `images/step-07-alarms.png`

---

# Step 8 — Incident response simulation

```bash
clear
python3 scripts/simulate_incident.py
```

**Expected output:**

```text
⚠️ Simulated incident: latency spike
   ✅ Alarm triggered
   ✅ Runbook executed
   ✅ Notification sent (simulated)
✅ Incident drill complete
```

**Optional screenshot:** `images/step-08-incident.png`

---

# Step 9 — Compliance monitoring report

```bash
clear
python3 scripts/generate_monitoring_report.py
```

**Expected output:**

```text
✅ Monitoring compliance report generated
   Overall status: COMPLIANT
   Audit trail: logs/monitoring_audit.json
```

**Optional screenshot:** `images/step-09-report.png`

---

# Step 10 — Validate lab7

```bash
clear
python3 scripts/validate_lab7.py
```

**Expected output:**

```text
Validate Lab 7
============================================================
   ✅ data: baseline_data.csv
   ✅ data: current_data.csv
   ✅ results: monitoring_report_final.json
Prerequisites OK — proceed to Lab 8
```

**Optional screenshot:** `images/step-10-validate.png`

---

## Lab 7 complete → [Lab 8](../lab8/STEPS.md)
