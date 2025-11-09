from pydantic import BaseModel, Field

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_purchase: float

    class Config:
        from_attributes = True