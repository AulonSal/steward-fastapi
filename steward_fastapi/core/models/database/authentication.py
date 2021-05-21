from tortoise import fields
from tortoise.contrib.pydantic.creator import PydanticMeta
from tortoise.models import Model


class Agent(Model):
    username = fields.CharField(max_length=50, pk=True)
    disabled = fields.BooleanField(default=False)
    hashed_password = fields.CharField(max_length=200)

    def __repr__(self):
        return self.username

