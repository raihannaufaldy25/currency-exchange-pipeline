SELECT
    e1.quote,
    e1.inverse_rate AS first_rate,
    e2.inverse_rate AS last_rate,
    ROUND(((e2.inverse_rate - e1.inverse_rate) / e1.inverse_rate * 100)::numeric, 2) AS pct_change
FROM exchange_rates e1
JOIN exchange_rates e2 ON e1.quote = e2.quote
WHERE e1.date = (SELECT MIN(date) FROM exchange_rates)
    AND e2.date = (SELECT MAX(date) FROM exchange_rates)
ORDER BY pct_change DESC