import logging
import os

from aiogram.bot.bot import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling

from app.bot import on_shutdown, on_startup

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot)

start_polling(dispatcher,
              on_startup=on_startup,
              on_shutdown=on_shutdown,
              skip_updates=True)
