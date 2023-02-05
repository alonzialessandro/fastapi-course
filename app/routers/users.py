from .. import models, schemas, utils, oauth2
from fastapi import HTTPException, status, Depends, APIRouter, Response
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #cursor.execute(""" INSERT INTO users(email, password) 
    #                   VALUES (%s, %s) RETURNING *""", (user.email, user.password))
    
    #new_user = cursor.fetchone()
    #conn.commit()

    found_user = db.query(models.User.email).filter(models.User.email == user.email).first()

    if(found_user):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"User with this email alredy exists")
    
    hashed_psw =utils.generateHash(user.password)
    user.password = hashed_psw

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id : int, db: Session = (Depends(get_db)), current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.User).filter(models.User.id == id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found")

    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Forbidden operation")

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.patch('/{id}', response_model=schemas.UserOut)
def update_user(id: int, new_info: schemas.UserUpdate, db: Session = (Depends(get_db)), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.User).filter(models.User.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found")

    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Forbidden operation")

    new_info_dict = new_info.dict(exclude_unset=True)

    if len(new_info_dict.keys()) == 0:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "No valid field has been provided")    
    
    for key, value in new_info_dict.items():
        if(key == 'password'):
            value = utils.generateHash(value)
        setattr(post, key, value)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found")
    
    return user