from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserRole
from app.schemas.user import UserCreate, UserRead
from app.schemas.token import Token 
from app.crud import crud_user
from app.core.security import verify_password, create_access_token
from app.api import deps

router = APIRouter()

@router.post("/register", response_model=UserRead)
@router.post("/register", response_model=UserRead)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate
):
    
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Um usuário com este e-mail já existe.",
        )

    if user_in.role == UserRole.ADMIN:
        admin_exists = crud_user.get_first_admin(db)
        if admin_exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão negada. Um administrador já existe no sistema."
            )
    
    new_user = crud_user.create_user(db, user_in=user_in)

    try:
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar utilizador: {e}"
        )

    return new_user

@router.post("/login", response_model=Token)
def login_for_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    
    user = crud_user.get_user_by_email(db, email=form_data.username)
    
    
    if not user or not verify_password(form_data.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.email}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}