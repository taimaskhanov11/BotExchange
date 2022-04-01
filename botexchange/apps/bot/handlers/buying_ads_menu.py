from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from botexchange.apps.bot import markups
from botexchange.apps.bot.handlers.base_menu import start
from botexchange.db.models import PlatformSearch
from botexchange.loader import _


class BuyingAds(StatesGroup):
    platform_type = State()
    thematic = State()
    audience_size = State()
    edit_field = State()


async def back(call: types.CallbackQuery, state: FSMContext):
    logger.trace(f"back {call}")
    pre_state = await BuyingAds.previous()
    if pre_state:
        new_state = await BuyingAds.previous()
        if new_state:
            logger.trace(f"Предыдущая стадия {pre_state=}")
            logger.trace(f"Текущая стадия {new_state=}")
            method = new_state.split(":")[1]
            await globals()[method](call, state)
        else:
            await buying_start(call, state)
    else:
        await start(call.message, state)


async def buying_start(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer(_("Выберите тип Телеграм-площадки"), reply_markup=markups.buying_ads.platform_type())
    await BuyingAds.platform_type.set()


async def platform_type(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logger.trace(f"platform_type|{data=}")
    thematics_list = data.get("thematics", [])
    await state.update_data(page=1)
    if call.data != "back" and not thematics_list:

        await call.message.delete()
        # валидация
        if not PlatformSearch.platform_type_validator(call.data):
            logger.warning("Неправильный тип платформы")
            await call.message.answer(
                _("Неправильный ввод, нажмите на кнопки ниже"), reply_markup=markups.buying_ads.platform_type()
            )
            return

        await state.update_data(platform_type=call.data, thematics=thematics_list)
        await call.message.answer(
            _("Выберите интересующие тематики"), reply_markup=markups.buying_ads.thematics(thematics_list)
        )
    else:
        logger.trace(call)
        await call.message.edit_reply_markup(markups.buying_ads.thematics(thematics_list))
    await BuyingAds.thematic.set()


# todo 01.04.2022 13:29 taima: добавить далее для тематик
async def thematic(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logger.trace(f"thematic|{data=}")
    if call.data in ["next", "back"]:
        await call.message.delete()
        await call.message.answer(
            _("Укажите желаемый объем аудитории"), reply_markup=markups.buying_ads.audience_size()
        )
        await BuyingAds.audience_size.set()
    elif call.data.startswith("right") or call.data.startswith("left"):
        markups.buying_ads.thematics(data["thematics"], data.get("page"))

    else:
        if PlatformSearch.thematic_validator(call.data):
            if call.data in data["thematics"]:
                data["thematics"].remove(call.data)
            else:
                data["thematics"].append(call.data)
            await state.update_data(data)
            await call.message.edit_reply_markup(markups.buying_ads.thematics(data["thematics"]))
            # await platform_type(call, state)
        else:
            logger.warning("Неправильный тип платформы")
            await call.message.answer(
                _("Неправильный тип платформы, нажмите на кнопки ниже"),
                reply_markup=markups.buying_ads.thematics(data["thematics"]),
            )


async def audience_size_specify(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        _("Введите желаемый объем аудитории\n\nНапример: “1000-2000” или ”2000-4000”"),
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await BuyingAds.audience_size.set()


async def audience_size(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if call.data != "back":
        is_edit = data.get("edit")
        if not is_edit:
            data.update(audience_size=call.data)
        else:
            if is_edit == "thematic":
                if call.data != "next":
                    if call.data in data["thematics"]:
                        data["thematics"].remove(call.data)
                    else:
                        data["thematics"].append(call.data)
                    await state.update_data(data)
                    await call.message.edit_reply_markup(markups.buying_ads.thematics(data["thematics"]))
                    return

            else:
                data.update({is_edit: call.data})
                await state.update_data(data)
    logger.trace(f"{data=}")
    await call.message.delete()
    await call.message.answer(_("Вам подойдут следующие площадки"), reply_markup=markups.buying_ads.edit_field())
    await call.message.answer(str(data))
    await BuyingAds.edit_field.set()


async def audience_size_message(message: types.Message, state: FSMContext):
    # todo 01.04.2022 23:16 taima: parsing
    await state.update_data(audience_size=message.text)
    data = await state.get_data()
    await message.delete()
    await message.answer(_("Вам подойдут следующие площадки"), reply_markup=markups.buying_ads.edit_field())
    await message.answer(str(data))
    await BuyingAds.edit_field.set()


async def edit_field(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    method = call.data
    data = await state.get_data()
    if method == "platform_type":
        await call.message.answer(_("Выберите тип Телеграм-площадки"), reply_markup=markups.buying_ads.platform_type())

    elif method == "thematic":
        thematics_list = data.get("thematics")
        await call.message.answer(
            _("Выберите интересующие тематики"), reply_markup=markups.buying_ads.thematics(thematics_list)
        )

    # elif method == "audience_size":
    else:
        await call.message.answer(
            _("Укажите желаемый объем аудитории"), reply_markup=markups.buying_ads.audience_size()
        )

    await state.update_data(edit=method)
    await BuyingAds.audience_size.set()


def register_buying_ads_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(buying_start, text="buying_ads", state="*")
    dp.register_callback_query_handler(back, text="back", state=BuyingAds)

    dp.register_callback_query_handler(platform_type, state=BuyingAds.platform_type)
    dp.register_callback_query_handler(thematic, state=BuyingAds.thematic)

    dp.register_callback_query_handler(audience_size_specify, text="specify", state=BuyingAds.audience_size)
    dp.register_message_handler(audience_size_message, state=BuyingAds.audience_size)
    dp.register_callback_query_handler(audience_size, state=BuyingAds.audience_size)

    dp.register_callback_query_handler(edit_field, state=BuyingAds.edit_field)
