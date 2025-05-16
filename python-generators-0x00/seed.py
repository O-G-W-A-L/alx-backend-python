import mysql.connector
from mysql.connector import Error
import csv

def connect_db():
    """Create a connection to the MySQL server."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='hunter',
            password='pass',
        )
        return connection
    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL: {error}")
        return None

def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist."""
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
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='hunter',
            password='pass',
            database='ALX_prodev',
        )
        return connection
    except mysql.connector.Error as error:
        print(f"Error connecting to ALX_prodev: {error}")
        return None

def create_table(connection):
    """Create the user_data table with appropriate columns."""
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                age DECIMAL(5,2) NOT NULL
            );
        ''')
        print("Table user_data created successfully")
    except mysql.connector.Error as error:
        print(f"Error creating table: {error}")
    finally:
        cursor.close()

def insert_data(connection, data_file):
    """Insert data from CSV into user_data table with proper type conversion."""
    if not connection:
        return
    try:
        cursor = connection.cursor()
        with open(data_file, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                if len(row) != 4:
                    print(f"Skipping invalid row: {row}")
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
