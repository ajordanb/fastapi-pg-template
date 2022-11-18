from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(prefix="/user", tags=["Users"])


@router.get(
    "/get_all",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.UserOut],
)
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exits",
        )
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(
    user: schemas.UserIn,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.verify_admin),
):
    # print(current_user)
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
