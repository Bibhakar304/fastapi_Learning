from fastapi import Depends
from core.security import CreatToken_for_UserLogin
from Repository.UserLoginAuth import UserLoginAuth 


class AuthUserService:
    def __init__(self, user_login_auth: UserLoginAuth = Depends()):
        self._userLoginAuth = user_login_auth
 
    def getUser_On_login(
        self,
        username: str,
        password: str
    ):
        if not username or not password:
            return None

        user = self._userLoginAuth.get_user_OnLogin(
            username,
            password
        )

        if user is None:
            return None

        token = CreatToken_for_UserLogin(user.user_id)

        return token