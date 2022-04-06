from aiogram.types import InlineKeyboardMarkup

from botexchange.apps.bot.markups.common import ibtn
from botexchange.db.models import AdvertisingPlatform
from botexchange.loader import _


def my_platforms(platforms: list[AdvertisingPlatform]):
    count = 0
    inline_keyboard = []
    for platform in platforms:
        count += 1
        inline_keyboard.append([ibtn(platform.title, f"platform_{platform.pk}")])
        if count > 50:
            break
    inline_keyboard.extend(
        [
            [
                ibtn(_("Добавить площадку"), "add_platform"),
                ibtn(_("Главное меню"), "start"),
            ]
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def platform_view(pk):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Продлить"), f"extend_{pk}"),
             ibtn(_("Редактировать"), f"edit_platform_{pk}")],
            [ibtn(_("Удалить"), f"delete_{pk}")],
            [ibtn(_("Мои площадки"), "my_platforms"),
             ibtn(_("Главное меню"), "start")],
        ],
    )


def extend_platform():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Мои площадки"), "my_platforms")],
        ],
    )


def delete_platform():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Да"), "yes")],
            [ibtn(_("Нет"), "no")],
        ],
    )


def delete_platform_done():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Мои площадки"), "my_platforms")],
            [ibtn(_("Добавить новую"), "add_platform")],
        ],
    )


def edit_platform_platform(pk):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Изменить тематику"), f"edit_thematic")],
            [ibtn(_("Изменить описание"), f"edit_description")],
            [ibtn(_("Изменить валюту"), f"edit_currency")],
            [ibtn(_("Изменить цену"), f"edit_price")],
            [ibtn(_("Изменить контакты"), f"edit_communication")],
            [ibtn(_("Назад"), f"platform_{pk}")],
        ],
    )


def edit_platform_platform_done():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Изменить тематику"), f"edit_thematic")],
            [ibtn(_("Изменить описание"), f"edit_description")],
            [ibtn(_("Изменить цену"), f"edit_price")],
            [ibtn(_("Изменить контакты"), f"edit_communication")],
        ],
    )
