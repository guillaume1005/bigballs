import time
from telethon.sync import TelegramClient
from telethon import functions, types
import json

api_id = 11365474
# api_id = 19227292

api_hash = "4902ed7aab38298fb9f6af56ec3648d2"
# api_hash = '1a500b8ff493d9ced16431d7f171147c'


def link_tel_tok(name, token):

    with TelegramClient("king", api_id, api_hash) as client:
        result = client(functions.contacts.SearchRequest(q=name, limit=100))
        print(result.stringify())
        chats = []
        # j = 0
        for j in range(len(result.chats)):
            chats.append(result.chats[j].__dict__)

        print(chats[0])
        max = 0
        index = 0
        for p in range(len(result.chats)):
            if result.chats[p].__dict__["participants_count"] > max:
                index = p
                max = result.chats[p].__dict__["participants_count"]

        # gather data

        username = result.chats[index].__dict__["username"]
        channel = result.chats[index].__dict__["id"]
        path = f"{channel}" + ".png"

        client.download_profile_photo(
            f"{channel}" + ".png",
            "../../JupyterNotebooks/ImageRecommenderResnet18/images",
        )

        # save data in "infos.json"
        infosStream = open("./infos.json", "r")
        infosString = infosStream.read()
        infos = json.loads(infosString)

        infos[f"{channel}" + ".png"] = token

        infosFile = open("infos.json", "w")
        infosFile.write(json.dumps(infos))

        # client.download_profile_photo(channel, path)  # 640x640, register image with id
        # client.download_profile_photo(channel, path, download_big=False)  # 160x160


# server that runs continuously (communicate through file, socket is maybe better)
while True:
    # load com
    dbcStream = open("../node/dbc/dbc.json", "r")
    dbcString = dbcStream.read()
    dbc = json.loads(dbcString)

    dbcStream.close()  # always synchronous

    comStream = open("./com.json", "r")
    comString = comStream.read()
    com = json.loads(comString)

    comStream.close()

    if dbc["newToken"] == com["newToken"]:
        print("here")
        time.sleep(5)
        pass
    else:
        name = dbc["newToken"]["name"]
        token = dbc["newToken"]["token"]
        link_tel_tok(name, token)
        com["newToken"] = dbc["newToken"]

        comFile = open("./com.json", "w")

        comFile.write(json.dumps(com))
        comFile.close()
        time.sleep(5)
