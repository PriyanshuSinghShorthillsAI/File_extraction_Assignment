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
        """Save extracted data based on its type."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if data_type == 'table':
            # Convert the list of tables into a string format to store in the database
            for table in data:
                table_content = "\n".join(["\t".join(row) for row in table])  # Create tab-separated rows
                cursor.execute('INSERT INTO extracted_data (type, content) VALUES (?, ?)', (data_type, table_content))
        else:
            # Save text, images, and URLs normally
            for item in data:
                cursor.execute('INSERT INTO extracted_data (type, content) VALUES (?, ?)', (data_type, item))

        conn.commit()
        conn.close()

