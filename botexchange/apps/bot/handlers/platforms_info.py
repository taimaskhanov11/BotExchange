from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from botexchange.apps.bot import markups
from botexchange.apps.bot.filters.base_filters import UserFilter
from botexchange.apps.bot.utils.search_helpers import pretty_view
from botexchange.apps.bot.validators.sale_ads_validator import SaleAdsValidator
from botexchange.db.models import AdvertisingPlatform, User
from botexchange.loader import _


class DeletePlatform(StatesGroup):
    delete = State()


class EditPlatform(StatesGroup):
    edit_platform = State()
    edit_thematic = State()
    edit_description = State()
    edit_currency = State()
    edit_price = State()
    edit_communication = State()


class EditCommunication(StatesGroup):
    phone = State()
    email = State()
    tg = State()


async def my_platforms(call: types.CallbackQuery, state: FSMContext, user: User):
    # pprint(dir(user))
    platforms = await user.advertisingplatforms.all().order_by("-id")
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


async def get_platform(call: types.CallbackQuery, state: FSMContext):
    pk = call.data[9:]
    platform = await AdvertisingPlatform.get(pk=pk)
    await state.update_data(pk=pk)
    await call.message.answer(
        pretty_view(platform),
        parse_mode=types.ParseMode.HTML,
        reply_markup=markups.platforms_info.platform_view(pk),
    )


async def get_platform_message(message: types.Message, state: FSMContext):
    pk = message.text
    platform = await AdvertisingPlatform.get(pk=pk)
    await state.update_data(pk=pk)
    await message.answer(
        pretty_view(platform),
        parse_mode=types.ParseMode.HTML,
        reply_markup=markups.platforms_info.platform_view(pk),
    )


async def default_view_platform(message: types.CallbackQuery | types.Message, platform: AdvertisingPlatform):
    if isinstance(message, types.CallbackQuery):
        message = message.message

    await message.answer(
        pretty_view(platform),
        parse_mode=types.ParseMode.HTML,
        reply_markup=markups.platforms_info.platform_view(platform.pk),
    )


async def extend_platform(call: types.CallbackQuery, state: FSMContext):
    pk = call.data[7:]
    platform = await AdvertisingPlatform.get(pk=pk)
    await platform.refresh_duration()
    await call.message.answer(
        _("Срок активности обновлен. До деактивации {duration} дней.".format(duration=platform.duration)),
        reply_markup=markups.platforms_info.extend_platform(),
    )


async def delete_platform(call: types.CallbackQuery, state: FSMContext):
    pk = call.data[7:]
    await state.update_data(delete_platform=pk)
    platform = await AdvertisingPlatform.get(pk=pk)
    await call.message.answer(
        _("Уверены что хотите удалить площадку {title}?").format(title=platform.title),
        reply_markup=markups.platforms_info.delete_platform(),
    )
    await DeletePlatform.delete.set()


async def delete_platform_done(call: types.CallbackQuery, state: FSMContext):
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


async def edit_platform(call: types.CallbackQuery, state: FSMContext):
    pk = call.data[14:]
    await state.update_data(pk=pk)
    await call.message.edit_reply_markup(markups.platforms_info.edit_platform_platform(pk))


