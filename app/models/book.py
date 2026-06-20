from sqlalchemy import Integer, String, Column, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    isbn = Column(String(20), nullable=False, unique=True)
    publication_year = Column(Integer, nullable=False)
    total_copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    author = relationship('Author', back_populates='books')
    category = relationship('Category', back_populates='books')