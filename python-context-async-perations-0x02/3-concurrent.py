#!/usr/bin/env python3
"""
Run multiple database queries concurrently using asyncio and aiosqlite
"""

import asyncio
import aiosqlite

DB_PATH = "users.db"

async def async_fetch_users():
    """Fetch all users from the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        await cursor.close()
        print("\n All Users:")
        for user in users:
            print(user)
        return users

async def async_fetch_older_users():
    """Fetch users older than 40 from the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        older_users = await cursor.fetchall()
        await cursor.close()
        print("\n Users older than 40:")
        for user in older_users:
            print(user)
        return older_users

async def fetch_concurrently():
    """Run both fetches concurrently."""
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
