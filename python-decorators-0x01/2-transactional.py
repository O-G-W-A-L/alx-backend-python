import sqlite3
import functools

def with_db_connection(func):
    """
    Opens and closes the database connection automatically.
    Passes the connection as the first argument.
    """
    @functools.wraps(func)
        conn = sqlite3.connect("database.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def transactional(func):
    """
    Manages transactions for database operations.
    Commits if successful, rolls back if an exception is raised.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback() 
            raise e
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

@with_db_connection
def fetch_user(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()
try:
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("User email updated successfully!")
except Exception as e:
    print(f"Failed to update user: {e}")

#  Display updated user data
user = fetch_user(user_id=1)
print("Updated user:", user)
