#!/usr/bin/env python3
'''An example of async operation in Python'''

import asyncio
import random

async def wait_random(max_delay: int = 10) -> float:
    '''An asynchronous function that waits for a random amount of time between 0 and max_delay seconds.'''
    value = random.uniform(0, max_delay)
    await asyncio.sleep(value)
    return value
