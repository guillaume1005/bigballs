from re import search
import time
from telethon.sync import TelegramClient
from telethon import functions, types
import json
import os
import requests

# from features_images import compute_features_add

api_id = 11365474
# api_id = 19227292

api_hash = "4902ed7aab38298fb9f6af56ec3648d2"
# api_hash = '1a500b8ff493d9ced16431d7f171147c'

# coinsStream = open("../node/dbc/dbc.json")
# coinsFile = coinsStream.read()
# coins = json.loads(coinsFile)

# infosStream = open("./infos.json")
# infosFile = infosStream.read()
# infos = json.loads(infosFile)
# infosStream.close()


def link_tel_tok(name, token):

    with TelegramClient("king", api_id, api_hash) as client:
        result = client(functions.contacts.SearchRequest(q=name, limit=100))
        # print(result.stringify())
        chats = []
        # j = 0
        try:
            # getting data from telegram
            for j in range(len(result.chats)):
                chats.append(result.chats[j].__dict__)
            print(chats)
            print(chats[0])
            max = 0
            index = 0
            # filtering by taking the max number of participants
            for p in range(len(result.chats)):
                if result.chats[p].__dict__["participants_count"] > max:
                    index = p
                    max = result.chats[p].__dict__["participants_count"]

            # filtering by looking if it contains the address
            for p in range(len(result.chats)):
                username = result.chats[p].__dict__["username"]

                count = search_address(username, token, client)

                index = p

                if count == 1:
                    # result is true
                    break

            # gather data

            if count == 0:
                print("not found any groups with this token")
                return

            # now the channel contains the code and thus is the official coin
            global channel

            channel = result.chats[index].__dict__["id"]

            try:
                pic = client.download_profile_photo(  # downloading the photo
                    channel,
                    file=f"{channel}.png",
                    download_big=False,
                )

                print("here is the channel for the photo")

                # then send this photo to the server
                files = {"image": open(pic, "rb").read()}
                requests.post(
                    "http://localhost:3010/uploadImages",
                    files=files,
                    data={"contract": token},
                )

                dataInfos = {}
                dataInfos["token"] = token
                dataInfos["imageName"] = f"{channel}.png"

                requests.post("http://localhost:3010/addInfos", data=dataInfos)

                imgPath = f"{channel}.png"
                print("here is the imgPath")

                return imgPath  # before list

                # compute the vector similarity
            except Exception as e:
                print(e)
                # requests.get("mongourl/infos")
                dataInfos = {}
                dataInfos["error"] = "error"
                # dataInfos["imageName"] = f"{channel}.png"
                dataInfos["token"] = token
                requests.post("http://localhost:3010/addInfos", data=dataInfos)
                pass
        except Exception as e:
            pass


def search_address(name, address, client):

    # result = client.get_messages("SeekTigerOfficial", limit=100)
    # print(result)
    result = client.iter_messages(
        name,
        search=address,
        limit=1,
    )
    count = 0
    for x in result:
        count = 1

    return count

    # for x in result:
    #     print(x)

    # client.send_message("me", "hey")


# name = "CMC_fastest_alerts"
# address = "0x4f5f7a7Dca8BA0A7983381D23dFc5eaF4be9C79a"

# key_pairs = list(coins)

# infos_coins = []
# for image in list(infos):
#     infos_coins.append(infos[image])


# # delete images not in dbc
# tokens = []
# for pair in key_pairs:
#     tokens.append(coins[pair]["token"])


###############################################  COMMENT ###############################################


# for coin in list(infos_coins):
#     if coin != "error":
#         if coin not in tokens:

#             print(coin)
#             for image in list(infos):
#                 if infos[image] == coin:
#                     infos.pop(image)
#                     # os.remove(
#                     #     f"../../JupyterNotebooks/ImageRecommenderResnet18/images/{image}"
#                     # )

#     infosFile = open("infos.json", "w")
#     infosFile.write(json.dumps(infos))
#     infosFile.close()

############################################### END ###############################################
# for i in range(len(list(key_pairs))):
#     name = coins[key_pairs[i]]["name"]
#     coin = coins[key_pairs[i]]["token"]
#     if coin not in infos_coins:
#         if coin not in list(infos):
#             print(coin)
#             link_tel_tok(name, coin)
#             time.sleep(2)
