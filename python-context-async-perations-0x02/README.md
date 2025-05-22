# Python Context Managers & Async Database Queries

## Overview

This project demonstrates the use of **custom class-based context managers** and **asynchronous database queries** in Python, focusing on SQLite interactions.

---

## Features

- **DatabaseConnection**: A class-based context manager to handle opening and closing SQLite database connections automatically.
- **ExecuteQuery**: A reusable context manager that accepts a SQL query and parameters, executes it, and returns the results.
- **Concurrent Async Queries**: Using `aiosqlite` and `asyncio.gather` to perform multiple database queries concurrently.

---

## Setup

1. Ensure Python 3.7+ is installed.
2. Install dependencies:

```bash
pip install aiosqlite
```
    Setup the database with sample data:
```bash
python setup_db.py
```
# Usage
    - Synchronous Context Managers
        1- databaseconnection.py: Connects to the database and fetches all users.
        2- execute.py: Executes parameterized queries within a reusable context manager.

    - Asynchronous Queries
        3-concurrent.py: Runs two queries concurrently — fetching all users and users older than 40.

# Run each script directly using:
```bash
python <script_name>.py
```
## Notes

    - The database users.db contains a users table with columns: id, name, email, and age.
    - Context managers ensure resource safety by automatically handling connection lifecycle.
    - Asynchronous code optimizes database access for I/O-bound operations.