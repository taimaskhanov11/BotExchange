import pprint
import typing

from aiogram.utils import markdown
from loguru import logger
from pydantic import BaseModel

from botexchange.db.models import AdvertisingPlatform
from botexchange.loader import _


class PlatformSearch(BaseModel):
    platform_type: typing.Optional[typing.Literal["channel", "group", "bot", "any", "chat"]]
    thematics: typing.Optional[list[str]]
    audience_size: int | tuple[int, int]

    async def search(self):
        expressions = {}
        if self.platform_type == "chat":
            self.platform_type = "group"

        if self.platform_type != "any":
            expressions.update({"platform_type": self.platform_type})

        if self.thematics:
            expressions.update(
                {
                    "thematic__in": self.thematics,
                }
            )

        if isinstance(self.audience_size, tuple):
            _min = self.audience_size[0]
            _max = self.audience_size[1]
            expressions.update(
                {
                    "audience_size__gte": _min,
                    "audience_size__lte": _max,
                }
            )
        else:
            if self.audience_size != 0:
                expressions.update(
                    {
                        "audience_size__gte": self.audience_size - 1000,
                        "audience_size__lte": self.audience_size + 1000,
                    }
                )
        logger.info(
            f"Поля для поиска:\n{self.platform_type}|{self.thematics}|{self.audience_size}\n{pprint.pformat(expressions)}"
        )
        platforms = await AdvertisingPlatform.filter(**expressions)
        res = ""
        count = 0
        if platforms:
            for p in platforms:
                if not p.is_hidden:
                    count += 1
                    await p.incr_views()
                    res += f"{pretty_view(p, is_admin=False)}\n{'_' * 30}\n"
                    if count == 10:
                        break
        return res


def get_currency(_min, _max, cur):
    if cur == "rub":
        s = "₽ "
    elif cur == "usd":
        s = "₴"

    elif cur == "eur":
        s = "€"
    else:
        s = "$"

    if _min and _max:
        return _("от {min} до {max} {s}").format(min=_min, max=_max, s=s)
    elif _max:
        return _("{max} {s}").format(max=_max, s=s)
    else:
        return _("{_min} {s}").format(min=_min, s=s)


def pretty_view(self, is_admin=True):
    link = self.link if self.platform_type == "bot" else markdown.hlink(self.title, self.link)
    audience_size = markdown.hbold(f"Аудитория - {self.audience_size:,}\n") if self.audience_size else ""
    price = get_currency(self.min_price, self.max_price, self.currency)

    # link = markdown.hlink(self.title, "html.com")
    # tg = f"TG - {self.tg}\n" if self.tg else ""
    # phone = f"Phone. - {self.phone}\n" if self.phone else ""
    # email = f"Email - {self.email}\n" if self.email else ""
    # contacts = f"{tg}{phone}{email}"
    # tg = f"TG - {self.tg}\n" if self.tg else ""
    # phone = f"Phone. - {self.phone}\n" if self.phone else ""
    # email = f"Email - {self.email}\n" if self.email else ""
    contacts_list = []
    if self.tg:
        contacts_list.append(f"TG - {self.tg}")
    if self.phone:
        contacts_list.append(f"Phone. - {self.phone}")
    if self.email:
        contacts_list.append(f"Email - {self.email}")
    contacts = "\n".join(contacts_list)
    duration = (
        _("\nСтатус: {status}. {duration} дней до деактивации\n").format(
            duration=self.duration,
            status=_("Активна") if not self.is_hidden else _("Неактивна"),
        )
        if is_admin
        else ""
    )
    views = _("Показы: {views}\n").format(views=self.views) if is_admin else ""
    return _(
        "{link} ({platform_type} / {thematic}) - {about}\n\n"
        "{audience_size}"
        "Размещение - {price}\n\n"
        "Контакты: {contacts}"
        "{duration}{views}"
    ).format(
        link=link,
        platform_type=self.platform_type,
        thematic=self.thematic,
        about=self.about,
        audience_size=audience_size,
        price=markdown.hbold(price),
        contacts=contacts,
        duration=duration,
        views=views,
    )
