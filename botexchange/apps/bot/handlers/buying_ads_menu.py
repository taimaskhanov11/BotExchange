from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from botexchange.apps.bot import markups
from botexchange.apps.bot.handlers.base_menu import start
from botexchange.apps.bot.utils.search_helpers import PlatformSearch
from botexchange.apps.bot.validators.buying_ads_validator import BuyingAdsValidator
from botexchange.config.config import MESSAGE_DELETE
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
    # await call.message.edit_text(_("Выберите тип Телеграм-площадки"))
    # await call.message.edit_reply_markup(markups.buying_ads.platform_type())
    if MESSAGE_DELETE:
        await call.message.delete()
    await call.message.answer(
        _("Выберите тип Телеграм-площадки"),
        reply_markup=markups.buying_ads.platform_type(),
    )

    await BuyingAds.platform_type.set()


async def platform_type(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logger.trace(f"platform_type|{data=}")
    thematics_list = data.get("thematics", [])
    await state.update_data(page=1)
    if call.data != "back" and not thematics_list:

        if MESSAGE_DELETE:
            await call.message.delete()

        # валидация
        if not BuyingAdsValidator.platform_type(call.data):
            logger.warning("Неправильный тип платформы")
            await call.message.answer(
                _("Неправильный ввод, нажмите на кнопки ниже"),
                reply_markup=markups.buying_ads.platform_type(),
            )
            return
        data.update(platform_type=call.data, thematics=thematics_list, page=1)
        await state.update_data(data)

        await call.message.answer(
            _("Выберите интересующие тематики"),
            reply_markup=markups.common.thematics(data),
        )
    else:
        logger.trace(call)
        await call.message.edit_reply_markup(markups.common.thematics(data))
    await BuyingAds.thematic.set()


# todo 01.04.2022 13:29 taima: добавить далее для тематик
async def thematic(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logger.trace(f"thematic|{data=}")
    if call.data in ["next", "back"]:
        if MESSAGE_DELETE:
            await call.message.delete()
        await call.message.answer(
            _("Укажите желаемый объем аудитории"),
            reply_markup=markups.buying_ads.audience_size(),
        )
        await BuyingAds.audience_size.set()

    else:
        if BuyingAdsValidator.thematic(call.data, data["platform_type"]):
            if call.data == "left":
                data["page"] -= 1
            elif call.data == "right":
                data["page"] += 1
            else:
                if call.data in data["thematics"]:
                    data["thematics"].remove(call.data)
                else:
                    data["thematics"].append(call.data)
            await state.update_data(data)
            await call.message.edit_reply_markup(markups.common.thematics(data))
            # await platform_type(call, state)
        else:
            logger.warning("Неправильный тип платформы")
            await call.message.answer(
                _("Неправильный тип платформы, нажмите на кнопки ниже"),
                reply_markup=markups.common.thematics(data),
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
            _audience_size = BuyingAdsValidator.audience_size(call.data)
            if _audience_size is not False:
                await state.update_data(audience_size=_audience_size)
            else:
                await call.message.answer(_("Неправильный ввод, повторите попытку"))
                return
        else:
            if is_edit == "thematic":
                if call.data != "next":
                    if BuyingAdsValidator.thematic(call.data, data["platform_type"]):
                        if call.data == "left":
                            data["page"] -= 1
                        elif call.data == "right":
                            data["page"] += 1
                        else:
                            if call.data in data["thematics"]:
                                data["thematics"].remove(call.data)
                            else:
                                data["thematics"].append(call.data)
                        await state.update_data(data)
                        await call.message.edit_reply_markup(markups.common.thematics(data))
                    else:
                        logger.warning("Неправильный тип платформы")
                        await call.message.answer(
                            _("Неправильный тип платформы, нажмите на кнопки ниже"),
                            reply_markup=markups.common.thematics(data),
                        )
                    return
            elif is_edit == "audience_size":
                _audience_size = BuyingAdsValidator.audience_size(call.data)
                if _audience_size is not False:
                    data.update({is_edit: _audience_size})
                    await state.update_data(data)
                else:
                    await call.message.answer(_("Неправильный ввод, повторите попытку"))
                    return
            else:
                data.update({is_edit: call.data})
                await state.update_data(data)
    data = await state.get_data()
    logger.trace(f"{data=}")
    if MESSAGE_DELETE:
        await call.message.delete()
    # await call.message.answer(_("Вам подойдут следующие площадки"), reply_markup=markups.buying_ads.edit_field())
    platform_searcher = PlatformSearch(**data)
    find = await platform_searcher.search()

    if not find:
        answer = _("По вашим критерям ничего не найдено :(")
    else:
        answer = _("Вам подойдут следующие площадки:\n\n{find}").format(find=find)
    await call.message.answer(answer, reply_markup=markups.buying_ads.edit_field(), parse_mode="HTML")
    await BuyingAds.edit_field.set()


async def audience_size_message(message: types.Message, state: FSMContext):
    _audience_size = BuyingAdsValidator.audience_size(message.text)
    if _audience_size is not False:
        await state.update_data(audience_size=_audience_size)
    else:
        await message.answer(_("Неправильный ввод, повторите попытку"))
        return
    data = await state.get_data()
    if MESSAGE_DELETE:
        await message.delete()
    # await message.answer(_("Вам подойдут следующие площадки"), reply_markup=markups.buying_ads.edit_field())
    platform_searcher = PlatformSearch(**data)
    find = await platform_searcher.search()
    if not find:
        answer = _("По вашим критерям ничего не найдено :(")
    else:
        answer = _("Вам подойдут следующие площадки:\n\n{find}").format(find=find)
    await message.answer(answer, reply_markup=markups.buying_ads.edit_field(), parse_mode="HTML")
    await BuyingAds.edit_field.set()


async def edit_field(call: types.CallbackQuery, state: FSMContext):
    if MESSAGE_DELETE:
        await call.message.delete()
    method = call.data
    data = await state.get_data()
    if method == "platform_type":
        await call.message.answer(
            _("Выберите тип Телеграм-площадки"),
            reply_markup=markups.buying_ads.platform_type(),
        )

    elif method == "thematic":
        await call.message.answer(
            _("Выберите интересующие тематики"),
            reply_markup=markups.common.thematics(data),
        )

    # elif method == "audience_size":
    else:
        await call.message.answer(
            _("Укажите желаемый объем аудитории"),
            reply_markup=markups.buying_ads.audience_size(),
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
