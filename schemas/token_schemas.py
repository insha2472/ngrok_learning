from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    user_name: str

class TokenRefresh(BaseModel):
    refresh_token: str

class LoginRequest(BaseModel):
    email: str
    password: str