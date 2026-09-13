from fastapi import FastAPI, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from Models.model import User
from Schemas.schemas import UserCreate, UserResponse, UserUpdate
from Schemas.ConstantResponce import ApplicationResponce
from Services.User_Services import User_Services
from typing import List, Optional
from core.dependencies import get_current_client, get_current_user_id

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=ApplicationResponce[UserResponse], status_code=status.HTTP_200_OK)
def get_current_user_profile(
    user_id: int = Depends(get_current_user_id),
    user_services: User_Services = Depends()
):
    user = user_services.GetUserById(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return ApplicationResponce(
        StatusCode=200,
        Message="User profile retrieved successfully",
        Data=user
    )

@router.post("/users", response_model=ApplicationResponce[UserResponse], status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, User_Services: User_Services = Depends()):
    res = User_Services.createUser(user)
    Application_Responce = ApplicationResponce(
        Data=res,
        StatusCode=201,
        Message="Appication created with code 201"
    )
    return Application_Responce


@router.get("/alluser",response_model = ApplicationResponce[List[UserResponse]],status_code = status.HTTP_200_OK)
def get_allUser(User_Services : User_Services = Depends(), current_client=Depends(get_current_client)):
    res = User_Services.getAllUser()
    Application_Response = ApplicationResponce(
        StatusCode = 200,
        Message = "Sucess",
        Data = res
    )
    return Application_Response

@router.get("",response_model= ApplicationResponce[UserResponse], status_code= status.HTTP_200_OK)
def get_user_by_ID(id :Optional[int],User_Services : User_Services =Depends()):
    if id is None:
        raise HTTPException(
            status_code= 404,
            detail = "User not found"
        )
    else:
        res = User_Services.GetUserById(id)
        Application_Responce = ApplicationResponce(
            StatusCode =200,
            Message = "Data Found",
            Data = res
        )

    return Application_Responce
@router.put("/UpdateUser",response_model= ApplicationResponce[UserResponse],status_code=status.HTTP_200_OK)
def Update_user(UserDto:UserUpdate, User_Services:User_Services=Depends()):
    res= User_Services.UpdateUserById(UserDto)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail ="User Not found"
        )
    else:
        Application_Responce =ApplicationResponce(
            StatusCode = 200,
            Message = "Data Updated Sucessfully",
            Data = res
        )
    return Application_Responce