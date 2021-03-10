import steward_fastapi.core.models.database as database

from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import Tortoise

# Early init to generate models properly
Tortoise.init_models(["steward_fastapi.core.models.database"], "models")

Content = pydantic_model_creator(database.Content, name='Content')
ContentSource = pydantic_model_creator(database.ContentSource, name='ContentSource', exclude=('content',))
ContentType = pydantic_model_creator(database.ContentType, name='ContentType', exclude=('content',))
# ContentSource = pydantic_model_creator(database.ContentSource, name='ContentSource', exclude=('content', 'id'))
# ContentType = pydantic_model_creator(database.ContentType, name='ContentType', exclude=('content', 'id'))

ContentIn = pydantic_model_creator(database.Content, name='ContentIn', exclude_readonly=True)
ContentSourceIn = ContentSource
ContentTypeIn = ContentType
# ContentSourceIn = pydantic_model_creator(database.ContentSource, name='ContentSourceIn', exclude_readonly=True)
# ContentTypeIn = pydantic_model_creator(database.ContentType, name='ContentTypeIn', exclude_readonly=True, include=("name",))

