from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ChatType
from loguru import logger

from botexchange.apps.bot import markups
from botexchange.apps.bot.filters.base_filters import UserFilter
from botexchange.config.config import MESSAGE_DELETE
from botexchange.db.models import User
from botexchange.loader import bot, storage, _


class LanguageChoice(StatesGroup):
    land_choice_state = State()


async def start(message: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(message, types.CallbackQuery):
        message = message.message
    if MESSAGE_DELETE:
        await message.delete()
    await state.finish()
    await message.answer(
        _(
            "Добро пожаловать в бесплатную биржу Telegram рекламы."
            " Тут вы сможете найти каналы/ботов для размещения своего объявления,"
            " либо предоставить свой канал/бота для размещения чужих объявлений."
            " С чего начнем?"
        ),
        reply_markup=markups.base_menu.start_menu(),
    )


async def language(call: types.CallbackQuery, state: FSMContext, user: User):
    logger.trace("language")
    await call.message.delete()
    await call.message.answer(
        _("Выберите язык интерфейса"),
        reply_markup=markups.base_menu.language(user.language),
    )
    await LanguageChoice.land_choice_state.set()


async def language_choice(call: types.CallbackQuery, state: FSMContext, user: User):
    logger.trace("language_choice")
    await user.set_language(call.data)
    # await call.message.answer(_("Язык интерфейса изменен"))
    # await start(call, state)
    answer = "The interface language has been changed" if call.data == "en" else "Язык интерфейса изменен"
    # answer = _("Язык интерфейса изменен")
    await call.message.delete()
    await call.message.answer(answer, reply_markup=markups.base_menu.language_choice(user.language))


@logger.catch
async def add_platform_chat_member(update: types.ChatMemberUpdated):
    # logger.warning(update)
    if update.new_chat_member.is_chat_admin():
        chat_id = update.chat.id
        admin_id = update.from_user.id
        type = update.chat.type
        title = update.chat.title
        members_count = await bot.get_chat_members_count(update.chat.id)
        chat = await bot.get_chat(chat_id)
        try:
            link = chat.invite_link
        except Exception as e:
            logger.warning(e)
            link = None

        chat_data = {
            "chat_id": chat_id,
            "admin_id": admin_id,
            "type": type,
            "title": title,
            "members_count": members_count,
            "can_invite_users": update.new_chat_member.can_invite_users,
            "link": link,
        }
        await storage.update_data(user=admin_id, chat_info=chat_data)
        logger.success(f"Add new chat {chat_data}")


async def support(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Группа поддержки - None")


def register_base_handlers(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart(), state="*", chat_type=ChatType.PRIVATE)
    dp.register_callback_query_handler(start, text="start", state="*")
    dp.register_callback_query_handler(support, text="support", state="*")

    dp.register_callback_query_handler(language, UserFilter(), text="language")
    dp.register_callback_query_handler(language_choice, UserFilter(), state=LanguageChoice.land_choice_state)

    # dp.register_chat_member_handler(chat_member)
    dp.register_my_chat_member_handler(add_platform_chat_member)
    # dp.register_message_handler(start)
