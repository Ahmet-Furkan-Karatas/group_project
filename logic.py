import sqlite3

deneme = "deneme"

class DatabaseManager:
    def __init__(self, database):
        self.database = database
        self.create_tables()

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS journal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    content TEXT,
                    timestamp TEXT
                )
            ''')

    def add_entry(self, user_id, content, timestamp):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('INSERT INTO journal (user_id, content, timestamp) VALUES (?, ?, ?)', 
                         (user_id, content, timestamp))

    def get_entries(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.execute('SELECT id, content, timestamp FROM journal WHERE user_id = ?', (user_id,))
            return cursor.fetchall()

    def delete_entry(self, user_id, entry_id):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('DELETE FROM journal WHERE user_id = ? AND id = ?', (user_id, entry_id))

    def search_entries(self, user_id, keyword):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.execute(
                'SELECT id, content, timestamp FROM journal WHERE user_id = ? AND content LIKE ?', 
                (user_id, f'%{keyword}%')
            )
            return cursor.fetchall()

    def update_entry(self, user_id, entry_id, new_content):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute(
                'UPDATE journal SET content = ? WHERE user_id = ? AND id = ?', 
                (new_content, user_id, entry_id)
            )

    def get_entry(self, user_id, entry_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.execute('SELECT id, content, timestamp FROM journal WHERE user_id = ? AND id = ?', 
                                  (user_id, entry_id))
            return cursor.fetchone()
