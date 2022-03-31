from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from botexchange.loader import _


def ibtn(text, data):
    return InlineKeyboardButton(text=text, callback_data=data)


def thematics() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                ibtn(_("Авто/Мото"), "auto"),
                ibtn(_("Спорт"), "sport"),
            ],
            [
                ibtn(_("Крипта"), "crypt"),
                ibtn(_("Инвестиции"), "investment"),
            ],
            [
                ibtn(_("Авторский блог"), "blog"),
                ibtn(_("Новости"), "news"),
            ],
            [
                ibtn(_("Мемы"), "memes"),
                ibtn(_("Музыка"), "music"),
            ],
            [
                ibtn(_("Фильмы"), "films"),
                ibtn(_("18+"), "18+"),
            ],
            [
                ibtn(_("Влево"), "left"),
                ibtn(_("Далее"), "next"),
                ibtn(_("Вправо"), "right"),
            ],
            [
                ibtn(_("Назад"), "back"),
            ],
        ],
    )
