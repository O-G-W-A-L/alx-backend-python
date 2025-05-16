#!/usr/bin/python3
"""
Simulate fetching paginated data from the users database,
using a generator to lazily load each page on demand.
"""

import mysql.connector
from mysql.connector import Error
import seed  # assumes seed.py provides connect_to_prodev()

def paginate_users(page_size, offset):
    """
    Fetches up to `page_size` rows from user_data starting at `offset`.
    Returns a list of dict‑rows.
    """
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM user_data "
        f"LIMIT {page_size} OFFSET {offset}"
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def lazy_pagination(page_size):
    """
    Generator that yields successive pages of users:
      - calls paginate_users(page_size, offset)
      - stops when an empty list is returned
    Uses exactly one loop.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
