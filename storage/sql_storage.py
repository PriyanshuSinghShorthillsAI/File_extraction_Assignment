import sqlite3
from storage.storage import Storage

class SQLStorage(Storage):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extracted_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                content TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for item in data:
            cursor.execute('INSERT INTO extracted_data (type, content) VALUES (?, ?)', ('text', item))
        conn.commit()
        conn.close()
