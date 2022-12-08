import time
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv
import json
import os

api_id = 19227292

api_hash = "1a500b8ff493d9ced16431d7f171147c"

client = TelegramClient("bigboss", api_id, api_hash)


client.start()


dataStream = open("./test.json")
dataString = dataStream.read()
data = json.loads(dataString)

for member in data[60:]:
    if member[0] != "Zemmoon":
        try:
            client.send_message(member[0], "Yoo mate")
            time.sleep(5)
        except Exception as e:
            print(e)
            pass
