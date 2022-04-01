from pprint import pprint

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from botexchange.loader import _


def ibtn(text, data):
    return InlineKeyboardButton(text=text, callback_data=data)


def thematics(selected_list: list = None, page: int = 1, edit=False) -> InlineKeyboardMarkup:
    # thematics_data = [
    #     [(_("Авто/Мото"), "auto"), (_("Спорт"), "sport")],
    #     [(_("Крипта"), "crypt"), (_("Инвестиции"), "investment")],
    #     [(_("Авторский блог"), "blog"), (_("Новости"), "news")],
    #     [(_("Мемы"), "memes"), (_("Музыка"), "music")],
    #     [(_("Фильмы"), "films"), (_("18+"), "18+")],
    # ]
    # switching_menu = (
    #     [
    #         [(_("Влево"), "left"), (_("Далее"), "next"), (_("Вправо"), "right")],
    #         [(_("Назад"), "back")],
    #     ],
    # )
    # if selected_list:
    #     inline_keyboard = []
    #     for tdata, tdata2 in thematics_data:
    #         if tdata[0] in selected_list:
    #             tdata[0]
    #         if tdata2:
    #             pass
    #
    #         inline_keyboard.append([ibtn(*tdata), ibtn(*tdata2)])
    #
    # else:
    #     inline_keyboard = [[ibtn(*tdata), ibtn(*tdata2)] for tdata, tdata2 in [*thematics_data, *switching_menu]]
    # inline_keyboard.append()
    # pprint(inline_keyboard)
    def ibtne(text, data):
        if data in selected_list:
            text = f"✅ {text}"
        return InlineKeyboardButton(text=text, callback_data=data)

    ibtne = ibtn if not selected_list else ibtne

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ibtne(_("Авто/Мото"), "auto"), ibtne(_("Спорт"), "sport")],
            [ibtne(_("Крипта"), "crypt"), ibtne(_("Инвестиции"), "investment")],
            [ibtne(_("Авторский блог"), "blog"), ibtne(_("Новости"), "news")],
            [ibtne(_("Мемы"), "memes"), ibtne(_("Музыка"), "music")],
            [ibtne(_("Фильмы"), "films"), ibtne(_("18+"), "18+")],
            [ibtn(_("Влево"), "left"), ibtn(_("Далее"), "next"), ibtn(_("Вправо"), "right")],
            [ibtn(_("Назад"), "back")],
        ],
    )


if __name__ == "__main__":
    thematics()