async def edit_thematic(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(page=1)
    data = await state.get_data()
    await call.message.answer(
        _("Выберите тематику вашей площадки"),
        reply_markup=markups.common.thematics(data),
    )
    await EditPlatform.edit_thematic.set()


async def edit_thematic_done(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pk = data.get("pk")
    platform = await AdvertisingPlatform.get(pk=pk)

    if call.data == "back":
        await state.finish()
        await default_view_platform(call, platform)
        return

    if SaleAdsValidator.thematic(call.data, platform.platform_type):
        if call.data == "left":
            data["page"] -= 1
            await call.message.edit_reply_markup(markups.common.thematics(data))
            await state.update_data(data)
            return
        elif call.data == "right":
            data["page"] += 1
            await call.message.edit_reply_markup(markups.common.thematics(data))
            await state.update_data(data)
            return
        else:
            await platform.update_thematic(call.data)
            await call.message.answer(_("Тематика успешно обновлена"))
            await state.finish()
            await default_view_platform(call, platform)
            return
    else:
        await call.message.answer(
            _("Неправильный ввод. Выберите тематику из списка"),
            reply_markup=markups.common.thematics(data),
        )


async def edit_description(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        _(
            "Пришлите текст, описывающий вашу площадку. Нужно уместиться в 80 символов\n\n"
            "Например: “канал про топовые гаджеты с активной и вовлеченной аудиторией” "
        )
    )
    await EditPlatform.edit_description.set()


async def edit_description_done_call(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pk = data.get("pk")
    platform = await AdvertisingPlatform.get(pk=pk)
    if call.data == "back":
        await state.finish()
        await default_view_platform(call, platform)
        return


async def edit_description_done(message: types.Message | types.CallbackQuery, state: FSMContext):
    if SaleAdsValidator.about(message.text):
        data = await state.get_data()
        pk = data.get("pk")
        platform = await AdvertisingPlatform.get(pk=pk)
        await platform.update_about(message.text)
        await message.answer(_("Тематика успешно обновлена"))
        await state.finish()
        await default_view_platform(message, platform)
    else:
        await message.answer(_("Длинна текста превышает 80 символов"))


async def edit_currency(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(_("Выберите валюту"), reply_markup=markups.sale_ads.currency())
    await EditPlatform.edit_currency.set()


async def edit_currency_done(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pk = data.get("pk")
    platform = await AdvertisingPlatform.get(pk=pk)

    if call.data == "back":
        await state.finish()
        await default_view_platform(call, platform)
        return

    if SaleAdsValidator.currency(call.data):
        await platform.update_currency(call.data)
        await call.message.answer(_("Валюта успешно обновлена"))
        await state.finish()
        await default_view_platform(call, platform)

    else:
        await call.message.answer(
            _("Неправильный ввод валюты, нажмите на кнопку ниже"),
            reply_markup=markups.sale_ads.currency(),
        )


async def edit_price(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        _("Пришлите цену, которую собираетесь брать за размещение рекламы" "\n\nНапример: “500” или ”400-1000”"),
        reply_markup=markups.sale_ads.price(),
    )
    await EditPlatform.edit_price.set()


async def edit_price_done_call(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pk = data.get("pk")
    platform = await AdvertisingPlatform.get(pk=pk)
    if call.data == "back":
        await state.finish()
        await default_view_platform(call, platform)
        return


async def edit_price_done(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if _price := SaleAdsValidator.price(message.text):
        pk = data.get("pk")
        platform = await AdvertisingPlatform.get(pk=pk)
        logger.trace(platform)
        await platform.update_price(_price)
        await message.answer(_("Цена успешно обновлена"))
        await state.finish()
        await default_view_platform(message, platform)

    else:
        await message.answer(
            _(
                "Не удалось найти цены, проверьте правильность ввода.\nЕсли вы указали промежуток, "
                "то минимальная сумма не должна превышать максимальную"
            ),
            reply_markup=markups.common.back_keyboard(),
        )


async def edit_communication(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        _("Выберите способ связи с вами. Он будет отображаться в вашем объявлении"),
        reply_markup=markups.sale_ads.communication_type(),
    )
    await EditPlatform.edit_communication.set()


async def edit_communication_choice(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pk = data.get("pk")
    platform = await AdvertisingPlatform.get(pk=pk)
    if call.data == "back":
        await state.finish()
        await default_view_platform(call, platform)
        return

    match call.data:
        case "phone":
            await call.message.answer(
                _("Введите номер телефона\n\nНапример: ”+7 999 999 99 99”"),
                reply_markup=markups.common.back_keyboard(),
            )
            await EditCommunication.phone.set()
        case "email":
            await call.message.answer(
                _("Введите Email\n\nНапример: ”example@example.com”"),
                reply_markup=markups.common.back_keyboard(),
            )
            await EditCommunication.email.set()
        case "tg":
            if await SaleAdsValidator.communication_type_tg(call.from_user.id):
                await platform.update_tg(f"@{call.from_user.username}")
                await call.message.answer(_("Способ связи тг успешно обновлен"))
                await state.finish()
                await default_view_platform(call, platform)

            else:
                await call.message.answer(
                    _("Произошла ошибка. Ваш профиль должен быть открытым"), reply_markup=markups.common.back_keyboard()
                )
        case _:
            pass


async def edit_communication_phone(obj: types.CallbackQuery | types.Message, state: FSMContext):
    data = await state.get_data()
    pk = data.get("pk")
    platform = await AdvertisingPlatform.get(pk=pk)
    if isinstance(obj, types.CallbackQuery):
        if obj.data == "back":
            await state.finish()
            await default_view_platform(obj, platform)
            return
        obj = obj.message
    try:
        if await SaleAdsValidator.communication_type_phone(obj.text):
            await platform.update_phone(obj.text)
            await obj.answer(_("Номер успешно обновлен"))
            await state.finish()
            await default_view_platform(obj, platform)
        else:
            await obj.answer(
                _("Не удалось найти номер, проверьте правильность веденных данных и повторите попытку"),
                reply_markup=markups.common.back_keyboard(),
            )
    except Exception as e:
        logger.critical(e)
        await obj.answer(
            _("Не удалось найти номер, проверьте правильность веденных данных и повторите попытку"),
            reply_markup=markups.common.back_keyboard(),
        )


async def edit_communication_email(obj: types.CallbackQuery | types.Message, state: FSMContext):
    data = await state.get_data()
    pk = data.get("pk")
    platform = await AdvertisingPlatform.get(pk=pk)
    if isinstance(obj, types.CallbackQuery):
        if obj.data == "back":
            await state.finish()
            await default_view_platform(obj, platform)
            return
        obj = obj.message

    if await SaleAdsValidator.communication_type_email(obj.text):
        await platform.update_email(obj.text)
        await obj.answer(_("Имейл успешно обновлен"))
        await state.finish()
        await default_view_platform(obj, platform)

    else:
        await obj.answer(
            _("Не удалось найти email, проверьте правильность веденных данных и повторите попытку"),
            reply_markup=markups.common.back_keyboard(),
        )


def register_platforms_info_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(my_platforms, UserFilter(), text="my_platforms")
    dp.register_callback_query_handler(get_platform, text_startswith="platform_")

    # dp.register_message_handler(get_platform_message, state=EditPlatform)

    dp.register_callback_query_handler(extend_platform, text_startswith="extend_")
    dp.register_callback_query_handler(delete_platform, text_startswith="delete_")
    dp.register_callback_query_handler(delete_platform_done, state=DeletePlatform.delete)

    dp.register_callback_query_handler(edit_platform, text_startswith="edit_platform_")

    dp.register_callback_query_handler(edit_thematic, text="edit_thematic")
    dp.register_callback_query_handler(edit_thematic_done, state=EditPlatform.edit_thematic)

    dp.register_callback_query_handler(edit_description, text="edit_description")
    dp.register_message_handler(edit_description_done, state=EditPlatform.edit_description)
    dp.register_callback_query_handler(edit_description_done_call, state=EditPlatform.edit_description)

    dp.register_callback_query_handler(edit_currency, text="edit_currency")
    dp.register_callback_query_handler(edit_currency_done, state=EditPlatform.edit_currency)

    dp.register_callback_query_handler(edit_price, text="edit_price")
    dp.register_message_handler(edit_price_done, state=EditPlatform.edit_price)
    dp.register_callback_query_handler(edit_price_done_call, state=EditPlatform.edit_price)

    dp.register_callback_query_handler(edit_communication, text="edit_communication")
    dp.register_callback_query_handler(edit_communication_choice, state=EditPlatform.edit_communication)

    dp.register_message_handler(edit_communication_phone, state=EditCommunication.phone)
    dp.register_callback_query_handler(edit_communication_phone, state=EditCommunication.phone)

    dp.register_message_handler(edit_communication_email, state=EditCommunication.email)
    dp.register_callback_query_handler(edit_communication_email, state=EditCommunication.email)

    dp.register_callback_query_handler(edit_communication_choice, state=EditPlatform.edit_communication)
