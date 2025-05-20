import sqlite3
import functools

DB_NAME = 'users.db'

def with_db_connection(func):
    """
    Decorator that handles opening and closing the SQLite database connection.
    Passes the open connection as the first argument to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_NAME)
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetch a user by ID using the provided database connection.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# ---- Test the decorator in action ----
user = get_user_by_id(user_id=1)
print(user)
