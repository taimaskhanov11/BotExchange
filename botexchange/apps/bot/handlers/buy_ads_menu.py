from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from botexchange.apps.bot import markups
from botexchange.apps.bot.handlers.base_menu import start
from botexchange.loader import _


class BuyingAds(StatesGroup):
    platform_type = State()
    thematic = State()
    audience_size = State()
    budget = State()


async def back(call: types.CallbackQuery, state: FSMContext):
    pre_state = await BuyingAds.previous()
    if pre_state:
        new_state = await BuyingAds.previous()
        if new_state:
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
    await call.message.answer(_("Выберите тип Телеграм-площадки"), reply_markup=markups.buy_ads.platform_type())
    await BuyingAds.first()


async def platform_type(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(platform_type=call.data)
    await call.message.answer(_("Выберите интересующие тематики"), reply_markup=markups.buy_ads.thematics())
    await BuyingAds.next()


async def thematic(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(thematic=call.data)
    await call.message.answer(_("Укажите желаемый объем аудитории"), reply_markup=markups.buy_ads.audience_size())
    await BuyingAds.next()


async def audience_size(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(audience_size=call.data)
    await call.message.answer(_("Укажите бюджет за размещение"), reply_markup=markups.buy_ads.budget())
    await BuyingAds.next()


async def budget_and_done(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(budget=call.data)
    await call.message.answer(_("Вам подойдут следующие площадки"), reply_markup=markups.buy_ads.edit_field())
    data = await state.get_data()
    await call.message.answer(str(data))
    await state.finish()


def register_buy_ads_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(buying_start, text="buying_ads")
    dp.register_callback_query_handler(back, text="back", state=BuyingAds)

    dp.register_callback_query_handler(platform_type, state=BuyingAds.platform_type)
    dp.register_callback_query_handler(thematic, state=BuyingAds.thematic)
    dp.register_callback_query_handler(audience_size, state=BuyingAds.audience_size)
    dp.register_callback_query_handler(budget_and_done, state=BuyingAds.budget)
