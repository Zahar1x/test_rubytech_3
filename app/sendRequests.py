import asyncio
import datetime
from datetime import datetime

import aiohttp as aiohttp
import requests
import schedule as schedule

from app import Links_crud
from app.writeLog import writeLog


async def send(url):
    json_responces = []
    writeLog(datetime.now(), __file__,  ':send:Started send method...')
    async with aiohttp.ClientSession() as session:
        tasks = []
        for u in url:
            writeLog(datetime.now(), __file__,  ':send:sending request to ' + u)
            tasks.append(asyncio.create_task(session.get(u)))

    resp = await asyncio.gather(*tasks)
    for r in resp:
        json_responces.append(await r.json())
        writeLog(datetime.now(), __file__,  ':send:recieved responce ' + r.json())


def getAllUrls():
    writeLog(datetime.now(), __file__,  ':getAllUrls():getting all urls from DB...')
    return Links_crud.read_all()


def sendRequestOnSchedule():
    schedule.every(5).minutes.do(send, getAllUrls())


def sendOnce(url):
    writeLog(datetime.now(), __file__,  ':sendOnce:sending request to url ' + url)
    r = requests.get(url)
    writeLog(datetime.now(), __file__,  ':sendOnce:recieved responce with status code ' + str(r.status_code))
    return r.status_code, str(r.status_code), datetime.now()
