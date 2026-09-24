"""
Database connection manager supporting both PostgreSQL and local SQLite.
Seamlessly falls back to SQLite when PostgreSQL server is not configured or offline.
"""

import os
import sqlite3
from typing import List, Dict, Any, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
SQLITE_DB_PATH = os.getenv("ENTERPRISE_DB_PATH") or os.path.join(DATA_DIR, "enterprise.db")
DATABASE_URL = os.getenv("DATABASE_URL", "")


class DatabaseManager:
    def __init__(self, db_path: str = SQLITE_DB_PATH, pg_url: str = DATABASE_URL):
        self.db_path = db_path
        self.pg_url = pg_url
        self.is_postgres = False
        self._check_driver()

    def _check_driver(self):
        if self.pg_url and ("postgresql://" in self.pg_url or "postgres://" in self.pg_url):
            try:
                import psycopg2
                # Test connection
                conn = psycopg2.connect(self.pg_url)
                conn.close()
                self.is_postgres = True
                print("Connected successfully to PostgreSQL database.")
                return
            except Exception as e:
                print(f"PostgreSQL connection failed ({e}). Falling back to local SQLite.")

        self.is_postgres = False

    def get_connection(self):
        if self.is_postgres:
            import psycopg2
            import psycopg2.extras
            return psycopg2.connect(self.pg_url, cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn

    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a read-only SELECT query safely and return dictionary rows."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        finally:
            cursor.close()
            conn.close()

    def execute_commit(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an INSERT/UPDATE/DELETE query with commit."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    def init_schema(self, schema_sql: str):
        """Initialize database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if self.is_postgres:
                cursor.execute(schema_sql)
            else:
                cursor.executescript(schema_sql)
            conn.commit()
        finally:
            cursor.close()
            conn.close()


# Singleton
_db_instance = None

def get_db() -> DatabaseManager:
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance
