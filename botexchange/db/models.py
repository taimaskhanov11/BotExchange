from loguru import logger
from tortoise import models, fields
from tortoise.expressions import F


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
        self.views = F("views") + 1
        await self.save(update_fields=["views"])

    async def decr_duration(self):
        # self.views = F('views') - 1
        self.duration -= 1
        if self.duration <= 0:
            self.is_hidden = True
            logger.warning(f"{self.title} показ выключен")
        await self.save()
        # await self.refresh_from_db(fields=['views'])
