import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
account_id = os.getenv("DOTA_ACCOUNT_ID")

conn = sqlite3.connect(f"dota_{account_id}.db")
pd.read_sql("SELECT * FROM matches", conn).to_csv("matches.csv", index=False)
pd.read_sql("SELECT * FROM heroes", conn).to_csv("heroes.csv", index=False)
conn.close()