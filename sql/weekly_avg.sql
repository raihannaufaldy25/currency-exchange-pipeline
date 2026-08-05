SELECT
    DATE_TRUNC('week', date) AS week_start,
    quote,
    ROUND(AVG(inverse_rate)::numeric, 2) AS avg_weekly_rate
FROM exchange_rates
GROUP BY DATE_TRUNC('week', date), quote
ORDER BY week_start, quote