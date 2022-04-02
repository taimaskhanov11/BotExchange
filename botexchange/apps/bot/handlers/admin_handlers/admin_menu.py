from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from botexchange.apps.bot import markups
from botexchange.config.config import config
from botexchange.db.models import User, _


class Ban(StatesGroup):
    ban = State()


class Unban(StatesGroup):
    unban = State()


async def admin_menu(message: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(message, types.CallbackQuery):
        message = message.message

    await state.finish()
    await message.answer(_("Доступные функции"), reply_markup=markups.admin_menu.admin_menu())


async def all_users(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    users = await User.all()
    answer = ""
    for u in users:
        answer += f"{u.username or u.user_id}\n"
    await call.message.answer(answer or _("Пусто"), reply_markup=markups.admin_menu.all_users())


async def ban(call: types.CallbackQuery, state: FSMContext):
    await Ban.ban.set()
    await call.message.answer(_("Введите имя пользователя или username для бана"), reply_markup=ReplyKeyboardRemove())
    await state.finish()


async def ban_done(message: types.Message, state: FSMContext):
    try:
        if message.text.isdigit():
            config.bot.block_list.append(int(message.text))
        else:
            u = await User.get(username=message.text)
            config.bot.block_list.append(u.user_id)
        await message.answer(_("Пользователь {user} забанен").format(user=message.text),
                             reply_markup=markups.admin_menu.ban_done())
        await state.finish()
    except Exception as e:
        logger.critical(e)
        await message.answer(
            _("Ошибка при удалении, проверьте правильность веденных данных",
              reply_markup=markups.admin_menu.ban_done()))


async def unban(call: types.CallbackQuery, state: FSMContext):
    await Ban.ban.set()
    await call.message.answer(_("Введите имя пользователя или username для разбана"),
                              reply_markup=ReplyKeyboardRemove())
    await state.finish()


async def unban_done(message: types.Message, state: FSMContext):
    try:
        if message.text.isdigit():
            config.bot.block_list.remove(int(message.text))
        else:
            u = await User.get(username=message.text)
            config.bot.block_list.remove(u.user_id)
        await message.answer(_("Пользователь {user} разбанен").format(user=message.text), reply_markup=markups.admin_menu.unban_done())
        await state.finish()
    except Exception as e:
        logger.critical(e)
        await message.answer(
            _("Ошибка при удалении, проверьте правильность веденных данных",
              reply_markup=markups.admin_menu.ban_done()))


async def ban_list(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    banned_user = config.bot.block_list or _("Пусто")
    await call.message.answer(banned_user, reply_markup=markups.admin_menu.ban_done())


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_menu, commands="admin")
    dp.register_callback_query_handler(admin_menu, text="admin")
    dp.register_callback_query_handler(all_users, text="all_users")
    dp.register_callback_query_handler(ban, text="ban")
    dp.register_message_handler(ban_done, state=Ban.ban)
    dp.register_callback_query_handler(unban, text="unban")
    dp.register_message_handler(unban_done, state=Unban.unban)
    dp.register_callback_query_handler(ban_list, text="ban_list")
