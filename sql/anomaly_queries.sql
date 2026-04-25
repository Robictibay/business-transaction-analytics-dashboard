-- Anomaly Query 1: Daily transaction volume spike detection

WITH daily_counts AS (
    SELECT
        transaction_date,
        COUNT(*) AS daily_transaction_count
    FROM transactions
    GROUP BY transaction_date
),
stats AS (
    SELECT
        AVG(daily_transaction_count) AS avg_daily_count,
        2.0 * (
            AVG(daily_transaction_count * daily_transaction_count) 
            - AVG(daily_transaction_count) * AVG(daily_transaction_count)
        ) AS variance_component
    FROM daily_counts
)
SELECT
    d.transaction_date,
    d.daily_transaction_count,
    ROUND(s.avg_daily_count, 2) AS average_daily_count,
    CASE
        WHEN d.daily_transaction_count > s.avg_daily_count + s.variance_component THEN 'Potential Spike'
        ELSE 'Normal'
    END AS anomaly_flag
FROM daily_counts d
CROSS JOIN stats s
ORDER BY d.daily_transaction_count DESC;


-- Anomaly Query 2: Client-level transaction spike

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
