-- 2 statistic per side: matches, wins, wr

 SELECT 
    CASE 
        WHEN (player_slot < 128) THEN 'radiant' 
        ELSE 'dire'
    END AS side,  
    COUNT(*) AS matches,

    SUM((player_slot < 128) = radiant_win) AS wins,

        ROUND(
        100 * AVG((player_slot < 128) = radiant_win), 2
    ) AS winrate

 FROM matches
 GROUP BY side
 ORDER BY side DESC;