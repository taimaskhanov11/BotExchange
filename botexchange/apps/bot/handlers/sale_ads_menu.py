from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from botexchange.apps.bot import markups
from botexchange.apps.bot.handlers.base_menu import start
from botexchange.apps.bot.validators.sale_ads_validator import SaleAdsValidator
from botexchange.loader import _


class SellingAds(StatesGroup):
    platform_type = State()
    add_platform = State()
    check = State()
    thematic = State()
    about = State()
    currency = State()
    price = State()
    communication_type = State()
    communication = State()
    additional_communication = State()
    finish = State()


async def back(call: types.CallbackQuery, state: FSMContext):
    logger.trace(f"back {call}")
    pre_state = await SellingAds.previous()
    # new_state = await SellingAds.previous()
    # new_state1 = await SellingAds.previous()
    # logger.trace(f"{pre_state=}")
    # logger.trace(f"{new_state=}")
    # logger.trace(f"{new_state1=}")
    if pre_state:
        new_state = await SellingAds.previous()
        logger.trace(f"{new_state=}")
        if new_state:
            method = new_state.split(":")[1]
            logger.trace(f"Предыдущая стадия {pre_state=}")
            logger.trace(f"Текущая стадия {new_state=}")
            await globals()[method](call, state)
        else:
            await selling_start(call, state)
    else:
        await selling_menu(call, state)


async def selling_menu(call: types.CallbackQuery, state: FSMContext):
    logger.trace(f"selling_menu|{call.data=}")
    if call.data == "back":
        await start(call, state)
        return
    await state.finish()
    await call.message.delete()
    await call.message.answer(
        "Каждая площадка добавляется в каталог на 15 дней на безвозмездной основе,"
        " после чего автоматически снимается с публикации."
        " Ее можно заново опубликовать с помощью раздела “мои площадки”",
        reply_markup=markups.sale_ads.selling_menu(),
    )


