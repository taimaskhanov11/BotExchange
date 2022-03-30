from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from botexchange.apps.bot import markups
from botexchange.loader import _


async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(_("Добро пожаловать в бесплатную биржу Тelegram рекламы."
                           " Тут вы сможете найти каналы/ботов для размещения своего объявления,"
                           " либо предоставить свой канал/бота для размещения чужих объявлений."
                           " С чего начнем?"), reply_markup=markups.start_menu())


def register_base_handlers(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart(), state="*")
