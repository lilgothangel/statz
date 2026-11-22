-- stats for each match
SELECT
    match_id,
    strftime('%Y-%m-%d', start_time, 'unixepoch') AS day,
    ((player_slot < 128) = radiant_win) as win,
    ROUND((kills + assists) * 1.0 / MAX(deaths, 1), 2) AS kda,
    ROUND(duration/60.0, 2) AS duration_min
FROM matches
ORDER BY start_time DESC;