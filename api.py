import requests

def request_check(resp):
    if not resp.ok:
        raise SystemExit(f"Exception: {resp.status_code}")

def get_data(account_id, limit=100):

    try:
        r = requests.get(f'https://api.opendota.com/api/players/{account_id}/matches', params={'limit': limit}, timeout=30)
        q = requests.get('https://api.opendota.com/api/heroes', timeout=10)
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Network error: {e}")


    request_check(r)
    request_check(q)



    matches = r.json()
    heroes = q.json()

    return matches, heroes