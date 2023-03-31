from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from database.database_session import Session
from core.authentication import oauth2_schema
from core.configs import settings
from models.user_model import UserModel

class TokenData(BaseModel):
    user_id: Optional[str] = None

async def get_session() -> Generator:
    session: AsyncSession = Session()
    
    try:
        yield session
    finally:
        await session.close()



async def validate_access_token(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_schema)) -> UserModel:

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Usuário não autorizado',
        headers={"WWW=Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms={settings.ALGORITHM}, options={"verify_aud": False})
        user_id: str = payload.get('sub')

        if user_id is None: raise credential_exception
        
        token_data: TokenData = TokenData(user_id=user_id)
    except JWTError:
        raise credential_exception
    
    async with db as session:
        query = await session.execute(select(UserModel).filter(UserModel.id == int(token_data.user_id)))
        user = query.scalars().unique().one_or_none()
        
        if not user: raise credential_exception
        return user
