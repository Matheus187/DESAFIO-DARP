from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.product import Produto 
from app.schemas.product import ProductCreate, ProductUpdate
from app.crud import crud_product

def create_product(
    db: Session, *, obj_in: ProductCreate, current_user: User
) -> Produto:
    
    if current_user.role not in [UserRole.PRODUTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão negada. Apenas produtores podem criar produtos."
        )
        
    db_product = crud_product.create_with_owner(
        db=db, 
        obj_in=obj_in, 
        owner_id=current_user.id
    )
    
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(
    db: Session, *, product_id: int, obj_in: ProductUpdate, current_user: User
) -> Produto:
    
    
    db_product = crud_product.get(db, id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    
    if db_product.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão negada. Você não é o dono deste produto."
        )
        
    
    updated_product = crud_product.update(
        db=db, 
        db_obj=db_product, 
        obj_in=obj_in
    )
    
    
    db.commit()
    db.refresh(updated_product)
    
    return updated_product


def delete_product(
    db: Session, *, product_id: int, current_user: User
) -> Produto:
    
    db_product = crud_product.get(db, id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    if db_product.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão negada. Você não é o dono deste produto."
        )
        
    deleted_product = crud_product.delete(db=db, db_obj=db_product)
    
    db.commit()
    
    return deleted_product