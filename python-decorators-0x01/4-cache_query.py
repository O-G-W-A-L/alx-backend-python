import time
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    """
    Decorator to create a database connection and close it after use
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """
    Decorator to cache the result of a function call
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query in query_cache:
            print("Using cached result.")
            return query_cache[query]
        
        print("Query not cached. Fetching from database...")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print("Query result cached.")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
for user in users:
    print(user)

print("------------")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
for user in users_again:
    print(user)
