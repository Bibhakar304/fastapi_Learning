from core.security import Create_access_Token

CLIENT_ID = "Fast-api_Learning"
CLIENT_SECERET = "FastAPISecereate"


class AuthService:
    def generate_tokken(
        self,
        client_id: str,
        client_secret: str
    ):
        # Validate client_id
        if client_id != CLIENT_ID:
            return None

        # Validate client_secret
        if client_secret != CLIENT_SECERET:
            return None

        token = Create_access_Token(client_id)

        return token


    