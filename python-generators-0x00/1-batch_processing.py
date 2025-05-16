import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """Generator function to stream rows from the user_data table in batches."""
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

        # Execute the SQL query to select all rows from user_data
        cursor.execute("SELECT * FROM user_data")

        # Fetch and yield rows in batches
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except Error as e:
        print(f"Error: {e}")
    finally:
        # Close the connection if it was established
        if connection and not connection.is_closed():
            connection.close()

def batch_processing(batch_size):
    """Generator function to process each batch and filter users over the age of 25."""
    # Iterate over each batch fetched from the database
    for batch in stream_users_in_batches(batch_size):
        # Iterate over each user in the batch
        for user in batch:
            # Check if the user's age is over 25
            if user['age'] > 25:
                # Yield the user if they meet the condition
                yield user