import time
from flask import Flask, request
import asyncio

# import addLoop
import os
from features_images import compute_features_add

from modules.addLoop import link_tel_tok


app = Flask(__name__)

print("go")


@app.route("/addImage", methods=["GET"])
def answer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    token = request.args["token"]
    name = request.args["name"]
    print(name)
    print(token)
    imgPath = link_tel_tok(name, token)
    if imgPath is not None:
        # look if it works with image path, or query from database
        compute_features_add(
            imgPath, imgPath  # use normally buffer in here
        )  # or if asyncio not working, add the request to another server, or combine the files
        # loop.run_until_complete(asyncio.wait(tasks))
        while loop.is_running():
            time.sleep(1)
            pass
        loop.close()
        return "boom"
    while loop.is_running():
        time.sleep(1)
        pass
    loop.close()
    return "boom"
