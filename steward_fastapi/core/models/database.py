from tortoise.models import Model
from tortoise import fields, Tortoise, timezone
from datetime import datetime
from zoneinfo import ZoneInfo


class ContentSource(Model):
    name = fields.CharField(max_length=50, unique=True)

    def __repr__(self):
        return self.name


class ContentType(Model):
    name = fields.CharField(max_length=50, unique=True)

    def __repr__(self):
        return self.name


class Content(Model):
    meta = fields.TextField(null=True)
    source = fields.ForeignKeyField(
            model_name='models.ContentSource',
            on_delete=fields.CASCADE,
            to_field='name',
            related_name='content',
        )
    type = fields.ForeignKeyField(
            model_name='models.ContentType',
            on_delete=fields.CASCADE,
            to_field='name',
            related_name='content',
        )
    url = fields.TextField()
    # TODO: Fix pydantic_model_creator error with default factory
    # date = fields.DatetimeField(default=timezone.now)

    id = fields.IntField(pk=True)

    def __repr__(self):
        return self.meta

