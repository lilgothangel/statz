# TODO — Dota 2 Stats Tracker

## 1. Fix what already exists
- [x] Fix `count_kd`: `match['deaths', 1]` → `max(match['deaths'], 1)` (crashed with KeyError)
- [x] Move the `if not ACCOUNT_ID` check BEFORE the API requests
- [x] Rewrite the radiant/dire logic: first detect the side (`player_slot < 128` → radiant, otherwise dire), then win/lose — in one function `is_win(match)`
- [x] Check `r.status_code` and handle API errors (timeout, 429, empty response)
- [x] Remove old commented-out code

## 2. Finish the metrics
- [x] Add the hero to best/worst KDA
- [x] Add average KDA
- [x] Winrate by hero (games, wins, WR%)
- [x] Average kills / deaths / assists
- [ ] GPM / XPM (not returned by `/matches` by default — needs the `project` parameter)
- [x] Radiant vs Dire winrate

## 3. Move to pandas
- [x] Load matches into a DataFrame, merge with heroes on `hero_id`
- [x] Calculate all metrics from block 2 with pandas (groupby, agg) instead of loops
- [x] Switch from `/recentMatches` (20 games) to `/matches?limit=100+` to have enough data to analyze

## 4. Add SQL
- [x] Store matches and heroes in SQLite (`matches`, `heroes`)
- [x] Don't duplicate already saved matches (PRIMARY KEY on `match_id`)
- [x] Move the main metrics into SQL queries (`sql/*.sql`): WR by hero, top heroes, weekly dynamics
- [x] At least one query with JOIN, one with GROUP BY + HAVING, one with a window function

## 5. Visualization
- [x] Charts (matplotlib): winrate by hero, cumulative winrate, KDA over time, side winrate, weekly winrate
- [x] Save charts to `output/`
- [ ] Match duration distribution chart
- [ ] (bonus) Dashboard in Tableau Public on exported CSV

## 6. Portfolio polish
- [x] Split the code into modules: `api.py`, `db.py`, `stats.py`, `charts.py`, `main.py`
- [x] `requirements.txt`
- [x] README in English: what it does, stack, how to run, chart screenshots, key findings
- [ ] Repo description and pin on the profile

## 7. Extra features
- [x] Multiple accounts: separate database and charts folder for each account ID
- [x] `UPDATE_DATA` flag to work offline with the local database
- [x] Short stats summary in the console (`SHOW_SUMMARY`)
- [x] Databricks version: Spark SQL and PySpark notebooks, results cross-checked against SQLite + pandas