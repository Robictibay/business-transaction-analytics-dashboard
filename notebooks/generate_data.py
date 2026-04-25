import pandas as pd
import numpy as np
import random
from pathlib import Path

np.random.seed(42)
random.seed(42)

OUTPUT_PATH = Path("data/raw/transactions.csv")
SAMPLE_PATH = Path("data/sample/transactions_sample.csv")

clients = [f"Client_{1000+i}" for i in range(1, 21)]
categories = ["SaaS Subscription", "Cloud Hosting", "E-commerce", "Consulting", "Hardware"]
statuses = ["Completed", "Failed", "Refunded"]
payment_methods = ["Credit Card", "Bank Transfer", "E-Wallet", "Debit Card"]

start_date = pd.Timestamp("2025-10-01")
end_date = pd.Timestamp("2026-04-30")
dates = pd.date_range(start_date, end_date, freq="D")

records = []
transaction_id = 1

for date in dates:
    daily_count = np.random.randint(45, 95)

    for _ in range(daily_count):
        client = random.choice(clients)
        category = random.choice(categories)
        status = np.random.choice(statuses, p=[0.88, 0.08, 0.04])
        payment_method = random.choice(payment_methods)

        if category == "SaaS Subscription":
            amount = np.random.normal(2500, 600)
        elif category == "Cloud Hosting":
            amount = np.random.normal(5000, 1500)
        elif category == "E-commerce":
            amount = np.random.normal(1200, 400)
        elif category == "Consulting":
            amount = np.random.normal(12000, 3000)
        else:
            amount = np.random.normal(8000, 2000)

        amount = max(100, round(amount, 2))

        records.append({
            "transaction_id": transaction_id,
            "transaction_date": date.date(),
            "client_id": client,
            "category": category,
            "payment_method": payment_method,
            "status": status,
            "amount": amount
        })

        transaction_id += 1

# Inject anomaly: abnormal completed E-commerce spike for one client
anomaly_date = pd.Timestamp("2026-03-15").date()
for _ in range(450):
    records.append({
        "transaction_id": transaction_id,
        "transaction_date": anomaly_date,
        "client_id": "Client_1004",
        "category": "E-commerce",
        "payment_method": random.choice(payment_methods),
        "status": "Completed",
        "amount": round(np.random.normal(1500, 300), 2)
    })
    transaction_id += 1

df = pd.DataFrame(records)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)
df.sample(500, random_state=42).to_csv(SAMPLE_PATH, index=False)

print("Synthetic transaction dataset created successfully.")
print(f"Rows: {len(df)}")
print(f"Saved full dataset to: {OUTPUT_PATH}")
print(f"Saved sample dataset to: {SAMPLE_PATH}")
print()
print("Status counts:")
print(df["status"].value_counts())
print()
print("Date range:")
print(df["transaction_date"].min(), "to", df["transaction_date"].max())
