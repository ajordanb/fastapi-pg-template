from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator


class UserIn(BaseModel):
    email: EmailStr
    password: str
    role:Optional[str] = "user"
    temporary_password:Optional[str] = None

    @validator("password")
    def minimim_length(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        elif len(v) > 18:
            raise ValueError("Password must be at most 18 characters long")
        elif True not in [char.isdigit() for char in v]:
            raise ValueError("Password must contain at least a number")
        return v


class UserOut(BaseModel):
    email: str
    id: int
    role: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    role:Optional[str] = None
    temporary: bool


class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None