import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand
from loguru import logger

from botexchange.apps.bot.handlers.admin_handlers.admin_menu import (
    register_admin_handlers,
)
from botexchange.apps.bot.handlers.base_menu import register_base_handlers
from botexchange.apps.bot.handlers.buying_ads_menu import register_buying_ads_handlers
from botexchange.apps.bot.handlers.errors_handlers import register_error_handlers
from botexchange.apps.bot.handlers.platforms_info import (
    register_platforms_info_handlers,
)
from botexchange.apps.bot.handlers.sale_ads_menu import register_sale_ads_handlers
from botexchange.apps.bot.middleware.auth_middleware import AuthMiddleware
from botexchange.apps.bot.utils.everyday_processes import views_update
from botexchange.config.log_settings import init_logging
from botexchange.db.db_main import init_tortoise
from botexchange.loader import bot, dp, scheduler


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Главное меню"),
        BotCommand(command="/admin", description="Админ меню"),
    ]
    await bot.set_my_commands(commands)


# todo 01.04.2022 1:08 taima:  tzlocal, scheduler
# todo 01.04.2022 15:29 taima: F, Q tortoise;atomic;
async def main():
    # Настройка логирования
    init_logging(old_logger=True, level="TRACE", old_level=logging.DEBUG, steaming=True)
    logger.info(f"Starting bot {(await bot.get_me()).username}")

    await init_tortoise()
    # Установка команд бота
    await set_commands(bot)

    # Меню админа
    # register_admin_commands_handlers(dp)

    # Регистрация хэндлеров
    register_base_handlers(dp)
    register_admin_handlers(dp)
    register_platforms_info_handlers(dp)
    register_buying_ads_handlers(dp)
    register_sale_ads_handlers(dp)
    register_error_handlers(dp)
    # Регистрация middleware
    # dp.middleware.setup(TestMiddleware())
    dp.middleware.setup(AuthMiddleware())
    # todo 19.03.2022 17:42 taima:
    # dp.middleware.setup(ThrottlingMiddleware(limit=0.5))

    # Регистрация фильтров
    # dp.filters_factory.bind(chat_type=ChatType.PRIVATE, user_id=config.bot.admins,event_handlers=admin_start )

    # asyncio.create_task(message_delete_worker())
    scheduler.add_job(views_update, trigger="cron", hour=0, minute=0, second=0)
    logger.info(f"Количество задач")
    for j in scheduler.get_jobs():
        logger.info(j)
    # Запуск поллинга
    # await dp.skip_
    # updates()  # пропуск накопившихся апдейтов (необязательно)
    scheduler.start()
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
