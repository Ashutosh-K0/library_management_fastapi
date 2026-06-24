from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
from datetime import datetime
class BorrowRecordBase(BaseModel):
    book_id: Annotated[int, Field(...,gt=0)]
    borrower_name: Annotated[str, Field(...,min_length=1, max_length=100)]

class BorrowRecordCreate(BorrowRecordBase):
    pass

class BorrowRecordResponse(BorrowRecordBase):
    id: int
    issue_date: datetime
    due_date: datetime
    return_date: datetime | None = None
    status: Annotated[str, Field(min_length=1, max_length=20)]
    model_config = ConfigDict(from_attributes=True) #Pydantic uses dictionary but borrow_record is a SQLAlchemy object so from_attributes = True tells Pydantic to read values directly from the object attributes.