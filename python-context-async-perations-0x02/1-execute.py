#!/usr/bin/env python3
"""
Reusable query context manager for executing parameterized SQL queries
"""
import sqlite3

class ExecuteQuery:
    """
    A reusable context manager for executing SQL queries with parameters
    Manages connection and query lifecycle cleanly
    """
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self.cursor.execute(self.query, self.params)
            self.result = self.cursor.fetchall()
            return self.result
        except sqlite3.Error as e:
            print(f"[ERROR] Failed executing query: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
                print(f"[ROLLBACK] Exception: {exc_val}")
            self.cursor.close()
            self.connection.close()


if __name__ == "__main__":
    db_path = "users.db"
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    try:
        with ExecuteQuery(db_path, query, params) as results:
            print(f"Users older than 25:")
            for row in results:
                print(row)
    except sqlite3.Error as err:
        print(f"[DB ERROR] {err}")
