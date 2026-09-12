from fastapi import Depends
from Repository.UserRepo import UserRepository
from Models.model import User
from Schemas.schemas import UserCreate,UserResponse,UserUpdate
class User_Services:
    userRepo: UserRepository

    def __init__(self,userRepo:UserRepository = Depends()) -> None:
        self.userRepo = userRepo

    def createUser(self,user:UserCreate):
        res = self.userRepo.CreateUser(user)
        return res

    def getAllUser(self):
        res = self.userRepo.GetAllUser()
        return res
    
    def GetUserById(self,userId:int):
        res = self.userRepo.GetUserById(userId)
        return res
            
    def UpdateUserById(self,user:UserUpdate):
        res = self.userRepo.UpdateUserById(user)
        return res