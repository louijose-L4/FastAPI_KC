from pydantic import BaseModel,EmailStr,Field,ConfigDict
from datetime import datetime
from typing import Optional
from typing import Annotated



class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime

class Post(PostBase):
    id: int    
    created_at: datetime
    owner_id:int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    post: Post
    votes: int

    class Config:
        orm_mode = True
    #model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=-1, le=1)]

