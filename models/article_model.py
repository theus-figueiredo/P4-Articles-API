from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings

class ArticleModel(settings.DB_BASE_MODEL):
    __tablename__ = 'articles'
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title: Column(String(256))
    body: Column(String(512))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_by = relationship('UserModel', back_populates='articles', lazy='joined')

