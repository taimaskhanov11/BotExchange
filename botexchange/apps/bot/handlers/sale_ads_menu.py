from pprint import pprint

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from botexchange.apps.bot import markups
from botexchange.apps.bot.handlers.base_menu import start
from botexchange.apps.bot.validators.sale_ads_validator import SaleAdsValidator
from botexchange.config.config import MESSAGE_DELETE
from botexchange.db.models import AdvertisingPlatform, User, _


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


class AddBotPlatform(StatesGroup):
    add = State()


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
    if MESSAGE_DELETE:
        await call.message.delete()

    await call.message.answer(
        "Каждая площадка добавляется в каталог на 15 дней на безвозмездной основе,"
        " после чего автоматически снимается с публикации."
        " Ее можно заново опубликовать с помощью раздела “мои площадки”",
        reply_markup=markups.sale_ads.selling_menu(),
    )


async def selling_start(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    if MESSAGE_DELETE:
        await call.message.delete()
    await call.message.answer("Укажите тип вашей рекламной площадки", reply_markup=markups.sale_ads.platform_type())
    await SellingAds.first()


async def platform_type(call: types.CallbackQuery, state: FSMContext):
    if MESSAGE_DELETE:
        await call.message.delete()
    if call.data != "back":
        await state.update_data(platform_type=call.data)

    data = await state.get_data()
    if data["platform_type"] == "bot":
        await call.message.answer(
            _("Перешлите сюда любое сообщение из вашего бота"), reply_markup=markups.sale_ads.about()
        )
        await AddBotPlatform.add.set()
        return
    else:
        await call.message.answer(
            _(
                "Добавьте @{username} в список администраторов вашего канала или чата. "
                "У него должны быть права для создания пригласительных ссылок\n"
                "Только таким образом мы сможем собрать точное число подписчиков, "
                "удостовериться что канал существует, и что вы его администратор.\n\nНе беспокойтесь - "
                "бот не будет как-либо взаимодействовать с вашей аудиторией или каналом, а только соберет актуальную "
                "информацию о нем.\n\nБот должен являться администратором канала на протяжении всего срока размещения "
                "площадки, иначе она будет изъята из каталога досрочно."
                "\n\nПосле добавления и назначения администратором нажмите `Готово`"
            ).format(username=(await call.bot.get_me()).username),
            reply_markup=markups.sale_ads.add_platform(),
        )
        # await SellingAds.add.set()
    await SellingAds.next()


async def add_bot_platform_call(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back":
        # await SellingAds.platform_type.set()
        await selling_start(call, state)


async def add_bot_platform(message: types.Message, state: FSMContext):
    data = await state.get_data()
    forward = message.forward_from
    pprint(message.to_python())
    # pprint(f"{forward.to_python()=}")
    if data["platform_type"] == "bot":
        if forward:
            if forward.is_bot:
                await state.update_data(bot_info=forward.to_python())
                await message.answer(
                    _(
                        "Чтобы удостовериться что вы владелец бота,"
                        " добавьте к имени вашего бота `сheckingforaddition` на время проверки."
                        " (Изменить название вашего бота можно через @BotFather)"
                    ),
                    reply_markup=markups.sale_ads.add_platform(),
                )

        else:
            await message.answer(_("Это сообщения не из телеграм-бота, пожалуйста повторите попытку"))
            return

    await SellingAds.add_platform.set()


# todo 30.03.2022 23:24 taima:  Проверки корректности
async def add_platform(call: types.CallbackQuery, state: FSMContext):
    obj = call.message
    data = await state.get_data()
    chat_type = data["platform_type"]
    if data["platform_type"] == "channel":
        if chat_info := data.get("chat_info"):
            chat_type = _("Чат") if chat_info["type"] == "supergroup" else _("Канал")
        else:
            await obj.answer(
                _(
                    "Не удалось найти ваш чат. Проверьте что вы добавляете бота как администратора со своего аккаунта."
                    " Если не помогло попробуйте исключить и заново добавить бота в чат/канал"
                )
            )
            return

    elif data["platform_type"] == "bot":
        bot_info = types.User.to_object(data.get("bot_info"))
        new_bot_info = await call.bot.get_chat(bot_info.id)
        logger.debug(bot_info)
        logger.debug(new_bot_info)
        if "сheckingforaddition" not in new_bot_info.first_name:
            await call.message.answer(
                _(
                    "Не найдено изменений в имени бота, "
                    "добавьте к названию вашего бота `сheckingforaddition` чтобы понять, "
                    "что бот принадлежит вам"
                )
            )
            return

    if MESSAGE_DELETE:
        await call.message.delete()
    answer = _("Проверка успешно завершена, ваш {chat} найден")
    if data["platform_type"] == "bot":
        answer += _(". Можете вернуть имя бота")
    await call.message.answer(answer.format(chat=chat_type), reply_markup=markups.sale_ads.check())
    await SellingAds.next()


async def check(call: types.CallbackQuery, state: FSMContext):
    if MESSAGE_DELETE:
        await call.message.delete()
    if call.data != "back":
        await state.update_data(check=call.data)

    await call.message.answer(_("Выберите тематику вашей площадки"), reply_markup=markups.sale_ads.thematics())
    await SellingAds.next()


async def thematic(call: types.CallbackQuery, state: FSMContext):
    if MESSAGE_DELETE:
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
        if MESSAGE_DELETE:
            await obj.message.delete()
        obj = obj.message
    else:
        if MESSAGE_DELETE:
            await obj.delete()
        if SaleAdsValidator.about(obj.text):
            await state.update_data(about=obj.text)
        else:
            await obj.answer(_("Длинна текста превышает 80 символов"))
            return
    await obj.answer(_("Выберите валюту"), reply_markup=markups.sale_ads.currency())
    await SellingAds.next()


async def currency(call: types.CallbackQuery, state: FSMContext):
    if MESSAGE_DELETE:
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
        if MESSAGE_DELETE:
            await obj.message.delete()
        obj = obj.message
    else:
        if MESSAGE_DELETE:
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
    if MESSAGE_DELETE:
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
        if await SaleAdsValidator.communication_type_phone(obj.text):
            data["communication_type"].update({choice: obj.text})
            communicate = _("Номер")
        else:
            await obj.answer(_("Не удалось найти номер, проверьте правильность веденных данных и повторите попытку"))
            return
    elif choice == "email":
        if await SaleAdsValidator.communication_type_email(obj.text):
            data["communication_type"].update({choice: obj.text})
            communicate = _("Имейл")
        else:
            await obj.answer(_("Не удалось найти email, проверьте правильность веденных данных и повторите попытку"))
            return

    else:
        if await SaleAdsValidator.communication_type_tg(obj.from_user.id):
            data["communication_type"].update({choice: True})
            communicate = _("Телеграм")
        else:
            del data["communication_type"][choice]
            await state.update_data(data=data)
            await obj.answer(_("Произошла ошибка. Ваш профиль должен быть открытым"))
            return
    if MESSAGE_DELETE:
        await obj.delete()
    await state.update_data(data=data)
    await obj.answer(
        _("{communicate} добавлен. Желаете казать дополнительный контакт?").format(communicate=communicate),
        reply_markup=markups.sale_ads.additional_communication(data["communication_type"].keys()),
    )
    await SellingAds.additional_communication.set()


# Finish
async def additional_communication(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if call.data == "finish":
        if MESSAGE_DELETE:
            await call.message.delete()
        await call.message.answer(str(data))
        owner = await User.get(user_id=call.from_user.id)
        _price = data.get("price")
        if isinstance(_price, tuple):
            _min_price, _max_price = _price
        else:
            _min_price = 0
            _max_price = _price

        common_platform_info = {
            "owner": owner,
            "about": data.get("about"),
            "thematic": data.get("thematic"),
            "currency": data.get("currency"),
            "min_price": _min_price,
            "max_price": _max_price,
            "tg": data["communication_type"].get("tg"),
            "phone": data["communication_type"].get("phone"),
            "email": data["communication_type"].get("email"),
            # "is_hidden": data.get("is_hidden"),
            # "views": data.get("views"),
            # "duration": data.get("duration"),
        }
        if data["platform_type"] == "bot":
            common_platform_info.update(
                {
                    "platform_type": data["platform_type"],
                    "chat_id": data["bot_info"].get("id"),
                    "title": data["bot_info"].get("first_name"),
                    "link": f'@{data["bot_info"].get("username")}',
                }
            )

        else:
            _platform_type = "group" if data["chat_info"].get("type") == "supergroup" else data["chat_info"].get("type")

            common_platform_info.update(
                {
                    "platform_type": _platform_type,
                    "chat_id": data["chat_info"].get("chat_id"),
                    "title": data["chat_info"].get("title"),
                    "link": data["chat_info"].get("link"),
                    "audience_size": data["chat_info"].get("members_count"),
                }
            )

        # Добавление площадки
        platform = await AdvertisingPlatform.create(**common_platform_info)
        logger.success(f"Платформа {platform} успешно создана")

        await call.message.answer(
            _(
                "Площадка успешно добавлена в каталог на 15 дней. "
                "По истечении срока вы сможете повторно добавить ее "
                "в каталог через раздел “мои площадки”"
            ),
            reply_markup=markups.sale_ads.finish(),
        )

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
    if MESSAGE_DELETE:
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

    # todo 02.04.2022 14:16 taima:
    dp.register_message_handler(add_bot_platform, state=AddBotPlatform.add)
    dp.register_callback_query_handler(add_bot_platform_call, state=AddBotPlatform.add)

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
