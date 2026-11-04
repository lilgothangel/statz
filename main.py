import requests 
import os
from dotenv import load_dotenv

load_dotenv()
ACCOUNT_ID = os.getenv("DOTA_ACCOUNT_ID")

r = requests.get(f'https://api.opendota.com/api/players/{ACCOUNT_ID}/recentMatches')
q = requests.get('https://api.opendota.com/api/heroes')

if not ACCOUNT_ID:
    raise ValueError("DOTA_ACCOUNT_ID не найден в .env")

matches = r.json()
heroes = q.json()


#TODO 
# fix radiant/dire (if player in slot 128 - game doesnt count)xdd -> full rewrite the logic: first determin radiant/dire, then - win/lose
# add hero to best/worst kda
# add avg kda


# len(matches)

# player slot <128 - radiant, >128 - dire

# for match in matches:
#     if match['player_slot'] <128:
#         if match['radiant_win']:
#             print(f'match_id: {match["match_id"]} - win')
#         else:
#             print(f'match_id: {match["match_id"]} - lose')
#     if match['player_slot'] >128:
#         if match['radiant_win']:
#             print(f'match_id: {match["match_id"]} - lose')
#         else:
#             print(f'match_id: {match["match_id"]} - win')


def count_wr():
    win = 0
    
    for match in matches:
        if match['player_slot'] <128:
            if match['radiant_win']:
                win = win + 1
            else:
                pass
        if match['player_slot'] >128:
            if match['radiant_win']:
                pass
            else:
                win= win + 1


    wr = win / len(matches) * 100
    return wr

print(f"Winrate: {count_wr():.2f}%")

def count_kd(match):
    kda = (match['kills'] + match['assists']) / match['deaths', 1]

    return kda

for match in matches:
    print(f'Match {match['match_id']} - KDA {round(count_kd(match), 2)}')

best_match = max(matches, key=count_kd)
# print(best_match)

print(f'Best KDA - {count_kd(best_match):.2f}')

worst_match = min(matches, key = count_kd)

print(f'Worst KDA - {count_kd(worst_match):.2f}')

def avg_time():
    return sum(match['duration'] for match in matches) / len(matches)

minutes, seconds = divmod(round(avg_time()), 60)

# print(minutes)
# print(seconds)

print(f" Avg match time - {minutes}:{seconds:02d} min")

heroes_by_id = {hero['id']: hero for hero in heroes}

for match in matches:
    hero = heroes_by_id.get(match['hero_id'])
    print(hero['localized_name'], match['kills'], match['deaths'], match['assists'])