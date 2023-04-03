from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from core.configs import Settings

class UserModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'users'
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(256), nullable=False)
    email = Column(String, unique=True)
    password = Column(String(256), nullable=False)
    is_admin = Column(Boolean, default=False)
    articles = relationship('ArticleModel', cascade='all,delete-orphan', back_populates='created_by', uselist=True, lazy='joined')

