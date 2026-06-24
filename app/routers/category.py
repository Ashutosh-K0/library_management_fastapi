from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix='/Categories', tags =['Categories'])

# CREATE Category(POST HTTP Method): API Endpoint
@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # Checking if a category with the same name already exists or not
    existing_category = db.query(Category).filter(Category.name==category.name).first()
    if existing_category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Category already exists')
    
    # Creating SQLAlchemy model instance from Pydantic schema
    new_category = Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

#RETRIEVE all the Categories(GET HTTP Method): API ENDPOINT
@router.get("/", response_model=list[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

#RETRIEVE the Category using category_id(GET HTTP Method): API Endpoint
@router.get("/{category_id}", response_model= CategoryResponse)
def get_category_id(category_id: int, db: Session = Depends(get_db)):
    return_category = db.query(Category).filter(Category.id==category_id).first()
    if not return_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not present')
    return return_category

#DELETE category using category_id(DELETE HTTP Method): API Endpoint
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db:Session = Depends(get_db)):
    category_remove = db.query(Category).filter(Category.id == category_id).first()
    if not category_remove:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category is not present')
    db.delete(category_remove)
    db.commit()

#UPDATE Category using category_id(PUT HTTP Method): API Endpoint
@router.put("/{category_id}", response_model=CategoryResponse)
def updated_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    category_record = db.query(Category).filter(Category.id==category_id).first()
    if not category_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 'Category not present')
    name_owner = db.query(Category).filter(Category.name==category.name).first()
    if name_owner and name_owner.id != category_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Name already used')
    category_record.name = category.name
    db.commit()
    db.refresh(category_record)
    return category_record