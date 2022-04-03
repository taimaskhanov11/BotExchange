from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from botexchange.apps.bot import markups
from botexchange.apps.bot.filters.base_filters import UserFilter
from botexchange.apps.bot.utils.search_helpers import pretty_view
from botexchange.db.models import AdvertisingPlatform, User
from botexchange.loader import _


class DeletePlatform(StatesGroup):
    delete = State()


async def my_platforms(call: types.CallbackQuery, state: FSMContext, user: User):
    # pprint(dir(user))
    platforms = await user.advertisingplatforms.all()
    count = 0
    for platform in platforms:
        count += 1
        logger.info(f"Platforms {platform}|{count}")
        if count > 50:
            break

    await call.message.answer(
        _("Ниже список всех ваших площадок"),
        reply_markup=markups.platforms_info.my_platforms(platforms),
    )


async def get_platform(call: types.CallbackQuery, state: FSMContext, user: User):
    pk = call.data[9:]
    platform = await AdvertisingPlatform.get(pk=pk)
    await call.message.answer(
        pretty_view(platform),
        parse_mode=types.ParseMode.HTML,
        reply_markup=markups.platforms_info.platform_view(pk),
    )


async def extend_platform(call: types.CallbackQuery, state: FSMContext, user: User):
    pk = call.data[7:]

    platform = await AdvertisingPlatform.get(pk=pk)
    await platform.refresh_duration()
    await call.message.answer(
        _("Срок активности обновлен. До деактивации {duration}".format(duration=platform.duration)),
        reply_markup=markups.platforms_info.extend_platform(),
    )


async def delete_platform(call: types.CallbackQuery, state: FSMContext, user: User):
    pk = call.data[7:]
    await state.update_data(delete_platform=pk)
    platform = await AdvertisingPlatform.get(pk=pk)
    await call.message.answer(
        _("Уверены что хотите удалить площадку {title}").format(title=platform.title),
        reply_markup=markups.platforms_info.delete_platform(),
    )
    await DeletePlatform.delete.set()


async def delete_platform_done(call: types.CallbackQuery, state: FSMContext, user: User):
    data = await state.get_data()
    pk = data.get("delete_platform")
    platform = await AdvertisingPlatform.get(pk=pk)
    if call.data == "yes":
        await platform.delete()
        answer = _("Площадка {title} удалена").format(title=platform.title)
    else:
        answer = _("Удаление {title} отменено").format(title=platform.title)
    await call.message.answer(answer, reply_markup=markups.platforms_info.delete_platform_done())
    await state.finish()


def register_platforms_info_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(my_platforms, UserFilter(), text="my_platforms")
    dp.register_callback_query_handler(get_platform, UserFilter(), text_startswith="platform_")
    dp.register_callback_query_handler(extend_platform, UserFilter(), text_startswith="extend_")
    dp.register_callback_query_handler(delete_platform, UserFilter(), text_startswith="delete_")
    dp.register_callback_query_handler(delete_platform_done, UserFilter(), state=DeletePlatform.delete)
