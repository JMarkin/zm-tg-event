import os
from hachiko.hachiko import AIOWatchdog
from app.watcher import EventHandler
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.filters import Filter

from app.utils import get_chat_ids


async def cmd_start(message: types.Message):
    return await message.reply(f"Твой chat_id {message.chat.id}")


async def current_chat_ids(message: types.Message):
    chat_ids = get_chat_ids()
    return await message.reply(
        f"Текущие подписанные на рассылку chat_ids {chat_ids}")


class InChatIds(Filter):
    key = "in_chat_ids"

    async def check(self, message: types.Message):
        chat_ids = get_chat_ids()
        return message.chat.id in chat_ids


def setup_handlers(dp: Dispatcher):
    dp.bind_filter(InChatIds)
    dp.register_message_handler(
        cmd_start,
        commands=['start'],
    )

    dp.register_message_handler(
        InChatIds(),
        current_chat_ids,
        commands=['chat_ids'],
    )


async def on_startup(dp):
    evh = EventHandler(dp.bot)
    dp.watch = AIOWatchdog(os.getenv("ZM_FOLDER", "/zm"), event_handler=evh)
    dp.watch.start()
    setup_handlers(dp)


async def on_shutdown(dp):
    dp.watch.stop()
