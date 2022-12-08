import requests


# response = requests.get("http://localhost:3010/token", {"token": 10})
# print(response)

try:
    response = requests.get(
        "http://localhost:3011/addImage?token=10", timeout=0.0000000001
    )
    print(response)
except requests.exceptions.ReadTimeout:
    pass
