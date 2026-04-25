-- KPI Query 1: Overall transaction summary

SELECT
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN status = 'Completed' THEN amount ELSE 0 END) AS completed_revenue,
    ROUND(100.0 * SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS failed_transaction_rate,
    ROUND(100.0 * SUM(CASE WHEN status = 'Refunded' THEN 1 ELSE 0 END) / COUNT(*), 2) AS refund_rate
FROM transactions;


-- KPI Query 2: Revenue by category

SELECT
    category,
    COUNT(*) AS transaction_count,
    ROUND(SUM(CASE WHEN status = 'Completed' THEN amount ELSE 0 END), 2) AS completed_revenue
FROM transactions
GROUP BY category
ORDER BY completed_revenue DESC;


-- KPI Query 3: Top clients by completed revenue

SELECT
    client_id,
    COUNT(*) AS transaction_count,
    ROUND(SUM(CASE WHEN status = 'Completed' THEN amount ELSE 0 END), 2) AS completed_revenue
FROM transactions
GROUP BY client_id
ORDER BY completed_revenue DESC
LIMIT 10;


-- KPI Query 4: Daily transaction trend

SELECT
    transaction_date,
    COUNT(*) AS transaction_count,
    ROUND(SUM(CASE WHEN status = 'Completed' THEN amount ELSE 0 END), 2) AS completed_revenue
FROM transactions
GROUP BY transaction_date
ORDER BY transaction_date;
