import psycopg2
from psycopg2.extras import RealDictCursor
import os
from .utils.logger import setup_logger

logger = setup_logger()

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(
            os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/microservice'),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

def init_db(app):
    """Initialize database connection"""
    try:
        with app.app_context():
            conn = get_db_connection()
            conn.close()
            logger.info("Database connection established successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise