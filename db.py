import sqlite3

def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            match_id    INTEGER PRIMARY KEY,
            hero_id     INTEGER,
            player_slot INTEGER,
            radiant_win INTEGER,
            kills       INTEGER,
            deaths      INTEGER,
            assists     INTEGER,
            duration    INTEGER,
            start_time  INTEGER
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS heroes (
            id              INTEGER PRIMARY KEY,
            localized_name  TEXT
        )
    """)

    conn.commit()


def save_matches(conn, matches):
    rows = [
        (m['match_id'], m['hero_id'], m['player_slot'], m['radiant_win'], m['kills'], m['deaths'], m['assists'], m['duration'], m['start_time']) 
        for m in matches
    ]

    conn.executemany("""
        INSERT OR IGNORE INTO matches
            (match_id, hero_id, player_slot, radiant_win, kills, deaths, assists, duration, start_time)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, rows)

    conn.commit()


def save_heroes(conn, heroes):
    rows = [
        (h['id'], h['localized_name']) for h in heroes
    ]

    conn.executemany("""
        INSERT OR IGNORE INTO heroes
            (id, localized_name)
        VALUES (?,?)
    """, rows)

    conn.commit()