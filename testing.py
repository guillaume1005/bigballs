import time
from PIL import Image
from io import BytesIO
import requests
import json
from telethon.sync import TelegramClient
from telethon import functions, types

api_id = 11365474
api_hash = "4902ed7aab38298fb9f6af56ec3648d2"

#################################### TESTING OF SENDING AN IMAGE ####################################
# buffer = requests.get(
#     "http://localhost:3010/imageStream",
#     params={"contract": "10000000"},
# ).content

# i = Image.open(BytesIO(buffer))
# i.show()


# files = {"image": BytesIO(buffer)}

# with TelegramClient("king", api_id, api_hash) as client:
#     pic = client.download_profile_photo(
#         "CMC_fastest_alerts",
#         download_big=False,
#     )


# files = {"image": open(pic, "rb").read()}

# res = requests.post(
#     "http://localhost:3010/uploadImages", files=files, data={"contract": 1000000}
# )
# print(res)


#################################### TESTING OF UPDATING INFOS ####################################

# requests.post(
#     "http://localhost:3010/addInfos",
#     data={"token": "1000000", "imageName": "100030", "error": "error"},
# )

# res = json.loads(requests.get("http://localhost:3010/infos").content)
# print(res)
#################################### TESTING OF DOWNLOADING/ADDING ALLVECTORS ####################################
# requests.post(
#     "http://localhost:3010/addVector",
#     data={
#         "image": "13452678",
#         "features": [234567, 56789],
#     },
# )

# vectorsString = requests.get("http://localhost:3010/allVectors").content


# vectors = json.loads(vectorsString)

#################################### TESTING THE COUNT ####################################

# requests.post("http://localhost:3010/addCount", data={"count": 1001})

# count = json.loads(requests.get("http://localhost:3010/counter").content)["count"]

#################################### TESTING OF SENDING AN CNNIMAGE ####################################
# buffer = requests.get(
#     "http://localhost:3010/imageStream", params={"contract": "bim"}
# ).content


# i = Image.open(BytesIO(buffer))


# files = {"image": BytesIO(buffer)}

# with TelegramClient("king", api_id, api_hash) as client:
#     pic = client.download_profile_photo(
#         "CMC_fastest_alerts",
#         download_big=False,
#     )
#     Image.open(pic)

# files = {"image": pic}

# res = requests.post(
#     "http://localhost:3010/uploadImagesCNN", files=files, data={"contract": 100000}
# )
# print(res)


#################################### TELEGRAM TESTING ####################################

# with TelegramClient("king", api_id, api_hash) as client:
#     # result = client(functions.contacts.SearchRequest(q=name, limit=100))
#     pic = client.download_profile_photo(
#         "CMC_fastest_alerts",
#         f"boom.png",
#         download_big=False,
#     )

#     img = Image.open(pic)
#     print(img.shape)

################################## testing cmc images ##################################
# link = "https://s2.coinmarketcap.com/static/img/coins/200x200/19500.png"
# new_url_image = requests.get(link)
# buffer = BytesIO(new_url_image.content)
# img = Image.open(buffer)
# print(buffer)


# super = open("./testingboss.png", "rb").read()  # this is the buffer
# print(buffer)
# print(dir(buffer))
# print(new_url_image.content)
# img.show()

# boss = open(img, "rb").read()
# files = {"image": BytesIO(new_url_image.content)}  # BytesIO

# send it to mongodb before
# requests.post(
#     "http://localhost:3010/uploadImages",
#     files=files,
#     data={"contract": 100000},
# )
# send it to mongodb before

################################## testing receive ##################################

# buffer = requests.get(
#     "http://localhost:3010/imageStream",
#     params={"contract": "100000"},
# ).content

# print("here is the buffer")
# print(BytesIO(buffer))

# i = Image.open(BytesIO(buffer))
# i.show()

################################## testing token server ##################################

requests.get("http://localhost:3010/token", params={"token": "30000"})  # to buy
