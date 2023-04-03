from typing import List, Optional, Any
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel
from schemas.user_schemas import UserBaseSchema, UserSchemaUpdate, UserSchemaCreate, UserArticleSchema
from core.dependencies import get_session, validate_access_token
from core.security import password_hash_generate
from core.authentication import authenticate_user, generate_access_token

user_router = APIRouter()

#GET LOGGED IN USER
@user_router.get('/logged-in', response_model=UserBaseSchema)
def get_logged_user(user: UserModel = Depends(validate_access_token)):
    return user


#POST USER
@user_router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserBaseSchema)
async def post_user(data: UserSchemaCreate, db: AsyncSession = Depends(get_session)) -> Response:
    
    new_user = UserModel(fullname=data.fullname, email=data.email, password=password_hash_generate(data.password), is_admin=data.is_admin)
    
    async with db as database:
        database.add(new_user)
        await database.commit()
        
        return new_user


#GET ALL USERS
@user_router.get('/', response_model=List[UserBaseSchema], status_code=status.HTTP_200_OK)
async def get_all(db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(UserModel))
        users: List[UserBaseSchema] = query.scalars().unique().all()
        
        return users


#GET USER BY ID
@user_router.get('/{id}', response_model=UserArticleSchema, status_code=status.HTTP_200_OK)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        query = await database.execute(select(UserModel).filter(UserModel.id == id))
        user: UserArticleSchema = query.scalars().unique().one_or_none()
        
        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')


#UPDATE USER
@user_router.patch('/{id}', response_model=UserBaseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_user(id: int, data: UserSchemaUpdate, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(UserModel).filter(UserModel.id == id))
        user_to_update = query.scalars().unique().one_or_none()
        
        if user_to_update:
            
            if user_to_update.id != user.id or user.is_admin is not True: 
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Ação não autorizada')
            else:
                for key, value in data.dict(exclude_unset=True).items():
                    setattr(user_to_update, key, value)

                    return user_to_update
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')


#CHANGE USER PASSWORD
@user_router.patch('/password/{id}', response_model=UserBaseSchema, status_code=status.HTTP_202_ACCEPTED)
async def change_password(id: int, password: str, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
     async with db as database:
        
        query = await database.execute(select(UserModel).filter(UserModel.id == id))
        user_to_update = query.scalars().unique().one_or_none()
        
        if user_to_update:
            
            if user_to_update.id != user.id or user.is_admin is not True: 
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Ação não autorizada')
            else:
                user_to_update.password = password_hash_generate(password)
                return user_to_update
            
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')


#LOGIN
@user_router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)) -> Response:
    
    user = await authenticate_user(email=form_data.username, password=form_data.password, db=db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email ou senha incorretos')
    
    return JSONResponse(content={"access_token": generate_access_token(sub=user.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)

