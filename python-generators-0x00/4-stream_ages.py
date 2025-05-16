import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    """Generator function to stream user ages one by one."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='hunter',
            password='pass',
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        while True:
            age = cursor.fetchone()
            if age is None:
                break
            yield age[0]

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and not connection.is_closed():
            connection.close()

def calculate_average_age():
    """Function to calculate the average age using the generator."""
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    if count == 0:
        return 0
    return total / count
average_age = calculate_average_age()
print(f"Average age of users: {average_age}")