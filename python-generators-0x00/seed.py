"""a generator that streams rows from an SQL database one by one
"""

import mysql.connector
from mysql.connector import Error
import mariadb.connector
import csv

def connect_db():
    """create a connection to the databse
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
        )
        return connection
    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL: {error}")
        return None

def create_db(connection):
    """create a database
    """
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("ALX_prodev database created successfully")
    except mysql.connector.Error as error:
        print(f"Error creating database: {error}")
    finally:
        cursor.close()

def connect_to_prodev():
    """create a connection to the ALX_prodev database
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            name='root',
            password='password',
            database='ALX_prodev',
        )
        return connection
    except mysql.connector.Error as error:
        print(f"Error connecting to ALX_prodev: {error}")
        return None

def create_table(connection):
    """create a table in the ALX_prodev database
    """
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                age DECIMAL NOT NULL
            );
        """)
        print("table user data created successfully")
    except mysql.connector.Error as error:
        print(f"Error creating table: {error}")
    finally:
        cursor.close()

def insert_data(connection, data):
    """insert data into the user_data table
    """
    if not connection:
        return
    try:
        cursor = connection.cursor()
        with open(data, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                if len(row) != 4:
                    print(f"Skipping Invalid row: {row}")
                    continue
                user_id, name, email, age_str = row
                query = "INSERT IGNORE INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
                values = (user_id, name, email, age_str)
                cursor.execute(query, values)
            connection.commit()
            print("Data inserted successfully")
    except Exception as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()

def stream_user_data(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM user_data.csv")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
    finally:
        cursor.close()

if __name__ == "__main__":
    connection = connect_to_prodev()
    if connection:
        create_table(connection)
        insert_data(connection, "user_data.csv")
        connection.close()