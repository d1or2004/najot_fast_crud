from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from model import User
from database import SessionLocal
from schemas import UserModel

user_update = APIRouter(prefix="/user")


@user_update.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update(user_id: int, user: UserModel, db: Session = Depends(SessionLocal)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = bcrypt.hash(user.password)
    db_user.is_staff = user.is_staff
    db_user.is_active = user.is_active

    db.commit()
    db.refresh(db_user)

    return {
        "code": 200,
        "msg": "User updated successfully",
        "User": db_user
    }


@user_update.get('/{id}')
async def category_id(id: int, db: Session = Depends(SessionLocal)):
    check_user = db.query(User).filter(User.id == id).first()
    if check_user:
        return jsonable_encoder(check_user)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday id ga ega User yo'q")
