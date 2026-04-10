import sqlite3


class Database:
    def __init__(self, db_path: str = "duplicates.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS files (
                path TEXT PRIMARY KEY,
                hash TEXT NOT NULL
            )""")

    def save(self, file_path: str, hash_value: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO files (path, hash) VALUES (?, ?)", (file_path, hash_value))

    def get_hash(self, file_path: str) -> str | None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT hash FROM files WHERE path = ?", (file_path,))
            row = cursor.fetchone()
            return row[0] if row else None
