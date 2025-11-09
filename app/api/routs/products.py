from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.models.user import User
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.crud import crud_product 
from app.services import product_service 

router = APIRouter()

@router.post(
    "/products", 
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: ProductCreate,
    current_user: User = Depends(deps.get_current_user) 
):
   
    return product_service.create_product(
        db=db, obj_in=product_in, current_user=current_user
    )

@router.put(
    "/products/{product_id}", 
    response_model=ProductRead
)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    product_in: ProductUpdate,
    current_user: User = Depends(deps.get_current_user)
):
    
    return product_service.update_product(
        db=db, product_id=product_id, obj_in=product_in, current_user=current_user
    )


@router.delete(
    "/products/{product_id}", 
    response_model=ProductRead 
)
def delete_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    
    return product_service.delete_product(
        db=db, product_id=product_id, current_user=current_user
    )


@router.get(
    "/products",
    response_model=List[ProductRead]
)
def read_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    return crud_product.get_multi(db, skip=skip, limit=limit)

@router.get(
    "/products/{product_id}",
    response_model=ProductRead
)
def read_product_by_id(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int
):
    
    db_product = crud_product.get(db, id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    return db_product