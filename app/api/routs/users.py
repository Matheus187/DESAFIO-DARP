from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List 

from app.api import deps
from app.models.user import User
from app.schemas.user import UserRead 
from app.services import user_service 
router = APIRouter()


@router.delete(
    "/users/{user_id}", 
    response_model=UserRead,
    tags=["Admin (Utilizadores)"] 
)
def delete_user_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: User = Depends(deps.get_current_user) 
):
    
    deleted_user = user_service.delete_user(
        db=db, 
        user_id_to_delete=user_id, 
        current_user=current_user
    )
    return deleted_user