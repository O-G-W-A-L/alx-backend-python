import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator function to stream rows from the user_data table one by one."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='hunter',
            password='pass',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Database Error: {e}")
        yield None

# Make the function available at module level
globals()['stream_users'] = stream_users