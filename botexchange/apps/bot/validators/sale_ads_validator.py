from loguru import logger

from botexchange.loader import bot


class SaleAdsValidator:
    about_len_limit = 80
    thematics = ("auto", "sport", "crypt", "investment", "blog", "news", "memes", "music", "films", "18+")
    currencies = ("rub", "usd", "eur", "uah")
    communication_types = ("phone", "email", "tg")

    @classmethod
    def thematic(cls, text: str):
        if text not in cls.thematics:
            return False
        return True

    @classmethod
    def about(cls, text: str):
        if len(text) > cls.about_len_limit:
            return False
        return True

    @classmethod
    def currency(cls, text: str):
        if text not in cls.currencies:
            return False
        return True

    @classmethod
    def price(cls, text: str) -> bool | tuple[int, int] | int:
        try:
            pr = map(lambda x: x.strip(), text.split("-"))
            pr = tuple(map(int, pr))
            if pr == 2:
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
    def communication_type(cls, text: str):
        if text not in cls.communication_types:
            return False
        return True

    @classmethod
    async def communication_type_tg(cls, user_id: int):
        user_info = await bot.get_chat(user_id)
        if user_info["type"] == "private":
            return False
        return True
