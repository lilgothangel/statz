from api import get_data
import stats
import pandas as pd
import sqlite3
import db


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
    conn = sqlite3.connect('dota.db')
    db.create_tables(conn)

    matches, heroes = get_data() #default - 100 matches. put in () another amount
    db.save_matches(conn, matches)
    db.save_heroes(conn, heroes)


    df = stats.build_df(conn, 20)
    conn.close()


    show_winrate(df)
    show_kda(df)
    show_time(df)