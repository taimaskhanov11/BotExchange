import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand
from loguru import logger

from botexchange.apps.bot.handlers.base_menu import register_base_handlers
from botexchange.apps.bot.handlers.buy_ads_menu import register_buy_ads_handlers
from botexchange.apps.bot.handlers.sell_ads_menu import register_sell_ads_handlers
from botexchange.apps.bot.middleware.test_middleware import TestMiddleware
from botexchange.config.log_settings import init_logging
from botexchange.db.db_main import init_tortoise
from botexchange.loader import bot, dp


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Главное меню"),
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования
    init_logging(old_logger=True,
                 level="TRACE",
                 old_level=logging.DEBUG,
                 steaming=True)
    logger.info(f"Starting bot {(await bot.get_me()).username}")

    await init_tortoise()
    # Установка команд бота
    await set_commands(bot)

    # Меню админа
    # register_admin_commands_handlers(dp)

    # Регистрация хэндлеров
    register_base_handlers(dp)
    register_buy_ads_handlers(dp)
    register_sell_ads_handlers(dp)

    # Регистрация middleware
    # dp.middleware.setup(TestMiddleware())
    # todo 19.03.2022 17:42 taima:
    # dp.middleware.setup(ThrottlingMiddleware(limit=0.5))

    # Регистрация фильтров
    # dp.filters_factory.bind(chat_type=ChatType.PRIVATE, user_id=config.bot.admins,event_handlers=admin_start )

    # asyncio.create_task(message_delete_worker())

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
