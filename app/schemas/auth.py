from datetime import datetime

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }