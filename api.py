import requests 
import os
from dotenv import load_dotenv

def request_check(resp):
    if not resp.ok:
        raise SystemExit(f"Exception: {resp.status_code}")

def get_data(limit=100):

    load_dotenv()
    ACCOUNT_ID = os.getenv("DOTA_ACCOUNT_ID")

    if not ACCOUNT_ID:
        raise ValueError("DOTA_ACCOUNT_ID не найден в .env")


    try:
        r = requests.get(f'https://api.opendota.com/api/players/{ACCOUNT_ID}/matches', params={'limit': limit}, timeout=10)
        q = requests.get('https://api.opendota.com/api/heroes', timeout=10)
    except requests.exceptions.RequestException as e: 
        raise SystemExit(f"Network error: {e}")


    request_check(r)
    request_check(q)



    matches = r.json()
    heroes = q.json()

    return matches, heroes