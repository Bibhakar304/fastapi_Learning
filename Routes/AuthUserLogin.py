from fastapi import APIRouter,Depends,HTTPException,status
from Services.AuthUserService import AuthUserService
from Schemas.AuthSchema import TokenRequest,TokenResponse,UserLoginRequest

router = APIRouter(prefix="/userauth",tags=["Authentication"])

@router.post("/userlogintoken",response_model=TokenResponse,status_code=status.HTTP_200_OK)
def generate_user_token(request:UserLoginRequest,_authService:AuthUserService=Depends()):
    usertoken =_authService.getUser_On_login(request.user_name,request.password)

    if usertoken is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invallid Client Credentials for Userloingtoken"
        )    
    return TokenResponse(
        access_token = usertoken,
        token_type = "bearer"
    )
