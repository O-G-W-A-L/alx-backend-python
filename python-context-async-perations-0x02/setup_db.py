#!/usr/bin/env python3
"""
Setup script to initialize 'users.db' with a 'users' table including age,
and populate it with 10+ sample users for testing.
"""

import sqlite3

def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Drop table if you want to reset it (optional)
    cursor.execute('DROP TABLE IF EXISTS users')

    # Create the 'users' table with age column
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL
        )
    ''')

    # Sample users with name, email, and age
    sample_users = [
        ('Alice Smith', 'alice@example.com', 22),
        ('Bob Johnson', 'bob@example.com', 30),
        ('Charlie Brown', 'charlie@example.com', 26),
        ('Diana Prince', 'diana@example.com', 35),
        ('Ethan Hunt', 'ethan@example.com', 40),
        ('Fiona Glenanne', 'fiona@example.com', 29),
        ('George Bluth', 'george@example.com', 55),
        ('Helen Parr', 'helen@example.com', 33),
        ('Ian Malcolm', 'ian@example.com', 24),
        ('Jenny Matrix', 'jenny@example.com', 28),
    ]

    cursor.executemany(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        sample_users
    )

    conn.commit()
    conn.close()
    print("✅ users.db created and populated with sample users.")

if __name__ == "__main__":
    setup_database()
