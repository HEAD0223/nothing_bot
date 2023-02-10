import logging

from aiogram import Bot, Dispatcher, types
from data import config
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)