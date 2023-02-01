from .. import models, schemas, utils
from fastapi import HTTPException, status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #cursor.execute(""" INSERT INTO users(email, password) 
    #                   VALUES (%s, %s) RETURNING *""", (user.email, user.password))
    
    #new_user = cursor.fetchone()
    #conn.commit()

    hashed_psw =utils.generateHash(user.password)
    user.password = hashed_psw

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found")
    
    return user