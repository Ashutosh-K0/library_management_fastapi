from sqlalchemy import Integer, String, Column
from app.database import Base
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key= True)
    name = Column(String(100), nullable= False)
    email = Column(String(150), nullable=False, unique=True)

    books = relationship('Book', back_populates='author')