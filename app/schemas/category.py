from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated

class CategoryBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id : int
    model_config = ConfigDict(from_attributes=True)# Pydantic uses dictionary but category is a SQLAlchemy object so from_attributes = True tells Pydantic to read values directly from the object attributes.