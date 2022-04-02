from loguru import logger

from botexchange.db.models import AdvertisingPlatform


async def views_update():
    logger.info("Запуск обновления статус")
    platforms = await AdvertisingPlatform.all()
    for platform in platforms:
        await platform.decr_duration()
        logger.trace(f"{platform.title} статус обновлен")
