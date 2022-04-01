from aiogram.types import InlineKeyboardMarkup

from botexchange.apps.bot.markups.common import ibtn, thematics
from botexchange.loader import _


def selling_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Добавить площадку"), "add_platform")],
            [ibtn(_("Мои площадки"), "my_platforms")],
            [ibtn(_("Главное меню"), "start")],
            # [ibtn(_("Назад"), "back"), ],
        ],
    )


def platform_type():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Канал / чат"), "channel"), ibtn(_("Бот"), "bot")],
            [ibtn(_("Назад"), "back")],
        ],
    )


def add_platform():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Назад"), "back")],
        ],
    )


def check():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Готово"), "okay")],
            [ibtn(_("Назад"), "back")],
        ],
    )


def about():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Назад"), "back")],
        ],
    )


def currency():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("₽ (рубль)"), "rub"), ibtn(_("$ (доллар)"), "usd")],
            [ibtn(_("€ (евро)"), "eur"), ibtn(_("₴ (гривна)"), "uah")],
            # [ibtn(_("Указать произвольную валюту"), "specify")],
            [ibtn(_("Назад"), "back")],
        ],
    )


def price():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                ibtn(_("Назад"), "back"),
            ],
        ],
    )


def communication_type():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Телефон"), "phone"), ibtn(_("Имейл"), "email")],
            [ibtn(_("Использовать этот TG профиль"), "tg")],
            [ibtn(_("Назад"), "back")],
        ],
    )


def communication(okay=False):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Готово"), "okay")] if okay else [],
            [ibtn(_("Назад"), "back")],
        ],
    )


def additional_communication(communication):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Телефон"), "phone")] if "phone" not in communication else [],
            [ibtn(_("Имейл"), "email")] if "email" not in communication else [],
            [ibtn(_("Использовать этот TG профиль"), "tg")] if "tg" not in communication else [],
            [ibtn(_("Опубликовать площадку"), "finish")] if communication else [],
            # [ibtn(_("Назад"), "back"), ],
        ],
    )


def finish():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Мои площадки"), "my_platforms"), ibtn(_("Добавить еще площадку"), "add_platform")],
            [ibtn(_("Главное меню"), "start")],
            # [ibtn(_("Назад"), "back"), ],
        ],
    )
