import sqlite3
from typing import Dict, List, Optional
import os

DB_PATH = "data/atlas.db"

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def insert_document(doc: Dict):
    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO documents (id, user_id, title, file_type, source_path, page_count, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (doc['id'], doc.get('user_id', 'user_1'), doc['title'], doc['file_type'], doc['source_path'], doc.get('page_count', 1), doc.get('status', 'ingesting')))
        conn.commit()
    finally:
        conn.close()

def update_document_status(doc_id: str, status: str, chunk_count: int = 0):
    conn = get_db_connection()
    try:
        conn.execute("UPDATE documents SET status = ?, chunk_count = ? WHERE id = ?", (status, chunk_count, doc_id))
        conn.commit()
    finally:
        conn.close()

def insert_chunks(chunks: List[Dict]):
    conn = get_db_connection()
    try:
        conn.executemany("""
            INSERT INTO chunks (chunk_id, doc_id, text_content, chunk_index)
            VALUES (?, ?, ?, ?)
        """, [(c['chunk_id'], c['doc_id'], c['text_content'], c['chunk_index']) for c in chunks])
        conn.commit()
    finally:
        conn.close()

def get_chunks_by_ids(chunk_ids: List[str]) -> Dict[str, str]:
    if not chunk_ids:
        return {}
    conn = get_db_connection()
    try:
        placeholders = ','.join('?' * len(chunk_ids))
        cursor = conn.execute(f"SELECT chunk_id, text_content FROM chunks WHERE chunk_id IN ({placeholders})", chunk_ids)
        return {row['chunk_id']: row['text_content'] for row in cursor.fetchall()}
    finally:
        conn.close()

def get_all_documents():
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT * FROM documents ORDER BY ingested_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()
        
def get_stats():
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT COUNT(*) as doc_count FROM documents")
        doc_count = cursor.fetchone()['doc_count']
        cursor = conn.execute("SELECT COUNT(*) as chunk_count FROM chunks")
        chunk_count = cursor.fetchone()['chunk_count']
        return {"doc_count": doc_count, "chunk_count": chunk_count}
    except:
        return {"doc_count": 0, "chunk_count": 0}
    finally:
        conn.close()
