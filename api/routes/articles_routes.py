from typing import List
from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from  models.article_model import ArticleModel
from models.user_model import UserModel
from schemas.article_schemas import ArticleSchema, ArticleUpdateSchema
from core.dependencies import get_session, validate_access_token

article_route = APIRouter()

#POST NEW ARTICLE
@article_route.post('/', status_code=status.HTTP_201_CREATED, response_model=ArticleSchema)
async def post_article(article: ArticleSchema, user_logged: UserModel = Depends(validate_access_token), db: AsyncSession = Depends(get_session)) -> Response:
    
    new_article = ArticleModel(title=article.title, body=article.body, user_id=user_logged.id)
    
    async with db as database:
        database.add(new_article)
        await database.commit()
    
        return new_article


#GET ALL ARTICLES
@article_route.get('/', status_code=status.HTTP_200_OK, response_model=List[ArticleSchema])
async def get_all(db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(ArticleModel))
        articles: List[ArticleModel] = query.scalars().unique().all()
        
        return articles


#GET ARTICLE BY ID
@article_route.get('/{id}', status_code=status.HTTP_200_OK, response_model=ArticleSchema)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(ArticleModel).filter(ArticleModel.id == id))
        article = query.scalars().unique().one()
        
        if article is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Artigo não encontrado')
        
        return article


#UPDATE ARTICLE
@article_route.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ArticleSchema)
async def update_article(id: int, new_data: ArticleUpdateSchema, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(ArticleModel).filter(ArticleModel.id == id))
        article_to_update = query.scalars().unique().one()
        
        if article_to_update:
            if user.id == article_to_update.user_id or user.is_admin is True:
                for key, value in new_data.dict(exclude_unset=True).items():
                    setattr(article_to_update, key, value)
                
                    await database.commit()
                
                    return article_to_update
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Ação não autorizada')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Artigo não encontrado')


#DELETE ARTICLE
@article_route.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(id: int, user: UserModel = Depends(validate_access_token), db: AsyncSession = Depends(get_session)) -> None:
    
    async with db as database:
        
        query = await database.execute(select(ArticleModel).filter(ArticleModel.id == id))
        article_to_delete = query.scalars().unique().one()
        
        if article_to_delete:
            if user.id == article_to_delete.user_id or user.is_admin is True:
                await database.delete(article_to_delete)
                await database.commit()
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Ação não autorizada')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Artigo não encontrado')


