from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from app.database import Base
from sqlalchemy.orm import relationship

class BorrowRecord(Base):
    __tablename__ = 'borrow_records'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrower_name = Column(String(100), nullable=False)
    issue_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False)

    book = relationship('Book', back_populates='borrow_records')