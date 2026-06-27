<h1 align="center">AI-MLOps on AWS</h1>
<h2 align="center">Participant Labs</h2>

<p align="center">
  <strong>Class:</strong> ai-mlops-2026-jun30 &nbsp;·&nbsp;
  <strong>Region:</strong> us-west-2
</p>

<p align="center">
  <strong>Cloud delivery:</strong> EC2 in <code>us-west-2</code> + SSH + VS Code Remote SSH.
  See <a href="CLOUD-DELIVERY.md">CLOUD-DELIVERY.md</a> for golden AMI, fresh start, and 30-minute timing.
</p>

<p align="center">
  Clone once in Lab 0 — open each lab’s <code>STEPS.md</code> in order.
  Outputs go under <code>workspace/labN/</code> (gitignored).
</p>

---

<h2>Fresh start</h2>

<pre>
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab1,lab2
cd lab2 && python3 scripts/cleanup_lab2.py --aws   # optional: remove Feature Groups
</pre>

<p>Then re-run <a href="lab0/STEPS.md">Lab 0</a> verify → <a href="lab1/STEPS.md">Lab 1</a> → <a href="lab2/STEPS.md">Lab 2</a>.</p>

---

<h2>Lab index</h2>

| Lab | Folder | Duration | Guide |
|-----|--------|----------|-------|
| Lab 0 — Environment Setup | <code>lab0/</code> | 30 min | <a href="lab0/STEPS.md">lab0/STEPS.md</a> |
| Lab 1 — Secure MLOps Environment | <code>lab1/</code> | 30 min | <a href="lab1/STEPS.md">lab1/STEPS.md</a> |
| Lab 2 — Banking Data &amp; PII | <code>lab2/</code> | 30 min | <a href="lab2/STEPS.md">lab2/STEPS.md</a> |

---

<h2>Lab 0 — Environment Setup</h2>

<p>SSH to EC2, clone repo, AWS CLI, Python packages, workspace folders, verification.</p>
<p><a href="lab0/STEPS.md"><strong>Open lab0/STEPS.md</strong></a></p>

---

<h2>Lab 1 — Secure MLOps Environment Setup</h2>

<p>SageMaker Studio (start first), KMS, S3, IAM, CloudTrail, validation. Requires Lab 0.</p>
<p><a href="lab1/STEPS.md"><strong>Open lab1/STEPS.md</strong></a></p>

---

<h2>Lab 2 — Banking Data Management &amp; PII Protection</h2>

<p>Synthetic data, PII anonymization, feature engineering, Feature Store, drift, compliance. Requires Lab 1.</p>
<p><a href="lab2/STEPS.md"><strong>Open lab2/STEPS.md</strong></a></p>

<p><strong>Classroom defaults:</strong> <code>LAB_NUM_RECORDS=1000</code>, <code>LAB_USE_COMPREHEND=0</code> (pattern PII, ~30 min total).</p>
