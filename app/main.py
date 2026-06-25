from fastapi import FastAPI
from app.database import Base
from app.models import author, book, borrow_record, category
from app.database import engine
from app.routers.author import router as author_router
from app.routers.category import router as category_router
from app.routers.book import router as book_router
from app.routers.borrow_record import router as borrow_record_router

app = FastAPI()

@app.get("/")
def welcome():
    return {'message': 'Library Management System'}

Base.metadata.create_all(engine)

app.include_router(author_router)
app.include_router(category_router)
app.include_router(book_router)
app.include_router(borrow_record_router)