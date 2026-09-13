from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.security import validate_access_token, validate_user_token

seccurity = HTTPBearer()

def get_current_client(
    credentials: HTTPAuthorizationCredentials = Depends(seccurity)
):
    token = credentials.credentials

    payload = validate_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return payload

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(seccurity)
) -> int:
    token = credentials.credentials

    payload = validate_user_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing user_id"
        )

    return user_id