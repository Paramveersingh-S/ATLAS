import sqlite3

def init_db(db_path: str):
    schema = """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        settings_json TEXT DEFAULT '{}'
    );
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL REFERENCES users(id),
        title TEXT NOT NULL,
        file_type TEXT NOT NULL,
        source_path TEXT,
        source_url TEXT,
        page_count INTEGER,
        word_count INTEGER,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        chunk_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'ingesting',
        error_message TEXT,
        metadata_json TEXT DEFAULT '{}'
    );
    CREATE TABLE IF NOT EXISTS chunks (
        chunk_id TEXT PRIMARY KEY,
        doc_id TEXT NOT NULL REFERENCES documents(id),
        text_content TEXT NOT NULL,
        chunk_index INTEGER
    );
    """
    import os
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.executescript(schema)
    conn.close()
    print("DB initialized")

if __name__ == "__main__":
    init_db("data/atlas.db")
