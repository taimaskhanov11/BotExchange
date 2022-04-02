from aiogram.types import InlineKeyboardMarkup

from botexchange.apps.bot.markups.common import ibtn
from botexchange.db.models import AdvertisingPlatform, _


def my_platforms(platforms: list[AdvertisingPlatform]):
    count = 0
    inline_keyboard = []
    for platform in platforms:
        count += 1
        inline_keyboard.append([ibtn(platform.title, f"platform_{platform.pk}")])
        if count > 50:
            break
    inline_keyboard.extend([[ibtn(_("Добавить площадку"), "add_platform"), ibtn(_("Главное меню"), "start")]])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def platform_view(pk):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Продлить"), f"extend_{pk}")],
            [ibtn(_("Удалить"), f"delete_{pk}")],
            [ibtn(_("Мои площадки"), "my_platforms")],
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
