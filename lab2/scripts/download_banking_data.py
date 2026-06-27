"""Generate synthetic banking dataset with PII for lab exercises."""
import json
import os
import random
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
from lab_paths import CONFIG_DIR, DATA_DIR, LAB1_CONFIG_DIR, RESULTS_DIR, ensure_workspace


def generate_banking_dataset():
    """
    Generate synthetic banking dataset with realistic patterns
    Includes PII elements for detection and anonymization practice
    """
    ensure_workspace()

    print("🏦 Generating Banking Transaction Dataset")
    print("=" * 60)

    np.random.seed(42)
    random.seed(42)

    num_records = 10000

    first_names = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph",
        "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy",
        "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Helen", "Mark", "Sandra",
        "Donald", "Donna", "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon",
        "Joshua", "Michelle", "Kenneth", "Laura", "Kevin", "Brian", "Kimberly",
        "George", "Deborah", "Timothy", "Maria",
    ]

    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
        "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
        "Mitchell", "Carter", "Roberts",
    ]

    domains = ["gmail.com", "yahoo.com", "hotmail.com", "bank.com", "financial.com"]
    customers = []

    for i in range(num_records // 10):
        first = random.choice(first_names)
        last = random.choice(last_names)
        email = f"{first.lower()}.{last.lower()}@{random.choice(domains)}"
        phone = f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"
        ssn = f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
        account_number = f"{random.randint(10000000, 99999999)}"
        routing_number = f"{random.randint(100000000, 999999999)}"
        age = random.randint(18, 85)
        income = random.randint(25000, 250000)

        customers.append(
            {
                "customer_id": f"CUST{100000 + i}",
                "first_name": first,
                "last_name": last,
                "email": email,
                "phone": phone,
                "ssn": ssn,
                "account_number": account_number,
                "routing_number": routing_number,
                "age": age,
                "income": income,
                "credit_score": random.randint(300, 850),
                "address": (
                    f"{random.randint(100, 9999)} "
                    f"{random.choice(['Main', 'Oak', 'Pine', 'Maple', 'Cedar', 'Elm', 'Washington'])} St, "
                    f"{random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])}"
                ),
                "zip_code": f"{random.randint(10000, 99999)}",
            }
        )

    print("\n📊 Generating Transaction Records...")

    transactions = []
    transaction_types = ["DEPOSIT", "WITHDRAWAL", "TRANSFER", "PAYMENT", "CHECK_CASH"]

    for i in range(num_records):
        customer = random.choice(customers)
        amount = round(random.uniform(10, 10000), 2)
        transaction_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 365))

        transactions.append(
            {
                "transaction_id": f"TXN{20240000 + i}",
                "customer_id": customer["customer_id"],
                "first_name": customer["first_name"],
                "last_name": customer["last_name"],
                "email": customer["email"],
                "phone": customer["phone"],
                "account_number": customer["account_number"],
                "transaction_type": random.choice(transaction_types),
                "amount": amount,
                "transaction_date": transaction_date.isoformat(),
                "merchant": random.choice(
                    ["Amazon", "Walmart", "Target", "Costco", "Best Buy", "Starbucks", "Apple"]
                ),
                "location": random.choice(["Online", "Store", "ATM", "Mobile"]),
                "card_present": random.choice([True, False]),
                "international": random.choice([True, False]),
                "risk_score": round(random.uniform(0, 100), 2),
            }
        )

    customers_df = pd.DataFrame(customers)
    transactions_df = pd.DataFrame(transactions)

    ensure_workspace()
    customers_df.to_csv(DATA_DIR / "customers.csv", index=False)
    transactions_df.to_csv(DATA_DIR / "transactions.csv", index=False)

    print(f"✅ Generated {len(customers)} customer records")
    print(f"✅ Generated {len(transactions)} transaction records")

    metadata = {
        "dataset_name": "Banking Transaction Dataset",
        "created_date": datetime.now(timezone.utc).isoformat(),
        "num_customers": len(customers),
        "num_transactions": len(transactions),
        "pii_fields": [
            "first_name", "last_name", "email", "phone", "ssn",
            "account_number", "routing_number", "address", "zip_code",
        ],
        "sensitive_fields": ["income", "credit_score", "risk_score"],
        "classification": "CONFIDENTIAL",
        "retention_required_days": 2555,
        "data_lineage": {
            "source": "Synthetic Generation",
            "created_by": "MLOps-Banking-Lab",
            "version": "1.0",
        },
    }

    ensure_workspace()
    with open(CONFIG_DIR / "dataset_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("✅ Dataset metadata saved")
    return customers_df, transactions_df


if __name__ == "__main__":
    generate_banking_dataset()
