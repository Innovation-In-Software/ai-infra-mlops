"""Clean up resources created in Lab 1.1 (instructor use)."""


def cleanup_lab1():
    """Clean up resources created in Lab 1.1."""

    print("🧹 Cleaning up Lab 1.1 Resources")
    print("=" * 60)

    print("\n📋 Deleting SageMaker Studio...")
    print("   ⚠️ Please delete SageMaker Studio domain manually from console")

    print("\n📋 Deleting S3 buckets...")
    print("   ⚠️ Please empty and delete buckets manually from console")

    print("\n📋 Deleting IAM roles...")
    print("   ⚠️ Please delete IAM roles manually from console")

    print("\n📋 Deleting KMS keys...")
    print("   ⚠️ Please schedule KMS key deletion manually")

    print("\n" + "=" * 60)
    print("✅ Cleanup instructions provided")


if __name__ == "__main__":
    cleanup_lab1()
