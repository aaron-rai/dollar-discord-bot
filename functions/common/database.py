"""
DESCRIPTION: Database connection pooling and management service.
Provides proper connection pooling with context managers for safe cursor/connection cleanup.
"""

import logging
import os
import time
from contextlib import contextmanager
from psycopg2 import pool

logger = logging.getLogger("database")


class DatabaseService:
	"""
	Manages PostgreSQL connection pooling with proper resource cleanup.
	Uses context managers to ensure cursors and connections are always closed.
	"""

	def __init__(self):
		"""Initialize the database service (connection pool created on first connect)."""
		self._pool = None
		self._connection_params = {
			"host": os.getenv("DB_HOST", "db"),
			"user": os.getenv("DB_USER"),
			"password": os.getenv("DB_PW"),
			"database": os.getenv("DB_SCHEMA"),
			"minconn": 1,
			"maxconn": 8
		}

	def connect(self, max_retries=5, retry_delay=2):
		"""
		Create connection pool with retry logic.

		Parameters:
		- max_retries (int): Maximum number of connection attempts
		- retry_delay (int): Initial delay between retries (exponential backoff)

		Returns:
		- bool: True if connection successful, False otherwise
		"""
		if self._pool is not None:
			logger.warning("Connection pool already exists. Skipping initialization.")
			return True

		for attempt in range(1, max_retries + 1):
			try:
				logger.info(f"Connecting to database... (attempt {attempt}/{max_retries})")
				self._pool = pool.SimpleConnectionPool(**self._connection_params)

				# Test connection
				with self.get_connection() as conn:
					with self.get_cursor(conn) as cursor:
						cursor.execute("SELECT 1")

				logger.info("Database connection pool initialized successfully.")
				return True

			except Exception as err:
				logger.warning(f"Failed to connect to database (attempt {attempt}/{max_retries}): {err}")
				if attempt < max_retries:
					logger.info(f"Retrying in {retry_delay} seconds...")
					time.sleep(retry_delay)
					retry_delay *= 2  # Exponential backoff
				else:
					logger.error(f"Failed to connect to database after {max_retries} attempts.")
					return False

	@contextmanager
	def get_connection(self):
		"""
		Context manager for database connections.
		Ensures connection is always returned to pool.

		Usage:
			with db_service.get_connection() as conn:
				# Use connection
		"""
		if self._pool is None:
			raise RuntimeError("Database pool not initialized. Call connect() first.")

		conn = None
		try:
			conn = self._pool.getconn()
			yield conn
			conn.commit()  # Auto-commit on successful completion
		except Exception as err:
			if conn:
				conn.rollback()
			logger.error(f"Database error: {err}")
			raise
		finally:
			if conn:
				self._pool.putconn(conn)  # Always return to pool

	@contextmanager
	def get_cursor(self, conn):
		"""
		Context manager for database cursors.
		Ensures cursor is always closed.

		Parameters:
		- conn: Database connection object

		Usage:
			with db_service.get_cursor(conn) as cursor:
				cursor.execute("SELECT ...")
		"""
		cursor = None
		try:
			cursor = conn.cursor()
			yield cursor
		finally:
			if cursor:
				cursor.close()

	def close_pool(self):
		"""Close all connections in the pool."""
		if self._pool:
			self._pool.closeall()
			self._pool = None
			logger.info("Database connection pool closed.")

	def validate_connection(self):
		"""
		Validate that a connection can be established and executed.

		Returns:
		- bool: True if connection is valid, False otherwise
		"""
		try:
			with self.get_connection() as conn:
				with self.get_cursor(conn) as cursor:
					cursor.execute("SELECT 1")
					cursor.fetchone()
			logger.debug("Database connection validated successfully.")
			return True
		except Exception as err:
			logger.error(f"Database validation failed: {err}")
			return False


# Global database service instance
_DB_SERVICE = None


def get_database_service():
	"""
	Get the global database service instance (singleton pattern).

	Returns:
	- DatabaseService: The global database service instance
	"""
	global _DB_SERVICE
	if _DB_SERVICE is None:
		_DB_SERVICE = DatabaseService()
	return _DB_SERVICE


def initialize_database(max_retries=5):
	"""
	Initialize the global database service with retry logic.

	Parameters:
	- max_retries (int): Maximum connection attempts

	Returns:
	- DatabaseService: The initialized database service

	Raises:
	- ConnectionError: If database connection fails after all retries
	"""
	db_service = get_database_service()

	if not db_service.connect(max_retries=max_retries):
		raise ConnectionError(f"Failed to connect to database after {max_retries} attempts. Cannot start bot.")

	return db_service
