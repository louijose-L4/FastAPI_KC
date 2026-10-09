from .. import schemas,models,utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import Optional,List
from sqlalchemy import func


router = APIRouter(prefix="/posts",tags=['Posts'])

#,response_model=list[schemas.PostOut]
@router.get("/",response_model=list[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit:int=2,skip:int=0,search:Optional[str]=""):
    # cursor.execute('''SELECT * FROM posts ''')f
    # posts = cursor.fetchall()  
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #try:
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).all()
    #print(posts)
    #except Exception as e:
        #print(e)
    #.filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(posts)
    #return posts
    result = []

    for post, votes in posts:
        result.append({
            "post": post,
            "votes": votes
        })

    return result

# @app.post("/createposts")
# def create_posts(payload: dict=Body(...))
#     return {"message":f"title {payload['title']} content {payload['content']}"}

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
        # dic = post.model_dump()
        # dic["id"] = randrange(3,1000000)
        # my_posts.append(dic)
        

        # cursor.execute('''INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *''',(post.title,post.content,post.published))
        # new_post = cursor.fetchone()
        # conn.commit()
        # return {"data":new_post}

        # new_post = models.Post(title=post.title,content=post.content,published=post.published)
        new_post = models.Post(owner_id=current_user.id,**post.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''SELECT * FROM posts WHERE id = %s''',(str(id)))
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    result = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    # post = cursor.fetchone()
    # # post = find_post(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")       
    post, votes = result   
    return {
        "post": post,
        "votes": votes
        }       
    


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # index = find_index_post(id)
    # cursor.execute('''DELETE FROM posts WHERE id = %s returning *''',(str(id)),)    
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query  = db.query(models.Post).filter(models.Post.id==id)

    post = post_query.first()

    

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')

    if post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    #my_posts.pop(index)
    #return {"message":f"post {id} successfuly got deleted"}
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id:int,updated_post:schemas.PostCreate,db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #index = find_index_post(id)
    # cursor.execute('''UPDATE posts SET title = %s , content= %s, published= %s WHERE id = %s RETURNING *''',(post.title,post.content,post.published,(str(id))))
    # updated_post = cursor.fetchone()
    # conn.commit()
    #post_query = db.query(models.Post).filter(models.Post.id == id)

    #updated_post = post_query.first()

    post_query  = db.query(models.Post).filter(models.Post.id==id)
    
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    # if post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    # post_dict = post.model_dump()
    # post_dict["id"] = id
    # my_posts[index] = post_dict 
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    #db.refresh(post_query)
    return post_query.first()

