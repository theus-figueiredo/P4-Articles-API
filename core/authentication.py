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
