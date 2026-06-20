from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Annotated

class AuthorBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    email: EmailStr

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True) # Pydantic uses dictionary but author is a SQLAlchemy object so from_attributes = True tells Pydantic to read values directly from the object attributes.
