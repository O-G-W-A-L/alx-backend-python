import mysql.connector
from mysql.connector import Error
import sys

def stream_users():
    """Generator function to stream rows from the user_data table one by one."""
    connection = None
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

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

sys.modules[__name__] = stream_users
