from sqlalchemy import Column, Integer, String
from app.database.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_api_key = Column(String, unique=True)
