from api import get_data
import pandas as pd
import sqlite3
import db
import os
import stats
import charts

pd.set_option('display.precision', 2)


def show_winrate(df):
    print(f"Winrate: {stats.count_wr(df):.2f}%")
    print(f"Radiant wr: {stats.wr_side(df, True):.2f}%")
    print(f"Dire wr: {stats.wr_side(df, False):.2f}%")


def show_kda(df):
    best_match = df.loc[df['kda'].idxmax()]
    worst_match = df.loc[df['kda'].idxmin()]


    print(df[['match_id', 'localized_name', 'kills', 'deaths', 'assists', 'kda']])


    print(f'Best KDA - {best_match['localized_name']} - {best_match['kda']:.2f}')

    print(f'Worst KDA - {worst_match['localized_name']} - {worst_match['kda']:.2f}')

    print(f"Average KDA - {stats.avg_kda(df):.2f}") 


def show_time(df): 
    minutes, seconds = divmod(round(stats.avg_time(df)), 60)

    print(f"Avg match time - {minutes}:{seconds:02d} min")

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    conn = sqlite3.connect('dota.db')
    db.create_tables(conn)

    # matches, heroes = get_data() #default - 100 matches. put in () another amount
    # db.save_matches(conn, matches)
    # db.save_heroes(conn, heroes)


    df_stats = stats.build_df(conn, 100) #get the stats from OpenDota

    df_heroes = db.run_query(conn, "hero_stats")
    df_cumulative = db.run_query(conn, "cumulative_wr")
    df_matches = db.run_query(conn, "match_stats")
    df_weekly = db.run_query(conn, "weekly")
    df_side_wr = db.run_query(conn, "side_stats")

    conn.close()

    # print(df[['kills', 'deaths', 'assists']].mean())

    # show_winrate(df)
    # show_kda(df)
    # show_time(df)

    # print(df_matches.head())
    # print(df_heroes)


    heroes_chart = charts.plot_hero_winrate(df_heroes)
    cumulative_chart = charts.plot_cumulative_wr(df_cumulative, 100)
    kda_chart = charts.plot_kda(df_matches, 20)
    weekly_chart = charts.plot_weekly(df_weekly)
    side_wr_chart = charts.plot_side_winrate(df_side_wr)