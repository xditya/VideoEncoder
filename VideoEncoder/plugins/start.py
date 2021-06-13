#  Copyright (C) 2021 The Authors

from . import *


@BotzHub.on(
    events.NewMessage(incoming=True, pattern="^/start$", func=lambda e: e.is_private)
)
async def starter(event):
    user = await BotzHub.get_entity(event.sender_id)
    if not await check_user(event.sender_id):
        await add_user(event.sender_id)
    await event.reply(
        f"Hi {user.first_name}\nI can encode Telegram files in x265, just send me a video.",
        buttons=[
            Button.url("Channel", url="https://t.me/BotzHub"),
            Button.url("Source", url="https://github.com/xditya/video-encoder-bot"),
        ],
    )
