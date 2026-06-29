# EC2 terminal capture (instructor testing)

**Dual delivery:** ProTech VM for slides/console + EC2 for lab commands — see [PROTECH-VM-SETUP.md](PROTECH-VM-SETUP.md).

## SSH status

**Instructor lab EC2** (account `028417007274`):

| Item | Value |
|------|--------|
| Instance | `ai-mlops-lab` (`i-0326933d0bc3b45f1`) |
| Public IP | `35.161.45.178` (changes if instance stopped/started) |
| Key pair | `ai-mlops-instructor` |
| PEM path | `~/.ssh/ai-mlops-instructor.pem` |
| User | `ec2-user` |
| IAM | Instance profile `EC2MLOpsLabProfile` (PowerUserAccess) |

Launch with **30 GB+ root volume** (expand if needed). Lab 0 `pip install` needs ~3 GB with `sagemaker<3`.

Example `~/.ssh/config`:

```
Host ai-mlops-lab
    HostName 35.161.45.178
    User ec2-user
    IdentityFile ~/.ssh/ai-mlops-instructor.pem
```

If SSH times out: start the instance, refresh public IP (`aws ec2 describe-instances`), and ensure security group `mlops-lab-sg` allows **port 22** from your IP.

## If workspace was cleared but AWS Lab 1 still exists

```bash
cd ~/ai-infra-mlops
python3 scripts/sync_lab1_config_from_aws.py
python3 lab1/scripts/validate_environment.py
```

Then continue Lab 2+ without re-creating KMS/S3/IAM.

## On EC2 — capture fresh outputs for STEPS.md

```bash
cd ~/ai-infra-mlops
git pull
chmod +x scripts/capture_lab_steps.sh
./scripts/capture_lab_steps.sh
# Review: docs/terminal-captures/
```

## Configure AWS on EC2 (instructor demo — access keys)

For this training demo, use **Instructor01 access keys** on EC2 (not committed to git):

```bash
aws configure set aws_access_key_id YOUR_KEY
aws configure set aws_secret_access_key YOUR_SECRET
aws configure set region us-west-2
aws configure set output json
aws sts get-caller-identity   # confirm account 028417007274, user Instructor01
```

Keys stay in `~/.aws/credentials` on the EC2 instance only. **Never commit keys to git** or paste them into lab repos.

## Instructor progress checklist (EC2 shell)

| Done | Lab | Validate on EC2 |
|------|-----|-----------------|
| ✅ | 0–4 | `lab4/scripts/validate_lab4.py` |
| ✅ | 3 (Steps 10–12) | SageMaker Processing job in console |
| ✅ | 4 (Steps 11–15) | `optional/lab4b/scripts/validate_lab4b.py` |
| ▶ | 5 | `lab5/scripts/validate_lab5.py` after Docker + ECR push |
| | 6–10 | `labN/scripts/validate_labN.py` |

```bash
cd ~/ai-infra-mlops && git pull
whoami   # ec2-user
cd lab5 && python3 scripts/run_lab5.py && python3 scripts/validate_lab5.py
```

Verify in console: **ECR** → `banking-ml-inference` → image `latest` + scan results.

The instructor EC2 may also have instance profile `EC2MLOpsLabRole`; for demos that match student steps, **`aws configure` with access keys** is fine.

## Instructor console

- URL: https://iis-instructor-03.signin.aws.amazon.com/console
- Username: `Instructor01` (case-sensitive)
- Region: `us-west-2`

## Security (instructor demo)

- **Never commit** access keys or `.pem` files (see `.gitignore`).
- Store keys only in `~/.aws/credentials` on your demo EC2 or local shell for the session.
- Do not embed keys in scripts, STEPS.md, or screenshots.

## Full course teardown (after Lab 10)

```bash
cd ~/ai-infra-mlops
python3 scripts/teardown_course.py --yes
python3 scripts/teardown_course.py --yes --terminate-ec2   # also terminate mlops EC2
python3 scripts/teardown_course.py --dry-run               # preview only
```

Removes workspace, Lab 1–2 AWS resources, IAM roles, KMS keys (7-day pending), alarms, SageMaker experiments, ECR, EC2 key pairs/SG, and more. See [Lab 10 Step 11](../lab10/STEPS.md).
