from datetime import datetime, timedelta
from typing import Literal, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from steward_fastapi.config.config import JWT_SECRET_KEY
from steward_fastapi.core.models.database import Agent as AgentDB
from steward_fastapi.core.models.validation import Agent

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 40

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def hash_password(password):
    return password_context.hash(password)

async def get_agent(db, username: str) -> Optional[Agent]:
    agent = await db.get_or_none(username=username)
    
    return await Agent.from_tortoise_orm(agent) if agent else None

async def authenticate_agent(db, username: str, password: str) -> Union[Agent, Literal[False]]:
    agent = await get_agent(db, username)

    if agent is None:
        return False
    if not verify_password(password, agent.hashed_password):
        return False
    return agent

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    expires = datetime.utcnow() + expires_delta if expires_delta else timedelta(minutes=15)
    to_encode.update(dict(exp=expires))

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_agent(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    agent = await get_agent(AgentDB, username=token_data.username)
    if agent is None:
        raise credentials_exception

    return agent

async def get_current_active_agent(current_agent: Agent = Depends(get_current_agent)):
        if current_agent.disabled:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive agent')
        return current_agent

async def create_new_active_agent(username: str, password: str, disabled: Optional[bool] = None):
    hashed_password = hash_password(password)
    return await AgentDB.create(
            hashed_password=hashed_password,
            username=username,
        )

