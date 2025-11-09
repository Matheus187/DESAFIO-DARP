from pydantic import BaseModel, Field
from app.models.product import ProductCategory 

class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(gt=0) 
    amount: int = Field(ge=0) 
    category: ProductCategory


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float | None = Field(default=None, gt=0)
    amount: int | None = Field(default=None, ge=0)
    category: ProductCategory | None = None


class ProductRead(ProductCreate):
    id: int
    owner_id: int 
    
    class Config:
        from_attributes = True