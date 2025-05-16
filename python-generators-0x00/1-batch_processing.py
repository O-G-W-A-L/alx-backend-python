import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """Generator function to stream rows from the user_data table in batches"""
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
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and not connection.is_closed():
            connection.close()

def batch_processing(batch_size):
    """Function to process each batch and filter users over the age of 25"""
    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user['age'] > 25]
        for user in filtered_users:
            yield user