async def selling_start(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Укажите тип вашей рекламной площадки", reply_markup=markups.sale_ads.platform_type())
    await SellingAds.first()


# todo 30.03.2022 22:49 taima: Проверить тип площадки и вывести соответствующее сообщение
async def platform_type(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(platform_type=call.data)
    data = await state.get_data()
    if data["platform_type"] == "bot":
        await call.message.answer(_("Пришлите юзернейм бота"), reply_markup=markups.sale_ads.add_platform())
    else:
        await call.message.answer(
            _(
                "Добавьте @Ad Maker Bot в список администраторов вашего канала или чата, и перешлите сюда любое "
                "сообщение из него. Только таким образом мы сможем собрать точное число подписчиков, "
                "удостовериться что канал существует, и что вы его администратор.\n\nНе беспокойтесь - "
                "бот не будет как-либо взаимодействовать с вашей аудиторией или каналом, а только соберет актуальную "
                "информацию о нем.\n\nБот должен являться администратором канала на протяжении всего срока размещения "
                "площадки, иначе она будет изъята из каталога досрочно"
            ),
            reply_markup=markups.sale_ads.add_platform(),
        )
    await SellingAds.next()


# todo 30.03.2022 23:24 taima:  Проверки корректности
async def add_platform(obj: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(obj, types.CallbackQuery):
        obj = obj.message
    else:
        await state.update_data(add_platform=obj.text)
    await obj.delete()
    await obj.answer(_("Проверка успешно завершена"), reply_markup=markups.sale_ads.check())
    await SellingAds.next()


async def check(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(check=call.data)
    await call.message.answer(_("Выберите тематику вашей площадки"), reply_markup=markups.sale_ads.thematics())
    await SellingAds.next()


async def thematic(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        if SaleAdsValidator.thematic(call.data):
            await state.update_data(thematic=call.data)
        else:
            await call.message.answer(
                _("Неправильный ввод. Выберите тематику из списка"), reply_markup=markups.sale_ads.thematics()
            )
            return
    await call.message.answer(
        _(
            "Пришлите текст, описывающий вашу площадку. Нужно уместиться в 80 символов\n\n"
            "Например: “канал про топовые гаджеты с активной и вовлеченной аудиторией” "
        ),
        reply_markup=markups.sale_ads.about(),
    )
    await SellingAds.next()


async def about(obj: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(obj, types.CallbackQuery):
        await obj.message.delete()
        obj = obj.message
    else:
        await obj.delete()
        if SaleAdsValidator.about(obj.text):
            await state.update_data(about=obj.text)
        else:
            await obj.answer(_("Длинна текста превышает 80 символов"))
            return
    await obj.answer(_("Выберите валюту"), reply_markup=markups.sale_ads.currency())
    await SellingAds.next()


async def currency(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        if SaleAdsValidator.currency(call.data):
            await state.update_data(currency=call.data)
        else:
            await call.message.answer(
                _("Неправильный ввод валюты, нажмите на кнопку ниже"), reply_markup=markups.sale_ads.currency()
            )
            return
    await call.message.answer(
        _("Пришлите цену, которую собираетесь брать за размещение рекламы" "\n\nНапример: “500” или ”400-1000”"),
        reply_markup=markups.sale_ads.price(),
    )
    await SellingAds.next()


async def price(obj: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(obj, types.CallbackQuery):
        await obj.message.delete()
        obj = obj.message
    else:
        await obj.delete()
        if _price := SaleAdsValidator.price(obj.text):
            await state.update_data(price=_price, communication_type=dict())
        else:
            await obj.answer(
                _(
                    "Не удалось найти цены, проверьте правильность ввода.\nЕсли вы указали промежуток, "
                    "то минимальная сумма не должна превышать максимальную"
                )
            )
            return
    await obj.answer(
        _("Выберите способ связи с вами. Он будет отображаться в вашем объявлении"),
        reply_markup=markups.sale_ads.communication_type(),
    )
    await SellingAds.next()


async def communication_type(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if call.data != "back":
        if SaleAdsValidator.communication_type(call.data):
            for i in ["phone", "tg", "email"]:
                if data["communication_type"].get(i) is False:
                    del data["communication_type"][i]
            data["communication_type"].update({call.data: False})
            await state.update_data(data=data)
        else:
            await call.message.answer(
                _("Выберите способ связи из списка"),
                reply_markup=markups.sale_ads.communication_type(),
            )
            return
    logger.trace(f"communication_type|{data=}")
    choice = list(filter(lambda x: x[1] is False, data["communication_type"].items()))[0][0]
    okay = False
    if choice == "phone":
        answer = _("Введите номер телефона\n\nНапример: ”+7 999 999 99 99”")
    elif choice == "email":
        answer = _("Введите Email\n\nНапример: ”example@example.com”")
    # tg
    else:
        await communication(call, state)
        return
    await call.message.delete()
    await call.message.answer(answer, reply_markup=markups.sale_ads.communication(okay))
    await SellingAds.communication.set()


async def communication(obj: types.Message | types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    choice = list(filter(lambda x: x[1] is False, data["communication_type"].items()))[0][0]
    logger.info(f"{choice=}")
    if isinstance(obj, types.CallbackQuery):
        # logger.warning("Назад в коммуникации")
        # await obj.message.delete()
        # await SellingAds.previous()
        # await communication_type(obj, state)
        obj = obj.message

    logger.trace(f"communication|{data=}")
    if choice == "phone":
        data["communication_type"].update({choice: obj.text})
        communicate = _("Номер")
    elif choice == "email":
        data["communication_type"].update({choice: obj.text})
        communicate = _("Имейл")
    else:
        if await SaleAdsValidator.communication_type_tg(obj.from_user.id):
            data["communication_type"].update({choice: True})
            communicate = _("Телеграм")
        else:
            del data["communication_type"][choice]
            await state.update_data(data=data)
            await obj.answer(_("Произошла ошибка. Ваш профиль должен быть открытым"))
            return
    await obj.delete()
    await state.update_data(data=data)
    await obj.answer(
        _("{communicate} добавлен. Желаете казать дополнительный контакт?").format(communicate=communicate),
        reply_markup=markups.sale_ads.additional_communication(data["communication_type"].keys()),
    )
    await SellingAds.additional_communication.set()


async def additional_communication(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if call.data == "finish":
        await call.message.delete()
        await call.message.answer(
            _(
                "Площадка успешно добавлена в каталог на 15 дней. "
                "По истечении срока вы сможете повторно добавить ее "
                "в каталог через раздел “мои площадки”"
            ),
            reply_markup=markups.sale_ads.finish(),
        )

        await call.message.answer(str(data))
        await state.finish()
        # await SellingAds.next()
    else:
        # if call.data != "back":
        #     await state.update_data(additional_communication=call.data)
        await communication_type(call, state)
        logger.warning("Дополнительный способ связи")
        # todo 31.03.2022 1:03 taima: добавить при повторном выбери связи


# todo 31.03.2022 1:05 taima: убрать
async def finish(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(finish=call.data)
    await call.message.answer(_("Выберите интересующие тематики"), reply_markup=markups.sale_ads.finish())
    await SellingAds.next()


def register_sale_ads_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(selling_menu, text="selling_ads", state="*")
    dp.register_callback_query_handler(selling_start, text="add_platform")
    # todo 31.03.2022 12:00 taima: стадия
    # dp.register_callback_query_handler(back, text="back", state="*")
    dp.register_callback_query_handler(back, text="back", state=SellingAds)

    dp.register_callback_query_handler(platform_type, state=SellingAds.platform_type)

    dp.register_callback_query_handler(add_platform, state=SellingAds.add_platform)
    dp.register_message_handler(add_platform, state=SellingAds.add_platform)

    dp.register_callback_query_handler(check, state=SellingAds.check)
    dp.register_callback_query_handler(thematic, state=SellingAds.thematic)

    dp.register_callback_query_handler(about, state=SellingAds.about)
    dp.register_message_handler(about, state=SellingAds.about)

    dp.register_callback_query_handler(currency, state=SellingAds.currency)

    dp.register_callback_query_handler(price, state=SellingAds.price)
    dp.register_message_handler(price, state=SellingAds.price)

    dp.register_callback_query_handler(communication_type, state=SellingAds.communication_type)

    dp.register_callback_query_handler(communication, state=SellingAds.communication)
    dp.register_message_handler(communication, state=SellingAds.communication)

    dp.register_callback_query_handler(additional_communication, state=SellingAds.additional_communication)

    dp.register_callback_query_handler(finish, state=SellingAds.finish)
