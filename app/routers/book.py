from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.book import Book
from app.schemas.book import BookCreate, BookResponse
from app.models.author import Author
from app.models.category import Category

router = APIRouter(prefix='/Books', tags=['Books'])

# RETRIEVE all the books(GET HTTP Method): API Endpoint
@router.get("/", response_model=list[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

# RETRIEVE a single book by book_id(GET HTTP Method): API Endpoint
@router.get("/{book_id}", response_model=BookResponse)
def get_book_id(book_id: int, db: Session =Depends(get_db)):
    book = db.query(Book).filter(Book.id==book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book is not present in the database')
    return book

# DELETE Book using book_id(DELETE HTTP Method): API Endpoint
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_record = db.query(Book).filter(Book.id==book_id).first()
    if not book_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found in the database')
    db.delete(book_record)
    db.commit()


# CREATE Book(POST HTTP Method): API Endpoint
@router.post("/",response_model=BookResponse)
def create_book(book:BookCreate, db: Session = Depends(get_db)):
    #Checking if the book already exists or not
    existing_book = db.query(Book).filter(Book.isbn==book.isbn).first()
    if existing_book:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = 'Book with same ISBN already exists')
    
    #Checking if the author is present or not
    author = db.query(Author).filter(Author.id==book.author_id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')
    
    #Checking if the category is present or not
    category = db.query(Category).filter(Category.id==book.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not present')
    new_book = Book(**book.model_dump(), available_copies = book.total_copies)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

#UPDATE Book using book_id(PUT HTTP Method): API Endpoint
@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db:Session=Depends(get_db)):
    #Checking if the book exists or not
    book_record = db.query(Book).filter(Book.id==book_id).first()
    if not book_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book is not present in the database')
    #Checking if the ISBN is unique or not
    isbn_owner = db.query(Book).filter(Book.isbn==book.isbn).first()
    if isbn_owner and isbn_owner.id != book_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='The book with same ISBN already exists')
    #Checking if the author exists or not
    author_record = db.query(Author).filter(Author.id == book.author_id).first()
    if not author_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')
    #Checking if the category exists
    category = db.query(Category).filter(Category.id==book.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

    if book.total_copies < book_record.available_copies:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Total copies cannot be less than available copies")

    book_record.title = book.title
    book_record.isbn = book.isbn
    book_record.publication_year = book.publication_year
    book_record.total_copies = book.total_copies
    book_record.author_id = book.author_id
    book_record.category_id = book.category_id
    db.commit()
    db.refresh(book_record)
    return book_record