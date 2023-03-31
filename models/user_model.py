from sqlalchemy import Column, Integer, String

from core.configs import Settings

class UserModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'users'
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    fullname = Column(String)
    email = Column(String)
    password = Column(String(15))

