import asyncio

import aiohttp as aiohttp
import requests


async def send(url):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for u in url:
            tasks.append(asyncio.create_task(session.get(u)))

    resp = await asyncio.gather(*tasks)
    return [await r.json() for r in resp]


def sendOnce(url):
    r = requests.get(url)
    return r.status_code