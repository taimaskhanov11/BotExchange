from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class PlatformTypeFilter(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        if call.data in ["chanell", "bot"]:
            return True


class ThematicFilter(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        if call.data in [
            "auto",
            "sport",
            "crypt",
            "investment",
            "blog",
            "news",
            "memes",
            "music",
            "films",
            "18+",
        ]:
            return True


class AudienceSizeFilter(BoundFilter):
    async def check(self, obj: types.CallbackQuery | types.Message):
        pass


class BudgetFilter(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        pass
