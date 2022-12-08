from telethon.sync import TelegramClient
from telethon import functions, types

api_id = 11365474
# api_id = 19227292

api_hash = "4902ed7aab38298fb9f6af56ec3648d2"
# api_hash = '1a500b8ff493d9ced16431d7f171147c'

with TelegramClient("king", api_id, api_hash) as client:
    result = client(
        functions.channels.JoinChannelRequest(channel="moonastronauts_official")
    )
    print(result.stringify())


# def has_to_dict(obj):
#    method = getattr(obj, "to_dict", None)

#    return callable(method)

# def to_dict_req(obj):
# res = {}
# if has_to_dict(obj):
#     for key, value in obj.to_dict().items():
#         if has_to_dict(value):
#             value = to_dict_req(value)
#         else:
#             value = str(value)
#         res[key] = value
#     return res
# else:
#     return str(obj)
