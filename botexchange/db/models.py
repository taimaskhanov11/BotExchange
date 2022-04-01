import typing

from pydantic import BaseModel, validator
from tortoise import models, fields


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
    link = fields.CharField(max_length=255)

    platform_type = fields.CharField(max_length=30, null=True, index=True)
    thematic = fields.CharField(max_length=50, index=True)
    audience_size = fields.BigIntField()

    currency = fields.CharField(max_length=10)
    min_price = fields.DecimalField(max_digits=10, decimal_places=1, null=True)
    max_price = fields.DecimalField(max_digits=10, decimal_places=1, null=True)


class PlatformSearch(BaseModel):
    platform_type: typing.Optional[typing.Literal["channel", "bot"]]
    thematics: typing.Optional[list[str]]
    budget: typing.Optional[tuple[int, int] | int | str]
