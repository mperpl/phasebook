from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr, SecretStr

class UserRead(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    bio: Optional[str]
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)

class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: EmailStr
    password: SecretStr = Field(min_length=3, max_length=16)
    password_repeat: SecretStr = Field(min_length=3, max_length=16)


class UserLogin(BaseModel):
    identifier: str = Field(min_length=3, max_length=254)
    password: SecretStr = Field(min_length=3, max_length=32)


class UserPasswordReset(BaseModel):
    old_password: SecretStr
    new_password: SecretStr = Field(min_length=3, max_length=32)
    confirm_new_password: SecretStr = Field(min_length=3, max_length=32)

class UserForgotPassword(BaseModel):
    new_password: SecretStr = Field(min_length=3, max_length=32)
    confirm_new_password: SecretStr = Field(min_length=3, max_length=32)

class UserSessionContext(BaseModel):
    session_uuid: str
    id: int
    email: EmailStr
    username: Optional[str]
    bio: Optional[str]
    is_verified: bool

    model_config = {"from_attributes": True}

class UserProfileCache(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str]
    bio: Optional[str]
    is_verified: bool

    model_config = {"from_attributes": True}

class UserUpdateBio(BaseModel):
    bio: str = Field(min_length=3, max_length=254)

class UserUpdateUsername(BaseModel):
    username: str = Field(min_length=3, max_length=32)



class WritePost(BaseModel):
    content: str

class ReadPost(BaseModel):
    author_id: int
    content: str

    model_config = ConfigDict(from_attributes=True)



class WriteComment(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

class CommentRead(BaseModel):
    id: int
    content: str
    author_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PostDiscussionRead(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    # This is the magic line that nests the comments
    comments: list[CommentRead] = []

    model_config = ConfigDict(from_attributes=True)