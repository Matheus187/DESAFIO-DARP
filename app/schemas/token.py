from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema do payload (conteúdo) do token JWT."""
    email: str | None = None