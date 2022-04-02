import aiohttp


async def get_currency_rate(currency: str = "rub"):
    async with aiohttp.ClientSession() as session:
        async with session.get("") as response:
            print(await response.json())
