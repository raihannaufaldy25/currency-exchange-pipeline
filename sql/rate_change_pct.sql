WITH lagged_rates AS(
    SELECT
        date,
        quote,
        inverse_rate,
        LAG(inverse_rate) OVER(
            PARTITION BY quote
            ORDER BY date
        ) AS prev_inverse_rate
    FROM exchange_rates
)
SELECT
    *,
    ((inverse_rate - prev_inverse_rate) / prev_inverse_rate) * 100 AS pct_change
FROM lagged_rates
ORDER BY quote, date