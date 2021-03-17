# from enum import Enum
# from typing import Optional
from datetime import timedelta
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from steward_fastapi.core.authentication import (
        ACCESS_TOKEN_EXPIRE_MINUTES,
        authenticate_agent,
        create_access_token,
        get_current_active_agent,
        get_current_agent,
        hash_password, oauth2_scheme
    )

from steward_fastapi.core.models.validation import Agent, AgentIn, AgentOut
from steward_fastapi.core.models.database import Agent as AgentDB


router = APIRouter()

@router.get('/agent')
async def read_current_agent(current_agent: Agent = Depends(get_current_active_agent)):
    return current_agent

@router.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    agent = await authenticate_agent(AgentDB, form_data.username, form_data.password)

    if not agent:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect username or password',
                headers={'WWW-Authenticate': 'Bearer'},
                )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
            data={'sub': agent.username},
            expires_delta=access_token_expires,
    )
    
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.post('/agent')
async def create_agent(agent_in: AgentIn, token: str = Depends(oauth2_scheme)):
    print(agent_in)
    print('B', 'B', sep='\n')
    
    agent = Agent(
            username=agent_in.username, 
            hashed_password=hash_password(agent_in.password),
            disabled=agent_in.disabled,
        )

    await AgentDB.create(
            **agent.dict()
        )

@router.delete('/agent')
async def delete_agent(username: str, token: str = Depends(oauth2_scheme)):
    await AgentDB.get(username=username).delete()
    
@router.get('/agents', response_model=list[AgentOut])
async def read_agents():
    return await AgentOut.from_queryset(AgentDB.all())

