from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from botexchange.apps.bot import markups
from botexchange.loader import _


class SellingAds(StatesGroup):
    platform_type = State()
    add_platform = State()
    check = State()
    thematic = State()
    about = State()
    price = State()
    communication_type = State()
    communication = State()
    additional_communication = State()
    finish = State()


async def selling_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Каждая площадка добавляется в каталог на 15 дней на безвозмездной основе,"
                              " после чего автоматически снимается с публикации."
                              " Ее можно заново опубликовать с помощью раздела “мои площадки”",
                              reply_markup=markups.sell_ads.selling_menu())


async def selling_start(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Укажите тип вашей рекламной площадки", markups.sell_ads.platform_type())
    await SellingAds.first()


# todo 30.03.2022 22:49 taima: Проверить тип площадки и вывести соответствующее сообщение
async def platform_type(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(platform_type=call.data)
    data = await state.get_data()
    if data["platform_type"] == "bot":
        await call.message.answer(_("Пришлите юзернейм бота"), reply_markup=markups.sell_ads.add_platform())
    else:
        await call.message.answer(
            _("Добавьте @Ad Maker Bot в список администраторов вашего канала или чата, и перешлите сюда любое "
              "сообщение из него. Только таким образом мы сможем собрать точное число подписчиков, "
              "удостовериться что канал существует, и что вы его администратор.\n\nНе беспокойтесь - "
              "бот не будет как-либо взаимодействовать с вашей аудиторией или каналом, а только соберет актуальную "
              "информацию о нем.\n\nБот должен являться администратором канала на протяжении всего срока размещения "
              "площадки, иначе она будет изъята из каталога досрочно"),
            reply_markup=markups.sell_ads.add_platform())
    await SellingAds.next()


# todo 30.03.2022 23:24 taima:  Проверки корректности
async def add_platform(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(add_platform=call.data)
    await call.message.answer(_("Проверка успешно завершена"), reply_markup=markups.sell_ads.check())
    await SellingAds.next()


async def check(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(check=call.data)
    await call.message.answer(_("Выберите тематику вашей площадки"), reply_markup=markups.sell_ads.thematics())
    await SellingAds.next()


async def thematic(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(thematic=call.data)
    await call.message.answer(_("Пришлите текст, описывающий вашу площадку. Нужно уместиться в 80 символов\n\n"
                                "Например: “канал про топовые гаджеты с активной и вовлеченной аудиторией” "),
                              reply_markup=markups.sell_ads.about())
    await SellingAds.next()


async def about(obj: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(obj, types.CallbackQuery):
        await obj.message.delete()
    else:
        await obj.delete()
        await state.update_data(about=obj.text)

    await obj.answer(_("Укажите цену, которую собираетесь брать за размещение рекламы. "
                       "Не забудьте указать валюту!\n\nНапример: “От 1 000 до 2 000 руб”"),
                     reply_markup=markups.sell_ads.price())
    await SellingAds.next()


async def price(obj: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(obj, types.CallbackQuery):
        await obj.message.delete()
        obj = obj.message
    else:
        await obj.delete()
        await state.update_data(price=obj.text)

    await obj.answer(_("Выберите способ связи с вами. Он будет отображаться в вашем объявлении"),
                     reply_markup=markups.sell_ads.communication_type())
    await SellingAds.next()


# todo 30.03.2022 23:38 taima: ответ в зависимости от выбранной связи
async def communication_type(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(communication_type={call.data: None})
    data = await state.get_data()
    if data["communication_type"] == "phone":
        answer = _("Введите номер телефона\n\nНапример: ”+7 999 999 99 99”")
    elif data["communication_type"] == "email":
        answer = _("Введите Email\n\nНапример: ”example@example.com”")
    # tg
    else:
        # todo 30.03.2022 23:50 taima: Провести проверку телеграмма
        answer = _("Телеграмм успешно добавлен")
    await call.message.answer(answer, reply_markup=markups.sell_ads.communication())
    await SellingAds.next()


async def communication(obj: types.Message | types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    choice = list(filter(lambda x: x[1] is None, data["communication_type"].items()))[0][0]
    if isinstance(obj, types.CallbackQuery):
        logger.warning("Назад в коммуникации")
        await obj.message.delete()
        await SellingAds.previous()
        await communication_type(obj, state)
        obj = obj.message
    else:
        await obj.delete()
        data["communication_type"].update({choice: obj.text})
        if choice == "phone":
            communicate = _("Номер")
        elif choice == "email":
            communicate = _("Имейл")
        else:
            communicate = _("Телеграм")

        await obj.answer(
            _("{communicate} добавлен. Желаете казать дополнительный контакт?").format(communicate=communicate),
            reply_markup=markups.sell_ads.additional_communication(data["communication_type"].keys()))
        await SellingAds.next()


async def additional_communication(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(additional_communication=call.data)
    data = await state.get_data()
    if data["additional_communication"] == "finish":
        await call.message.answer(_("Площадка успешно добавлена в каталог на 15 дней. "
                                    "По истечении срока вы сможете повторно добавить ее "
                                    "в каталог через раздел “мои площадки”"),
                                  reply_markup=markups.sell_ads.finish())
        await SellingAds.next()
    else:
        logger.warning("Не реализовано")
        # todo 31.03.2022 1:03 taima: добавить при повторном выбери связи


# todo 31.03.2022 1:05 taima: убрать
async def finish(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data != "back":
        await state.update_data(finish=call.data)
    await call.message.answer(_("Выберите интересующие тематики"), reply_markup=markups.sell_ads.add_platform())
    await SellingAds.next()


def register_sell_ads_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(selling_menu, text="selling_ads", state="*")
    dp.register_callback_query_handler(selling_start, text="add_platform")
    dp.register_callback_query_handler(platform_type, state=SellingAds.platform_type)
    dp.register_callback_query_handler(add_platform, state=SellingAds.add_platform)
    dp.register_callback_query_handler(check, state=SellingAds.check)
    dp.register_callback_query_handler(thematic, state=SellingAds.thematic)

    dp.register_callback_query_handler(about, state=SellingAds.about)
    dp.register_message_handler(about, state=SellingAds.about)

    dp.register_callback_query_handler(price, state=SellingAds.price)
    dp.register_message_handler(price, state=SellingAds.price)

    dp.register_callback_query_handler(communication_type, state=SellingAds.communication_type)

    dp.register_callback_query_handler(communication, state=SellingAds.communication)
    dp.message_handlers(communication, state=SellingAds.communication)

    dp.register_callback_query_handler(additional_communication, state=SellingAds.additional_communication)

    dp.register_callback_query_handler(finish, state=SellingAds.finish)
