from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent.parent


def load_yaml(file) -> dict:
    with open(Path(BASE_DIR, file), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class Bot(BaseModel):
    token: str
    admins: Optional[list[int]]


class Database(BaseModel):
    username: str
    password: str
    host: str
    port: int
    db_name: str


class Config(BaseModel):
    bot: Bot
    db: Database


I18N_DOMAIN = "botexchange"
LOCALES_DIR = BASE_DIR / "botexchange/apps/bot/locales"

config = Config(**load_yaml("config.yml"))
