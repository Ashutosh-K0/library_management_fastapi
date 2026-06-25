from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.borrow_record import BorrowRecordCreate, BorrowRecordResponse
from app.models.borrow_record import BorrowRecord
from app.models.book import Book
from datetime import datetime, timedelta

router  = APIRouter(prefix='/borrow_records', tags=['Borrow_Records'])

#CREATE a borroww record(POST HTTP Method): API Endpoint
@router.post("/", response_model=BorrowRecordResponse)
def create_borrow_record(record: BorrowRecordCreate, db: Session = Depends(get_db)):
    book_record= db.query(Book).filter(Book.id==record.book_id).first()
    if not book_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book does not exist')
    if book_record.available_copies<=0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No available copies')
    issue_date = datetime.now()
    due_date = issue_date + timedelta(days=14)
    new_borrow_record = BorrowRecord(**record.model_dump(), issue_date=issue_date, due_date=due_date,status = 'Borrowed', return_date = None)
    book_record.available_copies -= 1
    db.add(new_borrow_record)
    db.commit()
    db.refresh(new_borrow_record)
    return new_borrow_record

#UPDATE the Book_record(PUT HTTP Method): API Endpoint
@router.put("/{borrow_record_id}/return", response_model=BorrowRecordResponse)
def update_borrow_record(borrow_record_id: int, db: Session = Depends(get_db)):
    borrow_record = db.query(BorrowRecord).filter(BorrowRecord.id==borrow_record_id).first()
    if not borrow_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No Book Record found')
    book_record = db.query(Book).filter(Book.id == borrow_record.book_id).first()
    if not book_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Associated book not found")
    if borrow_record.return_date is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Book has already been returned")
    book_record.available_copies += 1
    borrow_record.return_date = datetime.now()
    borrow_record.status = 'Returned'
    db.commit()
    db.refresh(borrow_record)
    return borrow_record

#RETRIEVE all the Borrow_Records(GET HTTP Method): API Endpoint
@router.get("/",response_model=list[BorrowRecordResponse])
def get_borrow_records(db:Session = Depends(get_db)):
    borrow_records = db.query(BorrowRecord).all()
    return borrow_records

#RETRIEVE single borrow_record(GET HTTP Method): API Endpoint
@router.get("/{borrow_record_id}",response_model=BorrowRecordResponse)
def get_single_borrow_record(borrow_record_id: int, db:Session= Depends(get_db)):
    borrow_record = db.query(BorrowRecord).filter(BorrowRecord.id==borrow_record_id).first()
    if not borrow_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Borrow Record is not present')
    return borrow_record