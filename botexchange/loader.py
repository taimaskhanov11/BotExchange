from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from botexchange.apps.bot.middleware.language_middleware import setup_lang_middleware
from botexchange.config.config import config

bot = Bot(token=config.bot.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

# Настроим i18n middleware для работы с многоязычностью
i18n = setup_lang_middleware(dp)
_ = i18n.gettext
