from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from botexchange.config.config import config

bot = Bot(token=config.bot.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Настроим i18n middleware для работы с многоязычностью
