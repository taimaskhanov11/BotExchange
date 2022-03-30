from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from loguru import logger

from botexchange.db.models import User


class AuthMiddleware(BaseMiddleware):

    async def on_process_message(self, message: types.Message):
        logger.trace(f"{message=}")
        user = message.from_user
        user, _is_created = await User.get_or_create(user_id=user.id, defaults={
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "language": user.language_code
        })
        if _is_created:
            logger.info(f"Новый пользователь {user=}")
