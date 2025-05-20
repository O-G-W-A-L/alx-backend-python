# 🧠 Python Database Decorators: Clean, Robust, and Reusable DB Operations

Welcome to the **Python Database Decorators** project — a hands-on journey into mastering Python decorators to improve database handling. This project is designed to simulate real-world challenges and help you build production-ready tools for robust, scalable, and clean Python applications.

---

## 📚 Project Overview

This project focuses on creating **custom Python decorators** that:

- Log all SQL queries
- Handle connection management
- Manage transactions safely
- Retry transient failures
- Cache query results

By wrapping your database logic with these decorators, you’ll write **less boilerplate**, handle **failures gracefully**, and ensure **data integrity** with minimal effort.

---

## 🎯 Learning Objectives

By the end of this project, you will:

- Master advanced decorator patterns in Python
- Automate repetitive DB tasks (logging, connections, transactions)
- Build resilient systems with retries and graceful failure recovery
- Boost performance with intelligent caching
- Apply clean architecture and separation of concerns in real codebases

---

## ⚙️ Requirements

- Python 3.8 or higher
- SQLite3 installed
- A `users` table in your SQLite database (for testing)
- Git & GitHub for version control
- Familiarity with:
  - Python decorators
  - Basic database operations

---

## 🛠 Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/python-db-decorators.git
   cd python-db-decorators```
   
    Create your virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
Install dependencies (if any):
```bash
pip install -r requirements.txt

Ensure your SQLite database and users table are ready:
```
Example SQL:

    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );

📦 Project Structure

```bash
├── decorators/
│   ├── __init__.py
│   ├── log_queries.py
│   ├── with_connection.py
│   ├── transactional.py
│   ├── retry.py
│   └── cache.py
├── db/
│   └── database.db
├── examples/
│   └── usage_examples.py
├── tests/
│   ├── test_log_queries.py
│   └── ...
├── README.md
└── requirements.txt
```
🔁 Task List
Task	Description	Output
✅ Task 0	@log_queries — Logs all SQL queries with timestamps	Logging SQL activity
✅ Task 1	@with_connection — Handles opening/closing DB connections	Cleaner DB functions
✅ Task 2	@transactional — Ensures commits/rollbacks	Robust transactions
✅ Task 3	@retry_on_failure — Retries failed operations	Fault tolerance
✅ Task 4	@cache_results — Caches query results	Performance boost

💡 Example Usage

from decorators.log_queries import log_queries
from decorators.with_connection import with_connection
from decorators.transactional import transactional

@log_queries
@with_connection
@transactional
def insert_user(conn, name, email):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))

✅ Best Practices Followed

    Functional purity through decorator abstraction
    Connection safety using with context managers
    Graceful failure with retries and fallbacks
    Readable, maintainable architecture
    Modular design for real-world reusability

📂 Contributing

Contributions are welcome! If you have ideas to improve the decorators or add more features (like metrics, rate limiting, async support), feel free to fork the repo and create a PR.
🧪 Running Tests

pytest tests/

🧠 Author

Built with ❤️ by Hunter passionate about clean code, database reliability, and Python mastery.

