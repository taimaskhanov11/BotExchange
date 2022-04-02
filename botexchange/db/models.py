import typing
import pprint

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram.utils import markdown
from loguru import logger
from pydantic import BaseModel
from tortoise import models, fields
from tortoise.expressions import F

from botexchange.config.config import I18N_DOMAIN, LOCALES_DIR
from botexchange.loader import dp


class User(models.Model):
    user_id = fields.BigIntField()
    username = fields.CharField(max_length=30, null=True)
    first_name = fields.CharField(max_length=255, null=True)
    last_name = fields.CharField(max_length=255, null=True)
    language = fields.CharField(max_length=3)
    referral = fields.ForeignKeyField("models.User", null=True)

    async def set_language(self, language):
        self.language = language
        await self.save()


class AdvertisingPlatform(models.Model):
    owner = fields.ForeignKeyField("models.User", index=True)
    chat_id = fields.BigIntField(index=True)
    title = fields.CharField(max_length=50)
    link = fields.CharField(max_length=255, null=True)
    about = fields.CharField(max_length=255)

    platform_type = fields.CharField(max_length=30, null=True, index=True)
    thematic = fields.CharField(max_length=50, index=True)
    audience_size = fields.BigIntField(null=True)

    currency = fields.CharField(max_length=10)
    min_price = fields.DecimalField(max_digits=10, decimal_places=1, null=True)
    max_price = fields.DecimalField(max_digits=10, decimal_places=1, null=True)

    tg = fields.CharField(max_length=255, null=True)
    phone = fields.CharField(max_length=255, null=True)
    email = fields.CharField(max_length=255, null=True)

    is_hidden = fields.BooleanField(default=False)
    views = fields.IntField(default=0)
    duration = fields.IntField(default=15)

    # def admin_view(self):
    #     pass

    # async def pretty_view(self, is_admin=True):
    #     return pretty_view(self)

    # todo 02.04.2022 16:23 taima:

    async def refresh_duration(self):
        self.duration = 15
        self.is_hidden = False
        await self.save()

    async def incr_views(self):
        self.views = F('views') + 1
        await self.save(update_fields=['views'])

    async def decr_duration(self):
        # self.views = F('views') - 1
        self.duration -= 1
        if self.duration <= 0:
            self.is_hidden = True
            logger.warning(f"{self.title} показ выключен")
        await self.save()
        # await self.refresh_from_db(fields=['views'])


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
                    res += f"{pretty_view(p, is_admin=False)}\n{'_' * 100}\n"
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
    audience_size = markdown.hbold(f"Аудитория - {self.audience_size:,}") if self.audience_size else ""
    price = get_currency(self.min_price, self.max_price, self.currency)

    # link = markdown.hlink(self.title, "html.com")
    tg = f"TG - {self.tg}\n" if self.tg else ""
    phone = f"Phone. - {self.phone}\n" if self.phone else ""
    email = f"Email - {self.email}\n" if self.email else ""
    contacts = f"{tg}{phone}{email}"
    duration = _("\nСтатус:\n{status}. {duration} до деактивации").format(duration=self.duration, status=_(
        'Активна') if not self.is_hidden else _('Неактивна')) if is_admin else ""
    views = _("Показы {views}").format(views=self.views) if is_admin else ""
    return _(
        """{link} ({platform_type} / {thematic}) - {about}

{audience_size}
Размещение - {price}

Контакты: 
{contacts}
{duration}
{views}
"""
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


# budget: typing.Optional[tuple[int, int] | int | str]


async def get_lang(user_id):
    # Делаем запрос к базе, узнаем установленный язык
    user = await User.get_or_none(user_id=user_id)
    if user:
        # Если пользователь найден - возвращаем его
        return user.language


class ACLMiddleware(I18nMiddleware):
    # Каждый раз, когда нужно узнать язык пользователя - выполняется эта функция
    async def get_user_locale(self, action, args):
        user = types.User.get_current()
        # Возвращаем язык из базы ИЛИ (если не найден) - язык из Телеграма
        # return await get_lang(user.id) or user.locale
        return await get_lang(user.id) or user.locale


def setup_lang_middleware(dp):
    # Устанавливаем миддлварь
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n


i18n = setup_lang_middleware(dp)
_ = i18n.gettext
