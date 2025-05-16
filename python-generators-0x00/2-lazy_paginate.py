import mysql.connector
from mysql.connector import Error

def paginate_users(page_size, offset):
    """Function to fetch a specific page of users from the database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='hunter',
            password='pass',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection and not connection.is_closed():
            connection.close()

def lazy_pagination(page_size):
    """Generator function to lazily load paginated data from the user_data table."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
    return