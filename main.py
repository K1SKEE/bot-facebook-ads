import os
import logging

from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv

from handlers import storage, register_handlers

load_dotenv()

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('TG_TOKEN')

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot=bot, storage=storage)

register_handlers(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
