from .database import get_db_connection
from .utils.logger import setup_logger

logger = setup_logger()

class User:
    """User model for CRUD operations"""
    
    @staticmethod
    def get_all():
        """Get all users"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM users ORDER BY id;')
            users = cur.fetchall()
            cur.close()
            conn.close()
            logger.info("Retrieved all users")
            return users
        except Exception as e:
            logger.error(f"Error getting all users: {str(e)}")
            raise
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE id = %s;', (user_id,))
            user = cur.fetchone()
            cur.close()
            conn.close()
            if user:
                logger.info(f"Retrieved user with ID: {user_id}")
            else:
                logger.warning(f"User not found with ID: {user_id}")
            return user
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {str(e)}")
            raise
    
    @staticmethod
    def create(name, email):
        """Create new user"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO users (name, email) VALUES (%s, %s) RETURNING *;',
                (name, email)
            )
            user = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            logger.info(f"Created new user: {name} ({email})")
            return user
        except Exception as e:
            logger.error(f"Error creating user {name}: {str(e)}")
            raise
    
    @staticmethod
    def update(user_id, name=None, email=None):
        """Update user"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            if email is not None:
                updates.append("email = %s")
                params.append(email)
            
            if not updates:
                return None
                
            params.append(user_id)
            query = f'UPDATE users SET {", ".join(updates)} WHERE id = %s RETURNING *;'
            
            cur.execute(query, params)
            user = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            
            if user:
                logger.info(f"Updated user with ID: {user_id}")
            else:
                logger.warning(f"User not found for update with ID: {user_id}")
            return user
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {str(e)}")
            raise
    
    @staticmethod
    def delete(user_id):
        """Delete user"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM users WHERE id = %s RETURNING *;', (user_id,))
            user = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            
            if user:
                logger.info(f"Deleted user with ID: {user_id}")
            else:
                logger.warning(f"User not found for deletion with ID: {user_id}")
            return user
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            raise