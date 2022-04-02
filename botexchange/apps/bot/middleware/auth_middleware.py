from pprint import pprint

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import ChatMemberUpdated
from loguru import logger

from botexchange.config.config import config
from botexchange.db.models import User


class AuthMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        logger.trace(update)
        if update.message:
            obj = update.message
            if obj.from_user.id in config.bot.block_list:
                logger.warning(f"Banned user {obj.from_user.id}")
                raise CancelHandler()
            # if obj.to_python()["from"]['id'] in config.bot.block_list:
            #     return False
        elif update.callback_query:
            obj = update.callback_query
            if obj.from_user.id in config.bot.block_list:
                logger.warning(f"Banned user {obj.from_user.id}")
                raise CancelHandler()
        else:
            return
            # if obj.to_python()["from"]['id'] in config.bot.block_list:
            #     return False

    # async def on_process_message(self, message: types.Message, data: dict):
    #     logger.trace(f"{message=}")
    #     logger.trace(f"{data=}")
    #     user = message.from_user
    #     user, _is_created = await User.get_or_create(
    #         user_id=user.id,
    #         defaults={
    #             "username": user.username,
    #             "first_name": user.first_name,
    #             "last_name": user.last_name,
    #             "language": user.language_code,
    #         },
    #     )
    #     if _is_created:
    #         logger.info(f"Новый пользователь {user=}")
