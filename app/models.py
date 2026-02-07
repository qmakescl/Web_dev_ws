from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- Auth Models ---

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None

# --- Post Models ---

class PostBase(BaseModel):
    content: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    user_id: int
    img_path: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# --- Comment Models ---

class CommentBase(BaseModel):
    comment: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
