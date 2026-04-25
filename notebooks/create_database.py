import sqlite3
import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw/transactions.csv")
DB_PATH = Path("data/processed/transactions.db")

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

conn = sqlite3.connect(DB_PATH)

df.to_sql("transactions", conn, if_exists="replace", index=False)

cursor = conn.cursor()

cursor.execute("CREATE INDEX IF NOT EXISTS idx_transaction_date ON transactions(transaction_date);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_client_id ON transactions(client_id);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON transactions(status);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON transactions(category);")

conn.commit()

print("SQLite database created successfully.")
print(f"Database path: {DB_PATH}")

print()
print("Preview from transactions table:")
preview = pd.read_sql_query("SELECT * FROM transactions LIMIT 5;", conn)
print(preview)

conn.close()
