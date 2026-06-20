from sqlalchemy import Integer, String, Column
from app.database import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
