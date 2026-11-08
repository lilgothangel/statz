import pandas as pd

#prepare data
def build_df(matches, heroes):
    df = pd.DataFrame(matches)
    heroes_df = pd.DataFrame(heroes)[['id', 'localized_name']]


    df = df.merge(heroes_df, how='left', left_on='hero_id', right_on='id')
    df = df.drop(columns=['id', 'version'])



    df['is_radiant'] = df['player_slot'] < 128 #check player side
    df['is_win'] = df['is_radiant'] == df['radiant_win'] #win\lose

    df['kda'] = (df['kills'] + df['assists'])/df['deaths'].clip(1)


    return df


# get winrate
def count_wr(df): #global winrate
    return df['is_win'].mean() * 100

def wr_side(df, radiant): #winrate for side
    side = df[df['is_radiant'] == radiant]
    if side.empty:
        return 0
    return side['is_win'].mean() * 100


def avg_time(df):#average match duration
    return df['duration'].mean()

def avg_kda(df):#average kda
    return df['kda'].mean()
