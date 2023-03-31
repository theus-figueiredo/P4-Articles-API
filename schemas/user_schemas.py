from typing import Optional, List
from pydantic import BaseModel, EmailStr

from schemas.article_schemas import ArticleSchema

class UserBaseSchema(BaseModel):
    
    id: Optional[int]
    fullname: str
    email: EmailStr
    is_admin: bool = False
    
    class Config:
        orm_mode = True


class UserSchemaCreate(UserBaseSchema):
    password: str

#O USER SHCEMA CREATE CONTÉM APENAS A SENHA POIS É O QUE VAI SER USADO PARA CRIAR O USER NO DB
# O QUE SERÁ RETORNADO PARA O USUÁRIO SERÁ O BASE, QUE NÃO CONTÉM INFORMAÇÕES DA SENHA


class UserArticleSchema(UserBaseSchema):
    articles: Optional[List[ArticleSchema]]


class UserSchemaUpdate(UserBaseSchema):
    fullname: Optional[str]
    email: Optional[str]
    is_admin: Optional[bool]
    password: Optional[str]
