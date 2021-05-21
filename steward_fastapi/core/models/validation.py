from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

import steward_fastapi.core.models.database as database

# Early init to generate models properly
Tortoise.init_models(['steward_fastapi.core.models.database'], 'models')

Content = pydantic_model_creator(database.Content, name='Content')
ContentSource = pydantic_model_creator(database.ContentSource, name='ContentSource')
ContentType = pydantic_model_creator(database.ContentType, name='ContentType')

ContentIn = pydantic_model_creator(database.Content, name='ContentIn', exclude_readonly=True)
ContentSourceIn = pydantic_model_creator(database.ContentSource, name='ContentSourceIn')
ContentTypeIn = pydantic_model_creator(database.ContentType, name='ContentTypeIn')

Agent = pydantic_model_creator(database.Agent, name='Agent')
AgentOut = pydantic_model_creator(database.Agent, name='AgentOut', exclude=('hashed_password',))

class AgentIn(pydantic_model_creator(database.Agent, name='AgentIn', exclude=('hashed_password',))):
    password: str

