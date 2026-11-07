import requests 
import os
from dotenv import load_dotenv

load_dotenv()
ACCOUNT_ID = os.getenv("DOTA_ACCOUNT_ID")

if not ACCOUNT_ID:
    raise ValueError("DOTA_ACCOUNT_ID не найден в .env")

def request_check(resp):
    if not resp.ok:
        raise SystemExit(f"Exeption: {resp.status_code}")
try:
    r = requests.get(f'https://api.opendota.com/api/players/{ACCOUNT_ID}/recentMatches', timeout=10)
    q = requests.get('https://api.opendota.com/api/heroes', timeout=10)
except requests.exceptions.RequestException as e: 
    raise SystemExit(f"Network error: {e}")

request_check(r)
request_check(q)



matches = r.json()
heroes = q.json()



# check win\lose
def is_radiant(match):
    return match['player_slot'] < 128

def is_win(match):
    return is_radiant(match) == match['radiant_win']

def count_wr():
    if not matches:
        return 0
    wins = sum(is_win(m) for m in matches)
    return wins/ len(matches) * 100

print(f"Winrate: {count_wr():.2f}%")


# count KDA
def count_kd(match):
    kda = (match['kills'] + match['assists']) / max(match['deaths'], 1)

    return kda

for match in matches:
    print(f'Match {match['match_id']} - KDA {round(count_kd(match), 2)}')

best_match = max(matches, key=count_kd)
# print(best_match)
heroes_by_id = {hero['id']: hero for hero in heroes}
hero = heroes_by_id.get(match['hero_id'])

print(f'Best KDA - {hero['localized_name']} - {count_kd(best_match):.2f}')

worst_match = min(matches, key = count_kd)

print(f'Worst KDA - {hero['localized_name']} - {count_kd(worst_match):.2f}')

def avg_time():
    return sum(match['duration'] for match in matches) / len(matches)



print(f"Average KDA - { (count_kd(best_match) + count_kd(worst_match)) /2 :.2f}")

minutes, seconds = divmod(round(avg_time()), 60)

# print(minutes)
# print(seconds)

print(f"Avg match time - {minutes}:{seconds:02d} min")


print("HERO K D A")
for match in matches:
    print(hero['localized_name'], match['kills'], match['deaths'], match['assists'])


