from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):

    organization_name: str

    name: str

    email: EmailStr

    password: str

class CurrentUser(BaseModel):
    id: int
    organization_id: int
    name: str
    email: EmailStr
    role: str