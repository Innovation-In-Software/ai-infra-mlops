@echo off
echo ============================================
echo Banking MLOps - Quick Commands (Lab 0)
echo ============================================
echo.
echo Select an option:
echo 1. Verify Environment (dry-run)
echo 2. Verify Environment (live AWS)
echo 3. Create Student Workspace
echo 4. Run Full Lab 0 Setup
echo 5. Check AWS Status
echo 6. Open SageMaker Console
echo 7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    python scripts\verify_environment.py --dry-run
) else if "%choice%"=="2" (
    python scripts\verify_environment.py
) else if "%choice%"=="3" (
    python scripts\setup_lab_directories.py
) else if "%choice%"=="4" (
    python scripts\run_lab0_setup.py --dry-run
) else if "%choice%"=="5" (
    aws sts get-caller-identity
    aws configure get region
    aws s3 ls --region us-west-2
) else if "%choice%"=="6" (
    start https://us-west-2.console.aws.amazon.com/sagemaker/home?region=us-west-2
) else if "%choice%"=="7" (
    exit /b 0
) else (
    echo Invalid choice.
)

pause
