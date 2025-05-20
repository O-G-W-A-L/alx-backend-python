import time
import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator to create a database connection and close it after use
    This decorator wraps a function that requires a database connection
    and ensures that the connection is opened before the function call
    and closed after the function call, even if an exception occurs.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("database.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator to retry a function call on failure
    This decorator retries the decorated function if it raises an exception.
    It will retry the specified number of times with a delay between attempts.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f"Attempt {attempt}...")
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Error: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            print("All retry attempts failed.")
            raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
    
#### attempt to fetch users with automatic retry on failure
try:
    users = fetch_users_with_retry()
    print(" Users fetched successfully!")
    for user in users:
        print(user)
except Exception as e:
    print(f"Final failure: {e}")
