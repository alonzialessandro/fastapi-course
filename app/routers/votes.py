from .. import models, schemas, oauth2
from fastapi import HTTPException, status, Response, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/vote',
    tags=['Votes']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Votes,  db: Session = Depends(get_db) , user : int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id {vote.post_id} doesn\'t exist') 
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id)
    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f'Current user with id {user.id} has already voted on post {vote.post_id}')

        new_vote = models.Vote(post_id = vote.post_id, user_id = user.id)
        db.add(new_vote)
        db.commit()
        return {'message' : 'Successfully added vote'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Current user with id {user.id} hasn\'t voted on post {vote.post_id} yet') 

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message' : 'Successfully deleted vote'}