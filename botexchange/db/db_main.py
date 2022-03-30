from loguru import logger
from tortoise import Tortoise

from botexchange.config.config import config


async def init_tortoise():
    db = config.db
    logger.debug(f"Инициализация BD {db.host}")
    data = {
        "db_url": f"postgres://{db.username}:{db.password}@{db.host}:{db.port}/{db.db_name}",
        "modules": {"models": ["botexchange.db.models"]},
    }
    try:
        await Tortoise.init(**data)
    except Exception as e:
        logger.critical(e)
        await Tortoise.init(_create_db=True, **data)
    await Tortoise.generate_schemas()
