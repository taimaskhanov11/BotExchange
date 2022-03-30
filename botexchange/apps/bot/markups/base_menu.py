from aiogram.types import InlineKeyboardMarkup

from botexchange.apps.bot.markups.utils import ibtn
from botexchange.loader import _


def start_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("У меня есть реклама"), "buying_ads")],
            [ibtn(_("У меня есть площадка для рекламы"), "selling_ads"), ],
            [ibtn(_("Язык (language)"), "language"),
             ibtn(_("Поддержка"), "support"), ],
        ],
    )
