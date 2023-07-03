from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import database, schemas, models
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings, secrets

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = secrets.secret_key
ALGORITHM = secrets.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = secrets.access_token_expire_minutes

admin_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Could not validate admin credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        role: str = payload.get("roles", None)
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id, role=role)
    except JWTError:
        raise credentials_exception
    return token_data

def verify_role(roles_needed:list, _exception:HTTPException, token:str):
    try:
        token_data = verify_access_token(token=token)
        role: str = token_data.role
        if not role:
            raise _exception
        if role not in roles_needed:
            raise _exception
    except JWTError:
        raise credentials_exception
    return token_data


def verify_admin(token: str = Depends(oauth2_scheme)):
    return verify_role(roles_needed=["admin"], _exception=admin_exception, token=token)

def get_current_user(
        token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    token = verify_access_token(token)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
