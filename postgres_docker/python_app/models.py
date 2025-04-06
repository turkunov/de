from sqlalchemy import Column, String
from python_app.db import Base

class User(Base):
    __tablename__ = "names"
    id = Column(String, primary_key=True, unique=True, index=True)
    name = Column(String, unique=False)
    surname = Column(String, unique=False)
    gender = Column(String, unique=False)
    img = Column(String, unique=False)