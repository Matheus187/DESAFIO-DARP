from sqlalchemy.orm import Session
from app.models.product import Produto 
from app.schemas.product import ProductCreate, ProductUpdate

def create_with_owner(
    db: Session, *, obj_in: ProductCreate, owner_id: int
) -> Produto:

    
    db_obj = Produto(
    **obj_in.model_dump(), 
    owner_id=owner_id
    )

    db.add(db_obj)
    return db_obj

def get(db: Session, id: int) -> Produto | None:
    """Busca um produto pelo seu ID."""
    return db.query(Produto).filter(Produto.id == id).first()


def update(
    db: Session, *, db_obj: Produto, obj_in: ProductUpdate | dict
) -> Produto:
    
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True) 

    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    return db_obj

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[Produto]:
    return (
        db.query(Produto)
        .order_by(Produto.id.asc()) 
        .offset(skip) 
        .limit(limit) 
        .all() 
    )

def delete(db: Session, *, db_obj: Produto) -> Produto:
    db.delete(db_obj)
    return db_obj