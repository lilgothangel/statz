-- 5 statistics per week
SELECT
    strftime('%G-%V', start_time, 'unixepoch') AS week,
    COUNT(*) AS games,
    ROUND(
        100 * AVG((player_slot < 128) = radiant_win), 2
    ) AS winrate,
    ROUND(AVG((kills + assists) * 1.0 / MAX(deaths, 1)), 2) AS avg_kda

FROM matches
GROUP BY week
ORDER BY week;