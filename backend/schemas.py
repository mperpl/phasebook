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