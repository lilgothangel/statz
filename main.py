from api import get_data
import stats
import pandas as pd

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
    matches, heroes = get_data(20) #default - 100 matches. put in () another amount

    df = stats.build_df(matches, heroes)

    # print(df.round(2).head())


    show_winrate(df)
    show_kda(df)
    show_time(df)