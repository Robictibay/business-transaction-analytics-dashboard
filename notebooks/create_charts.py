import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DB_PATH = Path("data/processed/transactions.db")
SCREENSHOT_PATH = Path("screenshots")
SCREENSHOT_PATH.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

daily = pd.read_sql_query("""
SELECT
    transaction_date,
    COUNT(*) AS transaction_count,
    SUM(CASE WHEN status = 'Completed' THEN amount ELSE 0 END) AS completed_revenue
FROM transactions
GROUP BY transaction_date
ORDER BY transaction_date;
""", conn)

category = pd.read_sql_query("""
SELECT
    category,
    SUM(CASE WHEN status = 'Completed' THEN amount ELSE 0 END) AS completed_revenue
FROM transactions
GROUP BY category
ORDER BY completed_revenue DESC;
""", conn)

top_clients = pd.read_sql_query("""
SELECT
    client_id,
    SUM(CASE WHEN status = 'Completed' THEN amount ELSE 0 END) AS completed_revenue
FROM transactions
GROUP BY client_id
ORDER BY completed_revenue DESC
LIMIT 10;
""", conn)

conn.close()

daily["transaction_date"] = pd.to_datetime(daily["transaction_date"])

plt.figure(figsize=(12, 6))
plt.plot(daily["transaction_date"], daily["transaction_count"])
plt.title("Daily Transaction Volume")
plt.xlabel("Date")
plt.ylabel("Transaction Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(SCREENSHOT_PATH / "daily_transaction_volume.png")
plt.close()

plt.figure(figsize=(10, 6))
plt.bar(category["category"], category["completed_revenue"])
plt.title("Completed Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Completed Revenue")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(SCREENSHOT_PATH / "revenue_by_category.png")
plt.close()

plt.figure(figsize=(10, 6))
plt.bar(top_clients["client_id"], top_clients["completed_revenue"])
plt.title("Top 10 Clients by Completed Revenue")
plt.xlabel("Client")
plt.ylabel("Completed Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(SCREENSHOT_PATH / "top_clients_revenue.png")
plt.close()

print("Charts created successfully in screenshots folder.")
