from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    full_name: str
    role: str

    class Config:
        from_attributes = True
