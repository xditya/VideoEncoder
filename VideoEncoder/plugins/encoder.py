#  Copyright (C) 2021 The Authors

from . import *


@BotzHub.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def encoder(event):
    if not (event.media or event.document):
        return
    if event.text and event.text.startswith("/"):
        return
    if event.media.document and event.media.document.mime_type not in video_mimetype:
        return await event.reply("`Invalid Video !\nMake sure its a valid video file.`")
    await event.reply(
        f"`Added to queue in position {len(data)}...\nKindly be patient...`"
    )
    data.append(event)
    if len(data) == 1:
        await add_task(event)
