import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/processed/transactions.db")
REPORT_PATH = Path("reports/client_insights_report.md")

conn = sqlite3.connect(DB_PATH)

overall_kpis = pd.read_sql_query("""
SELECT
    COUNT(*) AS total_transactions,
    ROUND(SUM(CASE WHEN status = 'Completed' THEN amount ELSE 0 END), 2) AS completed_revenue,
    ROUND(100.0 * SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS failed_transaction_rate,
    ROUND(100.0 * SUM(CASE WHEN status = 'Refunded' THEN 1 ELSE 0 END) / COUNT(*), 2) AS refund_rate
FROM transactions;
""", conn)

top_clients = pd.read_sql_query("""
SELECT
    client_id,
    COUNT(*) AS transaction_count,
    ROUND(SUM(CASE WHEN status = 'Completed' THEN amount ELSE 0 END), 2) AS completed_revenue
FROM transactions
GROUP BY client_id
ORDER BY completed_revenue DESC
LIMIT 5;
""", conn)

category_revenue = pd.read_sql_query("""
SELECT
    category,
    COUNT(*) AS transaction_count,
    ROUND(SUM(CASE WHEN status = 'Completed' THEN amount ELSE 0 END), 2) AS completed_revenue
FROM transactions
GROUP BY category
ORDER BY completed_revenue DESC;
""", conn)

anomalies = pd.read_sql_query("""
SELECT
    transaction_date,
    client_id,
    category,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount), 2) AS total_amount
FROM transactions
WHERE status = 'Completed'
GROUP BY transaction_date, client_id, category
HAVING transaction_count >= 100
ORDER BY transaction_count DESC;
""", conn)

conn.close()

def money(value):
    return f"PHP {value:,.2f}"

top_clients["completed_revenue"] = top_clients["completed_revenue"].apply(money)
category_revenue["completed_revenue"] = category_revenue["completed_revenue"].apply(money)
anomalies["total_amount"] = anomalies["total_amount"].apply(money)

REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

kpi = overall_kpis.iloc[0]

report = f"""# Client Transaction Insights Report

## Executive Summary

This report analyzes synthetic business transaction data from October 2025 to April 2026. The goal is to monitor transaction volume, completed revenue, failed transaction rate, refund rate, top client performance, and possible anomaly spikes.

## Overall KPIs

- Total transactions: {int(kpi['total_transactions']):,}
- Completed revenue: PHP {kpi['completed_revenue']:,.2f}
- Failed transaction rate: {kpi['failed_transaction_rate']}%
- Refund rate: {kpi['refund_rate']}%

## Top 5 Clients by Completed Revenue

{top_clients.to_markdown(index=False)}

## Revenue by Category

{category_revenue.to_markdown(index=False)}

## Anomaly Detection Findings

The anomaly detection query flagged unusually high completed transaction volume by client, date, and category.

{anomalies.to_markdown(index=False)}

## Business Interpretation

The most important anomaly is the transaction spike involving Client_1004 on 2026-03-15 in the E-commerce category. This may represent a promotional campaign, bot-like behavior, duplicate transaction processing, or a data quality issue. In a real business setting, this would require checking payment logs, client activity history, fraud signals, and operational notes from that date.

## Recommended Actions

1. Review the transaction spike for Client_1004 on 2026-03-15.
2. Confirm whether the spike came from a legitimate campaign or an abnormal system event.
3. Monitor failed and refunded transactions to identify payment issues.
4. Use the dashboard to track daily volume, revenue trends, and client-level performance.
"""

REPORT_PATH.write_text(report, encoding="utf-8")

print("Analysis complete.")
print(f"Report saved to: {REPORT_PATH}")
