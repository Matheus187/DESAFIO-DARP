from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Produto
from app.schemas.order import OrderCreate 

def create_order(
    db: Session, *, owner_id: int, total: float, items_to_create: list[dict]
) -> Order:
    
    db_order = Order(
        owner_id=owner_id,
        total_amount=total
    )
    db.add(db_order)
    db.flush()

    
    for item_data in items_to_create:
        item_data['order_id'] = db_order.id 
        
        db_item = OrderItem(**item_data)
        db.add(db_item)
    
    
    return db_order


def get_multi_by_owner(db: Session, *, owner_id: int) -> list[Order]:
    
    return (
        db.query(Order)
        .filter(Order.owner_id == owner_id)
        .order_by(Order.id.desc())
        .all()
    )