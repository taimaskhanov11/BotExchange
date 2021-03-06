from aiogram.types import InlineKeyboardMarkup

from botexchange.apps.bot.markups.common import ibtn
from botexchange.loader import _


def platform_type(edit=False):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Каналы"), "channel"), ibtn(_("Боты"), "bot")],
            [ibtn(_("Чаты"), "chat"), ibtn(_("Любой"), "any")],
            [ibtn(_("Назад"), "back")],
        ],
    )


def audience_size(edit=False):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Любой"), "any"), ibtn(_("0-1к"), "0-1000")],
            [ibtn(_("1к-10к"), "1-10"), ibtn(_("10к-100к"), "10000-100000")],
            [ibtn(_("100к-1кк"), "100-1000"), ibtn(_("Более 1кк"), "1000000-9999999")],
            [ibtn(_("Указать произвольный диапазон"), "specify")],
            [ibtn(_("Назад"), "back")],
        ],
    )


def budget():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Любой"), "any"), ibtn(_("0-1к"), "0-1000")],
            [ibtn(_("1к-10к"), "1-10"), ibtn(_("10к-100к"), "10-100")],
            [ibtn(_("100к-1кк"), "100-1000"), ibtn(_("Более 1кк"), "1000")],
            [ibtn(_("Указать произвольный диапазон"), "specify")],
            [ibtn(_("Назад"), "back")],
        ],
    )


def edit_field():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Изм. тип площадки"), "platform_type"), ibtn(_("Изм. тематику"), "thematic")],
            [ibtn(_("Изм. аудиторию"), "audience_size")],
            # ibtn(_("Изм. бюджет"), "budget")],
            [ibtn(_("Главное меню"), "start")],
        ],
    )
