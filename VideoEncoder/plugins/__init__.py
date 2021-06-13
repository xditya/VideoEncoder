#  Copyright (C) 2021 The Authors

from telethon import events, Button
from .. import *
from ..helpers import *

video_mimetype = [
    "video/x-flv",
    "video/mp4",
    "application/x-mpegURL",
    "video/MP2T",
    "video/3gpp",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-ms-wmv",
    "video/x-matroska",
    "video/webm",
    "video/x-m4v",
    "video/quicktime",
    "video/mpeg",
]

bot = bot_db["USERS"]


async def add_user(id):
    await bot.insert_one({"user": id})


async def check_user(id):
    return bool(await bot.find_one({"user": id}))


async def all_users():
    return [i async for i in bot.find()]
