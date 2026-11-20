-- 1 general statistic about account(games, wr, avg kills, deaths, assists, duration)

SELECT COUNT(*) AS games,
    
    ROUND(
        100 * AVG((player_slot < 128) = radiant_win), 2
    ) AS winrate,

    ROUND(AVG(kills), 2) AS avg_kills,
    ROUND(AVG(deaths), 2) AS avg_deaths,
    ROUND(AVG(assists), 2) AS avg_assists,

    ROUND(AVG(duration)/60.0, 2) AS avg_duration

FROM matches;