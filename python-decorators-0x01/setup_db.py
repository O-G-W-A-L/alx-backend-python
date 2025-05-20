import sqlite3

def setup_database():
    # Connect to (or create) the database file
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create the 'users' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    # Insert sample data (optional but useful for testing)
    sample_users = [
        ('Alice Smith', 'alice@example.com'),
        ('Bob Johnson', 'bob@example.com'),
        ('Charlie Brown', 'charlie@example.com')
    ]
    cursor.executemany(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        sample_users
    )

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database setup complete! Created 'users' table.")

if __name__ == "__main__":
    setup_database()