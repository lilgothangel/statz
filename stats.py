# check win\lose
def is_radiant(match):
    return match['player_slot'] < 128

def is_win(match):
    return is_radiant(match) == match['radiant_win']

# get winrate
def count_wr(matches): #global winrate
    if not matches:
        return 0
    wins = sum(is_win(m) for m in matches)
    return wins/ len(matches) * 100

def wr_side(matches, radiant): #winrate for side
    if not matches:
        return 0

    if radiant:
        wr = sum(is_win(m) and is_radiant(m) for m in matches)
        return wr/sum(is_radiant(m) for m in matches) * 100
    else:
        wr = sum(is_win(m) and not is_radiant(m) for m in matches)
        return wr/sum(not is_radiant(m) for m in matches) * 100



# count KDA
def count_kd(match):
    kda = (match['kills'] + match['assists']) / max(match['deaths'], 1)

    return kda


def avg_time(matches):#average match duration
    return sum(match['duration'] for match in matches) / len(matches)

def avg_kda(matches):#average kda
    return sum(count_kd(m) for m in matches) / len(matches)
