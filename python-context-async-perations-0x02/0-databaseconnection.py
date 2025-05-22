#!/usr/bin/env python3
"""
Custom class-based context manager for database connection (SQLite)
"""

import sqlite3


class DatabaseConnection:
    """
    Context manager to handle SQLite DB connections
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            return self.cursor
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to connect to database '{self.db_name}': {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
                print(f"[ROLLBACK] Exception occurred: {exc_val}")
            self.cursor.close()
            self.connection.close()


if __name__ == "__main__":
    db_path = "users.db"

    try:
        with DatabaseConnection(db_path) as cursor:
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()

            print("Users in database:")
            for row in rows:
                print(row)

    except sqlite3.Error as err:
        print(f"[DB ERROR] {err}")
