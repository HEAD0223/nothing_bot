import logging

from aiogram import Bot, Dispatcher, types
from data.config import TgKeys
from aiogram.dispatcher.webhook import SendMessage

from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TgKeys.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)