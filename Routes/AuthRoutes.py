from fastapi import APIRouter,Depends,HTTPException,status
from Services.AuthService import AuthService
from Schemas.AuthSchema import TokenRequest,TokenResponse

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/token",response_model=TokenResponse,status_code=status.HTTP_200_OK)
def generat_token(request:TokenRequest,_authService:AuthService = Depends()):
    token = _authService.generate_tokken(request.client_id,request.client_secret)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Client credentils"
        )

    return TokenResponse(
        access_token = token,
        token_type ="bearer"
    )


