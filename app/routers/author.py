from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorResponse


router = APIRouter(prefix = '/authors', tags= ['Authors'])

# Reminder:
# Pydantic schemas are used for request/response validation.
# SQLAlchemy models are used for database operations.
# AuthorCreate -> Author -> PostgreSQL -> AuthorResponse

# CREATE Author(POST HTTP Method): API Endpoint
@router.post("/", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    # Checking if an author with the same email already exists or not
    existing_author = (
        db.query(Author)
        .filter(Author.email == author.email)
        .first()
    )
    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Author with this email already exists."
        )
    
    # Creating SQLAlchemy model instance from Pydantic schema
    new_author = Author(**author.model_dump())

    # Save to database
    db.add(new_author)
    db.commit()

    # Fetch generated fields like id
    db.refresh(new_author)

    return new_author

# RETRIEVE Authors(GET HTTP Method): API Endpoint
@router.get("/", response_model=list[AuthorResponse]) # The output will  be the list of all the authors present in the database.
def get_author_all(db: Session = Depends(get_db)):
    authors = db.query(Author).all() # SQLAlchemy object for database operations
    return authors

# RETRIEVE a single author by ID(GET HTTP Method) : API Endpoint
@router.get("/{author_id}", response_model=AuthorResponse)
def get_author_id(author_id: int, db:Session = Depends(get_db)):
    return_author = db.query(Author).filter(Author.id == author_id).first()
    if  not return_author:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='Author does not exist in the database')
    return return_author

# UPDATE a single author using author_id(PUT HTTP Method): API Endpoint
@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db)):
    author_record = db.query(Author).filter(Author.id == author_id).first()
    if not author_record:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='Author does not exist in the database')
    email_owner = db.query(Author).filter(Author.email == author.email).first()
    if email_owner and email_owner.id!= author_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is already used')
    author_record.name = author.name
    author_record.email = author.email
    db.commit()
    db.refresh(author_record)
    return author_record

# Deleting a single author suign author_id(DELETE HTTP Method): API Endpoint
@router.delete("/{author_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session= Depends(get_db)):
    author_remove = db.query(Author).filter(Author.id == author_id).first()

    if not author_remove:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')
    db.delete(author_remove)
    db.commit()