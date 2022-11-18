from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ValidationError, validator


class UserIn(BaseModel):
    email: EmailStr
    password: str

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
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None
