from typing import Optional
from pydantic import BaseModel


class ArticleSchema(BaseModel):
    id: Optional[int]
    title: str
    body: str
    user_id: Optional[int]
    
    class Config:
        orm_mode = True


class ArticleUpdateSchema(ArticleSchema):
    title: Optional[str]
    body: Optional[str]

