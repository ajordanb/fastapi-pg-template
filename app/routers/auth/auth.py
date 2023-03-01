from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ...database import get_db
from ... import schemas, models, utils, oauth2
from .utils import authenticate_user, get_user_by_email, update_temp_password, update_new_password
router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    access_token = authenticate_user(
        db, user_credentials.username, user_credentials.password)
    user = get_user_by_email(db, user_credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials, user not found"
        )
    temporary = (True if user.temporary_password else False)
    return {"access_token": access_token, "token_type": "bearer", "role":user.role, "temporary":temporary}


@router.post("/forgot_password", status_code=status.HTTP_200_OK)
def forgot_password(
    email: str,
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials, user not found"
        )
    update_temp_password(db, user.email)
    return {"message": "email sent!"}


@router.post("/reset_password", status_code=status.HTTP_200_OK)
def reset_password(
        new_password: str,
        current_user: int = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)):
    update_new_password(db, int(current_user.id), new_password)
    return {"message": "Password updated succesfully"}
