import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        """Initialize SQLite database connection"""
        self.db_path = Path('instagram_analytics.db')
        self.connection = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            logger.info("Successfully connected to the SQLite database")
        except Exception as e:
            logger.error(f"Error connecting to the database: {str(e)}")
            raise

    def create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            with self.connection:
                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS restaurants (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        handle TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")
            raise

    def ensure_connection(self):
        """Ensure database connection is active"""
        try:
            # Try a simple query to test connection
            if self.connection:
                self.connection.cursor().execute('SELECT 1')
            else:
                self.connect()
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            logger.warning("Database connection lost, reconnecting...")
            self.connect()

    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            self.ensure_connection()
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(query, params or ())
                try:
                    results = cursor.fetchall()
                    return [dict(row) for row in results]
                except sqlite3.OperationalError:
                    return None
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise

    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")