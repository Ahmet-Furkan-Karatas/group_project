# logic.py
import sqlite3
from datetime import datetime
from config import DATABASE

class DatabaseManager:
    def __init__(self, database=DATABASE):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    user_name TEXT
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS gunlukler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    entry TEXT,
                    entry_date TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            ''')

    def add_user(self, user_id, user_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            if not cur.fetchone():
                conn.execute("INSERT INTO users (user_id, user_name) VALUES (?, ?)", (user_id, user_name))

    def add_entry(self, user_id, entry):
        entry_date = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute("INSERT INTO gunlukler (user_id, entry, entry_date) VALUES (?, ?, ?)", (user_id, entry, entry_date))

    def get_entries(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT entry_date, entry FROM gunlukler WHERE user_id = ? ORDER BY id DESC", (user_id,))
            return cur.fetchall()
