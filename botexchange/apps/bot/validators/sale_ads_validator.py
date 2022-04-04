import re

import phonenumbers
from loguru import logger

from botexchange.apps.bot.validators.common_validators import thematic_validator
from botexchange.loader import bot


class SaleAdsValidator:
    about_len_limit = 80
    currencies = ("rub", "usd", "eur", "uah")
    communication_types = ("phone", "email", "tg")

    @classmethod
    def thematic(cls, text: str, platform) -> bool:
        return thematic_validator(text, platform)

    @classmethod
    def about(cls, text: str) -> bool:
        if len(text) > cls.about_len_limit:
            return False
        return True

    @classmethod
    def currency(cls, text: str) -> bool:
        if text not in cls.currencies:
            return False
        return True

    @classmethod
    def price(cls, text: str) -> bool | tuple[int, int] | int:
        try:
            pr = map(lambda x: x.strip(), text.split("-"))
            pr = tuple(map(int, pr))
            if len(pr) == 2:
                _min, _max = pr
                if _min > _max:
                    return False
                return _min, _max
            _max = pr[0]
            return _max
        except Exception as e:
            logger.warning(e)
            return False

    @classmethod
    def communication_type(cls, text: str) -> bool:
        if text not in cls.communication_types:
            return False
        return True

    @classmethod
    async def communication_type_tg(cls, user_id: int) -> bool:
        user_info = await bot.get_chat(user_id)
        if user_info["type"] == "private":
            return False
        return True

    @classmethod
    async def phone(cls, user_id: int) -> bool:
        user_info = await bot.get_chat(user_id)
        if user_info["type"] == "private":
            return False
        return True

    @classmethod
    async def email(cls, user_id: int) -> bool:
        user_info = await bot.get_chat(user_id)
        if user_info["type"] == "private":
            return False
        return True

    @classmethod
    async def communication_type_phone(cls, text: str) -> bool:
        if phonenumbers.parse(text, None):
            return True
        return False

    @classmethod
    async def communication_type_email(cls, text: str) -> bool:
        match = re.match(r"[^@]+@[^@]+\.[^@]+", text.lower())
        if match:
            return True
        return False


if __name__ == "__main__":
    print(SaleAdsValidator.price("700-900"))
