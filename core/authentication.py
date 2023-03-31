from pytz import timezone
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from pydantic import EmailStr

from models.user_model import UserModel
from core.configs import settings
from core.security import validate_password

oauth2_schema = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1_STR}/user/login')

async def authenticate_user(email: EmailStr, password: str, db: AsyncSession) -> Optional[UserModel]:
    
    async with db as session:
        query = await session.execute(select(UserModel).filter(UserModel.email == email))
        user = query.scalars().unique().one_or_none()
        
        if not user: return None
        if not validate_password(password, user.password): return None
        
        return user


def make_token(token_type: str, token_life_time: timedelta, sub: str) -> str:
    
    payload = {}
    sp_timezone = timezone('America/Sao_Paulo')
    expiration_date = datetime.now(tz=sp_timezone) + token_life_time
    
    payload['type'] = token_type
    payload['exp'] = expiration_date
    payload['iat'] = datetime.now(tz=sp_timezone)
    payload['sub'] = str(sub)
    
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def generate_access_token(sub: str) -> str:
    
    return make_token(
        token_type='access_token',
        token_life_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN_MINUTES),
        sub=sub
    )

