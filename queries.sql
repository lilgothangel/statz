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
    heroes.localized_name as hero,
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
JOIN heroes on matches.hero_id = heroes.id
GROUP BY heroes.id;

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
JOIN heroes on matches.hero_id = heroes.id
GROUP BY heroes.id
HAVING COUNT(*) >=3
ORDER BY winrate DESC
LIMIT 5;

-- 5 statistics per week
SELECT
    strftime('%G-%V', start_time, 'unixepoch') as week,
    COUNT(*) AS games,
    ROUND(
        100 * AVG((player_slot < 128) = radiant_win), 2
    ) AS winrate,
    ROUND(AVG((kills + assists) * 1.0 / MAX(deaths, 1)), 2) AS avg_kda

FROM matches
GROUP BY week
ORDER BY week;
