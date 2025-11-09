from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole # Importa o Enum de perfis

class UserBase(BaseModel):
    email: EmailStr 
    full_name: str | None = Field(default=None, max_length=100)


class UserCreate(UserBase):
    password: str = Field(min_length=8)
    role: UserRole


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = Field(default=None, max_length=100)
    password: str | None = Field(default=None, min_length=8)


class UserRead(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True