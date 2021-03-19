import os

FILE_CHAT_PATH = os.getenv("FILE_CHAT_PATH", "chat_id")

CHAT_IDS = os.getenv("CHAT_IDS", None)


def get_chat_ids():
    if CHAT_IDS:
        return CHAT_IDS.split(",")

    if FILE_CHAT_PATH:
        with open(FILE_CHAT_PATH) as f:
            return f.read().strip().split(",")
    return []
