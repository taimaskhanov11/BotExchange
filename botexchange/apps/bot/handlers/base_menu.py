from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.state import State, StatesGroup
from loguru import logger

from botexchange.apps.bot import markups
from botexchange.apps.bot.filters.base_filters import UserFilter
from botexchange.db.models import User
from botexchange.loader import _


class LanguageChoice(StatesGroup):
    land_choice_state = State()


async def start(message: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await message.delete()

    print(await message.bot.get_chat(message.from_user.id))
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
    await call.message.answer(_("Выберите язык интерфейса"), reply_markup=markups.base_menu.language(user.language))
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
    # await call.message.answer(answer)
    # await start(call, state)


def register_base_handlers(dp: Dispatcher):
    dp.register_message_handler(start, UserFilter(), CommandStart(), state="*")
    dp.register_callback_query_handler(start, text="start", state="*")
    dp.register_callback_query_handler(language, UserFilter(), text="language")
    dp.register_callback_query_handler(language_choice, UserFilter(), state=LanguageChoice.land_choice_state)
