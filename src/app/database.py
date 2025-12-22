# src/app/database.py
"""
Database connection module.
Manages MySQL database connections using connection pooling.
"""

import mysql.connector
from mysql.connector import pooling, Error
from mysql.connector.pooling import PooledMySQLConnection
from typing import Optional, List, Dict, Any, Tuple
from contextlib import contextmanager
import logging

from app.config import DatabaseConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Singleton database manager that handles connection pooling.
    Provides methods for executing queries and transactions.
    """
    
    _instance: Optional['DatabaseManager'] = None
    _pool: Optional[pooling.MySQLConnectionPool] = None
    
    def __new__(cls):
        """Ensure only one instance exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the database manager (only once)."""
        if self._pool is None:
            self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize the connection pool."""
        try:
            pool_config = DatabaseConfig.get_pool_config()
            self._pool = pooling.MySQLConnectionPool(**pool_config)
            logger.info(f"Database connection pool created successfully: {DatabaseConfig.DATABASE}")
        except Error as e:
            logger.error(f"Failed to create connection pool: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for getting a database connection from the pool.
        
        Usage:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM table")
                results = cursor.fetchall()
        
        Yields:
            PooledMySQLConnection: A database connection from the pool
        """
        connection: Optional[PooledMySQLConnection] = None
        try:
            if self._pool is None:
                raise RuntimeError("Connection pool not initialized")
            
            connection = self._pool.get_connection()
            yield connection
        except Error as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    @contextmanager
    def get_cursor(self, dictionary=True, buffered=True):
        """
        Context manager for getting a cursor with automatic connection management.
        
        Args:
            dictionary: If True, fetch results as dictionaries (default: True)
            buffered: If True, fetch all results immediately (default: True)
        
        Usage:
            with db_manager.get_cursor() as cursor:
                cursor.execute("SELECT * FROM table")
                results = cursor.fetchall()
        
        Yields:
            Cursor: A database cursor
        """
        with self.get_connection() as connection:
            cursor = connection.cursor(dictionary=dictionary, buffered=buffered)
            try:
                yield cursor
                connection.commit()
            except Error as e:
                connection.rollback()
                logger.error(f"Query execution error: {e}")
                raise
            finally:
                cursor.close()
    
    def execute_query(
        self,
        query: str,
        params: Optional[Tuple] = None,
        fetch_one: bool = False,
        fetch_all: bool = True
    ) -> Optional[Any]:
        """
        Execute a SELECT query and return results.
        
        Args:
            query: SQL query string
            params: Query parameters (tuple)
            fetch_one: If True, return only first result
            fetch_all: If True, return all results (default)
        
        Returns:
            Query results (list of dicts, single dict, or None)
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params or ())
                
                if fetch_one:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
                return None
        except Error as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def execute_update(
        self,
        query: str,
        params: Optional[Tuple] = None
    ) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query.
        
        Args:
            query: SQL query string
            params: Query parameters (tuple)
        
        Returns:
            Number of affected rows
        """
        try:
            with self.get_cursor(dictionary=False) as cursor:
                cursor.execute(query, params or ())
                return cursor.rowcount
        except Error as e:
            logger.error(f"Update execution failed: {e}")
            raise
    
    def execute_insert(
        self,
        query: str,
        params: Optional[Tuple] = None
    ) -> int:
        """
        Execute an INSERT query and return the last inserted ID.
        
        Args:
            query: SQL INSERT query string
            params: Query parameters (tuple)
        
        Returns:
            Last inserted row ID
        """
        try:
            with self.get_cursor(dictionary=False) as cursor:
                cursor.execute(query, params or ())
                return cursor.lastrowid
        except Error as e:
            logger.error(f"Insert execution failed: {e}")
            raise
    
    def execute_many(
        self,
        query: str,
        params_list: List[Tuple]
    ) -> int:
        """
        Execute the same query multiple times with different parameters.
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
        
        Returns:
            Number of affected rows
        """
        try:
            with self.get_cursor(dictionary=False) as cursor:
                cursor.executemany(query, params_list)
                return cursor.rowcount
        except Error as e:
            logger.error(f"Batch execution failed: {e}")
            raise
    
    @contextmanager
    def transaction(self):
        """
        Context manager for handling database transactions.
        Automatically commits on success, rolls back on error.
        
        Usage:
            with db_manager.transaction() as cursor:
                cursor.execute("INSERT INTO table VALUES (%s)", (value,))
                cursor.execute("UPDATE table SET field = %s", (new_value,))
        
        Yields:
            Cursor: A database cursor within a transaction
        """
        connection: Optional[PooledMySQLConnection] = None
        cursor = None
        try:
            if self._pool is None:
                raise RuntimeError("Connection pool not initialized")
            
            connection = self._pool.get_connection()
            connection.start_transaction()
            cursor = connection.cursor(dictionary=True)
            
            yield cursor
            
            connection.commit()
            logger.debug("Transaction committed successfully")
        except Error as e:
            if connection:
                connection.rollback()
                logger.warning(f"Transaction rolled back due to error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
    
    def test_connection(self) -> bool:
        """
        Test the database connection.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                logger.info("Database connection test successful")
                return result is not None
        except Error as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def close_pool(self):
        """Close all connections in the pool."""
        if self._pool:
            # Note: mysql.connector doesn't provide a direct way to close the pool
            # Connections will be closed automatically when they're garbage collected
            self._pool = None
            logger.info("Database connection pool closed")


# Global database manager instance
db_manager = DatabaseManager()


# Convenience functions for quick access
def get_connection():
    """Get a database connection from the pool."""
    return db_manager.get_connection()


def get_cursor(dictionary=True, buffered=True):
    """Get a cursor with automatic connection management."""
    return db_manager.get_cursor(dictionary=dictionary, buffered=buffered)


def execute_query(query: str, params: Optional[Tuple] = None, fetch_one: bool = False) -> Optional[Any]:
    """Execute a SELECT query."""
    return db_manager.execute_query(query, params, fetch_one=fetch_one)


def execute_update(query: str, params: Optional[Tuple] = None) -> int:
    """Execute an UPDATE/DELETE query."""
    return db_manager.execute_update(query, params)


def execute_insert(query: str, params: Optional[Tuple] = None) -> int:
    """Execute an INSERT query and return last inserted ID."""
    return db_manager.execute_insert(query, params)


def test_connection() -> bool:
    """Test the database connection."""
    return db_manager.test_connection()
