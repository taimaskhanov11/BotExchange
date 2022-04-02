from aiogram.types import InlineKeyboardMarkup
from loguru import logger

from botexchange.apps.bot.markups.common import ibtn
from botexchange.db.models import _


def start_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtn(_("У меня есть реклама"), "buying_ads")],
            [ibtn(_("У меня есть площадка для рекламы"), "selling_ads")],
            [ibtn(_("Язык (language)"), "language"), ibtn(_("Поддержка"), "support")],
        ],
    )


def language(lang):
    lang_btn = ibtn(_("Русский"), "ru") if lang == "en" else ibtn(_("English"), "en")
    # lang_btn2 = ibtn(_("Главное меню"), "start") if lang == "ru" else ibtn(_("Main menu"), "start")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # [lang_btn],
            [lang_btn],
            [ibtn(_("Главное меню"), "start")],
            # [lang_btn2],
        ],
    )


def language_choice(lang):
    logger.trace(lang)
    lang_btn = ibtn(_("Русский"), "ru") if lang == "en" else ibtn(_("English"), "en")
    lang_btn2 = ibtn("Главное меню", "start") if lang == "ru" else ibtn("Main menu", "start")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # [lang_btn],
            [lang_btn],
            # [ibtn(_("Главное меню"), "start"), ],
            [lang_btn2],
        ],
    )
