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
# destination_user_id = 1111111111
# entity = client.get_entity(destination_user_id)
# client.send_message(entity=entity, message="Hi")


class Scraper:
    def __init__(self):
        # Enter Your 7 Digit Telegram API ID.
        self.api_id = api_id
        # Enter Yor 32 Character API Hash
        self.api_hash = "api_hash"
        # Enter Your Mobile Number With Country Code.
        self.phone = "+12222222222"

        self.client = client
        self.groups = []

    # def connect(self):
    #     # connecting to telegram and checking if you are already authorized.
    #     # Otherwise send an OTP code request and ask user to enter the code
    #     # they received on their telegram account.
    #     # After logging in, a .session file will be created. This is a database file which makes your session persistent.

    #     self.client.connect()
    #     if not self.client.is_user_authorized():
    #         self.client.send_code_request(self.phone)
    #         self.client.sign_in(self.phone, input("Enter verification code: "))

    def getGroups(self):
        # with this method you will get all your group names
        # offset_date and  offset_peer are used for filtering the chats. We are sending empty values to these parameters so API returns all chats
        # offset_id and limit are used for pagination.
        # limit is 200. it means last 200 chats of the user.

        chats = []
        last_date = None
        chunk_size = 200
        result = self.client(
            GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash=0,
            )
        )
        chats.extend(result.chats)

        for chat in chats:
            try:
                if chat.megagroup == True:
                    self.groups.append(chat)
            except:
                continue

        # choose which group you want to scrape  members:
        for i, g in enumerate(self.groups):
            print(str(i) + "- " + g.title)

    def saveFile(self):
        # with this method you will get group all members to json file that you choosed group.

        g_index = input("Please! Enter a Number: ")
        target_group = self.groups[int(g_index)]

        print("Fetching Members...")
        all_participants = []
        # all_participants = self.client.get_participants(target_group, aggressive=True)
        all_participants = self.client.get_participants(target_group)
        print(all_participants)

        print("Saving In file...")
        streamData = open("./test.json", "w")
        # fileData = streamData.read()
        # data = json.loads(fileData)
        data = []

        # writer = csv.writer(f, delimiter=",", lineterminator="\n")
        # writer.writerow(
        #     ["username", "user id", "access hash", "name", "group", "group id"]
        # )

        for user in all_participants:
            if user.username:
                username = user.username
            else:
                username = ""

            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""

            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""

            name = (first_name + " " + last_name).strip()

            data.append(
                [
                    username,
                    user.id,
                    user.access_hash,
                    name,
                    target_group.title,
                    target_group.id,
                ]
            )

        streamData.write(json.dumps(data))
        print("Members scraped successfully.......")


if __name__ == "__main__":
    telegram = Scraper()
    # telegram.connect()
    telegram.getGroups()
    telegram.saveFile()
