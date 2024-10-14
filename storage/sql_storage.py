
"""
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
        """

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

    def save(self, data, data_type: str):
        """
        Save extracted data to SQLite.
        data_type can be 'text', 'image', 'url', or 'table'.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if data_type == 'text':
            for item in data:
                cursor.execute('INSERT INTO extracted_data (type, content) VALUES (?, ?)', (data_type, item))
        
        elif data_type == 'url':
            for url in data:
                cursor.execute('INSERT INTO extracted_data (type, content) VALUES (?, ?)', (data_type, url))
        
        elif data_type == 'table':
            # Assuming tables are stored as a list of CSV strings
            for table in data:
                cursor.execute('INSERT INTO extracted_data (type, content) VALUES (?, ?)', (data_type, table.to_csv()))
        
        elif data_type == 'image':
            # Image saving is more complex, you may want to store image paths instead of binary data
            for image in data:
                cursor.execute('INSERT INTO extracted_data (type, content) VALUES (?, ?)', (data_type, 'Image saved'))
        
        conn.commit()
        conn.close()
