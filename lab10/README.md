# Lab 10: Enterprise MLOps Architecture

**Class:** `ai-mlops-2026-jun30` · **Module 11:** Enterprise MLOps Architecture · **Duration:** ~30 min

Hands-on steps: [STEPS.md](STEPS.md)

> **Note:** The participant repo ends at Lab 10. Module 11 course content maps to this lab — there is no separate `lab11` folder.

---

## Terms & acronyms (beginners)

| Term | Full form / meaning |
|------|---------------------|
| **MLOps** | **Machine Learning Operations** — end-to-end practice for production ML |
| **Enterprise architecture** | How all layers (security, data, training, etc.) **fit together** at scale |
| **Gap analysis** | Identifies what is **missing** vs. production best practices |
| **Roadmap** | **Phased plan** to close gaps over months |
| **Executive summary** | Short **leadership** document of course outcomes |
| **Compliance bundle** | **Zip archive** of reports for auditors and stakeholders |
| **SageMaker** | AWS ML service (endpoints, pipeline, registry checked in this lab) |
| **ECR** | **Elastic Container Registry** |
| **DR** | **Disaster Recovery** — multi-region backup (noted as a future gap) |
| **Teardown** | **Delete** AWS resources after the course (optional Step 11) |

---

## Overview

Lab 10 is the **course capstone**. You collect artifacts from Labs 1–9, score the enterprise architecture across seven MLOps layers, perform gap analysis, produce an implementation roadmap and checklist, generate an executive summary, and package everything into a **compliance bundle** for stakeholders.

Completing this lab with `validate_lab10.py` prints **COURSE COMPLETE**.

---

## Prerequisites

- Lab 9 complete — `validate_lab9.py` passed
- Workspaces `workspace/lab1` through `workspace/lab9` populated from prior labs

---

## Lab flow

```
validate_lab9.py
    → collect_course_artifacts.py
    → architecture_assessment.py (score /100)
    → gap_analysis.py
    → implementation_roadmap.py
    → implementation_checklist.py
    → generate_executive_summary.py
    → build_compliance_bundle.py
    → validate_lab10.py → 🎉 COURSE COMPLETE

Optional (after class):
    → reset_course.py (workspace only)
    → teardown_course.py (delete AWS resources)
```

| Step | Script | Purpose |
|------|--------|---------|
| 2 | `collect_course_artifacts.py` | Inventory lab workspaces + live AWS checks (ECR, endpoints, pipeline) |
| 3 | `architecture_assessment.py` | Score 7 layers against workspace evidence |
| 4 | `gap_analysis.py` | Identify remaining gaps (e.g. multi-region DR) |
| 5 | `implementation_roadmap.py` | 3-phase enterprise roadmap |
| 6 | `implementation_checklist.py` | 20-item checklist from Labs 1–9 |
| 7 | `generate_executive_summary.py` | Markdown summary for leadership |
| 8 | `build_compliance_bundle.py` | Zip bundle for auditors |
| 9 | `validate_lab10.py` | Course completion gate |

**Quick run:** `python3 scripts/run_lab10.py` then `validate_lab10.py`.

---

## Architecture layers (`architecture_assessment.py`)

| Layer | Evidence lab | Required config markers |
|-------|--------------|-------------------------|
| security | Lab 1 | `buckets.json`, `iam_roles.json` |
| data | Lab 2 | `feature_store_config.json` |
| training | Lab 3 | `training_results.json` |
| pipeline | Lab 8 | `pipeline_registration.json`, `model_registry.json`, `pipeline_execution.json` |
| deployment | Lab 6 | `staging_deployment.json`, `production_deployment.json` |
| monitoring | Lab 7 | `dashboard_config.json`, `alarms.json` |
| governance | Lab 9 | `iam_review.json`, `encryption_audit.json` |

**Target score:** 100/100 when all labs completed. Validation requires score ≥ 90 and `course_compliance_bundle.zip` exists.

---

## Scripts reference

### `collect_course_artifacts.py`

Walks `workspace/lab1`–`lab9` and records which folders have `config/`, `results/`, or `artifacts/`. Live AWS checks:

- ECR repository `banking-ml-inference`
- SageMaker banking endpoints
- Pipeline `banking-ml-pipeline`
- Model registry group `banking-risk-models`

Writes `config/artifact_manifest.json`.

### `architecture_assessment.py`

For each layer, checks marker files exist under the mapped lab workspace. Computes `score = complete_layers / 7 * 100`. Optionally counts live SageMaker endpoints. Writes `results/architecture_assessment.json`.

### `gap_analysis.py`

Documents known enterprise gaps (documentation depth, multi-region DR) with priority ratings. Writes `gap_analysis.json`.

### `implementation_roadmap.py`

Produces a phased roadmap:

- Phase 1 (0–3 mo): Production hardening
- Phase 2 (3–6 mo): Multi-account landing zone
- Phase 3 (6–12 mo): Federated feature store

### `implementation_checklist.py`

Checklist items mapped to course labs; marks completed vs future work (e.g. multi-region DR). Reports `9/10` or similar completion count.

### `generate_executive_summary.py`

Renders `executive_summary.md` with course ID, timestamp, layer status, and AWS region summary for executives.

### `build_compliance_bundle.py`

Zips key deliverables (`architecture_assessment.json`, `implementation_roadmap.json`, `executive_summary.md`) into `course_compliance_bundle.zip` with `bundle_manifest.json`.

### `validate_lab10.py`

Prints **COURSE COMPLETE** if architecture score ≥ 90 and compliance bundle exists; otherwise exits with error.

### `lab_paths.py`

Paths for Lab 10 workspace; `lab_workspace(n)` helper to resolve `workspace/labN/`.

### `run_lab10.py`

Runs Steps 2–8 in sequence (excludes validation and teardown).

---

## Configuration & outputs

**Repo (`config/`):**

| File | Purpose |
|------|---------|
| `lab_config.json` | Lab metadata |
| `enterprise_config.json` | Course ID, region, architecture tier names |

**Workspace (`workspace/lab10/`):**

| Path | Purpose |
|------|---------|
| `config/artifact_manifest.json` | Lab + AWS inventory |
| `results/architecture_assessment.json` | Layer scores |
| `results/gap_analysis.json` | Gap report |
| `results/implementation_roadmap.json` | Roadmap JSON |
| `results/implementation_checklist.json` | Checklist JSON |
| `results/executive_summary.md` | Leadership summary |
| `results/course_compliance_bundle.zip` | Auditor deliverable |
| `results/bundle_manifest.json` | Zip contents manifest |

---

## Optional cleanup (after class)

| Script | Location | Purpose |
|--------|----------|---------|
| `reset_course.py` | `scripts/` | Clear `workspace/lab1`–`lab10` only |
| `teardown_course.py` | `scripts/` | Full AWS teardown (S3, IAM, endpoints, pipeline, KMS, etc.) |

**Warning:** Do not run teardown until the course is fully complete — it deletes resources needed for labs.

---

## Course complete

You have implemented a full **banking MLOps platform** on AWS: secure foundation → data & PII → training & fairness → CI/CD → containers → blue-green deploy → monitoring → pipeline → governance → enterprise assessment.

Return to [course README](../README.md) or re-run from [Lab 0](../lab0/STEPS.md) for the next cohort.
