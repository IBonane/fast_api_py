from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.dialects.postgresql import ARRAY

from database import Base

class Heroes(Base):
    __tablename__ = "heroes"
    id = Column(Integer, autoincrement= True, index= True, primary_key=True)
    nick_name = Column(String)
    full_name = Column(String)
    occupation = Column(ARRAY(String))
    powers = Column(ARRAY(String))
    hobby = Column(ARRAY(String))
    type = Column(String)
    rank = Column(Integer)

class Players(Base):
    __tablename__ = "players"
    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)