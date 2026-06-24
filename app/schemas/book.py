from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated

class BookBase(BaseModel):
    title: Annotated[str, Field(..., min_length=1, max_length=200)]
    isbn: Annotated[str, Field(..., min_length=1, max_length=20)]
    publication_year: Annotated[int, Field(..., gt=0)]
    total_copies: Annotated[int, Field(..., gt=0)]
    author_id: int
    category_id: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    available_copies: Annotated[int, Field(ge=0)]
    model_config = ConfigDict(from_attributes=True) # Pydantic uses dictionary but book is a SQLAlchemy object so from_attributes = True tells Pydantic to read values directly from the object attributes.