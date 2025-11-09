from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, UserRole 
from app.crud import crud_user

def delete_user(
    db: Session, *, user_id_to_delete: int, current_user: User
) -> User:
    
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão negada. Apenas administradores podem apagar utilizadores."
        )

    
    user_to_delete = crud_user.get_user(db, user_id=user_id_to_delete)
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilizador a apagar não encontrado."
        )

    
    if current_user.id == user_to_delete.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Um administrador não se pode apagar a si mesmo."
        )


    deleted_user = crud_user.delete(db=db, db_obj=user_to_delete)

    db.commit()

    return deleted_user