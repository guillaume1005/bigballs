import requests
from PIL import Image
from io import BytesIO
import time
import os
import json
import features_images

# print("here")
# use read on open to get file ascii

id = json.loads(requests.get("http://localhost:3010/counter").content)["count"]

p = 0

while True:

    try:
        print(id)
        # check 5 values above
        link = f"https://s2.coinmarketcap.com/static/img/coins/200x200/{id}.png"
        f = requests.get(link)
        text = f.text

        # inputDir = "../../JupyterNotebooks/ImageRecommenderResnet18/images"

        # print(text)
        # time.sleep(5)
        if "Access Denied" in text:
            # print("not yet updated")
            time.sleep(5)

        else:
            new_url_image = requests.get(link)

            buffer = BytesIO(new_url_image.content)
            # new_img = Image.open(BytesIO(new_url_image.content))

            iPath = f"cmc{id}.png"

            # files = {"image": BytesIO(new_url_image.content)}

            # send it to mongodb before
            # requests.post(
            #     "http://localhost:3010/uploadImages",
            #     files=files,
            #     data={"contract": 100000},
            # ) # send it to mongodb before

            # new_img.save(os.path.join(inputDir, iPath))

            # import features_images

            print(f"The requested image is {iPath}")

            img = features_images.sim_im(iPath, buffer)  # before iPath
            print("now here")

            id += 1
            # update counter
            requests.post("http://localhost:3010/addCount", data={"count": id})
            time.sleep(5)

        p += 1

        if p % 20 == 0:  # every minute and fourty seconds, check
            for i in range(5):

                link = (
                    f"https://s2.coinmarketcap.com/static/img/coins/200x200/{id+i}.png"
                )

                f = requests.get(link)
                text = f.text

                # inputDir = "../../JupyterNotebooks/ImageRecommenderResnet18/images"

                # print(text)
                if "Access Denied" in text:
                    # print("not yet updated")
                    time.sleep(1)

                else:
                    new_url_image = requests.get(link)

                    # new_img = Image.open(BytesIO(new_url_image.content))

                    iPath = f"cmc{id+i}.png"

                    # new_img.save(os.path.join(inputDir, iPath))

                    # files = {"image": BytesIO(new_url_image.content)}

                    # send it to mongodb
                    # requests.post(
                    #     "http://localhost:3010/uploadImages",
                    #     files=files,
                    #     data={"imageName": iPath},
                    # )
                    # send it to mongodb (before)

                    # import features_images

                    buffer = BytesIO(new_url_image.content)

                    img = features_images.sim_im(
                        iPath, buffer
                    )  # second argument is usually buffer

                    id += i + 1

                    # update counter
                    requests.post("http://localhost:3010/addCount", data={"count": id})
                    time.sleep(5)

                    break
    except Exception as e:  # requests.exceptions.RequestException with requests error
        print("there")
        print(e)
        time.sleep(2)
        pass
