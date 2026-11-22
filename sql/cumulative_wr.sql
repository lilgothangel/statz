-- 6.5 better way to write ts
SELECT
    strftime('%Y-%m-%d', start_time, 'unixepoch') AS day,
    (player_slot < 128) = radiant_win AS is_win,

    SUM((player_slot < 128) = radiant_win) OVER w AS wins_so_far,
    COUNT(*) OVER w AS games_so_far,

    ROUND(
        100.0 * SUM((player_slot < 128) = radiant_win) OVER w
        / COUNT(*) OVER w,
        2
    ) AS cumulative_winrate

FROM matches

WINDOW w AS (
    ORDER BY start_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)

ORDER BY start_time DESC;