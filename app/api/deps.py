from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt

from app.db.session import SessionLocal
from app.core.security import decode_token
from app.core.config import settings
from app.crud import crud_user
from app.models.user import User
from app.schemas.token import TokenData 

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"/auth/login" 
)


def get_db():
    """Gera uma sessão do banco de dados para a requisição."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
        
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
   
    user = crud_user.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
        
    return user