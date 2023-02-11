from ... import  models, utils, oauth2
from fastapi import status, HTTPException
import random
import string
from ...proxy import Proxy
admin = Proxy()


def get_user_by_email(db, user_email:str):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_email)
        .first()
    )
    return user


def authenticate_user(db, user_email:str,user_password:str):
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    if not user.temporary_password:
        if utils.verify(user_password, user.password):    
            access_token = oauth2.create_access_token(
                data={"user_id": user.id, "roles": user.role}
            )
            return access_token
    elif user.temporary_password and utils.verify(user_password, user.temporary_password):
        print(user.temporary_password)
        access_token = oauth2.create_access_token(
            data={"user_id": user.id, "roles": user.role}
        )
        return access_token
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials"
        )
    
    
def update_temp_password(db, email:str):
    temporary_password = generate_password()
    password = utils.hash_password(temporary_password)
    db.query(models.User).filter(models.User.email == email).update({models.User.temporary_password: password})
    db.commit()
    admin.send_email(f"Hey,{email}, your password has been temporarily changed to: {temporary_password}, follow this link to change it and login: www.datapaip.com/login", "New password", "User", email)
    return temporary_password

def update_new_password(db, user_id, new_password:str):
    password = utils.hash_password(new_password)
    db.query(models.User).filter(models.User.id == user_id).update({models.User.password:password, models.User.temporary_password:None})
    user = db.query(models.User).filter(models.User.id == user_id).first()
    admin.send_email(f"Your password was succesfully updated, please refer back to our website for any further assistance", "New password", "User", user.email)
    return db.commit()

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))