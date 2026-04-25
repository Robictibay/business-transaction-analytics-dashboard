-- Create transactions table structure
-- The actual table is generated from data/raw/transactions.csv using notebooks/create_database.py

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    transaction_date TEXT,
    client_id TEXT,
    category TEXT,
    payment_method TEXT,
    status TEXT,
    amount REAL
);
