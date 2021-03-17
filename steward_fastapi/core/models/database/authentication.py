from tortoise import fields
from tortoise.models import Model

from tortoise.contrib.pydantic.creator import PydanticMeta

class Agent(Model):
    username = fields.CharField(max_length=50, pk=True)
    disabled = fields.BooleanField(default=False)
    hashed_password = fields.CharField(max_length=200)

    def __repr__(self):
        return self.username

