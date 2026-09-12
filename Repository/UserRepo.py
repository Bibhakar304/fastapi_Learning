from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from Models.model import User
from Schemas.schemas import UserCreate,UserUpdate

class UserRepository:
    db: Session

    def __init__(self,db: Session =Depends(get_db)) ->None:
        self.db = db

    def CreateUser(self,user:UserCreate):
        new_user = User(
            username = user.username,
            email = user.email,
            password = user.password
        )
        self.db.add(new_user)
        try:
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def GetAllUser(self):
        return self.db.query(User).all()

    def GetUserById(self,userID:int):
        res = self.db.query(User).filter(User.user_id == userID).first()
        
        return res

    def UpdateUserById(self,UserDto:UserUpdate):
        res =(self.db.query(User).filter(User.user_id == UserDto.user_id).first())
        if res is None:
            return None
        else:
            res.username = UserDto.username,
            res.email = UserDto.email,
            res.password = UserDto.password     
            

        try:
            self.db.commit()
            self.db.refresh(res)
            return res
        except Exception:
            self.db.rollback()
            raise



