from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

from botexchange.loader import _


def ibtn(text, data):
    return InlineKeyboardButton(text=text, callback_data=data)


def thematics(data: dict) -> InlineKeyboardMarkup:
    _selected_list = data.get("thematics")
    _platform_type = data.get("platform_type")
    _page = data.get("page")
    logger.trace(f"{_selected_list=}|{_platform_type=}|{_page=}")

    def ibtne(text, cd):
        if cd in _selected_list:
            text = f"✅ {text}"
        return InlineKeyboardButton(text=text, callback_data=cd)

    ibtne = ibtn if not _selected_list else ibtne
    inline_keyboard = []

    if _selected_list is None:
        switching_buttons = [ibtn(_("Влево"), "left"), ibtn(_("Вправо"), "right")]
        switching_buttons_right = [ibtn(_("Вправо"), "right")]
        switching_buttons_left = [
            ibtn(_("Влево"), "left"),
        ]
    else:
        switching_buttons = [
            ibtn(_("Влево"), "left"),
            ibtn(_("Далее"), "next"),
            ibtn(_("Вправо"), "right"),
        ]
        switching_buttons_right = [ibtn(_("Далее"), "next"), ibtn(_("Вправо"), "right")]
        switching_buttons_left = [ibtn(_("Влево"), "left"), ibtn(_("Далее"), "next")]

    if _platform_type == "bot":
        match _page:
            # case 1:
            #     inline_keyboard = [
            #         [ibtne(_("Авто/Мото"), "auto"), ibtne(_("Спорт"), "sport")],
            #         [ibtne(_("Крипта"), "crypt"), ibtne(_("Инвестиции"), "investment")],
            #         [ibtne(_("Авторский блог"), "blog"), ibtne(_("Новости"), "news")],
            #         [ibtne(_("Мемы"), "memes"), ibtne(_("Музыка"), "music")],
            #         [ibtne(_("Фильмы"), "films"), ibtne(_("18+"), "18+")],
            #         [ibtn(_("Далее"), "next"), ibtn(_("Вправо"), "right")]
            #     ]
            case 1:
                inline_keyboard = [
                    [
                        ibtne(_("Авто и мото"), "auto and moto"),
                        ibtne(_("Бизнес и стартапы"), "business and startups"),
                    ],
                    [ibtne(_("Видеоигры"), "video games"), ibtne(_("Другое"), "other")],
                    [
                        ibtne(_("Инвестиции"), "investments"),
                        ibtne(_("Иностранные языки"), "foreign languages"),
                    ],
                    [
                        ibtne(_("Искусство и дизайн"), "art and design"),
                        ibtne(_("Кино"), "movies"),
                    ],
                    [
                        ibtne(_("Книги"), "books"),
                        ibtne(_("Криптовалюты"), "cryptocurrencies"),
                    ],
                    switching_buttons_right,
                ]
            case 2:
                inline_keyboard = [
                    [
                        ibtne(_("Маркетинг и пиар"), "marketing and PR"),
                        ibtne(_("Мода и стиль"), "fashion and style"),
                    ],
                    [
                        ibtne(_("Мотивация и саморазвитие"), "motivation and self"),
                        ibtne(_("Музыка"), "music"),
                    ],
                    [
                        ibtne(_("Наука и технологии"), "science and technology"),
                        ibtne(_("Недвижимость"), "real estate"),
                    ],
                    [
                        ibtne(_("Новости и сми"), "news and media"),
                        ibtne(_("Образование"), "education"),
                    ],
                    [
                        ibtne(_("Отдых и развлечения"), "leisure and entertainment"),
                        ibtne(_("Работа и вакансии"), "jobs and vacancies"),
                    ],
                    switching_buttons,
                ]
            case 3:
                inline_keyboard = [
                    [
                        ibtne(_("Скидки и акции"), "discounts and promotions"),
                        ibtne(_("Спорт"), "sports"),
                    ],
                    [
                        ibtne(_("Ставки и азартные игры"), "betting and gambling"),
                        ibtne(_("Трейдинг"), "trading"),
                    ],
                    [
                        ibtne(_("Фитнес"), "fitness"),
                        ibtne(_("Хобби и развлечения"), "hobbies and entertainment"),
                    ],
                    [
                        ibtne(_("Экономика и финансы"), "economics and finance"),
                        ibtne(_("Юмор и мемы"), "humor and memes"),
                    ],
                    [ibtne(_("18+"), "18+")],
                    switching_buttons_left,
                ]

    else:
        match _page:
            case 1:
                inline_keyboard = [
                    [
                        ibtne(_("Авто и мото"), "auto and moto"),
                        ibtne(_("Авторские блоги"), "author blogs"),
                    ],
                    [
                        ibtne(_("Бизнес и стартапы"), "business and startups"),
                        ibtne(_("В мире животных"), "in the world of animals"),
                    ],
                    [
                        ibtne(_("Видеоигры"), "video games"),
                        ibtne(_("Дети и родители"), "children and parents"),
                    ],
                    [
                        ibtne(_("Другое"), "other"),
                        ibtne(_("Еда и кулинария"), "food and cooking"),
                    ],
                    [
                        ibtne(_("Здоровье и медицина"), "health and medicine"),
                        ibtne(_("Знаменитости и образ жизни"), "celebrities and lifestyle"),
                    ],
                    switching_buttons_right,
                ]
            case 2:
                inline_keyboard = [
                    [
                        ibtne(_("Инвестиции"), "investments"),
                        ibtne(_("Иностранные языки"), "foreign languages"),
                    ],
                    [
                        ibtne(_("Интернет технологии"), "internet technology"),
                        ibtne(_("Искусство и дизайн"), "art and design"),
                    ],
                    [ibtne(_("История"), "history"), ibtne(_("Кино"), "movies")],
                    [
                        ibtne(_("Книги"), "books"),
                        ibtne(_("Красота и уход"), "beauty and care"),
                    ],
                    [
                        ibtne(_("Криптовалюты"), "cryptocurrencies"),
                        ibtne(_("Культура и события"), "culture and events"),
                    ],
                    switching_buttons,
                ]
            case 3:
                inline_keyboard = [
                    [
                        ibtne(_("Любопытные факты"), "interesting facts"),
                        ibtne(_("Маркетинг и пиар"), "marketing and PR"),
                    ],
                    [
                        ibtne(_("Мода и стиль"), "fashion and style"),
                        ibtne(_("Мотивация и саморазвитие"), "motivation and self"),
                    ],
                    [
                        ibtne(_("Музыка"), "music"),
                        ibtne(_("Наука и технологии"), "science and technology"),
                    ],
                    [
                        ibtne(_("Недвижимость"), "real estate"),
                        ibtne(_("Новости и сми"), "news and media"),
                    ],
                    [
                        ibtne(_("Образование"), "education"),
                        ibtne(_("Отдых и развлечения"), "leisure and entertainment"),
                    ],
                    switching_buttons,
                ]
            case 4:
                inline_keyboard = [
                    [
                        ibtne(_("Психология и отношения"), "psychology and relationships"),
                        ibtne(_("Путешествия и туризм"), "travel and tourism"),
                    ],
                    [
                        ibtne(_("Работа и вакансии"), "jobs and vacancies"),
                        ibtne(_("Региональные"), "regional"),
                    ],
                    [
                        ibtne(_("Религия и духовность"), "religion and spirituality"),
                        ibtne(_("Скидки и акции"), "discounts and promotions"),
                    ],
                    [
                        ibtne(_("Спорт"), "sports"),
                        ibtne(_("Ставки и азартные игры"), "betting and gambling"),
                    ],
                    [
                        ibtne(_("Строительство и ремонт"), "construction and repair"),
                        ibtne(_("Трейдинг"), "trading"),
                    ],
                    switching_buttons,
                ]
            case 5:
                inline_keyboard = [
                    [
                        ibtne(_("Фитнес"), "fitness"),
                        ibtne(_("Хобби и развлечения"), "hobbies and entertainment"),
                    ],
                    [
                        ibtne(_("Экономика и финансы"), "economics and finance"),
                        ibtne(_("Юмор и мемы"), "humor and memes"),
                    ],
                    [
                        ibtne(_("Юриеспруденция"), "jurisprudence"),
                        ibtne(_("18+"), "18+"),
                    ],
                    switching_buttons_left,
                ]
    inline_keyboard.append([ibtn(_("Назад"), "back")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# def thematics(selected_list: list = None, page: int = 1, edit=False) -> InlineKeyboardMarkup:
#     # thematics_data = [
#     #     [(_("Авто/Мото"), "auto"), (_("Спорт"), "sport")],
#     #     [(_("Крипта"), "crypt"), (_("Инвестиции"), "investment")],
#     #     [(_("Авторский блог"), "blog"), (_("Новости"), "news")],
#     #     [(_("Мемы"), "memes"), (_("Музыка"), "music")],
#     #     [(_("Фильмы"), "films"), (_("18+"), "18+")],
#     # ]
#     # switching_menu = (
#     #     [
#     #         [(_("Влево"), "left"), (_("Далее"), "next"), (_("Вправо"), "right")],
#     #         [(_("Назад"), "back")],
#     #     ],
#     # )
#     # if selected_list:
#     #     inline_keyboard = []
#     #     for tdata, tdata2 in thematics_data:
#     #         if tdata[0] in selected_list:
#     #             tdata[0]
#     #         if tdata2:
#     #             pass
#     #
#     #         inline_keyboard.append([ibtn(*tdata), ibtn(*tdata2)])
#     #
#     # else:
#     #     inline_keyboard = [[ibtn(*tdata), ibtn(*tdata2)] for tdata, tdata2 in [*thematics_data, *switching_menu]]
#     # inline_keyboard.append()
#     # pprint(inline_keyboard)
#     def ibtne(text, data):
#         if data in selected_list:
#             text = f"✅ {text}"
#         return InlineKeyboardButton(text=text, callback_data=data)
#
#     ibtne = ibtn if not selected_list else ibtne
#
#     return InlineKeyboardMarkup(
#         inline_keyboard=[
#             [ibtne(_("Авто/Мото"), "auto"), ibtne(_("Спорт"), "sport")],
#             [ibtne(_("Крипта"), "crypt"), ibtne(_("Инвестиции"), "investment")],
#             [ibtne(_("Авторский блог"), "blog"), ibtne(_("Новости"), "news")],
#             [ibtne(_("Мемы"), "memes"), ibtne(_("Музыка"), "music")],
#             [ibtne(_("Фильмы"), "films"), ibtne(_("18+"), "18+")],
#             [ibtn(_("Влево"), "left"), ibtn(_("Далее"), "next"), ibtn(_("Вправо"), "right")],
#             [ibtn(_("Назад"), "back")],
#         ],
#     )


if __name__ == "__main__":
    thematics()
