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

    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
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
        if self.connection:
            self.connection.close()
