#!/usr/bin/env python3
'''async operation in python'''
import asyncio
from typing import List


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(count: int, max_delay: int) -> List[float]:
    '''executes task_wait_random count times and returns sorted results'''
    tasks = [task_wait_random(max_delay) for _ in range(count)]
    wait_times = await asyncio.gather(*tasks)
    return sorted(wait_times)

