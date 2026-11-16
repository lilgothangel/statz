SELECT sqlite_version();

-- 1 general statistic about account(games, wr, avg kills, deaths, assists, duration)
SELECT COUNT(*) AS games,
    
    ROUND(
        100 * AVG(
            CASE 
                WHEN (player_slot < 128 AND radiant_win = 1) 
                OR (player_slot >= 128 AND radiant_win = 0)
                THEN 1
                ELSE 0
            END
        ), 2
    ) AS winrate,

    ROUND(AVG(kills), 2) AS avg_kills,
    ROUND(AVG(deaths), 2) AS avg_deaths,
    ROUND(AVG(assists), 2) AS avg_assists,

    ROUND(AVG(duration)/60.0, 2) AS avg_duration

FROM matches;

-- 1.5 second option to write 1
-- SELECT COUNT(*) AS games,
    
--     ROUND(
--         100 * AVG((player_slot < 128) = radiant_win), 2
--     ) AS winrate,

--     ROUND(AVG(kills), 2) AS avg_kills,
--     ROUND(AVG(deaths), 2) AS avg_deaths,
--     ROUND(AVG(assists), 2) AS avg_assists,

--     ROUND(AVG(duration)/60.0, 2) AS avg_duration

-- FROM matches;

-- 2 statistic per side: matches, wins, wr
SELECT 
    CASE 
        WHEN (player_slot < 128) THEN 'radiant' 
        ELSE 'dire'
    END AS side,  
    COUNT(*) AS matches,

    SUM(
        CASE 
            WHEN (player_slot < 128 AND radiant_win = 1) 
            OR (player_slot >= 128 AND radiant_win = 0)
            THEN 1
            ELSE 0
        END
    ) AS wins,

        ROUND(
        100 * AVG(
            CASE 
                WHEN (player_slot < 128 AND radiant_win = 1) 
                OR (player_slot >= 128 AND radiant_win = 0)
                THEN 1
                ELSE 0
            END
        ), 2
    ) AS winrate

 FROM matches
 GROUP BY side
 ORDER BY side DESC;

 -- 2.5 second option to write 2
--  SELECT 
--     CASE 
--         WHEN (player_slot < 128) THEN 'radiant' 
--         ELSE 'dire'
--     END AS side,  
--     COUNT(*) AS matches,

--     SUM((player_slot < 128) = radiant_win) AS wins,

--         ROUND(
--         100 * AVG((player_slot < 128) = radiant_win), 2
--     ) AS winrate

--  FROM matches
--  GROUP BY side
--  ORDER BY side DESC;

-- 3 player statistic per hero
SELECT 
    heroes.localized_name AS hero,
    COUNT(*) AS games,
    SUM((player_slot < 128) = radiant_win) AS wins,
    ROUND(
        100 * AVG((player_slot < 128) = radiant_win), 2
    ) AS winrate,

    ROUND(AVG(kills), 2) AS avg_kills,
    ROUND(AVG(deaths), 2) AS avg_deaths,
    ROUND(AVG(assists), 2) AS avg_assists,
    ROUND(AVG((kills + assists) * 1.0 / MAX(deaths, 1)), 2) AS avg_kda

FROM matches
JOIN heroes ON matches.hero_id = heroes.id
GROUP BY heroes.id
ORDER BY hero;

-- 4 best heroes
SELECT 

    heroes.localized_name AS hero,
    COUNT(*) AS games,
    SUM((player_slot < 128) = radiant_win) AS wins,
    ROUND(
        100 * AVG((player_slot < 128) = radiant_win), 2
    ) AS winrate,
    ROUND(AVG((kills + assists) * 1.0 / MAX(deaths, 1)), 2) AS avg_kda

FROM matches
JOIN heroes ON matches.hero_id = heroes.id
GROUP BY heroes.id
HAVING COUNT(*) >=3
ORDER BY winrate DESC, games ASC
LIMIT 5;

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

-- 6 winrate change after each game (window func)
SELECT 
    strftime('%Y-%m-%d', start_time, 'unixepoch') AS day,
    (player_slot < 128) = radiant_win AS is_win,

    SUM((player_slot < 128) = radiant_win) OVER(ORDER BY start_time) AS wins_so_far,

    COUNT(*) OVER(ORDER BY start_time) AS games_so_far,

    ROUND(
        100.0 * SUM((player_slot < 128) = radiant_win) OVER(ORDER BY start_time) / COUNT(*) OVER(ORDER BY start_time), 2
    ) AS cumulative_winrate
FROM matches
ORDER BY start_time;

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

ORDER BY start_time;

-- 7 CTE (stats per hero)
WITH match_stats AS(
    SELECT 
        strftime('%Y-%m', start_time, 'unixepoch') AS day,
        hero_id,
        ((player_slot < 128) = radiant_win) AS win,
        (kills + assists) * 1.0 / MAX(deaths, 1) AS kda
    FROM matches
)

SELECT 

    heroes.localized_name AS hero,
    COUNT(*) AS games,
    SUM(win) AS wins,
    ROUND(AVG(win) * 100.0, 2) AS winrate,
    ROUND(AVG(kda), 2) AS avg_kda

FROM match_stats
JOIN heroes ON match_stats.hero_id = heroes.id
GROUP BY hero_id;

-- 7.2 just playing with CTE (stats per week)
WITH week_stats AS(
    SELECT 
        strftime('%G-%V', start_time, 'unixepoch') AS week,
        ((player_slot < 128) = radiant_win) AS is_win,
        (kills + assists) * 1.0 / MAX(deaths, 1) AS kda
    FROM matches
)

SELECT 
    week,
    COUNT(*) AS games,
    SUM(is_win) AS wins,
    ROUND(AVG(is_win) * 100.0, 2) AS winrate,
    ROUND(AVG(kda), 2) AS avg_kda
FROM week_stats
GROUP BY week
ORDER BY week;