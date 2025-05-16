#!/usr/bin/python3
"""
Objective: Create a generator to fetch and process data in batches from the users database.

Instructions:
- stream_users_in_batches(batch_size): fetch rows in batches
- batch_processing(batch_size): process each batch to filter users over age 25
- Use no more than 3 loops total
- Use `yield` for generators
"""

# Import the `stream_users` generator function from 0-stream_users.py
stream_users = __import__('0-stream_users')

def stream_users_in_batches(batch_size):
    """
    Generator that yields lists of user dicts in batches of size `batch_size`.
    """
    batch = []
    for user in stream_users():            # ← Loop 1: pulling one user at a time
        batch.append(user)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:                              # yield any remaining users
        yield batch

def batch_processing(batch_size):
    """
    Fetches batches via `stream_users_in_batches`, then prints each user
    over age 25, one per line.
    """
    for batch in stream_users_in_batches(batch_size):   # ← Loop 2: iterating batches
        for user in batch:                              # ← Loop 3: iterating within a batch
            if user['age'] > 25:
                print(user)
