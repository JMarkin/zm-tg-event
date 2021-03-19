import asyncio
import logging
import os
import re

from aiogram.types import InputFile
from hachiko.hachiko import (EVENT_TYPE_CREATED, EVENT_TYPE_DELETED,
                             EVENT_TYPE_MODIFIED, EVENT_TYPE_MOVED,
                             AIOEventHandler)

from app.utils import get_chat_ids

EVENT_TYPE_CLOSED = 'closed'

logger = logging.getLogger(__name__)

ZM_URL = os.getenv("ZM_URL", "")


class EventHandler(AIOEventHandler):
    def __init__(self, bot, loop=None):
        super().__init__(loop=loop)
        self.bot = bot
        self.events = set()

    def dispatch(self, event):
        _method_map = {
            EVENT_TYPE_MODIFIED: self.on_modified,
            EVENT_TYPE_MOVED: self.on_moved,
            EVENT_TYPE_CREATED: self.on_created,
            EVENT_TYPE_DELETED: self.on_deleted,
            EVENT_TYPE_CLOSED: self.on_closed,
        }
        handlers = [self.on_any_event, _method_map[event.event_type]]
        for handler in handlers:
            self._loop.call_soon_threadsafe(self._ensure_future,
                                            handler(event))

    async def clear_events(self):
        await asyncio.sleep(2)
        self.events = set()

    def get_event_id(self, path):
        m = re.match(r".*/([0-9]+)-video.mp4$", path)

        if not m:
            return

        event_id = m.group(1)

        if event_id in self.events:
            return

        return event_id

    async def on_closed(self, event):
        event_id = self.get_event_id(event.src_path)

        if not event_id:
            return

        logger.info(f"Complete write video {event.src_path}")
        self.events.add(event_id)

    async def on_created(self, event):
        event_id = self.get_event_id(event.src_path)

        if not event_id:
            return

        logger.info(f"New video {event.src_path}")
        while event_id not in self.events:
            await asyncio.sleep(2)

        if len(self.events) > 10:
            asyncio.create_task(self.clear_events())

        chat_ids = get_chat_ids()

        logger.info("Send message")
        await asyncio.wait([
            self.bot.send_message(
                chat_id, f"Новое уведомление "
                f"{ZM_URL}/zm/?view=event&eid={event_id}")
            for chat_id in chat_ids
        ])

        logger.info("Send video")

        video = InputFile(event.src_path)

        await asyncio.wait(
            [self.bot.send_video(chat_id, video) for chat_id in chat_ids])
