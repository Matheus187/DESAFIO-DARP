from pydantic import BaseModel
from app.models.order import OrderStatus # Importa nosso Enum de status
from app.schemas.order_item import OrderItemCreate, OrderItemRead

class OrderCreate(BaseModel):
    items: list[OrderItemCreate]


class OrderRead(BaseModel):
    id: int
    owner_id: int
    total_amount: float
    status: OrderStatus 
    items: list[OrderItemRead] 

    class Config:
        from_attributes = True