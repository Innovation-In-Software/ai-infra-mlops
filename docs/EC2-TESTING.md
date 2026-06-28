# EC2 terminal capture (instructor testing)

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
```

See [Lab 10 Step 11](../lab10/STEPS.md#step-11--delete-all-aws-resources-instructor).
