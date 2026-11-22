from api import get_data
from dotenv import load_dotenv
import pandas as pd
import sqlite3
import db
import os
import stats
import charts

pd.set_option('display.precision', 2)

UPDATE_DATA = False   # True - download new matches from OpenDota before analysis
SHOW_SUMMARY = True   # True - print a short stats summary to the console
SUMMARY_MATCHES = 100 # how many latest matches the console summary uses


def show_winrate(df):
    print(f"Winrate: {stats.count_wr(df):.2f}%")
    print(f"Radiant wr: {stats.wr_side(df, True):.2f}%")
    print(f"Dire wr: {stats.wr_side(df, False):.2f}%")


def show_kda(df):
    best_match = df.loc[df['kda'].idxmax()]
    worst_match = df.loc[df['kda'].idxmin()]
    avg_k, avg_d, avg_a = df[['kills', 'deaths', 'assists']].mean()

    print("\nLast 10 matches:")
    print(df[['match_id', 'localized_name', 'kills', 'deaths', 'assists', 'kda']].head(10))
    print()

    print(f"Best KDA - {best_match['localized_name']} - {best_match['kda']:.2f}")
    print(f"Worst KDA - {worst_match['localized_name']} - {worst_match['kda']:.2f}")
    print(f"Average KDA - {stats.avg_kda(df):.2f}")
    print(f"Avg K/D/A - {avg_k:.1f} / {avg_d:.1f} / {avg_a:.1f}")


def show_time(df):
    minutes, seconds = divmod(round(stats.avg_time(df)), 60)

    print(f"Avg match time - {minutes}:{seconds:02d} min")


def show_summary(df):
    print(f"=== Summary (last {len(df)} matches) ===")
    show_winrate(df)
    show_kda(df)
    show_time(df)


if __name__ == "__main__":
    load_dotenv()
    account_id = os.getenv("DOTA_ACCOUNT_ID")

    if not account_id:
        raise ValueError("DOTA_ACCOUNT_ID не найден в .env")

    db_path = f"dota_{account_id}.db"            # separate database for each account
    out_dir = os.path.join("output", account_id)  # separate charts folder for each account

    os.makedirs(out_dir, exist_ok=True)
    conn = sqlite3.connect(db_path)
    db.create_tables(conn)

    if UPDATE_DATA:
        matches, heroes = get_data(account_id) # default - 100 matches. put limit=... for another amount
        db.save_matches(conn, matches)
        db.save_heroes(conn, heroes)

    df = stats.build_df(conn, SUMMARY_MATCHES) # latest matches from the local database

    df_heroes = db.run_query(conn, "hero_stats")
    df_cumulative = db.run_query(conn, "cumulative_wr")
    df_matches = db.run_query(conn, "match_stats")
    df_weekly = db.run_query(conn, "weekly")
    df_side_wr = db.run_query(conn, "side_stats")

    conn.close()

    if SHOW_SUMMARY:
        show_summary(df)

    charts.plot_hero_winrate(df_heroes, out_dir)
    charts.plot_cumulative_wr(df_cumulative, out_dir)
    charts.plot_kda(df_matches, out_dir, 20)
    charts.plot_weekly(df_weekly, out_dir)
    charts.plot_side_winrate(df_side_wr, out_dir)