from aiogram import types
from tortoise import models, fields


class User(models.Model):
    user_id = fields.BigIntField()
    username = fields.CharField(max_length=30, null=True)
    first_name = fields.CharField(max_length=255, null=True)
    last_name = fields.CharField(max_length=255, null=True)
    language = fields.CharField(max_length=3)
    referral = fields.ForeignKeyField("models.User", null=True)



