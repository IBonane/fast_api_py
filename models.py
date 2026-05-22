from sqlalchemy import Column, String, Integer
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