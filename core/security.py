import jwt
from datetime import datetime,timedelta,timezone
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError

SECURITY_KEY = "Fastapi_application_Key"

ALORITHM = "HS256"

ACCESS_TOKEN_EXPIRES_MINUTES = 30
SECRET_KEY = "my-super-secret-key-change-this-later"

def Create_access_Token(client_id:str):
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    payload = {
        "client_id" : client_id,
        "token_type" : "access_token",
        "exp" : expiration_time
    }

    token = jwt.encode(
        payload,
        SECURITY_KEY,
        algorithm=ALORITHM
    )
    return token

def validate_access_token(token:str):
    try:
        Payload = jwt.decode(
            token,SECURITY_KEY,algorithms=[ALORITHM]
        )
        return Payload
    except ExpiredSignatureError:
        return None
    except InvalidTokenError:
        return None

def CreatToken_for_UserLogin(user_id:int):
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    payload ={
        "user_id":user_id,
        "token_type":"user_access_token",
        "exp": expiration_time
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALORITHM
    )
    return token

def validate_user_token(token:str):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALORITHM]
        )
        return payload
    except ExpiredSignatureError:
        return None
    except InvalidTokenError:
        return None