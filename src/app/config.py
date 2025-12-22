# src/app/config.py
"""
Configuration module for database connection settings.
Loads configuration from environment variables or uses defaults.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class DatabaseConfig:
    """Database configuration settings."""
    
    # Database connection settings
    HOST: str = os.getenv("DB_HOST", "localhost")
    PORT: int = int(os.getenv("DB_PORT", "3306"))
    USER: str = os.getenv("DB_USER", "root")
    PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DATABASE: str = os.getenv("DB_NAME", "GarageManagement")
    
    # Connection pool settings
    POOL_NAME: str = "garage_pool"
    POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    POOL_RESET_SESSION: bool = True
    
    # Connection timeout settings (in seconds)
    CONNECTION_TIMEOUT: int = int(os.getenv("DB_CONNECTION_TIMEOUT", "10"))
    
    # Charset
    CHARSET: str = "utf8mb4"
    
    @classmethod
    def get_connection_config(cls) -> Dict[str, Any]:
        """
        Get database connection configuration as a dictionary.
        
        Returns:
            Dictionary with connection parameters for mysql.connector
        """
        return {
            "host": cls.HOST,
            "port": cls.PORT,
            "user": cls.USER,
            "password": cls.PASSWORD,
            "database": cls.DATABASE,
            "charset": cls.CHARSET,
            "connection_timeout": cls.CONNECTION_TIMEOUT,
            "autocommit": False,  # Require explicit commit
        }
    
    @classmethod
    def get_pool_config(cls) -> Dict[str, Any]:
        """
        Get connection pool configuration as a dictionary.
        
        Returns:
            Dictionary with pool parameters for mysql.connector.pooling
        """
        config = cls.get_connection_config()
        config.update({
            "pool_name": cls.POOL_NAME,
            "pool_size": cls.POOL_SIZE,
            "pool_reset_session": cls.POOL_RESET_SESSION,
        })
        return config


# Application configuration
class AppConfig:
    """Application-wide configuration settings."""
    
    # Application metadata
    APP_NAME: str = "Auto Garage Management"
    APP_VERSION: str = "1.0.0"
    
    # Debug mode
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
