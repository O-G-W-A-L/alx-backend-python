#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

class StreamUsers:
    def __call__(self):
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

stream_users = StreamUsers()