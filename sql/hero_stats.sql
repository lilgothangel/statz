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
ORDER BY hero