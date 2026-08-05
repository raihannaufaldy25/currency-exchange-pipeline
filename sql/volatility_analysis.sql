SELECT
    quote,
    ROUND((STDDEV(inverse_rate) / AVG(inverse_rate))::numeric, 4) AS coefficient_of_variation
FROM exchange_rates
GROUP BY quote
ORDER BY coefficient_of_variation DESC
