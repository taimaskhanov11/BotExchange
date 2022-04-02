from aiogram.types import InlineKeyboardMarkup

from botexchange.apps.bot.markups.common import ibtn
from botexchange.db.models import _


def admin_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Все пользователи"), "all_users")],
            [ibtn(_("Бан лист"), "ban_list")],
            [ibtn(_("Забанить пользователя"), "ban")],
            [ibtn(_("Разбанить пользователя"), "unban")],
            [ibtn(_("Назад в меню"), "admin")],
        ],
    )
def all_users():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Назад в меню"), "admin")],
        ],
    )
def ban_list():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Назад в меню"), "admin")],
        ],
    )


def ban():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Назад в меню"), "admin")],
        ],
    )
def ban_done():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Назад в меню"), "admin")],
        ],
    )
def unban():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Назад в меню"), "admin")],
        ],
    )
def unban_done():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("Назад в меню"), "admin")],
        ],
    )
