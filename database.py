import os
import psycopg2
from psycopg2.extras import DictCursor
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.conn_params = {
            'dbname': os.getenv('PGDATABASE', 'postgres'),
            'user': os.getenv('PGUSER', 'postgres'),
            'password': os.getenv('PGPASSWORD', 'postgres'),
            'host': os.getenv('PGHOST', 'localhost'),
            'port': os.getenv('PGPORT', '5432')
        }
        self.connection = None
        self.connect()

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(**self.conn_params)
            logger.info("Successfully connected to the database")
        except Exception as e:
            logger.error(f"Error connecting to the database: {str(e)}")
            raise

    def ensure_connection(self):
        """Ensure database connection is active"""
        try:
            # Try a simple query to test connection
            if self.connection and not self.connection.closed:
                cur = self.connection.cursor()
                cur.execute('SELECT 1')
                cur.close()
            else:
                self.connect()
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            logger.warning("Database connection lost, reconnecting...")
            self.connect()

    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            self.ensure_connection()
            with self.connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                try:
                    results = cursor.fetchall()
                    return results
                except psycopg2.ProgrammingError:
                    return None
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            self.connection.rollback()
            raise

    def close(self):
        """Close the database connection"""
        if self.connection and not self.connection.closed:
            self.connection.close()
            logger.info("Database connection closed")