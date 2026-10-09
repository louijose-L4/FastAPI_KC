from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from . import models,schemas,utils
from .database import engine,get_db
from sqlalchemy.orm import Session
from .routers import posts,users,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


# class Post(BaseModel):
#     title:str
#     content:str
#     published: bool = True
#     #rating: Optional[int] = None




my_posts = [{"id":1,"title":"title of post 1","content":"content of post 1"},{"id":2,"title":"title of post 2","content":"content of post 2"}]   

def find_post(id):    
    for p in my_posts:
        if p["id"] == int(id):               
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_posts(db:Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

    


