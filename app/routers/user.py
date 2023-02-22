from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(prefix="/user", tags=["Manage Users"])


@router.get(
    "/get_all",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.UserOut],
)
async def get_users(db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
                    ):
    users = db.query(models.User).all()
    return users


@router.get("/get", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
                   
                   ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exits",
        )
    return user


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(
    user: schemas.UserIn,
    db: Session = Depends(get_db),
    admin: str = Depends(oauth2.verify_admin),
):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(oauth2.verify_admin),
):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")

    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
