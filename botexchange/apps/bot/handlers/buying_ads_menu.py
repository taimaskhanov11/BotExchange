from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from botexchange.apps.bot import markups
from botexchange.apps.bot.handlers.base_menu import start
from botexchange.loader import _


class BuyingAds(StatesGroup):
    platform_type = State()
    thematic = State()
    audience_size = State()
    budget = State()
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
    # await call.message.edit_text(_("Выберите тип Телеграм-площадки"))
    # await call.message.edit_reply_markup(markups.platform_type())
    await call.message.delete()
    await call.message.answer(_("Выберите тип Телеграм-площадки"), reply_markup=markups.buying_ads.platform_type())
    await BuyingAds.platform_type.set()


async def platform_type(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logger.trace(f"platform_type|{data=}")
    thematics_list = data.get("thematics") or []
    if call.data != "back" and not thematics_list:
        await call.message.delete()
        await state.update_data(platform_type=call.data, thematics=thematics_list)
        await call.message.answer(
            _("Выберите интересующие тематики"), reply_markup=markups.buying_ads.thematics(thematics_list)
        )
    else:
        logger.trace(call)
        # await call.message.edit_text("<kf,kf")
        await call.message.edit_reply_markup(markups.buying_ads.thematics(thematics_list))
    await BuyingAds.thematic.set()


async def thematic(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logger.trace(f"thematic|{data=}")
    if call.data in ["next", "back"]:
        await call.message.delete()
        # if call.data != "back":
        #     data["thematics"].append(call.data)
        #     await state.update_data(data)
        await call.message.answer(
            _("Укажите желаемый объем аудитории"), reply_markup=markups.buying_ads.audience_size()
        )
        await BuyingAds.audience_size.set()
    else:
        if call.data in data["thematics"]:
            data["thematics"].remove(call.data)
        else:
            data["thematics"].append(call.data)
        await state.update_data(data)
        await platform_type(call, state)


async def audience_size(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(audience_size=call.data)
    await call.message.answer(_("Укажите бюджет за размещение"), reply_markup=markups.buying_ads.budget())
    await BuyingAds.budget.set()


async def budget_and_done(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    is_edit = data.get("edit")

    if call.data != "back":
        if not is_edit:
            data.update(budget=call.data)
        else:
            data.update({is_edit: call.data})
            # await state.update_data(budget=call.data)
    await call.message.answer(_("Вам подойдут следующие площадки"), reply_markup=markups.buying_ads.edit_field())
    # data = await state.get_data()
    await call.message.answer(str(data))
    await BuyingAds.edit_field.set()


async def edit_field(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    # if call.data != "back":
    #     await state.update_data(budget=call.data)
    method = call.data
    if method == "platform_type":
        await call.message.answer(_("Выберите тип Телеграм-площадки"), reply_markup=markups.buying_ads.platform_type())

    elif method == "thematic":
        await call.message.answer(_("Выберите интересующие тематики"), reply_markup=markups.buying_ads.thematics())

    elif method == "audience_size":
        await call.message.answer(
            _("Укажите желаемый объем аудитории"), reply_markup=markups.buying_ads.audience_size()
        )
    # method == "budget"
    else:
        await call.message.answer(_("Укажите бюджет за размещение"), reply_markup=markups.buying_ads.budget())

    await state.update_data(edit=method)
    await BuyingAds.budget.set()
    # await globals()[method](call, state)


def register_buying_ads_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(buying_start, text="buying_ads", state="*")
    dp.register_callback_query_handler(back, text="back", state=BuyingAds)

    dp.register_callback_query_handler(platform_type, state=BuyingAds.platform_type)
    dp.register_callback_query_handler(thematic, state=BuyingAds.thematic)
    dp.register_callback_query_handler(audience_size, state=BuyingAds.audience_size)
    dp.register_callback_query_handler(budget_and_done, state=BuyingAds.budget)
    dp.register_callback_query_handler(edit_field, state=BuyingAds.edit_field)
