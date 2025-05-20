import sqlite3
import functools
from datetime import datetime

def log_queries():
    """
    Decorator to log all SQL queries executed by the decorated function.
    Intercepts cursor.execute() calls to capture queries dynamically.
    """
    def decorator_log_queries(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            query = kwargs.get('query', None)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            if query:
                print(f"[{timestamp}] [SQL LOG] Executing query: {query}")
            else:
                print(f"[{timestamp}] [SQL LOG] No SQL query found to log.")
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_log_queries

@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    for user in users:
        print(user)
