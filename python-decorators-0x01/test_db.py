import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Fetch all users
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print("Users in the database:")
for row in rows:
    print(row)

conn.close()