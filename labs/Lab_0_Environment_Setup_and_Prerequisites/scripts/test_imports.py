"""Test Python package imports for Lab 0."""
import sys

PACKAGES = ["boto3", "sagemaker", "pandas", "numpy", "sklearn"]


def main():
    failed = []
    for name in PACKAGES:
        try:
            __import__(name)
        except ImportError:
            failed.append(name)
    if failed:
        print(f"Import failed: {', '.join(failed)}")
        sys.exit(1)
    print("All imports successful!")


if __name__ == "__main__":
    main()
