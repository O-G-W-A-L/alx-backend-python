import mysql.connector
from mysql.connector import Error

def paginate_users(page_size, offset):
    """Function to fetch a specific page of users from the database."""
    connection = None
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='hunter',
            password='pass',
            database='ALX_prodev'
        )

        # Create a cursor object to interact with the database
        cursor = connection.cursor(dictionary=True)

        # Execute the SQL query to select a page of rows from user_data
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")

        # Fetch all rows for the current page
        rows = cursor.fetchall()

        return rows

    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        # Close the connection if it was established
        if connection and not connection.is_closed():
            connection.close()

def lazy_pagination(page_size):
    """Generator function to lazily load paginated data from the user_data table."""
    offset = 0
    while True:
        # Fetch the current page of users
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        # Increment the offset for the next page
        offset += page_size
    return