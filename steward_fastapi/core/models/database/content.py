# from zoneinfo import ZoneInfo

from tortoise import fields, timezone
from tortoise.models import Model


class ContentSource(Model):
    name = fields.CharField(max_length=50, pk=True)

    def __repr__(self):
        return self.name

    class PydanticMeta:
        backward_relations = False


class ContentType(Model):
    name = fields.CharField(max_length=50, pk=True)

    def __repr__(self):
        return self.name

    class PydanticMeta:
        backward_relations = False


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
    url = fields.CharField(max_length=300, unique=True)
    date = fields.DatetimeField(auto_now_add=True)

    id = fields.IntField(pk=True)

    def __repr__(self):
        return self.meta

