from .. import models, schemas, oauth2
from fastapi import HTTPException, status, Response, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func
from typing import List, Optional

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit : int = 10, skip : int = 0, search : Optional[str] = ''): #user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()
    
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    #post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message" : f"Post with id {id} not found"}

    #if user.id != post.owner_id:
    #    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Forbidden operation")     
    
    return post
   
    
@router.post('', status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" INSERT INTO posts(title, content) 
    #                   VALUES (%s, %s) RETURNING *""", (post.title, post.content))
    #post = cursor.fetchone()
    #conn.commit()
    
    new_post = models.Post(owner_id= user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    query = db.query(models.Post).filter(models.Post.id == id)

    post = query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found") 

    if user.id != post.owner_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Forbidden operation")     

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostBase, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (post.title, post.content, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    
    query = db.query(models.Post).filter(models.Post.id == id)

    post = query.first()

    if post == None:
       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")

    if user.id != post.owner_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Forbidden operation")    
        
    query.update(update_post.dict(), synchronize_session=False)
    db.commit()

    return query.first()


@router.patch("/{id}", response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostUpdate, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    
    query = db.query(models.Post).filter(models.Post.id == id)

    post = query.first()

    if post == None:
       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
    
    if user.id != post.owner_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Forbidden operation")    
    
    new_post_data = update_post.dict(exclude_unset=True)
    
    if len(new_post_data.keys()) == 0:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "No valid field has been provided")    
    
    for key, value in new_post_data.items():
            setattr(post, key, value)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post