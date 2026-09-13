from fastapi import Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session
from database import get_db
from Models.model import User

class UserLoginAuth:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_user_OnLogin(self, username: str, password: str):
        user = self.db.query(User).filter(
            or_(User.username == username, User.email == username),
            User.password == password
        ).first()
        return user


