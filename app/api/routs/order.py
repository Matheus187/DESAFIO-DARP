from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.schemas.order import OrderCreate, OrderRead
from app.services import order_service 
from app.crud import crud_order

router = APIRouter()

@router.post(
    "/orders", 
    response_model=OrderRead, 
    status_code=status.HTTP_201_CREATED 
)
def create_new_order_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    order_in: OrderCreate, 
    current_user: User = Depends(deps.get_current_user) 
):
    new_order = order_service.create_new_order(
        db=db, 
        order_in=order_in, 
        current_user=current_user
    )
    
    return new_order

@router.get(
    "/orders/me",
    response_model=list[OrderRead] 
)
def read_my_orders(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    
    orders = crud_order.get_multi_by_owner(db, owner_id=current_user.id)

    return orders