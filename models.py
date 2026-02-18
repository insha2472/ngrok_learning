from db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String,unique=True, index=True)
    name = Column(String)
    password= Column(String)

    sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")