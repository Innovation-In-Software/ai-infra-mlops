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

## Configure AWS on EC2 (once per session)

```bash
aws configure set region us-west-2
aws configure set output json
aws sts get-caller-identity   # confirm account 028417007274
```

Use instructor console or `aws configure` with your access keys — **never commit keys to git**.

## Instructor console

- URL: https://iis-instructor-03.signin.aws.amazon.com/console
- Username: `Instructor01` (case-sensitive)
- Region: `us-west-2`

## Security (instructor)

- **Never commit** access keys or `.pem` files (see `.gitignore`).
- If credentials were shared in chat or email, **rotate IAM access keys** before class.
- Prefer EC2 instance profile `EC2MLOpsLabProfile` over embedding keys on the instance.

## Full course teardown (after Lab 10)

```bash
cd ~/ai-infra-mlops
python3 scripts/teardown_course.py --yes
```

See [Lab 10 Step 11](../lab10/STEPS.md#step-11--delete-all-aws-resources-instructor).
