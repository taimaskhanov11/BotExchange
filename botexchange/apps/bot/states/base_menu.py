from aiogram.dispatcher.filters.state import StatesGroup, State


class BuyingAds(StatesGroup):
    platform_type = State()
    thematic = State()
    audience_size = State()
    budget = State()


class SellingAds(StatesGroup):
    pass
