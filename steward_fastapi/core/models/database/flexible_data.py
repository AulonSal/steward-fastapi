from tortoise import fields
from tortoise.models import Model


class FlexibleData(Model):
    name = fields.CharField(max_length=50)
    category_1 = fields.CharField(max_length=50)
    category_2 = fields.CharField(max_length=50)
    data = fields.JSONField(description="Freeform json data to suit any use case before the implementation is finalised")


    def __repr__(self):
        return ":".join((self.name, self.category_1, self.category_2, self.data)) # type: ignore

